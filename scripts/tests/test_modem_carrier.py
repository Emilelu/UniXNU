"""Guard the modem carrier contract between the payload and the firmware.

The payload ships the modem firmware as one LZMA-alone stream per loadable
segment under EFI/UniXNU/MODEM, and publishes a 16-byte zero K60ModemImage
placeholder in /chosen/memory-map.  DarwinBoot refuses to boot on either half
alone: a carrier without the placeholder fails at
"K60ModemImage placeholder missing" / EFI_COMPROMISED_DATA, and a placeholder
without a carrier fails the other way (uefi 72e51ca, 5d96806).  So the two are
one switch here, and this file pins the three facts that make that safe:

  * the table travels with the bytes, and every stream must agree with it,
  * exactly one producer writes K60ModemImage, and it is that switch,
  * nothing decodes a stream host-side, because that would only prove that this
    machine and the firmware agree about LZMA.

Run: python3 scripts/tests/test_modem_carrier.py
"""
import inspect
import os
import pathlib
import re
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]   # scripts/, so "from unixnu" resolves
sys.path.insert(0, str(ROOT))

from unixnu import devicetree, payload  # noqa: E402
from unixnu.util import Error  # noqa: E402

CASES = []

# The real carrier produced by the firmware dry run: 27 streams, 109,060,761
# declared bytes.  The table beside it is what gen-modem-table.py --manifest
# writes; the staged directory ships the streams only.
STAGED = pathlib.Path('/mnt/e/k60-work/artifacts/dxe-dryrun-d/stage/EFI/UniXNU/MODEM')
STAGED_TABLE = pathlib.Path('/mnt/e/k60-work/artifacts/dxe-dryrun-d/want.txt')


def case(fn):
    CASES.append(fn)
    return fn


def carrier(root, table, streams):
    """Write a carrier directory: table lines plus {name: (declared, payload bytes)}."""
    root.mkdir(parents=True, exist_ok=True)
    (root / payload.MODEM_MANIFEST).write_text(''.join(f'{name} {size}\n' for name, size in table),
                                               encoding='utf-8')
    for name, (declared, body) in streams.items():
        header = bytes([0x5D]) + (0).to_bytes(4, 'little') + declared.to_bytes(8, 'little')
        (root / f'{name}.lzma').write_bytes(header + body)
    return root


def real_carrier(root):
    """The staged streams, referenced without copying 47 MB."""
    for path in STAGED.iterdir():
        if path.suffix == '.lzma':
            os.symlink(path, root / path.name)
    (root / payload.MODEM_MANIFEST).write_text(STAGED_TABLE.read_text(), encoding='utf-8')
    return root


@case
def the_header_layout_matches_the_firmware_reader():
    """ImageCarrierLib.c: CarrierDeclaredSize walks Source[12]..Source[5]."""
    source = pathlib.Path('/mnt/e/hackios/uefi-mondrian/Platforms/Xiaomi/DarwinBootPkg/'
                          'Library/ImageCarrierLib/ImageCarrierLib.c')
    if not source.is_file():
        print('  skip: the firmware tree is not reachable from here')
        return
    text = source.read_text()
    header = int(re.search(r'#define CARRIER_HEADER_SIZE\s+(\d+)', text).group(1))
    if header != payload.MODEM_HEADER:
        raise AssertionError(f'payload reads {payload.MODEM_HEADER} header bytes, firmware {header}')
    if 'LZMA_PROPS_SIZE' not in text:
        raise AssertionError('the firmware size loop no longer starts at the props size')


@case
def the_real_carrier_matches_the_table_the_firmware_was_generated_from():
    if not STAGED.is_dir() or not STAGED_TABLE.is_file():
        print('  skip: the staged carrier is not reachable from here')
        return
    with tempfile.TemporaryDirectory() as tmp:
        report = payload.read_modem_carrier(real_carrier(pathlib.Path(tmp)))
    if len(report['names']) != 27:
        raise AssertionError(f'{len(report["names"])} streams, the firmware table lists 27')
    if report['declared'] != 109060761:
        raise AssertionError(f'declared {report["declared"]}, the firmware table says 109060761')
    if 'modem.b14' in report['names'] or 'modem.b29' not in report['names']:
        raise AssertionError(f'segment set is not the firmware one: {report["names"]}')


@case
def a_carrier_without_its_table_is_refused():
    with tempfile.TemporaryDirectory() as tmp:
        root = carrier(pathlib.Path(tmp), [('modem.b01', 4)], {'modem.b01': (4, b'abcd')})
        (root / payload.MODEM_MANIFEST).unlink()
        try:
            payload.read_modem_carrier(root)
        except Error as exc:
            if 'gen-modem-table.py' not in str(exc):
                raise AssertionError(f'the error does not say how to make the table: {exc}')
            return
    raise AssertionError('a carrier without a table was accepted')


@case
def a_stream_the_table_lists_but_the_directory_lacks_is_refused():
    with tempfile.TemporaryDirectory() as tmp:
        root = carrier(pathlib.Path(tmp), [('modem.b01', 4), ('modem.b02', 5)],
                       {'modem.b01': (4, b'abcd')})
        try:
            payload.read_modem_carrier(root)
        except Error as exc:
            if 'missing 1 stream' not in str(exc) or 'modem.b02' not in str(exc):
                raise AssertionError(f'wrong message: {exc}')
            return
    raise AssertionError('an incomplete carrier was accepted')


