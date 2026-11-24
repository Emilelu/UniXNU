#!/usr/bin/env python3
"""Check the CPU and UFS properties consumed by the Darwin handoff."""
from pathlib import Path
import struct
import subprocess
import tempfile
import unittest

from unixnu.devicetree import generate


DTS = '''/dts-v1/;
/ {
    #address-cells = <2>; #size-cells = <2>;
    model = "handoff-test"; compatible = "test,handoff";
    memory@900000000 { device_type = "memory"; reg = <9 0 1 0>; };
    cpus {
        #address-cells = <1>; #size-cells = <0>; timebase-frequency = <19200000>;
        cpu@0 { reg = <0>; compatible = "arm,cortex-a710"; unixnu,cluster-type = "P"; };
        cpu@100 { reg = <0x100>; compatible = "arm,cortex-a710"; status = "disabled"; };
        cpu@200 { reg = <0x200>; compatible = "arm,cortex-a710"; unixnu,cluster-type = "P"; };
    };
    psci { compatible = "arm,psci-1.0"; method = "smc"; };
    ufs@1d84000 {
        compatible = "qcom,sm8475-ufshc"; reg = <0 0x1d84000 0 0x3000>;
        unixnu,adt-name = "ufshc";
        pong,ufs-hc-base = <0 0x1d84000>; pong,ufs-hc-size = <0 0x3000>;
        pong,gcc-ufs-page = <0 0x187000>; pong,smmu-base = <0 0x15000000>;
        pong,smmu-size = <0 0x100000>; pong,smmu-stream-id = <0xe0>;
        pong,ufs-spi = <265>; pong,smmu-context-banks = <78>; pong,smmu-match-groups = <120>;
    };
};
'''


def decode(blob):
    entries = {}
    def consume(offset, parent):
        count, children = struct.unpack_from('<II', blob, offset)
        offset += 8
        properties = {}
        for _ in range(count):
            key, size = struct.unpack_from('<32sI', blob, offset)
            offset += 36
            properties[key.split(b'\0', 1)[0].decode()] = blob[offset:offset + size]
            offset += (size + 3) & ~3
        path = parent + '/' + properties.pop('name').rstrip(b'\0').decode()
        entries[path] = properties
        for _ in range(children):
            offset = consume(offset, path)
        return offset
    if consume(0, '') != len(blob):
        raise ValueError('trailing ADT bytes')
    return entries


class DeviceTreeHandoffTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            source, dtb = root / 'hardware.dts', root / 'hardware.dtb'
            source.write_text(DTS)
            subprocess.run(['dtc', '-I', 'dts', '-O', 'dtb', '-o', str(dtb), str(source)],
                           check=True, capture_output=True, timeout=20)
            cls.entries = decode(generate(dtb, {'payload': {}, 'adt': {}}))

    def test_logical_cpu_ids_are_dense_without_changing_affinity(self):
        cpus = self.entries['/device-tree/cpus']
        first = self.entries['/device-tree/cpus/cpu0']
        second = self.entries['/device-tree/cpus/cpu1']
        self.assertEqual(cpus['max_cpus'], struct.pack('<I', 2))
        self.assertEqual((first['cpu-id'], second['cpu-id']), (struct.pack('<I', 0), struct.pack('<I', 1)))
        self.assertEqual((first['reg'], second['reg']), (struct.pack('<I', 0), struct.pack('<I', 0x200)))
        self.assertEqual((first['state'], second['state']), (b'running\0', b'waiting\0'))

    def test_ufs_windows_and_cells_retain_driver_width_and_endianness(self):
        ufs = self.entries['/device-tree/arm-io/ufshc']
        windows = {'pong,ufs-hc-base': 0x1d84000, 'pong,ufs-hc-size': 0x3000,
                   'pong,gcc-ufs-page': 0x187000, 'pong,smmu-base': 0x15000000, 'pong,smmu-size': 0x100000}
        cells = {'pong,smmu-stream-id': 0xe0, 'pong,ufs-spi': 265,
                 'pong,smmu-context-banks': 78, 'pong,smmu-match-groups': 120}
        for key, value in windows.items():
            self.assertEqual(ufs[key], struct.pack('<Q', value), key)
        for key, value in cells.items():
            self.assertEqual(ufs[key], struct.pack('<I', value), key)
        self.assertEqual(ufs['reg'], struct.pack('<QQ', 0xd84000, 0x3000))


if __name__ == '__main__':
    unittest.main()
