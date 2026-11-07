# Redmi K40（alioth）

[FFT-infra/UniXNU-alioth](https://github.com/FFT-infra/UniXNU-alioth)

<div v-pre>

Device template. Complete each area with board-specific inputs and evidence.

源记录: [porting.toml](https://github.com/FFT-infra/UniXNU-alioth/blob/aed29c3ba15003062375eca41e90bf830920d765/porting.toml), `aed29c3ba15003062375eca41e90bf830920d765`.

本页按设备记录自动生成。

| 部分 | 状态 |
| --- | --- |
| [配置](#configuration) | `planned` |
| [固件与启动](#firmware) | `planned` |
| [CPU 与中断](#cpu) | `planned` |
| [内存与 DMA](#memory) | `planned` |
| [存储与根卷](#storage) | `device-verified` |
| [显示](#display) | `implemented` |
| [输入](#input) | `planned` |
| [GPU](#gpu) | `planned` |
| [网络](#network) | `planned` |
| [音频](#audio) | `planned` |
| [电源](#power) | `planned` |
| [镜像组装](#packaging) | `planned` |
| [诊断](#diagnostics) | `device-verified` |

## 配置 {#configuration}

`planned`

组件: `ArmDTPlatform`, `ArmCpu`, `SoftwareAES`, `XnuPrelink`, `DarwinBoot`, `AppleKeyStoreState`.

### 硬件与依赖

- Identify the configuration hardware, resources and existing component interfaces for this board.

### 配置

- Record the board.toml fields, DTS properties and defconfig values used for configuration.

### 操作步骤

- Follow the configuration stage in the porting guide and record the actual commands.

### 开发经验

- Collect the first configuration observation, its cause when established, and the resulting implementation decision.

### 完成条件

- All source pins resolve; every selected component has a record; status shows the intended overrides and patch order.

### 当前范围

- Hardware inputs and implementation are pending for this example board.

### 下一步

- Inventory the required configuration inputs before implementation.

### 证据

按下一步操作收集证据。

## 固件与启动 {#firmware}

`planned`

### 硬件与依赖

- Identify the firmware and boot hardware, resources and existing component interfaces for this board.

### 配置

- Record the board.toml fields, DTS properties and defconfig values used for firmware and boot.

### 操作步骤

- Follow the firmware and boot stage in the porting guide and record the actual commands.

### 开发经验

- Collect the first firmware and boot observation, its cause when established, and the resulting implementation decision.

### 完成条件

- Firmware image builds, enters UniXNU, publishes the framebuffer and preserves the documented memory reservations.

### 当前范围

- Hardware inputs and implementation are pending for this example board.

### 下一步

- Inventory the required firmware and boot inputs before implementation.

### 证据

按下一步操作收集证据。

## CPU 与中断 {#cpu}

`planned`

### 硬件与依赖

- Identify the cpu and interrupts hardware, resources and existing component interfaces for this board.

### 配置

- Record the board.toml fields, DTS properties and defconfig values used for cpu and interrupts.

### 操作步骤

- Follow the cpu and interrupts stage in the porting guide and record the actual commands.

### 开发经验

- Collect the first cpu and interrupts observation, its cause when established, and the resulting implementation decision.

### 完成条件

- Every enabled CPU reaches its entry checkpoint and timer/IPI handling works on each enabled CPU.

### 当前范围

- Hardware inputs and implementation are pending for this example board.

### 下一步

- Inventory the required cpu and interrupts inputs before implementation.

### 证据

按下一步操作收集证据。

## 内存与 DMA {#memory}

`planned`

### 硬件与依赖

- Identify the memory and dma hardware, resources and existing component interfaces for this board.

### 配置

- Record the board.toml fields, DTS properties and defconfig values used for memory and dma.

### 操作步骤

- Follow the memory and dma stage in the porting guide and record the actual commands.

### 开发经验

- Collect the first memory and dma observation, its cause when established, and the resulting implementation decision.

### 完成条件

- All handoff regions are accounted for and each enabled DMA engine accesses its allocated range with the documented cache policy.

### 当前范围

- Hardware inputs and implementation are pending for this example board.

### 下一步

- Inventory the required memory and dma inputs before implementation.

### 证据

按下一步操作收集证据。

## 存储与根卷 {#storage}

`device-verified`

组件: `ShengUfs`, `VerifiedRoot`, `VirtioMmioBlock`, `RamBlock`.

### 硬件与依赖

- UFS 3.1 host on SM8250, bound through ShengUfs, plus the two authenticated volume windows \(OS and SystemOS\) inside userdata.
- The Data seed is a raw APFS container: scripts/prepare-owner-data-fixture.py requires NXSB at 0x20, so the ADT reserves RAMDisk rather than PackedRAMDisk.

### 配置

- CONFIG\_XNU\_NATIVE\_UFS=y, CONFIG\_XNU\_VERIFIED\_ROOT\_PROBE=y, CONFIG\_XNU\_OWNER\_ROOT\_AUDIT=y, CONFIG\_XNU\_OWNER\_ROOT\_TRUST=y.
- CONFIG\_XNU\_NATIVE\_RAM\_BLOCK=y and CONFIG\_XNU\_OWNER\_DATA\_MOUNT=y; the Data mount must go through the RamBlock IOKit device, not /dev/md0.

### 操作步骤

- ./unixnu build payload --data-ramdisk &lt;seed&gt;, then bootimg, then fastboot flash boot\_b.
- The panel reports UFS read progress and the RAMDisk capacity; the USB console carries exit records.

### 开发经验

- UFS reads run through ShengUfs and the panel reports verified blocks; the root is published only with an owner-signed policy, so CONFIG\_XNU\_VERIFIED\_ROOT\_PROBE must stay on or IOFindBSDRoot times out ten times and panics.
- The Data mount fails with ENOENT through /dev/md0 \(measured 2026-10-26, panic screen offline scratch Data mount failed: 2\); publishing the seed through RamBlock as a real IOMedia is the path that mounts.
- The Data volume is 32 MiB and holds the original private/var excluding staged\_system\_apps \(39 files, 611715 bytes\). Measured 2026-10-27: 20000 directories fit in 5.8 MiB, so capacity and inodes are not the limit for the services that fail.
- cryptexd aborts with mkdirat \[28: No space left on device\] while that volume reports 31 MiB free, so the ENOSPC names a different mount than /private/var.

### 完成条件

- The configured OS volume mounts and launchd starts; the Data volume mounts read-write as apfs and is accepted by native\_owner\_data\_prepare.
- Persistence within the allocated Data region is not yet demonstrated across a reboot.

### 当前范围

- The write that fails with ENOSPC is not yet identified: the mkdir probe that prints its path is built but has not run on hardware.
- The Data seed cannot simply be enlarged: boot\_a and boot\_b are 192 MiB and the payload is a FAT volume, so a seed larger than that does not fit.

### 下一步

- Run the mkdir probe build and read the path it prints, then decide whether the failing write is on /private/var or elsewhere.

### 证据

- `device`: [The kernel reports cryptexd aborting with mkdirat ENOSPC while the Data volume reports 31 MiB free, which places the failing write on a mount other than /private/var.](https://github.com/FFT-infra/UniXNU-alioth/blob/aed29c3ba15003062375eca41e90bf830920d765/docs/evidence/2026-10-27-boot-diagnostics.md)
  Command: <code>read /dev/tty.usbmodem&lt;N&gt; at 115200 8N1 and collect EXITLOG records</code>. Revision: `24d127c47217eb580dbe3f3a94c32ad25cbaae00`.

## 显示 {#display}

`implemented`

组件: `GopFramebuffer`.

### 硬件与依赖

- The panel is 1080x2400 and the loader hands over a framebuffer at 0x9c000000 with 4320-byte rows and 32 bpp, so the display path starts from that memory rather than from a GPU.
- IOMobileFramebufferLegacy is prelinked and exports nothing, so the board archive binds each name to its original absolute address.

### 配置

- CONFIG\_XNU\_NATIVE\_LEGACY\_DISPLAY=y; offline-component-load-probes.patch calls both display entry points, so the archive must resolve them or the link fails.
- build-xnu-4k-baseline.sh force-loads libNativeLegacyDisplay.late.a and re-proves every address against this kernel on each run.

### 操作步骤

- Boot the image and read the diagnostic page rows for DISPLAY stage, CLIENT and SWAP; the USB console carries the exit records.
- A photograph of the panel is the frame evidence until a swap is submitted.

### 开发经验

- The diagnostic page reaches DISPLAY stage=10 and a real client connects: CLIENT calls=4 with class=IOMobileFramebufferUserClient. No frame is ever submitted: SWAP calls=0.
- The panel is driven directly by the kernel's own renderer, which is why the boot-progress page and the colour bands are visible before any userspace renderer runs.

### 完成条件

- A known frame appears with correct geometry and colors, then userland presentation and backlight controls work.

### 当前范围

- SWAP calls=0: nothing has ever presented a frame through this client. The panel shows only what the kernel draws.
- backboardd, the render server, has not been started in any recent boot, so a userspace presentation path has never been exercised.

### 下一步

- Get backboardd to start before investigating frame submission: with no render server there is no client that could call Swap.

### 证据

- `device`: [DISPLAY stage=10 with CLIENT calls=4 class=IOMobileFramebufferUserClient, and SWAP calls=0: a client connects but no frame is submitted.](https://github.com/FFT-infra/UniXNU-alioth/blob/aed29c3ba15003062375eca41e90bf830920d765/docs/evidence/2026-10-27-boot-diagnostics.md)
  Command: <code>read the diagnostic page and the USB console after booting the image</code>. Revision: `24d127c47217eb580dbe3f3a94c32ad25cbaae00`.

## 输入 {#input}

`planned`

### 硬件与依赖

- Identify the input hardware, resources and existing component interfaces for this board.

### 配置

- Record the board.toml fields, DTS properties and defconfig values used for input.

### 操作步骤

- Follow the input stage in the porting guide and record the actual commands.

### 开发经验

- Collect the first input observation, its cause when established, and the resulting implementation decision.

### 完成条件

- Touches map to the display, simultaneous contacts keep stable IDs, release events arrive, and buttons produce expected HID reports.

### 当前范围

- Hardware inputs and implementation are pending for this example board.

### 下一步

- Inventory the required input inputs before implementation.

### 证据

按下一步操作收集证据。

## GPU {#gpu}

`planned`

### 硬件与依赖

- Identify the gpu hardware, resources and existing component interfaces for this board.

### 配置

- Record the board.toml fields, DTS properties and defconfig values used for gpu.

### 操作步骤

- Follow the gpu stage in the porting guide and record the actual commands.

### 开发经验

- Collect the first gpu observation, its cause when established, and the resulting implementation decision.

### 完成条件

- GPU submissions complete, mapping/fence handling is correct, a known image renders, and the selected Metal client presents it.

### 当前范围

- Hardware inputs and implementation are pending for this example board.

### 下一步

- Inventory the required gpu inputs before implementation.

### 证据

按下一步操作收集证据。

## 网络 {#network}

`planned`

### 硬件与依赖

- Identify the network hardware, resources and existing component interfaces for this board.

### 配置

- Record the board.toml fields, DTS properties and defconfig values used for network.

### 操作步骤

- Follow the network stage in the porting guide and record the actual commands.

### 开发经验

- Collect the first network observation, its cause when established, and the resulting implementation decision.

### 完成条件

- Scanning, association, address configuration and sustained receive/transmit traffic pass with the selected firmware.

### 当前范围

- Hardware inputs and implementation are pending for this example board.

### 下一步

- Inventory the required network inputs before implementation.

### 证据

按下一步操作收集证据。

## 音频 {#audio}

`planned`

### 硬件与依赖

- Identify the audio hardware, resources and existing component interfaces for this board.

### 配置

- Record the board.toml fields, DTS properties and defconfig values used for audio.

### 操作步骤

- Follow the audio stage in the porting guide and record the actual commands.

### 开发经验

- Collect the first audio observation, its cause when established, and the resulting implementation decision.

### 完成条件

- Each declared route carries the selected audio format through playback or capture and handles start/stop correctly.

### 当前范围

- Hardware inputs and implementation are pending for this example board.

### 下一步

- Inventory the required audio inputs before implementation.

### 证据

按下一步操作收集证据。

## 电源 {#power}

`planned`

### 硬件与依赖

- Identify the power hardware, resources and existing component interfaces for this board.

### 配置

- Record the board.toml fields, DTS properties and defconfig values used for power.

### 操作步骤

- Follow the power stage in the porting guide and record the actual commands.

### 开发经验

- Collect the first power observation, its cause when established, and the resulting implementation decision.

### 完成条件

- Declared power controls and battery readings match observations; each claimed sleep/resume transition restores its dependent peripherals.

### 当前范围

- Hardware inputs and implementation are pending for this example board.

### 下一步

- Inventory the required power inputs before implementation.

### 证据

按下一步操作收集证据。

## 镜像组装 {#packaging}

`planned`

### 硬件与依赖

- Identify the image assembly hardware, resources and existing component interfaces for this board.

### 配置

- Record the board.toml fields, DTS properties and defconfig values used for image assembly.

### 操作步骤

- Follow the image assembly stage in the porting guide and record the actual commands.

### 开发经验

- Collect the first image assembly observation, its cause when established, and the resulting implementation decision.

### 完成条件

- Kernel and prelink succeed, payload contains all declared inputs, and the boot image matches the bootloader format and size limit.

### 当前范围

- Hardware inputs and implementation are pending for this example board.

### 下一步

- Inventory the required image assembly inputs before implementation.

### 证据

按下一步操作收集证据。

## 诊断 {#diagnostics}

`device-verified`

组件: `QcomXnuUsbDebug`.

### 硬件与依赖

- The board's DWC3 controller, its apps SMMU stream, and the boot arguments qcom-usb-debug=1 and qcom-usb-ctl=1 in board.toml.
- The diagnostic page is boot-progress=2 with boot-diag-resume=10, so it returns after scanout stops.

### 配置

- board.toml selects the QcomXnuUsbDebug component and passes qcom-usb-debug=1 and qcom-usb-ctl=1.
- configs/alioth\_defconfig sets CONFIG\_XNU\_BOOT\_PROGRESS=y and CONFIG\_XNU\_QCOM\_USB\_DEBUG=y.
- The apps SMMU is iommu@15000000 with qcom,skip-init; the USB node's iommus = &lt;0x47 0x00 0x00&gt; gives SID 0.

### 操作步骤

- ./unixnu build kernel, then build payload and bootimg, then fastboot flash boot\_b.
- Read the console at /dev/tty.usbmodem&lt;N&gt; with a raw 115200 8N1 tty; the dock's SN234567892 node is not the phone.
- Control frames are SXNU1 &lt;16 hex session&gt; &lt;8 hex seq&gt; &lt;VERB&gt; &lt;8 hex crc32&gt;, HELLO first to learn the session.

### 开发经验

- The CDC-ACM console refused to start with error=10 core=0 domain=5. QcomUsbDomainInstall calls halted\(\) before scan\(\), so a PRTCAPDIR of 3 would have returned CoreRunning=4; it returned 5, which proves the controller already reported device mode.
- Firmware leaves an SMR entry for SID 0 pointing at context bank 5 with SCTLR=0xe0 \(M=0\) and TTBR0=0: the stream is programmed but no table exists under it. scan\(\) now reclaims that slot only when translation is off and there is no table, and still refuses a bank that holds a live mapping.
- With that, the console enumerates as 1209:316d named QcomXnuUsbDebug and the kernel log is readable on the host. It is the only channel that keeps a record after the panel has moved on.
- printf and kprintf both fail to reach the console: a DEVELOPMENT kernel leaves disable\_kprintf\_output true without -enable\_kprintf\_spam, and printf's console path did not reach the \_cnputs tee either. qcom\_usb\_debug\_write\(\) is the entry point that works.
- Exit records measured over 420 s: 180 xpcproxy exits with status=0 \(normal fork and exit\), 13 cryptexd SIGABRT with ns=18 code=2 \(OS\_REASON\_LIBSYSTEM\_CODE\_FAULT\), 11 liveactivitiesd SIGTRAP, 2 lsd SIGSEGV. Each process crashes at one fixed PC repeated, so the fault is deterministic rather than a race.
- A software REBOOT via the control channel is acknowledged \(state=queued\) but does not reach fastboot: the worker calls reboot\_kernel\(0, NULL\), an orderly restart that unmounts every filesystem and returns through UEFI. Entering fastboot needs the ABL IMEM handshake, whose address is not measured here.

### 完成条件

- The console enumerates and answers HELLO and STATUS on the board; STATUS reports usb=3 er=0.
- Every process exit and crash reaches the host console, which is what the exit-loop investigation needs.

### 当前范围

- cryptexd's fault is not yet attributed: OWNER\_CRYPTEX\_FILES is 0 by design because UNION\_SYSTEMOS requires it off, so cryptexd's expected paths do not exist. Its crash PC is captured but not symbolicated.
- The MAC exec refusal is intermittent. One boot showed backboardd, imagent, lockdownd, cfprefsd, sharingd and nfcd exiting with status=9 ns=9 code=8; the next showed none of them, so the errno the patch now reports has not been observed yet.
- Symbolication of the crash PCs against the extracted dyld shared cache was attempted and produced implausible image names, so it is not reported as a result.

### 下一步

- Attribute cryptexd's fault, then decide whether the fix is a stub, a mount change, or accepting the crash.
- Wait for the MAC refusal to reproduce and read the ip\_mac\_return value it now prints.

### 证据

- `device`: [Console enumerated as 1209:316d named QcomXnuUsbDebug; STATUS returned usb=3 er=0 with the worker polling, so the port is live in both directions.](https://github.com/FFT-infra/UniXNU-alioth/blob/aed29c3ba15003062375eca41e90bf830920d765/docs/evidence/2026-10-27-boot-diagnostics.md)
  Command: <code>read /dev/tty.usbmodem&lt;N&gt; at 115200 8N1 and send SXNU1 ... HELLO / STATUS</code>. Revision: `15a15d7cc526262a64531ff56b3a33bdbc46379c`.
- `device`: [215 exit records captured. 180 xpcproxy status=0 \(normal\), 13 cryptexd ns=18 code=2, 11 liveactivitiesd sig5, 2 lsd sig11; each process repeats one fixed crash PC, so the faults are deterministic.](https://github.com/FFT-infra/UniXNU-alioth/blob/aed29c3ba15003062375eca41e90bf830920d765/docs/evidence/2026-10-27-serial-exit-records.log)
  Command: <code>./unixnu build kernel; ./unixnu bootimg; fastboot flash boot_b; read the CDC-ACM console for 420 s</code>. Revision: `15a15d7cc526262a64531ff56b3a33bdbc46379c`.

</div>
