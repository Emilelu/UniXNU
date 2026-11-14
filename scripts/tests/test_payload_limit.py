"""Guard the DarwinBoot command-line ceiling that payload.py enforces.

DarwinBoot copies BootArgs into CommandLine[DARWIN_BOOT_LINE_LENGTH] and
returns EFI_BAD_BUFFER_SIZE once Index >= sizeof - 1, so anything longer than
607 bytes is packaged happily but never loaded: the USB console stays at 0
bytes, which reads exactly like an early kernel death.  Three silent boots on
2026-11-14 were caused by this (bt-s1-20261114b carried 610 bytes).
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from unixnu.payload import check_args, DARWIN_BOOT_LINE_MAX, Error  # noqa: E402

CASES = []


def case(fn):
    CASES.append(fn)
    return fn


@case
def the_limit_matches_darwinboot():
    boot_args_h = pathlib.Path(
        '/mnt/e/hackios/uefi-mondrian/Platforms/Xiaomi/DarwinBootPkg/Driver/BootArgs.h')
    if not boot_args_h.is_file():
        print('  skip: BootArgs.h not reachable from here')
        return
    text = boot_args_h.read_text()
    marker = '#define DARWIN_BOOT_LINE_LENGTH '
    length = int(text.split(marker, 1)[1].split()[0])
    if DARWIN_BOOT_LINE_MAX != length - 1:
        raise AssertionError(
            f'payload.py allows {DARWIN_BOOT_LINE_MAX}, '
            f'DarwinBoot buffer is {length} -> usable {length - 1}')


@case
def a_normal_line_passes():
    for size in (1, 100, 575, DARWIN_BOOT_LINE_MAX):
        line = check_args(['a' * size])
        if len(line) != size:
            raise AssertionError(f'{size} byte argument came back as {len(line)}')


@case
def one_byte_over_the_limit_fails():
    try:
        check_args(['a' * (DARWIN_BOOT_LINE_MAX + 1)])
    except Error as exc:
        if 'DarwinBoot accepts at most' not in str(exc):
            raise AssertionError(f'wrong message: {exc}')
        return
    raise AssertionError('an over-long command line was accepted')


@case
def joining_arguments_counts_the_spaces():
    check_args(['a' * 300, 'b' * 300])
    try:
        check_args(['a' * 304, 'b' * 304])
    except Error:
        return
    raise AssertionError('the separator was not counted')


@case
def the_old_1000_byte_limit_is_gone():
    for size in (608, 700, 1000):
        try:
            check_args(['a' * size])
        except Error:
            continue
        raise AssertionError(f'{size} bytes slipped past the new limit')


def main():
    failures = 0
    for fn in CASES:
        try:
            fn()
            print(f'ok   {fn.__name__}')
        except AssertionError as exc:
            failures += 1
            print(f'FAIL {fn.__name__}: {exc}')
    print(f'TESTS OK {len(CASES) - failures} case(s) ({failures} failure(s))')
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
