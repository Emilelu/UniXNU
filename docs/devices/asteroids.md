# Nothing Phone \(3a\) \(asteroids\)

[rootstockos/UniXNU-asteroids](https://github.com/rootstockos/UniXNU-asteroids)

<div v-pre>

Nothing Phone \(3a\) runs the unchanged iPad7,1 iPadOS 17.7.11 image from its UFS userdata partition, with shared SM7635 support and board-owned storage, GPU, input and power integration. Bring-up runs as numbered staged tests; their results are in docs/asteroids-gpu-gen8.md and docs/asteroids-touch.md of rootstockos/iosonandng.

Source record: [porting.toml](https://github.com/rootstockos/UniXNU-asteroids/blob/decbdedfe9469322fbccc950a1a7248bca89b6e7/porting.toml), `decbdedfe9469322fbccc950a1a7248bca89b6e7`.

This page is generated from the device record.

| Area | Status |
| --- | --- |
| [Configuration](#configuration) | `implemented` |
| [Firmware and boot](#firmware) | `implemented` |
| [CPU and interrupts](#cpu) | `implemented` |
| [Memory and DMA](#memory) | `implemented` |
| [Storage and root](#storage) | `implemented` |
| [Display](#display) | `implemented` |
| [Input](#input) | `implemented` |
| [GPU](#gpu) | `implemented` |
| [clock](#clock) | `device-verified` |
| [Network](#network) | `planned` |
| [Audio](#audio) | `planned` |
| [Power](#power) | `implemented` |
| [Image assembly](#packaging) | `implemented` |
| [Diagnostics](#diagnostics) | `implemented` |

## Configuration {#configuration}

`implemented`

Components: `ArmDTPlatform`, `XnuPrelink`.

### Hardware and dependencies

- SM7635 SoC profile \(rootstockos/UniXNU-sm7635-common\), iPadOS 17.7.11 build 21H461, asteroids\_defconfig, the board's own driver forks as submodules.

### Configuration

- board.soc\_source = sm7635; board.os\_profile = ipados-17.7.11-21H461; schema\_version = 2.
- drivers/Adreno740, drivers/ShengUfs, drivers/ShengHidInput, drivers/ArmDTPlatform and kits/AdrenoFirmware are this repository's submodules at their catalog paths and take precedence over UniXNU's.

### Procedure

- Run ./unixnu status --json -D ../UniXNU-asteroids from rootstockos/UniXNU and review profiles, components and patch order.

### Development findings

- Format 2 builds every selected component's kernel recipe, so \[kernel\] archives lists them as component: entries in the format 1 order; build-arm-driver.py skips Adreno740 and VirtioMmioBlock while their configuration switches are off, as format 1 never built them \(T36 run 40297420036\).
- Format 2 applies the arch, SoC and OS configuration fragments before the defconfig; bootstrap\_defconfig turns off the five options common.config adds, so both passes have their format 1 configuration \(checked with parse\_config: no differences\).
- Format 2 keeps only catalog components, so the forks of NativeAdreno and NativeUfs moved from their legacy names to drivers/Adreno740 and drivers/ShengUfs; legacy aliases are made only for UniXNU's own sources.
- T36 is the first format 2 image \(build tag T36\). Every board.toml value matches the format 1 board \(4f05a36\) except what moved to the SoC and OS profiles, the ADT tool options and the firmware pins \(proprietary-files.txt\); a dry-run pack caught kernel\_args lost in the first rewrite.
- The ADT from the shared generator matches the former make-asteroids-adt.py output except for the OS profile's additions \(J120AP first in the root compatible, product-id, /product/audio\) and the arm-io window, which now covers UFS.
- T40a \(2026-10-27\): every fork has one working branch, asteroids \(former branches are archive/\* tags\); drivers/ArmDTPlatform became the submodule fork rootstockos/ArmDTPlatform; the record check runs rootstockos/UniXNU's workflow and catalog, since UniXNU main's catalog does not know Sm7635Platform or QcomPmicRtc.
- T40c \(2026-10-27\): build tag T40; the GPU governor and fence spin are board defaults \(see gpu\).

### Completion criteria

- All source pins resolve; every selected component has a record; status shows the intended overrides and patch order.

### Current limits

- The SoC profile is pinned to a local checkout \(local.toml\) until rootstockos/UniXNU-sm7635-common is published.

### Next action

- Publish the SoC repository and pin its commit in feeds.toml.

### Evidence

- `source`: [Format 2 board configuration with the SM7635 SoC and 21H461 OS profiles.](https://github.com/rootstockos/UniXNU-asteroids/blob/decbdedfe9469322fbccc950a1a7248bca89b6e7/board.toml)

## Firmware and boot {#firmware}

`implemented`

Components: `DarwinBoot`.

### Hardware and dependencies

- rootstockos/uefi-asteroids \(Mu-Silicium VolcanoPkg and asteroidsPkg\) with UniXNU, UniXNUDxe and DarwinBoot.
- The 3a's ABL loads the boot image with fastboot boot; it ignores the boot image's ramdisk.

### Configuration

- \[bootimg\] payload\_in\_kernel = true: the payload rides in the kernel image and ShengBootMemoryDxe finds it in the Kernel memory region.

### Procedure

- Build the payload and boot image with ./unixnu build payload and ./unixnu bootimg --dtb \(the phone's live DTB\), then fastboot boot the image.

### Development findings

- The ABL passes the vendor\_boot and init\_boot ramdisks plus bootconfig as the initrd, never the boot image's own ramdisk.
- Proprietary files follow sheng's method: proprietary-files.txt with an @fetch source and SHA-256 per file, put in .cache/firmware by scripts/extract-files.py \(which falls back to curl when Python has no CA store\).

### Completion criteria

- Firmware image builds, enters UniXNU, publishes the framebuffer and preserves the documented memory reservations.

### Current limits

- Images are booted from RAM only \(fastboot boot\); nothing is flashed.

### Next action

- Record the firmware revision with each boot image.

### Evidence

- `source`: [\[bootimg\] and \[firmware\] select uefi-asteroids and the payload in the kernel image.](https://github.com/rootstockos/UniXNU-asteroids/blob/decbdedfe9469322fbccc950a1a7248bca89b6e7/board.toml)

## CPU and interrupts {#cpu}

`implemented`

Components: `ArmCpu`.

### Hardware and dependencies

- Four Cortex-A520 \(cpus 0-3, EPSS domain 0\) and four Cortex-A720 \(4-6 domain 1, 7 domain 2\); EPSS domains at 17d91000/17d92000/17d93000.
- Gunyah hypervisor: SGIs are not delivered, so IPIs use armcpu-spi-ipi=1.

### Configuration

- sheng-smp=1 and armcpu-spi-ipi=1 in board.toml; unixnu,cluster-type E/P in dts/asteroids.dts; sheng-cpufreq=&lt;mode&gt; selects the CPU governor.

### Procedure

- Boot with sheng-cpufreq=1 and the banner on, read the CPU row \(domain state and LUT\), then sheng-cpufreq=4.

### Development findings

- The CPU governor is sheng's CpuFreqProbe with 4/3/1 CPUs per domain and no L3 vote \(the 3a has no EPSS L3\).
- The E/P Edge scheduler and the idle-time helper are sheng's zzyf and zzye patches \(patches/xnu\).
- T40c \(2026-10-27\): the cpu0 park thread is off by default \(sheng-cpu0-park=0, as UniXNU-sheng d361b53\): the E/P Edge scheduler places work by cluster, and T39b found the park thread holding cpu0 at 100 %. The governor and the AMP and idle patches already match sheng's latest.

### Completion criteria

- Every enabled CPU reaches its entry checkpoint and timer/IPI handling works on each enabled CPU.

### Current limits

- The governor and the E/P scheduler are not yet verified on the phone \(T35\).

### Next action

- Boot T35a \(read-only\) and T35b \(governor\) and record the clocks and frame rate.

### Evidence

- `source`: [EPSS CPU governor with touch boost and frame floor.](https://github.com/rootstockos/UniXNU-asteroids/blob/decbdedfe9469322fbccc950a1a7248bca89b6e7/package/CpuFreqProbe.cpp)

## Memory and DMA {#memory}

`implemented`

### Hardware and dependencies

- DRAM high bank 0x8C0000000-0xABFE00000 for the XNU window; GPU pool at 0xABFE00000 \(1 GiB\); GMU pool at 0xE6440000 \(32 MiB\); all reserved in the uefi-asteroids memory map.

### Configuration

- owned\_memory\_size 0x130000000 \(4.75 GiB\) and dram\_size 0x1FFE00000; the DTS memory node equals dram\_size.

### Procedure

- Check that payload.dram\_size equals the DTS memory node and that DarwinBoot places the window.

### Development findings

- 384 MiB of owned memory left iPadOS short; 4.75 GiB in the high bank \(uke's layout\) is enough.
- Metal's 64 MiB blocks need a 1 GiB GPU pool outside the XNU window.

### Completion criteria

- All handoff regions are accounted for and each enabled DMA engine accesses its allocated range with the documented cache policy.

### Current limits

- The GPU and GMU pools are fixed reservations in the firmware memory map.

### Next action

- Record the firmware memory map with each firmware change.

### Evidence

- `source`: [Memory node for the XNU window's DRAM bank.](https://github.com/rootstockos/UniXNU-asteroids/blob/decbdedfe9469322fbccc950a1a7248bca89b6e7/dts/asteroids.dts)

## Storage and root {#storage}

`implemented`

Components: `ShengUfs`, `RamBlock`, `SoftwareAES`, `VirtioMmioBlock`, `VerifiedRoot`.

### Hardware and dependencies

- UFS host 0x1d84000 and PHY 0x1d80000 \(SM8550's windows\), apps SMMU stream 0x60; userdata LUN 0 blocks 0x256248-0x3a8bffa.

### Configuration

- native-ufs-root=1 and native-ufs-allow-unverified=1; sheng-data-persist=2 keeps Data at the end of userdata.

### Procedure

- Build the userdata image, write it to userdata from recovery, boot, and pull the Data volume with scripts/pull-asteroids-data.py.

### Development findings

- Format 2 builds VirtioMmioBlock as ShengUfs's dependency; build-arm-driver.py skips it while XNU\_NATIVE\_VIRTIO\_BLOCK is off.
- NativeUfs \(the ShengUfs fork\) is built without the verified-root check until signed volume policies exist.
- Its IOBlockStorageDevice imports bind against the original class in a bootstrap kernel candidate built first in CI.

### Completion criteria

- The root volume mounts read-only from UFS and Data persists across boots.

### Current limits

- Root reads are not authenticated.

### Next action

- Build the owner verified-root bundle.

### Evidence

- `device`: [T29 booted iPadOS 17.7.11 from the UFS root with persistent Data to the first picture.](https://github.com/rootstockos/UniXNU-asteroids/blob/decbdedfe9469322fbccc950a1a7248bca89b6e7/board.toml)
  Command: <code>fastboot boot local/unixnu-asteroids-t29-boot.img</code>. Revision: `adf900cf453a6b318864913757f588c9f661596f`.

## Display {#display}

`implemented`

Components: `GopFramebuffer`.

### Hardware and dependencies

- The firmware's GOP framebuffer, 1080x2392 x8r8g8b8 at stride 4320, on a 120 Hz video-mode panel.

### Configuration

- offline-legacy-\* arguments, sheng-vsync=120, sheng-fb-gpu=1 \(the GPU copies each frame to the panel\).

### Procedure

- Boot and watch the banner rows \(sheng-banner=1\) for swaps per second and copy times.

### Development findings

- T37 \(2026-10-26\): DSI0 is reachable under Gunyah \(T37a st=1\), the brightness test ran \(T37b\), and with asteroids-panel=3 iOS sets the brightness and sleep turns the panel off and on again \(T37d\). It is a board default since then.
- T37: the panel \(Visionox RM69220 AMOLED, video mode, DSI0 at 0x0ae94000, dsi-ctrl v2.8\) takes DCS commands through the controller's TPG command FIFO, scheduled for the first front-porch line \(package/PanelProbe.cpp, asteroids-panel=1..4\): brightness 51 hi lo \(10..4095\), off 28 + 10, on 11 + 29. The iOS brightness service is sheng's AppleARMBacklight.cpp with the DCS write instead of I2C \(package/AsteroidsBacklight.cpp\); level 0 turns the panel off.
- The CPU copy \(143-285 ms a frame\) mapped the surfaces cacheable without invalidation and showed stale patches; the GPU copy removes both.
- GopFramebuffer 33e941a's direct scanout needs ShengUfs's display SMMU window \(native\_ufs\_dpu\_map\); our NativeUfs fork has none, so package/LegacyDisplayStubs.c supplies weak zero stand-ins that keep it off.
- T40c \(2026-10-27\): BootProgress.c's cpu0\_park defaults off \(see cpu\).

### Completion criteria

- The desktop presents through the legacy display with measured frame times.

### Current limits

- Under 60 frames per second.

### Next action

- Measure the frame rate with the CPU governor \(T35\).

### Evidence

- `device`: [T34b: GPU copy to the panel, no tearing or stale patches, stable.](https://github.com/rootstockos/UniXNU-asteroids/blob/decbdedfe9469322fbccc950a1a7248bca89b6e7/board.toml)
  Command: <code>fastboot boot local/unixnu-asteroids-t34b-boot.img</code>. Revision: `e022e84a9721ea6408ea12665b5a23e9b89fc5f6`.

## Input {#input}

`implemented`

Components: `ShengHidInput`, `ShengNovatekTouch`, `QcomGeniSpi`.

### Hardware and dependencies

- FocalTech FT3683G on GENI SE0 SPI; PMK8550 PON power and RESIN, PMXR2230 GPIO 6 volume up, through the SPMI arbiter and PDC pin 1 \(SPI 481\).

### Configuration

- asteroids-touch=6 \(package default\) and sheng-touch-hid=1; sheng-buttons=1 for the buttons.

### Procedure

- Boot, touch the desktop and press each button; read the BTN banner row.

### Development findings

- Touch is polled; stage 2's RPMh votes need a completion check.
- Every button constant equals sheng's \(SPMI arbiter v7 at the same addresses, same PPIDs\).
- TouchState.cpp's placeholder button sink is gone: ButtonProbe.cpp owns native\_buttons\_set\_sink.

### Completion criteria

- Contacts and buttons reach backboardd as HID events.

### Current limits

- The buttons are not yet verified on the phone \(T35\); ShengNovatekTouch is linked as ShengHidInput's dependency and not used.

### Next action

- Boot T35a with sheng-buttons=1.

### Evidence

- `device`: [Touch input works on the desktop \(stage 6\).](https://github.com/rootstockos/UniXNU-asteroids/blob/decbdedfe9469322fbccc950a1a7248bca89b6e7/package/AsteroidsTouchProbe.cpp)
  Command: <code>fastboot boot local/unixnu-asteroids-t34b-boot.img</code>. Revision: `e022e84a9721ea6408ea12665b5a23e9b89fc5f6`.

## GPU {#gpu}

`implemented`

Components: `Adreno740`, `AdrenoFirmware`, `AdrenoPM4`, `ArmSmmu4K`, `Sm7635Platform`, `Sm8550Platform`.

### Hardware and dependencies

- Adreno 810 \(gen8, chip 0x44010000\) at 0x3d00000 with GMU, RSCC and SMMU; firmware gen80300 from proprietary-files.txt \(scripts/extract-files.py, the pinned NullDebris vendor repository\).

### Configuration

- sheng-gpu-power=19, sheng-gpu-addon=1, sheng-gpu-level=6 \(763 MHz\); the Metal plugin and Turnip are built on the Mac into the payload addon.

### Procedure

- Build the kernel in CI, the addon with scripts/build-asteroids-metal-plugin.py --published, pack and boot.

### Development findings

- NativeAdreno's GMU headers \(NativeAdrenoGmuConfig.h, NativeAdrenoGmuPlatform.h\) include ShengGmu.h, so the driver compiles also take kits/Sm7635Platform \(T36 run 40296339052\).
- The gen8 GMU cold start and command-database parser are the SoC kit Sm7635Platform \(UniXNU-sm7635-common\), as sheng's are Sm8550Platform; the board keeps ShengGmuVotes.c. scripts/check-asteroids-gmu.py passes against the kit.
- The render server composites on the A810 \(window server ready in 1.9 s instead of 30.8 s\).
- The GPU clock does not limit the frame rate: 1050 MHz was barely faster than 763 MHz.
- T40b \(2026-10-27\): drivers/Adreno740 is UniXNU Adreno740 main \(5c8c145\) merged into our gen8 fork \(rootstockos/NativeAdreno asteroids 60f16a6\): ABI v2 \(128 buffers per submission\), no full GPU TLB flush per submission, owned and exclusive imports mapped without alias scans. The board's GPU probe keeps its ABI structures and native\_adreno\_publish signature; it passes no GMU AHB fence status to the ring \(the new optional fence\_cookie/fence\_status\), so WPTR writes stay unchecked as before.
- T40c \(2026-10-27\): sheng's GPU governor is on by default in board.toml \(sheng-gpu-dcvs=1\) with the 3a's range: floor level 6 \(763 MHz, the former fixed level; sheng's floor 3 is 510 MHz here and held every frame in T39b\), ceiling level 7 \(895 MHz; no GPU thermal throttle yet\). Fence waits spin \(sheng-gpu-irq=0\) as a board default.

### Completion criteria

- Core Animation renders through Metal on the GPU with measured frame times.

### Current limits

- Turnip runs without GMEM \(TU\_DEBUG=sysmem,nocb\); Sm8550Platform is linked as Adreno740's dependency and not used.

### Next action

- Try GMEM rendering.

### Evidence

- `device`: [GPU compositing and the GPU panel copy run stable.](https://github.com/rootstockos/UniXNU-asteroids/blob/decbdedfe9469322fbccc950a1a7248bca89b6e7/package/GpuPowerProbe.cpp)
  Command: <code>fastboot boot local/unixnu-asteroids-t34b-boot.img</code>. Revision: `e022e84a9721ea6408ea12665b5a23e9b89fc5f6`.

## clock {#clock}

`device-verified`

Components: `QcomPmicRtc`.

### Hardware and dependencies

- The PMK8550's RTC: a read-only seconds counter behind the SPMI arbiter \(v7.1, APID 94\), described in the SoC's sm7635.dtsi.
- The Data volume for the offset file, as Android's time\_daemon keeps it under /data/vendor/time.

### Configuration

- QcomPmicRtc \(UniXNU fork\) publishes IORTC with IORTCReadOnly; drivers/ArmDTPlatform \(rootstockos/ArmDTPlatform asteroids\) forwards the calendar to it as counter + offset; the kernel restores /private/var/db/unixnu-rtc-offset before launchd and stores it on every calendar set.

### Procedure

- Boot, set the time in Settings &gt; Date &amp; Time, restart, and compare the clock; the banner's RTC row shows the counter, restores and stores.

### Development findings

- T39: the counter reads \(plat 3, pmic 5\); no set reached the kernel while timed hung.
- T39d/T39e: timed hung in gethostuuid\(\) without a platform UUID; with the platform seed in the ADT it answers, and a time set in Settings survives a restart.

### Completion criteria

- The wall clock is right after every boot without a network.

### Current limits

- No automatic time \(no network or GNSS time source yet\).

### Next action

- Propose the IORTC forwarding and the RTC drivers upstream once stable.

### Evidence

- `device`: [T39e: the time set in Settings survived a restart; Settings &gt; Date &amp; Time opens.](https://github.com/rootstockos/UniXNU-asteroids/blob/decbdedfe9469322fbccc950a1a7248bca89b6e7/board.toml)
  Command: <code>fastboot boot local/unixnu-asteroids-t39e-boot.img</code>. Revision: `e4d1092cc3d051617ee88858b153ed2ba0d456fd`.

## Network {#network}

`planned`

### Hardware and dependencies

- The 3a's Wi-Fi and Bluetooth module; not yet identified for a driver.

### Configuration

- None yet.

### Procedure

- Identify the module and its bus from the live device tree.

### Development findings

- No network driver runs; bluetoothd is disabled.

### Completion criteria

- The device joins a network and passes traffic.

### Current limits

- No network.

### Next action

- Identify the Wi-Fi module.

### Evidence

Collect evidence using the next action.

## Audio {#audio}

`planned`

### Hardware and dependencies

- The audio DSP and its firmware; sheng's ADSP, GLINK and QRTR stack is the reference.

### Configuration

- None yet.

### Procedure

- Boot the ADSP from its firmware partition as sheng does.

### Development findings

- No audio path yet.
- T38 ports sheng's audio DSP bring-up \(AdspProbe.cpp, sheng-adsp=1 survey, 2 start\) with the 3a's IPCC \(0x405000\), carveouts \(0x99300000, 0x99280000\) and crash-reason partition; the firmware comes from modem\_a \(LUN 4\) through NativeUfs's native\_ufs\_part\_find/read \(rootstockos/NativeUfs efa8271, from UniXNU's ShengUfs\).

### Completion criteria

- Playback and capture through the audio server.

### Current limits

- No audio.

### Next action

- Port the ADSP start after the battery work.

### Evidence

Collect evidence using the next action.

## Power {#power}

`implemented`

Components: `AppleKeyStoreState`.

### Hardware and dependencies

- sheng's placeholder ApplePMGR provider; the AppleKeyStore stand-in.

### Configuration

- sheng-pmgr=2 \(required in board.toml by the payload check\); sheng-aks=1 publishes the AppleKeyStore stand-in with persistent Data.

### Procedure

- Boot and check that SpringBoard finishes booting \(AppleKeyStore opens\).

### Development findings

- Without the AppleKeyStore stand-in on persistent Data, SpringBoard never finished booting \(T20-T28\).
- T38: sheng's battery manager client and iOS power source \(ShengBattmgr.c, ShengBattery.cpp, sheng-battery\) with the 3a's standard property numbering \(temperature 12, charge counter 14, cycles 15, design 16, full 17\); sheng's board fields \(opcode 0x50, OEM\_GET\_LOG\_BUFFER on the 3a\) and charge current are skipped.

### Completion criteria

- The OS boots to the desktop with the platform power and keystore services it needs.

### Current limits

- No battery or charging status.

### Next action

- Port sheng's battery manager after the ADSP start.

### Evidence

- `device`: [T29: with the stand-in, SpringBoard boots to the first picture.](https://github.com/rootstockos/UniXNU-asteroids/blob/decbdedfe9469322fbccc950a1a7248bca89b6e7/package/KeyStoreProbe.cpp)
  Command: <code>fastboot boot local/unixnu-asteroids-t29-boot.img</code>. Revision: `adf900cf453a6b318864913757f588c9f661596f`.

## Image assembly {#packaging}

`implemented`

### Hardware and dependencies

- The payload carries the kernel, the ADT from the shared generator, the trust caches and the GPU addon; the boot image carries the phone's live DTB.

### Configuration

- \[payload\] size\_mib = 80, panic\_screen = true; the device patch series lists the fork's bring-up patches and the board CPU patches.

### Procedure

- ./unixnu build payload, then ./unixnu bootimg --dtb with the live DTB.

### Development findings

- Format 2 applies only the patches its series list; the fork's bring-up patches are listed in the device series with the arch: prefix.

### Completion criteria

- The boot image boots on the phone with the expected kernel arguments.

### Current limits

- The payload is built locally in the rootstock Podman machine.

### Next action

- Build the first format 2 kernel in CI and pack it.

### Evidence

- `source`: [Board patch series after the arch, SoC and OS series.](https://github.com/rootstockos/UniXNU-asteroids/blob/decbdedfe9469322fbccc950a1a7248bca89b6e7/patches/xnu/series)

## Diagnostics {#diagnostics}

`implemented`

### Hardware and dependencies

- sheng's boot progress kit: the live page, fault evidence, the UI trace and the banner rows.

### Configuration

- sheng-log=1 keeps a persistent kernel log; sheng-banner=1 draws the rows on the desktop.

### Procedure

- Boot with the banner on and photograph it; pull Data for the unified log.

### Development findings

- Never boot a test without on-screen diagnostics: T24b had none and taught nothing.
- T37 adds sheng's UFS diagnostic log \(BootLog.c, sheng-log=1\) through NativeUfs's log window \(the last 32 MiB of userdata\), with weak stand-ins \(BootLogStandins.c\) for the 104 references to probes this board does not build; scripts/pull-asteroids-log.py copies the window from recovery over adb and decodes it with sheng's read-sheng-log.py --decode. The unified log on Data cannot tell boots apart \(one boot UUID and clock base for every boot\).

### Completion criteria

- Each test boot shows its stage and counters on screen.

### Current limits

- The unified log needs a Data pull through recovery.

### Next action

- Keep the banner rows for each new driver.

### Evidence

- `source`: [Live page and banner rows.](https://github.com/rootstockos/UniXNU-asteroids/blob/decbdedfe9469322fbccc950a1a7248bca89b6e7/package/BootProgress.c)

</div>