@case
def a_stream_the_table_does_not_list_is_refused():
    with tempfile.TemporaryDirectory() as tmp:
        root = carrier(pathlib.Path(tmp), [('modem.b01', 4)],
                       {'modem.b01': (4, b'abcd'), 'modem.b02': (5, b'abcde')})
        try:
            payload.read_modem_carrier(root)
        except Error as exc:
            if 'does not list' not in str(exc) or 'modem.b02' not in str(exc):
                raise AssertionError(f'wrong message: {exc}')
            return
    raise AssertionError('an unlisted stream was accepted')


@case
def a_declared_size_that_disagrees_with_the_table_is_refused():
    """The exact check the firmware makes at boot: Declared != Bytes."""
    with tempfile.TemporaryDirectory() as tmp:
        root = carrier(pathlib.Path(tmp), [('modem.b01', 4)], {'modem.b01': (5, b'abcd')})
        try:
            payload.read_modem_carrier(root)
        except Error as exc:
            if 'declares 5 bytes' not in str(exc) or 'says 4' not in str(exc):
                raise AssertionError(f'wrong message: {exc}')
            return
    raise AssertionError('a stream that disagrees with the table was accepted')


@case
def a_stream_shorter_than_its_own_header_is_refused():
    with tempfile.TemporaryDirectory() as tmp:
        root = carrier(pathlib.Path(tmp), [('modem.b01', 4)], {'modem.b01': (4, b'abcd')})
        (root / 'modem.b01.lzma').write_bytes(b'\x5d\x00\x00')
        try:
            payload.read_modem_carrier(root)
        except Error as exc:
            if 'header alone is 13' not in str(exc):
                raise AssertionError(f'wrong message: {exc}')
            return
    raise AssertionError('a truncated stream was accepted')


@case
def a_file_that_is_not_a_stream_is_refused():
    with tempfile.TemporaryDirectory() as tmp:
        root = carrier(pathlib.Path(tmp), [('modem.b01', 4)], {'modem.b01': (4, b'abcd')})
        (root / 'notes.txt').write_text('scratch')
        try:
            payload.read_modem_carrier(root)
        except Error as exc:
            if 'notes.txt' not in str(exc):
                raise AssertionError(f'wrong message: {exc}')
            return
    raise AssertionError('a stray file was accepted')


@case
def a_multiplied_table_row_is_refused():
    with tempfile.TemporaryDirectory() as tmp:
        root = carrier(pathlib.Path(tmp), [('modem.b01', 4)], {'modem.b01': (4, b'abcd')})
        (root / payload.MODEM_MANIFEST).write_text('modem.b01 4\nmodem.b01 4\n', encoding='utf-8')
        try:
            payload.read_modem_carrier(root)
        except Error as exc:
            if 'twice' not in str(exc):
                raise AssertionError(f'wrong message: {exc}')
            return
    raise AssertionError('a duplicated table row was accepted')


@case
def a_name_the_firmware_would_never_open_is_refused():
    # ImageCarrierLib builds L"%a.lzma" from the row and probes "modem.b01" before
    # it loads anything, so a row without that shape names a file no boot opens.
    with tempfile.TemporaryDirectory() as tmp:
        root = carrier(pathlib.Path(tmp), [('b01', 4)], {'b01': (4, b'abcd')})
        try:
            payload.read_modem_carrier(root)
        except Error as exc:
            if 'never loaded' not in str(exc):
                raise AssertionError(f'wrong message: {exc}')
            return
    raise AssertionError('a table row the firmware never opens was accepted')


@case
def the_placeholder_is_off_unless_the_switch_is_on():
    if inspect.signature(devicetree.generate).parameters['modem'].default is not False:
        raise AssertionError('generate() no longer defaults the placeholder to off')


@case
def the_placeholder_has_exactly_one_producer():
    """Two producers would let a stale range survive a carrier that never loaded."""
    hits = [path for path in (ROOT / 'unixnu').rglob('*.py')
            if "('K60ModemImage', bytes(16))" in path.read_text(encoding='utf-8', errors='replace')]
    if [path.name for path in hits] != ['devicetree.py']:
        raise AssertionError(f'the property value is written in {[p.name for p in hits]}')


@case
def the_payload_pairs_the_two_halves_from_one_variable():
    text = (ROOT / 'unixnu/payload.py').read_text(encoding='utf-8')
    if text.count('modem=bool(carrier)') != 1:
        raise AssertionError('the ADT placeholder is not driven by the carrier switch')
    if 'read_modem_carrier(' not in text.split('def build(', 1)[1]:
        raise AssertionError('build() no longer checks the carrier')


@case
def the_boot_image_step_refuses_the_payload_option():
    text = (ROOT / 'unixnu/cli.py').read_text(encoding='utf-8')
    body = text.split('def cmd_bootimg(', 1)[1].split('\ndef ', 1)[0]
    if 'modem_carrier' not in body:
        raise AssertionError('bootimg silently ignores --modem-carrier')


def main():
    failures = 0
    for fn in CASES:
        try:
            fn()
            print(f'ok   {fn.__name__}')
        except Exception as exc:   # a broken case must not stop the rest of the file
            failures += 1
            print(f'FAIL {fn.__name__}: {type(exc).__name__}: {exc}')
    print(f'TESTS OK {len(CASES) - failures} case(s) ({failures} failure(s))')
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
