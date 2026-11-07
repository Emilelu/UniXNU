# 一加 13T（oneplus13t）

[IssacL04/UniXNU-Pagani_SM8750](https://github.com/IssacL04/UniXNU-Pagani_SM8750)

<div v-pre>

OnePlus 13T PKX110: format-2 migration of the single-core, read-only UFS root and CPU display port; volatile RAM Data.

源记录: [porting.toml](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/porting.toml), `3a12121d3ef9fdee1636500665c5cbb4baf5b83c`.

本页按设备记录自动生成。

| 部分 | 状态 |
| --- | --- |
| [配置](#configuration) | `host-verified` |
| [固件与启动](#firmware) | `host-verified` |
| [CPU 与中断](#cpu) | `host-verified` |
| [内存与 DMA](#memory) | `host-verified` |
| [存储与根卷](#storage) | `host-verified` |
| [显示](#display) | `host-verified` |
| [输入](#input) | `host-verified` |
| [GPU](#gpu) | `planned` |
| [网络](#network) | `planned` |
| [音频](#audio) | `planned` |
| [电源](#power) | `host-verified` |
| [镜像组装](#packaging) | `host-verified` |
| [诊断](#diagnostics) | `host-verified` |

## 配置 {#configuration}

`host-verified`

组件: `PaganiArmDTPlatform`, `NativeAES`, `NativeKeyStoreEvents`.

### 硬件与依赖

- Four layers: ARM64, pinned sm8750, ipados-17.7.11-21H461, OnePlus 13T. Arrays are complete replacements.

### 配置

- schema\_version=2; soc\_source=sm8750; complete component/fragment/archive arrays; configs/oneplus13t\_defconfig.

### 操作步骤

- From UniXNU: defconfig oneplus13t\_defconfig -D ../UniXNU-Pagani\_SM8750; fetch; status --json; tree; run scripts/test-format2.py with the main scripts on PYTHONPATH.

### 开发经验

- Four profiles select 18 components. PaganiInput and PaganiPanel are embedded in the ABI-qualified display archive and depend on QcomGeniSpi plus Sm8750Platform. Build 48 passed the complete configuration checks, driver compilation, final kernel link and prelink. Its source pins are device e6435b2bda6e91431f3bc0c442d1ff9c47be1451, main 42ffa07e9b82f7ffc37499392b2751e146647a6a, drivers 143e958bea8ae8ad7f47723cd105a589084f913d and SoC 9e90b16861612c0251c453ccbf6cf10592ea87e2.
- The documentation workflow checks out pinned driver submodules so repository-relative evidence links resolve during validation. Current pins include the UFS completion recheck. Build 49 passed cloud regressions, full kernel link and prelink; its matching boot image passed local assembly and readback. Build-49 hardware feedback is recorded below.
- Official UniXNU ae68700 is merged with the maintained 13T catalog. The J120AP/product-id identity and all selected XNU patches pass the updated format-2 contract. Build 49 was temporarily booted; the user reported no repeat panic during the observed test. Build 50 includes Setup completion preferences, upstream HID collection ordering and retained peripheral diagnostics. Cloud compilation, original/compiled ABI checks, full link/prelink and matching image readback passed; fastboot accepted the temporary boot, with runtime feedback pending.
- Build-50 hardware feedback confirms the lock screen after skipping Setup and working short/long power-key actions. Touch failed during TouchComm startup. Build 51 corrects SPI read bytes, detects v1/v2 and retains detailed protocol diagnostics below the camera cutout. Portable and cloud regressions, full compilation/link/prelink and matching image readback passed; fastboot accepted the temporary boot, with touch behavior awaiting observation.
- Build-51 hardware feedback reports first-transfer SPI timeout \(T0 00 header, r=ffffff92, v=0, n=0\). The next candidate exposes the existing pre-cancel GENI snapshot; its adapter and overlay regressions pass. Full compilation of this diagnostic update is pending.
- Build 52 reached input object compilation but the early-console dependency check rejected a compiler-generated bzero from the five-row stack snapshot. The renderer now copies one 80-byte row at a time. ARM64 automatic-initialization reproduction and host display/panic checks pass; build 53 subsequently passed the full production object and final kernel build.
- Build-53 feedback confirms GENI FIFO\_IF\_DISABLE=1 and a first-read timeout. The next candidate selects existing SE DMA for FIFO-disabled engines and supplies the board SMMU extent. Local transport, overlay and both SMMU build variants pass; full compilation and hardware DMA remain pending.
- Build 54 passed all component contracts, regressions, full compilation/link/prelink and image readback. Source pins: device fba1472, main 1397e2d, drivers 26a32f5, SoC b6706a5. Fastboot accepted the temporary boot; hardware DMA/touch feedback is pending.
- Build-54 hardware feedback reports T0 00 header r=ffffffb9 v=0 n=0 with no SPI error rows. The next candidate retains the first successful RX/header, GPIO levels and DMA counts. Local actual-adapter and overlay regressions pass; its full kernel build is pending.
- Build 55 passed all 18 component contracts, regressions, original/compiled ABI checks, full compilation/link/prelink and matching image readback. Source pins: device 664530f, main b689e9a, drivers 339d4df, SoC b6706a5. Fastboot accepted the temporary boot; first-read diagnostic values and touch behavior await observation.
- Build-55 hardware feedback confirms a completed four-byte SE DMA read with TX/RX length-in 4 and idle GENI state, but all RX bytes are zero. Touch still fails with -71 before HID startup. The next investigation compares stock Android power and SPI state.
- A read-only Android 16 baseline on the local 6.6.118 kernel confirms enabled 1.8 V/3.1 V touch rails and retained SPI logs with valid a5 frames. The OnePlus driver uses cs\_clk\_delay=50 and inter\_words\_delay=0; this port does not explicitly program SE\_SPI\_DELAY\_COUNTERS. No runtime code or build-55 image changed.
- The next touch candidate adds board-owned RPMh resource names/voltages and SPI delays, with shared checked controller operations. Actual-adapter, power fault, transport and overlay regressions pass. Full cloud compilation is pending; this round ends after downloading the kernel and matching inputs without a device boot.

### 完成条件

- All source pins resolve; every selected component has a record; status shows the intended overrides and patch order.

### 当前范围

- The main fork carries community catalog entries; stock upstream alone cannot resolve this selection.

### 下一步

- Complete the authorized cloud build, download and verify its kernel and paired inputs, then wait for the user before any device boot or flash.

### 证据

- `source`: [The next touch candidate adds board-owned RPMh resource names/voltages and SPI delays, with shared checked controller operations. Actual-adapter, power fault, transport and overlay regressions pass. Full cloud compilation is pending; this round ends after downloading the kernel and matching inputs without a device boot.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)
- `device`: [A read-only Android 16 baseline on the local 6.6.118 kernel confirms enabled 1.8 V/3.1 V touch rails and retained SPI logs with valid a5 frames. The OnePlus driver uses cs\_clk\_delay=50 and inter\_words\_delay=0; this port does not explicitly program SE\_SPI\_DELAY\_COUNTERS. No runtime code or build-55 image changed.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)
  Command: <code>Read-only ADB root capture of Android regulator, GPIO, clock and existing SPI IPC logs; compare OnePlus touch and GENI source</code>. Revision: `bdeec6693f1b8488a3286446f0b93c13c02d6785`.
- `device`: [Build-55 hardware feedback confirms a completed four-byte SE DMA read with TX/RX length-in 4 and idle GENI state, but all RX bytes are zero. Touch still fails with -71 before HID startup. The next investigation compares stock Android power and SPI state.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)
  Command: <code>Build-55 temporary boot; user transcribed TOUCH and both SPI rows, then confirmed return code b9</code>. Revision: `664530f8de814569c8255d07b67c7e2f6d6db3bd`.
- `host`: [Build 55 passed all 18 component contracts, regressions, original/compiled ABI checks, full compilation/link/prelink and matching image readback. Source pins: device 664530f, main b689e9a, drivers 339d4df, SoC b6706a5. Fastboot accepted the temporary boot; first-read diagnostic values and touch behavior await observation.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/actions/runs/40437346840)
  Command: <code>Actions build 55; ./unixnu payload; ./unixnu bootimg; APFS/FAT readback; fastboot boot</code>. Revision: `664530f8de814569c8255d07b67c7e2f6d6db3bd`.
- `host`: [Build 54 passed all component contracts, regressions, full compilation/link/prelink and image readback. Source pins: device fba1472, main 1397e2d, drivers 26a32f5, SoC b6706a5. Fastboot accepted the temporary boot; hardware DMA/touch feedback is pending.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/actions/runs/40369222494)
  Command: <code>Actions build 54; ./unixnu payload; ./unixnu bootimg; APFS/FAT readback; fastboot boot</code>. Revision: `fba147283bead8e3e9f7c3ce9edc36f012bb1ec9`.
- `host`: [Build 53 passed all 18 component contracts, full C/C++ compilation, early-console runtime checks, kernel link/prelink and matching image readback. Sending and Booting returned OKAY; SPI snapshot observations are pending.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)
  Command: <code>Actions build 53; ./unixnu payload; ./unixnu bootimg; APFS/FAT readback</code>. Revision: `c5edbf3617dd5effd63b74f915218539adca1476`.
- `host`: [Build 51 passed all 18 component contracts, full C/C++ compilation, kernel link/prelink and matching image readback. Sending and Booting returned OKAY; touch behavior awaits observation.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)
  Command: <code>Actions build 51; ./unixnu payload; ./unixnu bootimg; APFS/FAT readback</code>. Revision: `9d9726f53038aa5d090dd13502064de9b4c94128`.
- `host`: [Build 50 passed all 18 component contracts, full kernel compilation/link/prelink, matching image assembly and actual payload readback. Sending and Booting returned OKAY; system UI and peripheral behavior await observation.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)
  Command: <code>Actions build 50; ./unixnu payload; ./unixnu bootimg; APFS/FAT readback</code>. Revision: `1e98cc4c10c86904d7cafc6cb98dc4a29538628d`.
- `device`: [Sending and Booting returned OKAY. The user reported no repeat panic during the test, while touch, volume/power keys and brightness remained unusable. Test duration was not specified; this does not qualify long-term stability or input.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)
  Command: <code>fastboot -s 3B15BB01BAT00000 boot stage7-run-49/boot.img; user observation</code>. Revision: `be18db0025fbde66ffd0a55302f9c1bc0fe3c122`.
- `host`: [Build 49 passed configuration, UFS regressions, complete kernel link/prelink and matching boot-image assembly/readback. The UFS completion recheck is included; hardware retest remains pending.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)
  Command: <code>test-format2.py; test-stage6.py; ./unixnu kernel -j 3; ./unixnu payload; ./unixnu bootimg; FAT readback</code>. Revision: `be18db0025fbde66ffd0a55302f9c1bc0fe3c122`.
- `host`: [All 18 selected components resolved at their pinned revisions; archive ordering, ADT checks, full kernel link and prelink passed. Downloaded kernel and report agree at 127778816 bytes; hardware remains untested.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/actions/runs/40183635568)
  Command: <code>test-format2.py; ./unixnu status --json; ./unixnu kernel -j 3</code>. Revision: `e6435b2bda6e91431f3bc0c442d1ff9c47be1451`.
- `host`: [Four layers, 15 pinned components, complete archive order and matching required ADT properties passed.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/actions/runs/40174199304)
  Command: <code>test-format2.py; ./unixnu status --json</code>. Revision: `af2ba2975a5f0f6dcedfdcc719a1c646876f5804`.
- `source`: [Current format-2 selection and board policy.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/board.toml)
- `source`: [Historical PKX110 observations through build 39; no claim of migrated-image hardware verification.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)

## 固件与启动 {#firmware}

`host-verified`

组件: `PaganiDarwinBoot`.

### 硬件与依赖

- PKX110 ABL uses init\_boot ramdisk during fastboot boot; embedded payload plus the BootPayload HOB remains necessary.
- Private firmware checkout: IssacL04/UEFI-Pagani\_SM8750 at 50b7313f40684aa25481cd109d7f48b9a50663fa.

### 配置

- firmware.config=oneplus13t; firmware.packages points to PaganiDarwinBoot; bootimg.embed\_payload=true.

### 操作步骤

- From UniXNU after kernel inputs pass: build package; firmware; payload; bootimg using ignored local input paths.

### 开发经验

- PKX110 ABL uses init\_boot ramdisk during fastboot boot; embedded payload plus the BootPayload HOB remains necessary.
- UniXNURamDiskDxe, DiskIoDxe and FAT support the standard FDT handoff; the rebuilt FD contains both paths.
- Build 54 reused the unchanged UEFI and passed complete embedded-payload readback. The same-build kernel, trust cache and RAM Data were temporarily booted without flashing.
- Build 55 reused the unchanged UEFI and passed Android v4, empty ramdisk and embedded FD/FAT checks. Actual kernel, trust cache and volatile Data match this build. Sending and Booting returned OKAY without flashing a partition.
- Android regulator state reports pm\_humu\_l4 enabled at 1.8 V for spi0.0-vdd and pm\_humu\_l16 enabled at 3.1 V for spi0.0-vcc. This is a software power-state baseline, not a physical voltage measurement or evidence that the rails remain enabled under XNU. The read-only capture used the existing debugfs mount and changed no firmware or device configuration.
- Android command DB confirms ldob4 at 0x40800 and ldob16 at 0x41900. The candidate now explicitly enables those touch rails through apps DRV-2 before reset, while retaining GENI microcode. The firmware image is unchanged; no flash or temporary boot is authorized in this build round.

### 完成条件

- Firmware image builds, enters UniXNU, publishes the framebuffer and preserves the documented memory reservations.

### 当前范围

- Build 48 reached the UI through the existing embedded-payload path. The standard initrd driver was not separately exercised.

### 下一步

- Complete the authorized cloud build, download and verify its kernel and paired inputs, then wait for the user before any device boot or flash.

### 证据

- `source`: [Android command DB confirms ldob4 at 0x40800 and ldob16 at 0x41900. The candidate now explicitly enables those touch rails through apps DRV-2 before reset, while retaining GENI microcode. The firmware image is unchanged; no flash or temporary boot is authorized in this build round.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)
- `device`: [Android regulator state reports pm\_humu\_l4 enabled at 1.8 V for spi0.0-vdd and pm\_humu\_l16 enabled at 3.1 V for spi0.0-vcc. This is a software power-state baseline, not a physical voltage measurement or evidence that the rails remain enabled under XNU. The read-only capture used the existing debugfs mount and changed no firmware or device configuration.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)
  Command: <code>Read-only ADB root capture of Android regulator, GPIO, clock and existing SPI IPC logs; compare OnePlus touch and GENI source</code>. Revision: `bdeec6693f1b8488a3286446f0b93c13c02d6785`.
- `host`: [Build 55 reused the unchanged UEFI and passed Android v4, empty ramdisk and embedded FD/FAT checks. Actual kernel, trust cache and volatile Data match this build. Sending and Booting returned OKAY without flashing a partition.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/actions/runs/40437346840)
  Command: <code>Actions build 55; ./unixnu payload; ./unixnu bootimg; APFS/FAT readback; fastboot boot</code>. Revision: `664530f8de814569c8255d07b67c7e2f6d6db3bd`.
- `host`: [Build 54 reused the unchanged UEFI and passed complete embedded-payload readback. The same-build kernel, trust cache and RAM Data were temporarily booted without flashing.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/actions/runs/40369222494)
  Command: <code>Actions build 54; ./unixnu payload; ./unixnu bootimg; APFS/FAT readback; fastboot boot</code>. Revision: `fba147283bead8e3e9f7c3ce9edc36f012bb1ec9`.
- `host`: [Build 53 reused the unchanged UEFI and passed Android v4, empty ramdisk and embedded FD/FAT checks. The verified image was temporarily booted without flashing a partition.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)
  Command: <code>Actions build 53; ./unixnu payload; ./unixnu bootimg; APFS/FAT readback</code>. Revision: `c5edbf3617dd5effd63b74f915218539adca1476`.
- `host`: [Build 51 reused the unchanged UEFI and passed Android v4, empty ramdisk and embedded FD/FAT checks. The verified image was temporarily booted without flashing a partition.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)
  Command: <code>Actions build 51; ./unixnu payload; ./unixnu bootimg; APFS/FAT readback</code>. Revision: `9d9726f53038aa5d090dd13502064de9b4c94128`.
- `host`: [Build 50 reused the unchanged UEFI and passed Android v4, empty ramdisk, embedded FD/FAT and stock DTB packaging checks. fastboot boot returned OKAY without flashing a partition; this is not a runtime qualification.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)
  Command: <code>Actions build 50; ./unixnu payload; ./unixnu bootimg; APFS/FAT readback</code>. Revision: `1e98cc4c10c86904d7cafc6cb98dc4a29538628d`.
- `host`: [AARCH64 DEBUG package and 3145728-byte FD built locally, including UniXNURamDiskDxe and the retained embedded payload path; hardware boot remains untested.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/MIGRATION.md)
  Command: <code>./unixnu build package; ./unixnu firmware</code>. Revision: `af2ba2975a5f0f6dcedfdcc719a1c646876f5804`.
- `source`: [Current format-2 selection and board policy.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/board.toml)
- `source`: [Historical PKX110 observations through build 39; no claim of migrated-image hardware verification.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)

## CPU 与中断 {#cpu}

`host-verified`

组件: `PaganiArmCpu`.

### 硬件与依赖

- Only MPIDR affinity 0 is enabled. GICD=0x16000000/0x10000, GICR=0x16080000/0x200000, stride=0x40000, CNTFRQ=19200000.

### 配置

- cpus=1; cpu0 status=okay; XNU\_NATIVE\_ARCH\_TIMER and XNU\_NATIVE\_PAN enabled.

### 操作步骤

- Compile the board DTS, compare the generated ADT, run test-stage6.py and test-kernel-source.py, then obtain a fresh boot log for CPU0/timer.

### 开发经验

- Only MPIDR affinity 0 is enabled. GICD=0x16000000/0x10000, GICR=0x16080000/0x200000, stride=0x40000, CNTFRQ=19200000.
- The counter conversion uses the firmware CNTFRQ; the shared ARM64 patch preserves the Stage-6 timer correction. The source-kernel suite also executes the real RAMBlock link section with an alternate archive directory.

### 完成条件

- Every enabled CPU reaches its entry checkpoint and timer/IPI handling works on each enabled CPU.

### 当前范围

- SMP, other CPU affinities and CPU frequency control are unverified.

### 下一步

- Temporarily boot the exact migrated image only after separate authorization; record its image/source revisions and compare the affected runtime checkpoints with build 39.

### 证据

- `host`: [Eight source-kernel regressions and production ARM64 assembly checks passed; the enabled CPU0 code linked successfully. IRQ/IPI behavior was not tested on hardware.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/actions/runs/40174199304)
  Command: <code>test-kernel-source.py; test-stage6.py; ./unixnu kernel -j 3</code>. Revision: `af2ba2975a5f0f6dcedfdcc719a1c646876f5804`.
- `source`: [Current format-2 selection and board policy.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/board.toml)
- `source`: [Historical PKX110 observations through build 39; no claim of migrated-image hardware verification.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)

## 内存与 DMA {#memory}

`host-verified`

组件: `Sm8750Platform`.

### 硬件与依赖

- The captured live DT has contiguous RAM at 0x980000000 of size 0x180000000. DarwinBoot requests 0x100000000 and rewrites chosen dram-base/size to its actual allocation.

### 配置

- payload.dram\_size=0x180000000; payload.adt.owned\_memory\_size=0x100000000.

### 操作步骤

- Run check-memory-map.py against the captured live.dtb and current UEFI map; inspect actual DarwinBoot allocation before allowing more RAM or DMA.

### 开发经验

- The captured live DT has contiguous RAM at 0x980000000 of size 0x180000000. DarwinBoot requests 0x100000000 and rewrites chosen dram-base/size to its actual allocation.
- GIC register offsets remain unchanged; the common ADT converter rounds the arm-io window to 16 MiB. UFS uses the extracted SM8750 SMMU operations.

### 完成条件

- All handoff regions are accounted for and each enabled DMA engine accesses its allocated range with the documented cache policy.

### 当前范围

- Only the selected contiguous arena is handed to XNU; allocation size is a request. Other devices need their own RAM/reservation evidence.

### 下一步

- Temporarily boot the exact migrated image only after separate authorization; record its image/source revisions and compare the affected runtime checkpoints with build 39.

### 证据

- `host`: [DTS/ADT memory and GIC contracts and RAMBlock handoff address bounds passed on the host. DMA behavior was not tested on hardware.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/actions/runs/40174199304)
  Command: <code>test-format2.py; test-stage6.py</code>. Revision: `af2ba2975a5f0f6dcedfdcc719a1c646876f5804`.
- `source`: [Current format-2 selection and board policy.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/board.toml)
- `source`: [Historical PKX110 observations through build 39; no claim of migrated-image hardware verification.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)

## 存储与根卷 {#storage}

`host-verified`

组件: `NativeUfs`, `NativeVirtioBlock`, `NativeRamBlock`, `PaganiVerifiedRoot`.

### 硬件与依赖

- The physical root is unixnu on LUN 0, 4096-byte LBAs 44928768..61705983; runtime UFS writes are disabled.

### 配置

- userdata.partition=unixnu; XNU\_NATIVE\_UFS, OWNER\_ROOT\_AUDIT, TRUST\_CACHE\_RUNTIME, OWNER\_UNION\_SYSTEMOS, NATIVE\_RAM\_BLOCK enabled.

### 操作步骤

- Prepare UFS policy archives and original trust; prepare RAM Data on macOS; run test-stage6.py and test-root-audit.py; build the kernel.

### 开发经验

- The physical root is unixnu on LUN 0, 4096-byte LBAs 44928768..61705983; runtime UFS writes are disabled.
- Read-only OS/SystemOS windows use the original APFS/AMFI path. Data is a 1 GiB RAM seed and loses changes on reboot. Virtio is an ABI dependency, not tested 13T hardware. The RAMBlock addon query is synchronized with upstream RamBlock 25c57e0e9b68bf452dd1986914525edc9d2320bc for the shared kernel ABI; missing and invalid handoff ranges are checked on the host. No GPU addon is packaged. Build 48 reached the UI before a read timeout: one busy sample consumed about 1.54 seconds against a 1-second deadline; the subsequent snapshot had DB=0, OCS=0 and a response UPIU. The poller now samples completion once more after expiry. Regression tests reproduce the old false timeout and pass with the fix; Build-49 hardware feedback is recorded below.
- Build 49 was temporarily booted and the user reported no recurring panic during this observation; duration and sustained-load coverage were not supplied. Build 50 merges the five upstream skip-Setup preference groups while mounted. Independent APFS readback confirmed their values, mobile ownership and 0600 modes, and the packed image logical hash passed. seed.json records setup\_skipped=true; the original OS/SystemOS inputs remain read-only.
- The build-50 photo confirms lock-screen entry with the pre-seeded Setup preferences. Data remains volatile; this observation does not qualify persistent writes or long-term UFS stability.
- The shared SMMU planner accepts an explicit mapped extent for the QUP caller. UFS defaults and takeover policy are unchanged. Portable checks cover both build variants and preserve the UFS stream/context while allocating a separate QUP bypass bank.
- Build 54 passed UFS and SMMU regressions with the shared explicit-extent API, then compiled and linked the existing storage driver. No new hardware storage qualification is claimed.

### 完成条件

- Host: register, clock, link and SMMU facts match the board inventory.
- Reads: SCSI capacity, GPT and known blocks are correct; OS/SystemOS windows stay within the allocated unixnu partition.
- Root: the configured volume mounts and launchd starts. Persistence: writes survive reboot within the allocated Data region.

### 当前范围

- Physical writes and persistent Data are unsupported. Never deploy the historical userdata-root.img filename to Android userdata.

### 下一步

- Keep the verified skip-Setup seed preparation and observe continued root reads during the touch retest.

### 证据

- `host`: [Build 54 passed UFS and SMMU regressions with the shared explicit-extent API, then compiled and linked the existing storage driver. No new hardware storage qualification is claimed.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/actions/runs/40369222494)
  Command: <code>Actions build 54; ./unixnu payload; ./unixnu bootimg; APFS/FAT readback; fastboot boot</code>. Revision: `fba147283bead8e3e9f7c3ce9edc36f012bb1ec9`.
- `host`: [Build 53 passed storage regressions. Independent APFS readback confirmed five skip-Setup preference groups, migration, UID/GID 501 and 0600 modes. Packed Data logical hash, kernel Data UUID and embedded seed matched; physical writes remain disabled.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)
  Command: <code>Actions build 53; ./unixnu payload; ./unixnu bootimg; APFS/FAT readback</code>. Revision: `c5edbf3617dd5effd63b74f915218539adca1476`.
- `host`: [Build 51 passed UFS regressions; APFS readback confirmed the five skip-Setup preference groups, migration, UID/GID 501 and 0600 modes. Packed Data logical hash, kernel Data UUID and embedded seed matched; no persistent writes were enabled.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)
  Command: <code>Actions build 51; ./unixnu payload; ./unixnu bootimg; APFS/FAT readback</code>. Revision: `9d9726f53038aa5d090dd13502064de9b4c94128`.
- `host`: [Build 50 passed UFS regressions and full kernel compilation. Independent APFS readback confirmed all five skip-Setup preference groups, migration, UID/GID 501 and 0600 modes; packed Data logical hash, kernel UUID and embedded seed matched.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)
  Command: <code>Actions build 50; ./unixnu payload; ./unixnu bootimg; APFS/FAT readback</code>. Revision: `1e98cc4c10c86904d7cafc6cb98dc4a29538628d`.
- `device`: [Sending and Booting returned OKAY. The user reported no repeat panic during the test, while touch, volume/power keys and brightness remained unusable. Test duration was not specified; this does not qualify long-term stability or input.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)
  Command: <code>fastboot -s 3B15BB01BAT00000 boot stage7-run-49/boot.img; user observation</code>. Revision: `be18db0025fbde66ffd0a55302f9c1bc0fe3c122`.
- `host`: [Build 49 passed configuration, UFS regressions, complete kernel link/prelink and matching boot-image assembly/readback. The UFS completion recheck is included; hardware retest remains pending.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)
  Command: <code>test-format2.py; test-stage6.py; ./unixnu kernel -j 3; ./unixnu payload; ./unixnu bootimg; FAT readback</code>. Revision: `be18db0025fbde66ffd0a55302f9c1bc0fe3c122`.
- `device`: [Build 48 briefly reached the UI. Touch, volume/power keys and brightness did not respond; a UFS read timed out after 297989 reads. The screenshot shows one busy sample, elapsed time beyond the deadline and a later completed DMA snapshot. No partition was flashed.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)
  Command: <code>fastboot -s 3B15BB01BAT00000 boot out/oneplus13t/boot/stage7-run-48/boot.img</code>. Revision: `e6435b2bda6e91431f3bc0c442d1ff9c47be1451`.
- `host`: [Read-only partition bounds, root-window contracts, RAM Data preparation and original storage ABI qualification passed; UFS, Virtio and RAMBlock linked successfully.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/actions/runs/40174199304)
  Command: <code>test-stage6.py; test-root-audit.py; test-ram-data.py; ./unixnu kernel -j 3</code>. Revision: `af2ba2975a5f0f6dcedfdcc719a1c646876f5804`.
- `source`: [Current format-2 selection and board policy.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/board.toml)
- `source`: [Historical PKX110 observations through build 39; no claim of migrated-image hardware verification.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)

## 显示 {#display}

`host-verified`

组件: `NativeMobileDisplay`, `PaganiPanel`.

### 硬件与依赖

- Firmware GOP: 1216x2640, 32 bpp, stride 4864. The active AA594\_P\_7\_A0020 command-mode panel uses DSI0 at 0xae94000 and low-byte-first DCS brightness; normal max 0xdbb, initial level 0x599.

### 配置

- Native Legacy CPU framebuffer, sheng-vsync=60 and pagani-panel=1. Board constants are in PaganiPeripherals.h.

### 操作步骤

- Run test-stage7.py and test-peripherals.py against the resolved tree; run build-pagani-peripherals.py --audit-only against the pinned kernelcache, then build the full display archive with XNU compiler records. After a separately authorized temporary boot, verify first brightness completion before testing slider and power transitions.

### 开发经验

- PaganiPanel derives from the genuine original AppleARMBacklight class with qualified 0x370 storage and 169 virtual entries. It sends DCS 0x51/0x28/0x29 through the command FIFO and stops after a transport failure. The controller setup, DSC and panel timing stay as handed off by firmware.
- The 60 Hz software presentation timer pauses for logical display-off and resumes with a fresh deadline. Build 48 passed MMIO/timer tests, original and compiled-object ABI checks, full kernel link and prelink. PaganiPanel symbols are present in the downloaded kernel; Build-48 hardware testing reached the UI, but brightness and power-key control did not respond before a UFS timeout panic. Physical display control remains unverified.
- Build-49 feedback still reports unusable brightness and short power-key control. Build 50 retains panel map/start failures, DSI command results and accepted brightness requests on screen, with a count of successful DSI commands. The complete display archive and compiled ABI checks passed; physical control awaits runtime feedback.
- Build 50 shows the lock screen. The user confirmed short power presses switch the screen off/on and a long press opens the shutdown UI. PANEL reports DSI disabled \(e00002d8\); physical brightness remains unqualified. This iteration only changes the placement of diagnostic rows to clear the camera cutout.
- The next diagnostic candidate adds two retained SPI rows after KEYS/TOUCH/PANEL, below the camera. Host framebuffer bounds, overlay gating and panic-protection tests pass; no panel programming changes.
- Build 52 reached input object compilation but the early-console dependency check rejected a compiler-generated bzero from the five-row stack snapshot. The renderer now copies one 80-byte row at a time. ARM64 automatic-initialization reproduction and host display/panic checks pass; build 53 subsequently passed the full production object and final kernel build.
- DMA failures reuse the existing two diagnostic rows; SMMU refusal shows slot/bank and SMR/S2CR. The console uses the same per-row stack copy and retains panic/display boundaries. Local sanitizer checks pass.
- Build 54 passed the actual early-console runtime checks, diagnostic-row/panic regressions and compiled backlight ABI checks. DMA/SMMU diagnostic strings are present in the final kernel; brightness remains deferred.
- The first successful touch read now populates the existing two diagnostic rows even if a later protocol check fails. The number and placement of rows remain unchanged. Host console and panic-freeze checks pass.
- Build 55 passed early-console runtime and diagnostic-row/panic checks plus original/compiled backlight ABI checks. The final kernel contains both first-success SPI formats in the existing rows. Brightness remains deferred.
- Build-55 user-transcribed SPI RX and SPI dma rows confirm that the retained success snapshot is visible alongside TOUCH. This is diagnostic-overlay evidence only; brightness remains deferred.
- The existing two SPI diagnostic rows now retain the delay register or an RPMh failure snapshot. No rows are added; display-boundary and panic-preservation tests pass. Panel brightness work remains deferred.

### 完成条件

- A known frame appears with correct geometry and colors, then userland presentation and backlight controls work.

### 当前范围

- The DSI brightness/blanking command path has not passed hardware testing. Physical refresh measurement, TE/vblank synchronization, high-refresh switching, brightness calibration, fade interpolation and full panel suspend/resume remain incomplete. CoreBrightness property access and coexistence with firmware scanout remain unverified.

### 下一步

- Keep brightness work deferred; validate the changed diagnostic rows in the cloud kernel build.

### 证据

- `source`: [The existing two SPI diagnostic rows now retain the delay register or an RPMh failure snapshot. No rows are added; display-boundary and panic-preservation tests pass. Panel brightness work remains deferred.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)
- `device`: [Build-55 user-transcribed SPI RX and SPI dma rows confirm that the retained success snapshot is visible alongside TOUCH. This is diagnostic-overlay evidence only; brightness remains deferred.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)
  Command: <code>Build-55 temporary boot; user transcribed TOUCH and both SPI rows, then confirmed return code b9</code>. Revision: `664530f8de814569c8255d07b67c7e2f6d6db3bd`.
- `host`: [Build 55 passed early-console runtime and diagnostic-row/panic checks plus original/compiled backlight ABI checks. The final kernel contains both first-success SPI formats in the existing rows. Brightness remains deferred.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/actions/runs/40437346840)
  Command: <code>Actions build 55; ./unixnu payload; ./unixnu bootimg; APFS/FAT readback; fastboot boot</code>. Revision: `664530f8de814569c8255d07b67c7e2f6d6db3bd`.
- `host`: [Build 54 passed the actual early-console runtime checks, diagnostic-row/panic regressions and compiled backlight ABI checks. DMA/SMMU diagnostic strings are present in the final kernel; brightness remains deferred.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/actions/runs/40369222494)
  Command: <code>Actions build 54; ./unixnu payload; ./unixnu bootimg; APFS/FAT readback; fastboot boot</code>. Revision: `fba147283bead8e3e9f7c3ce9edc36f012bb1ec9`.
- `host`: [Build 53 passed the actual early-console runtime/FP checks after reducing the status snapshot to one 80-byte row. Diagnostic drawing, panic protection, compiled backlight ABI and full link/prelink passed. No new hardware brightness result is claimed.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)
  Command: <code>Actions build 53; ./unixnu payload; ./unixnu bootimg; APFS/FAT readback</code>. Revision: `c5edbf3617dd5effd63b74f915218539adca1476`.
- `host`: [Build 51 passed diagnostic-row drawing and panic-protection tests, original/compiled backlight ABI checks and full kernel link/prelink. The status rows moved below the camera; no new hardware brightness result is claimed.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)
  Command: <code>Actions build 51; ./unixnu payload; ./unixnu bootimg; APFS/FAT readback</code>. Revision: `9d9726f53038aa5d090dd13502064de9b4c94128`.
- `host`: [Build 50 passed display/status drawing regressions, C/C++ compilation, original and compiled backlight ABI checks, final kernel link/prelink and image readback. Physical brightness, blanking and the PANEL row await runtime observation.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)
  Command: <code>Actions build 50; ./unixnu payload; ./unixnu bootimg; APFS/FAT readback</code>. Revision: `1e98cc4c10c86904d7cafc6cb98dc4a29538628d`.
- `device`: [Sending and Booting returned OKAY. The user reported no repeat panic during the test, while touch, volume/power keys and brightness remained unusable. Test duration was not specified; this does not qualify long-term stability or input.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)
  Command: <code>fastboot -s 3B15BB01BAT00000 boot stage7-run-49/boot.img; user observation</code>. Revision: `be18db0025fbde66ffd0a55302f9c1bc0fe3c122`.
- `device`: [Build 48 briefly reached the UI. Touch, volume/power keys and brightness did not respond; a UFS read timed out after 297989 reads. The screenshot shows one busy sample, elapsed time beyond the deadline and a later completed DMA snapshot. No partition was flashed.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)
  Command: <code>fastboot -s 3B15BB01BAT00000 boot out/oneplus13t/boot/stage7-run-48/boot.img</code>. Revision: `e6435b2bda6e91431f3bc0c442d1ff9c47be1451`.
- `host`: [Display timer and DSI transport checks passed. The owned panel object passed the original/compiled ABI audit, entered the display archive and linked into the prelinked kernel; no hardware result claimed.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/actions/runs/40183635568)
  Command: <code>test-stage7.py; test-peripherals.py; ./unixnu kernel -j 3</code>. Revision: `e6435b2bda6e91431f3bc0c442d1ff9c47be1451`.
- `source`: [DSI command transport, genuine backlight ancestry, timer PM integration and explicit runtime limits; not a complete-kernel or device result.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/drivers/PaganiPanel/README.md)
- `host`: [Display lifecycle checks and original Legacy ABI qualification passed; the CPU presentation archive compiled and linked. The migrated framebuffer has not been observed on hardware.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/actions/runs/40174199304)
  Command: <code>test-stage7.py; ./unixnu kernel -j 3</code>. Revision: `af2ba2975a5f0f6dcedfdcc719a1c646876f5804`.
- `source`: [Current format-2 selection and board policy.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/board.toml)
- `source`: [Historical PKX110 observations through build 39; no claim of migrated-image hardware verification.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)

## 输入 {#input}

`host-verified`

组件: `PaganiInput`, `QcomGeniSpi`.

### 硬件与依赖

- S3910 HBP on GENI SPI QUP1 S4 at 0xa90000, wrapper 0xac0000, mode 0, maximum 19 MHz. GPIOs 48..51 carry SPI; reset 161 and ATTN 162 are active low. TLMM GPIO windows include the SM8750 0x100000 offset.
- SPMI v7 observer: PON SID 0 peripheral 0x13, bits 7/6 = Power/Volume Up; GPIO SID 1 peripheral 0x8d bit 0 active low = Volume Down.
- Live DTB: apps-smmu at 0x15000000, size 0x100000; QUP wrapper stream 0xa3 for SE DMA. GPI uses a different stream and is not selected.

### 配置

- pagani-touch=1 and pagani-buttons=1 select two original-ABI HID devices. Board wiring and timing are defined in PaganiPeripherals.h.

### 操作步骤

- Run test-peripherals.py --tree &lt;resolved-tree&gt; and the original HID ABI audit; build the full archive. On hardware first check SPI protocol, ID/application status and LBP/configuration acknowledgements, then single contacts, coordinate orientation, simultaneous contacts, releases and physical key holds.

### 开发经验

- The stock HBP driver exposes an LBP fallback through dynamic config 0x11=2. The new transport drains queued raw frames, installs and reads back a custom report format, filters palms and emits explicit releases with stable IDs. TouchComm CRC command suffixes are detected from identification.
- PMIC reads are bounded and keys use 32 ms debounce. Failed key reads release all keys; touch transport failure releases held contacts and disables further touch reads. ATTN is polled at 8 ms, keys at 16 ms. Build 48 passed portable tests, the original 207-slot HID and compiled-object ABI audits, C/C++ compilation, final link and prelink. Input, S3910 and GENI SPI symbols are present in the downloaded kernel; build-48 hardware testing found touch and volume/power keys unresponsive. Initialization status and event routing still need runtime evidence.
- Build-49 touch and keys remained unusable. Build 50 puts a keyboard application before the digitizer as in upstream NativeHidInput 5f3a37c; the physical report IDs and payload sizes remain unchanged. Retained status distinguishes HID resource/class/start failures, SPMI channel/subtype checks, SPI clock/firmware/setup, TouchComm startup and report submission.
- Build 50 confirms power-key short/long actions and increasing key report counts for volume presses. Touch stops at TouchComm start with r=ffffffb9 and n=0; its raw value is obscured by the camera. Compared with OnePlus S3910 and data-a-live S3910P, build 51 sends 0xff during full-duplex reads, supports validated v1/v2 headers, v2 CRC/ACK/RETRY/fragments, a 100 ms reset wait and detailed retained diagnostics. Host tests, full kernel build and image readback passed. The matching image was temporarily booted; the hardware fault is not yet qualified as fixed.
- Build 51 still has no touch response: T0 00 header r=ffffff92 v=0 n=0. The first four-byte full-duplex SPI transfer times out before protocol detection; v=0 is the unset header detail. The next candidate forwards GENI firmware/interface-disable and pre-cancel state/IRQ/TX/RX FIFO snapshots to two visible rows. It changes no transport mode, IRQ routing or wiring. Actual adapter and existing transport regressions pass.
- Build 53 passed full compilation/link/prelink and matching image readback; fastboot accepted the temporary boot. The pre-cancel GENI rows are present in the final kernel. No FIFO/DMA or IRQ-routing change has been made, and usable touch remains unverified.
- Build 53 remains unresponsive: TOUCH T0 00 header r=ffffff92 v=0 n=0; SPI fw=102 if=1 st=41 irq=0; SPI FIFO tx=0 rx=0. Bit 0 of if confirms FIFO disabled; bit 0 of st indicates the active master. The candidate reuses SE DMA with separate 4 KiB TX/RX buffers, explicit cache maintenance and the live-DTB QUP SID 0xa3. It refuses existing translated/shared firmware mappings and displays SMR/S2CR on refusal. DMA-exposed buffers remain allocated until reboot pending reset qualification.
- Build 54 compiled the DMA allocation/cache/SMMU adapter against the original kernel ABI and passed transport/contact/button regressions. The matching image passed local readback and fastboot boot. Whether the QUP stream is available and SE DMA works on the phone remains unverified.
- Build 54 returns success from its first SPI read, then rejects four zero header bytes with -71 before IOHIDDevice::start. No SPI error rows are expected on that path. The candidate captures the first successful read length/head, ATTN before/after, RESET GPIO low bits, DMA length-in readings and GENI status. Later protocol rejection preserves that evidence; no protocol, reset-timing or transport-mode change is made.
- Build 55 passed actual-adapter first-success retention and zero-header rejection tests, protocol/contact/button/PIO/SE DMA regressions, C/C++ compilation and original/compiled HID ABI checks. Both first-read diagnostic formats are present in the final kernel. The matching image passed readback and fastboot boot; raw RX/GPIO/counter values and usable touch remain unverified.
- Build 55 reports TOUCH T0 00 header r=ffffffb9 v=0 n=0; SPI RX n=4 h=00000000 a=0/0 rst=3; SPI dma=1 ti=4 ri=4 st=0. The RX canary is replaced by zeros and both DMA length-in readings are 4, but no valid sensor header or UI touch is obtained. ATTN is low before/after; RESET input and output latch are high. Stock Android explicitly enables ldob4 at 1.8 V and ldob16 at 3.1 V; this port still adopts retained rails, whose XNU state is unknown.
- The Android baseline uses the OnePlus HBP driver on the local 6.6.118 kernel. Retained GPI logs show ff TX, a5 23 ca 05 RX, CS delay 50 and inter-word delay 0. Idle RESET/ATTN are high and SPI is runtime suspended; live sampling captured no gesture or active interval. The current port omits an explicit SE\_SPI\_DELAY\_COUNTERS write, but its inherited value and XNU rail state remain unknown, so timing is a candidate cause rather than a confirmed diagnosis.
- A synchronized Android gesture capture contains 40 complete press/release cycles over 18.793234 seconds, 726 frames and 51 overlapping valid SPI RX records. Following the hummer S3910 power diagnosis, the candidate validates the 13T command DB resources, requests 1800/3100 mV, waits 200 ms, and sets checked CS/word delays to 50/0 before reset. First-read diagnostics include dly; power failures preserve resource, RSC, TCS and acknowledgement state. Host regressions pass; SE DMA and protocol validation are unchanged, and XNU touch remains unverified.

### 完成条件

- Touches map to the display, simultaneous contacts keep stable IDs, release events arrive, and buttons produce expected HID reports.

### 当前范围

- GENI firmware is retained. RPMh requests and SE DMA need XNU hardware validation; no physical rail voltage has been measured. No GIC IRQ path, GPI DMA, v1 command fragmentation, firmware recovery or system-sleep wake. Existing translated QUP mappings are refused. The exposed 8 KiB DMA buffer and any timed-out TCS remain reserved until reboot pending reset qualification. LBP availability, coordinates, UI delivery and system edge gestures remain unverified.

### 下一步

- Complete the authorized cloud build, download and verify its kernel and paired inputs, then wait for the user before any device boot or flash.

### 证据

- `source`: [A synchronized Android gesture capture contains 40 complete press/release cycles over 18.793234 seconds, 726 frames and 51 overlapping valid SPI RX records. Following the hummer S3910 power diagnosis, the candidate validates the 13T command DB resources, requests 1800/3100 mV, waits 200 ms, and sets checked CS/word delays to 50/0 before reset. First-read diagnostics include dly; power failures preserve resource, RSC, TCS and acknowledgement state. Host regressions pass; SE DMA and protocol validation are unchanged, and XNU touch remains unverified.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)
- `device`: [The Android baseline uses the OnePlus HBP driver on the local 6.6.118 kernel. Retained GPI logs show ff TX, a5 23 ca 05 RX, CS delay 50 and inter-word delay 0. Idle RESET/ATTN are high and SPI is runtime suspended; live sampling captured no gesture or active interval. The current port omits an explicit SE\_SPI\_DELAY\_COUNTERS write, but its inherited value and XNU rail state remain unknown, so timing is a candidate cause rather than a confirmed diagnosis.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)
  Command: <code>Read-only ADB root capture of Android regulator, GPIO, clock and existing SPI IPC logs; compare OnePlus touch and GENI source</code>. Revision: `bdeec6693f1b8488a3286446f0b93c13c02d6785`.
- `device`: [Build 55 reports TOUCH T0 00 header r=ffffffb9 v=0 n=0; SPI RX n=4 h=00000000 a=0/0 rst=3; SPI dma=1 ti=4 ri=4 st=0. The RX canary is replaced by zeros and both DMA length-in readings are 4, but no valid sensor header or UI touch is obtained. ATTN is low before/after; RESET input and output latch are high. Stock Android explicitly enables ldob4 at 1.8 V and ldob16 at 3.1 V; this port still adopts retained rails, whose XNU state is unknown.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)
  Command: <code>Build-55 temporary boot; user transcribed TOUCH and both SPI rows, then confirmed return code b9</code>. Revision: `664530f8de814569c8255d07b67c7e2f6d6db3bd`.
- `host`: [Build 55 passed actual-adapter first-success retention and zero-header rejection tests, protocol/contact/button/PIO/SE DMA regressions, C/C++ compilation and original/compiled HID ABI checks. Both first-read diagnostic formats are present in the final kernel. The matching image passed readback and fastboot boot; raw RX/GPIO/counter values and usable touch remain unverified.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/actions/runs/40437346840)
  Command: <code>Actions build 55; ./unixnu payload; ./unixnu bootimg; APFS/FAT readback; fastboot boot</code>. Revision: `664530f8de814569c8255d07b67c7e2f6d6db3bd`.
- `device`: [TOUCH T0 00 header r=ffffffb9 v=0 n=0. SPI returned success but the protocol parser rejected a zero header; touch setup stopped before HID start. No SPI error rows appeared. Valid sensor data and UI touch remain unverified.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)
  Command: <code>Build-54 temporary boot; user transcribed TOUCH row and absent SPI rows</code>. Revision: `fba147283bead8e3e9f7c3ce9edc36f012bb1ec9`.
- `host`: [Build 54 compiled the DMA allocation/cache/SMMU adapter against the original kernel ABI and passed transport/contact/button regressions. The matching image passed local readback and fastboot boot. Whether the QUP stream is available and SE DMA works on the phone remains unverified.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/actions/runs/40369222494)
  Command: <code>Actions build 54; ./unixnu payload; ./unixnu bootimg; APFS/FAT readback; fastboot boot</code>. Revision: `fba147283bead8e3e9f7c3ce9edc36f012bb1ec9`.
- `device`: [First four-byte SPI read still times out. fw=102 if=1 st=41 irq=0; FIFO tx=0 rx=0. FIFO interface disabled is observed; successful DMA and touch are not established.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)
  Command: <code>Build-53 temporary boot; user transcribed TOUCH and SPI rows</code>. Revision: `c5edbf3617dd5effd63b74f915218539adca1476`.
- `host`: [Build 53 passed actual SPI callback/snapshot and protocol/contact/button regressions, C/C++ compilation and original/compiled HID ABI checks. The final image contains both SPI status formats and was temporarily booted; hardware register values are pending.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)
  Command: <code>Actions build 53; ./unixnu payload; ./unixnu bootimg; APFS/FAT readback</code>. Revision: `c5edbf3617dd5effd63b74f915218539adca1476`.
- `device`: [Touch remains unresponsive. TOUCH T0 00 header r=ffffff92 v=0 n=0 locates the timeout in the first SPI transfer, before protocol identification. No GENI register snapshot was visible in build 51.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)
  Command: <code>Build-51 temporary boot; user transcribed TOUCH status</code>. Revision: `9d9726f53038aa5d090dd13502064de9b4c94128`.
- `host`: [Build 51 passed actual SPI read callback tests, v1/v2 protocol and contact/button/SPMI/GENI regressions, C/C++ compilation and original/compiled HID ABI checks. The matching image was temporarily booted; touch behavior and protocol status await observation.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)
  Command: <code>Actions build 51; ./unixnu payload; ./unixnu bootimg; APFS/FAT readback</code>. Revision: `9d9726f53038aa5d090dd13502064de9b4c94128`.
- `device`: [Lock screen after skipping Setup; short power presses switch the screen off/on, long press opens shutdown UI. Volume presses advance the key-report counter. Touch has no response: TouchComm start r=ffffffb9, n=0, raw value hidden by camera.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)
  Command: <code>Build-50 temporary boot; photo and user observation</code>. Revision: `1e98cc4c10c86904d7cafc6cb98dc4a29538628d`.
- `host`: [Build 50 passed actual HID descriptor parsing, TouchComm/contact/button/SPMI/GENI tests, C/C++ compilation and original/compiled HID ABI checks. The matching image was temporarily booted; touch/key response and KEYS/TOUCH rows await observation.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)
  Command: <code>Actions build 50; ./unixnu payload; ./unixnu bootimg; APFS/FAT readback</code>. Revision: `1e98cc4c10c86904d7cafc6cb98dc4a29538628d`.
- `device`: [Sending and Booting returned OKAY. The user reported no repeat panic during the test, while touch, volume/power keys and brightness remained unusable. Test duration was not specified; this does not qualify long-term stability or input.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)
  Command: <code>fastboot -s 3B15BB01BAT00000 boot stage7-run-49/boot.img; user observation</code>. Revision: `be18db0025fbde66ffd0a55302f9c1bc0fe3c122`.
- `device`: [Build 48 briefly reached the UI. Touch, volume/power keys and brightness did not respond; a UFS read timed out after 297989 reads. The screenshot shows one busy sample, elapsed time beyond the deadline and a later completed DMA snapshot. No partition was flashed.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)
  Command: <code>fastboot -s 3B15BB01BAT00000 boot out/oneplus13t/boot/stage7-run-48/boot.img</code>. Revision: `e6435b2bda6e91431f3bc0c442d1ff9c47be1451`.
- `host`: [TouchComm, contact lifecycle, key debounce/failure, SPMI and GENI tests passed. The HID object passed ABI checks and the S3910/GENI sources compiled as C; all three objects linked into the prelinked kernel. Hardware input remains untested.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/actions/runs/40183635568)
  Command: <code>test-peripherals.py; test-stage7.py; ./unixnu kernel -j 3</code>. Revision: `e6435b2bda6e91431f3bc0c442d1ff9c47be1451`.
- `source`: [Physical HID adapters, bounded TouchComm/SPMI paths, contact and key lifecycle tests; no hardware result claimed.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/drivers/PaganiInput/README.md)

## GPU {#gpu}

`planned`

### 硬件与依赖

- Adreno 830/SM8750 differs from the catalog A740/SM8550 implementation; no GPU component is selected.

### 配置

- No driver is enabled for this subsystem.

### 操作步骤

- Follow the subsystem guide to identify hardware, firmware and ABI inputs before enabling a component.

### 开发经验

- Adreno 830/SM8750 differs from the catalog A740/SM8550 implementation; no GPU component is selected.
- The SpringBoard/input candidate selects no GPU driver or bridge. Updated upstream Adreno submodules are outside the OnePlus 13T component selection; UI presentation still uses the CPU framebuffer.

### 完成条件

- GPU submissions complete, mapping/fence handling is correct, a known image renders, and the selected Metal client presents it.

### 当前范围

- No implemented or hardware-verified path is available for this subsystem.

### 下一步

- Capture SM8750 GPU/GMU resources and the firmware manifest; qualify a matching implementation before enabling GPU components.

### 证据

按下一步操作收集证据。

## 网络 {#network}

`planned`

### 硬件与依赖

- No verified Wi-Fi or cellular path is selected for PKX110.

### 配置

- No driver is enabled for this subsystem.

### 操作步骤

- Follow the subsystem guide to identify hardware, firmware and ABI inputs before enabling a component.

### 开发经验

- No verified Wi-Fi or cellular path is selected for PKX110.
- The SpringBoard candidate prepares an offline UI input test; the selected components contain no Wi-Fi, Bluetooth or cellular transport.

### 完成条件

- Scanning, association, address configuration and sustained receive/transmit traffic pass with the selected firmware.

### 当前范围

- No implemented or hardware-verified path is available for this subsystem.

### 下一步

- Identify the WLAN transport, firmware and IRQ/DMA requirements from the stock DTB before selecting a driver.

### 证据

按下一步操作收集证据。

## 音频 {#audio}

`planned`

### 硬件与依赖

- DSP/codec firmware interfaces, routes and playback/capture remain unimplemented.

### 配置

- No driver is enabled for this subsystem.

### 操作步骤

- Follow the subsystem guide to identify hardware, firmware and ABI inputs before enabling a component.

### 开发经验

- DSP/codec firmware interfaces, routes and playback/capture remain unimplemented.
- The merged OS identity adds the J120AP product-id and product/audio wireless-splitter metadata used by original services. No audio controller, codec or playback/capture backend is selected for this board.

### 完成条件

- Each declared route carries the selected audio format through playback or capture and handles start/stop correctly.

### 当前范围

- No implemented or hardware-verified path is available for this subsystem.

### 下一步

- Map the DSP, codec, clock and firmware dependencies from the stock platform before implementing an audio route.

### 证据

按下一步操作收集证据。

## 电源 {#power}

`host-verified`

组件: `ShengPlatformPower`.

### 硬件与依赖

- The component preserves the original Apple PMGR ABI and restricted boot-time operations.

### 配置

- XNU\_SHENG\_PMGR=y; sheng-pmgr=2; sleep-disabled=1.

### 操作步骤

- Build the compatibility PMGR archive against the exact kernelcache; observe boot transitions before changing any firmware-owned vote.

### 开发经验

- The existing PMGR compatibility behavior is unchanged. PaganiInput adds QUP1 S4 clock votes and GPIO reset while retaining firmware regulator state. PaganiPanel requests display blanking without turning off rails or replacing full suspend/resume.
- Battery, charging, suspend and frequency scaling remain unverified.
- The new touch-only RPMh path validates command DB bounds, unique VRM resources and captured board addresses before any rail write. It uses only an idle ACTIVE TCS, verifies register readback and all three voltage/mode/enable acknowledgements, and preserves unrelated TCSes and IRQ bits. Timeout retains the armed slot with its IRQ masked. Shared rail votes remain enabled on cleanup. This establishes a tested host implementation, not measured rail voltage or XNU hardware success.

### 完成条件

- Declared power controls and battery readings match observations; each claimed sleep/resume transition restores its dependent peripherals.

### 当前范围

- Battery, charging, sleep and full regulator/clock control are unsupported.

### 下一步

- Complete the authorized cloud build, download and verify its kernel and paired inputs, then wait for the user before any device boot or flash.

### 证据

- `source`: [The new touch-only RPMh path validates command DB bounds, unique VRM resources and captured board addresses before any rail write. It uses only an idle ACTIVE TCS, verifies register readback and all three voltage/mode/enable acknowledgements, and preserves unrelated TCSes and IRQ bits. Timeout retains the armed slot with its IRQ masked. Shared rail votes remain enabled on cleanup. This establishes a tested host implementation, not measured rail voltage or XNU hardware success.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)
- `host`: [The PMGR builder qualified the pinned original imports/provider dispatch and linked its archive. Physical power transitions, battery and frequency control remain unverified.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/actions/runs/40174199304)
  Command: <code>./unixnu kernel -j 3</code>. Revision: `af2ba2975a5f0f6dcedfdcc719a1c646876f5804`.
- `source`: [Current format-2 selection and board policy.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/board.toml)
- `source`: [Historical PKX110 observations through build 39; no claim of migrated-image hardware verification.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)

## 镜像组装 {#packaging}

`host-verified`

组件: `NativePrelink`.

### 硬件与依赖

- Kernel ABI and IPSW stay at 21H461. NativePrelink stays pinned in the community bundle; the OS series selects its matching patches.

### 配置

- kernel.prelink roots preserve the previously qualified subset; payload.adt.root\_match\_volume\_uuid=04769D26-2CA0-4825-B443-E2E5F88300F2.

### 操作步骤

- Run ipsw fetch, kernel, build package, firmware, payload, bootimg in order; inspect payload.json and the ADT in FAT.

### 开发经验

- Kernel ABI and IPSW stay at 21H461. NativePrelink stays pinned in the community bundle; the OS series selects its matching patches.
- Four byte-qualified userspace fixups now come from the shared OS profile and common validated-page implementation. Board root UUID and PackedRAMDisk/TrustCache placeholders are preserved.
- Android boot v4 packages gzip\(BootShim+3 MiB FD+160 MiB FAT\) followed by all stock DTBs; Android ramdisk remains empty.
- The build-48 kernel and matching trust/Data inputs are assembled at out/oneplus13t/boot/stage7-run-48/boot.img: 87945216 bytes, SHA-256 ed302c539495dcae18e21fefe0a424d4f09f2b5f480741dbd5b5f6f7ab44a9fe. The existing firmware was reused after confirming its source inputs and FD hash were unchanged. Image unpacking and FAT readback passed. The later temporary boot reached the UI, with nonfunctional peripheral controls and a subsequent UFS read-timeout panic; see STAGE6.md.
- Build 49 boot.img remains 87945216 bytes with SHA-256 5bceb7c3cac31cafde66d8b349c0fec547684aa16e7266645af544a7ae20564f. Its temporary boot succeeded and the user reported no repeat panic in this test. The next image must pair its new kernel, trust cache and pre-edited skip-Setup Data from one cloud build; the next image does not exist yet.

### 完成条件

- Kernel and prelink succeed, payload contains all declared inputs, and the boot image matches the bootloader format and size limit.

### 当前范围

- Host construction does not establish runtime equivalence to build 39.

### 下一步

- After the next cloud build, assemble and read back the matching image; verify seed.json setup\_skipped=true and preserve build 49 as the tested baseline.

### 证据

- `device`: [Sending and Booting returned OKAY. The user reported no repeat panic during the test, while touch, volume/power keys and brightness remained unusable. Test duration was not specified; this does not qualify long-term stability or input.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)
  Command: <code>fastboot -s 3B15BB01BAT00000 boot stage7-run-49/boot.img; user observation</code>. Revision: `be18db0025fbde66ffd0a55302f9c1bc0fe3c122`.
- `host`: [Build 49 passed configuration, UFS regressions, complete kernel link/prelink and matching boot-image assembly/readback. The UFS completion recheck is included; hardware retest remains pending.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)
  Command: <code>test-format2.py; test-stage6.py; ./unixnu kernel -j 3; ./unixnu payload; ./unixnu bootimg; FAT readback</code>. Revision: `be18db0025fbde66ffd0a55302f9c1bc0fe3c122`.
- `device`: [Build 48 briefly reached the UI. Touch, volume/power keys and brightness did not respond; a UFS read timed out after 297989 reads. The screenshot shows one busy sample, elapsed time beyond the deadline and a later completed DMA snapshot. No partition was flashed.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)
  Command: <code>fastboot -s 3B15BB01BAT00000 boot out/oneplus13t/boot/stage7-run-48/boot.img</code>. Revision: `e6435b2bda6e91431f3bc0c442d1ff9c47be1451`.
- `host`: [The build-48 boot image passed Android v4, embedded payload and stock-DTB round-trip checks. FAT readback matched the cloud kernel, trust cache and Data seed; all three pagani peripheral arguments and the 4 GiB DarwinBoot, root UUID and PackedRAMDisk/TrustCache handoff properties passed. Hardware remains untested.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/README.md)
  Command: <code>./unixnu payload; ./unixnu bootimg; mcopy FAT readback and input hash checks</code>. Revision: `fcab49e2ea2f9ddfaa08ee6e8109ba7ed67029ac`.
- `host`: [Kernel/prelink, 160 MiB FAT payload and 87928832-byte Android v4 boot image succeeded. Extracted ADT and payload kernel hashes match the reports; no GPU addon is supplied.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/MIGRATION.md)
  Command: <code>./unixnu kernel -j 3; ./unixnu build package; ./unixnu firmware; ./unixnu payload; ./unixnu bootimg</code>. Revision: `af2ba2975a5f0f6dcedfdcc719a1c646876f5804`.
- `source`: [Current format-2 selection and board policy.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/board.toml)
- `source`: [Historical PKX110 observations through build 39; no claim of migrated-image hardware verification.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)

## 诊断 {#diagnostics}

`host-verified`

组件: `BootProgress`, `Stage7Probe`.

### 硬件与依赖

- Early framebuffer, root checkpoints and panic rendering remain enabled. Source-only diagnostics are separate from the prelinked userspace kernel.

### 配置

- XNU\_BOOT\_PROGRESS=y; XNU\_EARLY\_BOOT\_PROGRESS=y; optional native-root-audit triggers the binding report.

### 操作步骤

- Run the panic/ADT/boot container checks; preserve old run artifacts; capture the last completed checkpoint in a future explicitly authorized temporary boot.

### 开发经验

- Early framebuffer, root checkpoints and panic rendering remain enabled. Source-only diagnostics are separate from the prelinked userspace kernel.
- Build 39 reached the iPadOS UI; see STAGE6.md. The complete driver archive plan passes on macOS. The early boot-logo builder now reads the IPSW from the format-2 output root and compiles successfully. A host regression checks that the final link selects the RAMBlock object beside the configured archive; the final kernel/prelink and local firmware, payload and boot-image assembly have now passed; build 48 subsequently reached the UI and captured the UFS timeout panic. Its screenshot distinguishes the earlier busy sample from the later completed DMA snapshot; see STAGE6.md.
- Build-49 feedback reports no repeat panic while input and brightness remain unusable. pagani-peripheral-status=1 keeps KEYS/TOUCH/PANEL stages, hexadecimal result/sample and decimal successful report/command counts visible after display handoff. The same three rows refresh once per second and after frame copies; host tests cover opt-in behavior, bounds, preserved UI pixels and panic precedence.
- Power failures retain PWR address/hardware/slot and status/command snapshots in the existing two diagnostic rows. Successful first-read diagnostics add the actual SPI delay register. Host tests verify formatting, retained first-read evidence and frozen panic output; kernel compilation and hardware readings are pending.

### 完成条件

- Each claimed milestone has a reproducible command, a matching source/image revision and an accessible result.

### 当前范围

- The first migrated-image hardware test reached the UI but did not establish stable operation or working peripherals. Historical observations remain identified separately.

### 下一步

- Complete the authorized cloud build, download and verify its kernel and paired inputs, then wait for the user before any device boot or flash.

### 证据

- `source`: [Power failures retain PWR address/hardware/slot and status/command snapshots in the existing two diagnostic rows. Successful first-read diagnostics add the actual SPI delay register. Host tests verify formatting, retained first-read evidence and frozen panic output; kernel compilation and hardware readings are pending.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)
- `device`: [Sending and Booting returned OKAY. The user reported no repeat panic during the test, while touch, volume/power keys and brightness remained unusable. Test duration was not specified; this does not qualify long-term stability or input.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)
  Command: <code>fastboot -s 3B15BB01BAT00000 boot stage7-run-49/boot.img; user observation</code>. Revision: `be18db0025fbde66ffd0a55302f9c1bc0fe3c122`.
- `device`: [Build 48 briefly reached the UI. Touch, volume/power keys and brightness did not respond; a UFS read timed out after 297989 reads. The screenshot shows one busy sample, elapsed time beyond the deadline and a later completed DMA snapshot. No partition was flashed.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)
  Command: <code>fastboot -s 3B15BB01BAT00000 boot out/oneplus13t/boot/stage7-run-48/boot.img</code>. Revision: `e6435b2bda6e91431f3bc0c442d1ff9c47be1451`.
- `host`: [Source-kernel regressions, early console compilation and panic-entry contract passed in CI; runtime checkpoints still require a hardware boot.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/actions/runs/40174199304)
  Command: <code>test-kernel-source.py; drivers/BootProgress/Test/panic-entry.py</code>. Revision: `af2ba2975a5f0f6dcedfdcc719a1c646876f5804`.
- `source`: [Current format-2 selection and board policy.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/board.toml)
- `source`: [Historical PKX110 observations through build 39; no claim of migrated-image hardware verification.](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/3a12121d3ef9fdee1636500665c5cbb4baf5b83c/STAGE6.md)

</div>
