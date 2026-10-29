# K60 (mondrian / SM8475) SMP 多核交付记录

状态（2026-10-29 23:10）：
- `0340` 的 kext 补丁**已在实机验证有效**：`CPU configuration in device tree is invalid @AppleARMCPU.cpp:111`
  消失，平台层（ArmDTPlatform/ArmCpu/cache/display/APFS）全部初始化。
- 当前卡点是根挂载（`Failed to mount root device @IOKitBSDInit.cpp:971`），原因是 ADT 的 UFS 节点名
  `ufs` 与 `NativeUfs` personality 的 `IONameMatch = ufshc` 不一致；device main `e40e548` 已改名。
- 8 核方案见 **§7**（device 分支 `smp-8cpu`），§4 是只有"AppleARMCPU 校验成立"时才需要的属性表。

## 1. 结论先行

| 问题 | 结论 | 证据 |
|---|---|---|
| `CPU configuration in device tree is invalid @AppleARMCPU.cpp:111` 是多核数量问题吗？ | **不是**。`cpus=1` 与 `cpus=8` 报同一条 panic | 实机两次启动 |
| 把 `AppleARMPlatform` 从 `[kernel.prelink] roots` 摘掉能解决吗？ | **不能**。依赖闭包会把它拉回来 | `__PRELINK_INFO` 39 个 bundle 的 `OSBundleLibraries` 闭包 |
| sheng（SM8550，8 核）能作为 CPU 节点形状参考吗？ | **不能**。sheng 用的是纯源码内核 `mach.development.bcm2837.unstripped.noctf`，不含任何 Apple kext；其 8 核走 UniXNU `ArmCpu` + PSCI（`sheng-smp=1`、`armcpu-spi-ipi=1`） | `UniXNU-sheng/scripts/build-sheng-payload.py` |
| 当前主线修复 | **0340：在 prelink 后用字节补丁让 `AppleARMCPU::_validateConfiguration()` 直接返回 true** | 见第 3 节 |

## 2. AppleARMPlatform 依赖链（离线实证）

解析 20G81 kernelcache 的 `__PRELINK_INFO`（`kits/XnuPrelink/native_prelink.py` 的 `unserialize_xml`），
对 `OSBundleLibraries` 做从 roots 出发的闭包：

- 去掉 `AppleARMPlatform` 本体后，28 项 roots 仍选中 31 个 bundle，`AppleARMPlatform` **仍在**，
  最短路径 `AppleARMPlatform <- IODARTFamily`。
- 会把它拉回来的 root 共 8 个：
  - `com.apple.driver.IODARTFamily` → 直接依赖
  - `com.apple.iokit.IOAVFamily` → 直接依赖
  - `com.apple.iokit.IOGPUFamily` → 直接依赖
  - `com.apple.iokit.IOMobileGraphicsFamily` → 直接依赖
  - `com.apple.driver.AppleMobileFileIntegrity` → `ApplePMGR` → `AppleARMPlatform`
  - `com.apple.security.sandbox` → AMFI → ApplePMGR → AppleARMPlatform
  - `com.apple.iokit.IOHIDFamily` → AMFI → ApplePMGR → AppleARMPlatform
  - `com.apple.iokit.IOHIDEventDriver` → IOHIDFamily → …
- 即使再摘掉 4 个直接依赖，闭包仍经 **AMFI → ApplePMGR → AppleARMPlatform** 回流；
  AMFI 是必需 root（代码签名），因此 **root trimming 路线不可行**。

复现脚本：`scripts/smp/roots_blame.py`、`scripts/smp/roots_chain.py`（会话工作区
`/mnt/d/Android/k60-ios/smp/`）。

## 3. 0340：跳过 AppleARMCPU 设备树校验（当前主线）

### 3.1 为什么是 kext 字节补丁

`AppleARMPlatform` 来自 Apple kernelcache，不在 XNU 源码里，`patches/xnu/*.patch` 改不到。
prelink 会把该 kext 的 `__TEXT`/`__TEXT_EXEC` 原样拷进 `__PRELINK_TEXT`，所以补丁必须在 prelink 之后、
按 kext 内部布局定位写入。

### 3.2 补丁内容（20G81 / kernelcache sha256 `d260def…`）

| 项 | 值 |
|---|---|
| kext | `com.apple.driver.AppleARMPlatform` |
| 函数 | `AppleARMCPU::_validateConfiguration()`（bool，失败即 panic AppleARMCPU.cpp:111） |
| 起始 VA（unslid） | `0xfffffff004b99460` |
| RVA（`__TEXT_EXEC` 内） | `0x2460` |
| 原始字节 | `ff 83 04 d1 fc 6f 0c a9`（`sub sp,sp,#0x120` / `stp x28,x27,[sp,#0x60]`） |
| 补丁字节 | `20 00 80 52 c0 03 5f d6`（`mov w0,#1` / `ret`） |

反汇编证据：
- `0xfffffff004b99460` 前一条是 `ret`，是干净函数边界；
- 成功路径 `0xfffffff004b99a14: mov w0,#1` → `ldp…; ret`；
- 失败路径 `0xfffffff004b996d8: cbz → 0xfffffff004b99a48`（panic 块，行号 `#0x6f`=111，
  文件串 `AppleARMCPU.cpp`，消息串 VA `0xfffffff00442da4f`）。

### 3.3 落点与配置

- 代码：`scripts/unixnu/kernel.py::patch_prelinked_kext()`，在 `emit_prelink` 之后执行；
  通过 `__PRELINK_INFO` 取 `_PrelinkExecutableLoadAddr`，再走 kext 自己的 `__TEXT_EXEC`，
  因此与 slide 无关；`expect` 不匹配直接 `Error`，不会静默写错位置。
- 配置（board.toml）：

```toml
[kernel.prelink]
kext_patch = [
  { kext = "com.apple.driver.AppleARMPlatform", rva = "0x2460",
    expect = "ff8304d1fc6f0ca9", replace = "20008052c0035fd6" },
]
```

### 3.4 离线验收

```bash
mcopy -i payload.img ::/EFI/UniXNU/Payloads/kernel.macho /tmp/kernel.macho
python3 patch_armcpu_validate.py /tmp/kernel.macho --check   # 打印 file offset 与原始字节
python3 patch_armcpu_validate.py /tmp/kernel.macho --apply
python3 patch_armcpu_validate.py /tmp/kernel.macho --check   # already patched
```

期望：`kext load 0xfffffff004429d40  file offset 0x195a460  bytes ff8304d1fc6f0ca9`。
`0x195a460` 是 20G81 prelink 结果的稳定偏移；换 kernelcache 必须重新推导。

## 4. 8 核 ADT 属性表（备用分支）

> 该分支的前提是「AppleARMCPU 校验必须通过」成立。当前主线已用 0340 跳过校验，
> 因此本表**不阻塞**当前 panic；只有 0340 放行后系统仍要求 AppleARMCPU 参与 CPU 枚举时才启用。

`AppleARMCPU::_validateConfiguration()` 的校验项（内核字符串表）：

```
fromPath failed to find /cpus
*** Max CPU count is zero
*** Actual CPU count (%d) greater than max (%d)
*** Length for CPU ordinal %d '%s' property is %d should be 0x%lx
*** CPU id %d from CPU ordinal %d '%s' property is out of range [0..%d]
*** Duplicate CPU entry for id %d
*** CPU %d interrupts[2] not equal to interrupts[0]+1
*** Missing '%s' property for CPU %d
*** %s for CPU %d (%d) must match interrupts[0] (%d)
*** %s for CPU %d (%d) must match interrupts[2] (%d)
*** Expected ipi_dispatch %d for CPU %d actual %d
*** CPU doesn't use AIC IPI's but function-ipi_dispatch defined
*** CPU doesn't use AIC IPI's but function-ipi_dispatch_other defined
```

| 属性 | 8 核取值 | 来源 |
|---|---|---|
| `max_cpus` | 8 | enabled CPU 节点数 |
| `cpu-id` | 0..7 | 节点顺序（`reg` 只做亲和性） |
| `reg` | 0x000/0x100/…/0x700 | SM8475 MPIDR Aff0（`sm8475.dtsi` 现有） |
| `state` | cpu0 `running`，其余 `waiting` | 由 `devicetree.py` 生成 |
| `cluster-type` | cpu0–3 `P`（X2+3×A710），cpu4–7 `E`（4×A510） | SM8475 拓扑；**当前 dtsi 把 8 个全标 P，是错的** |
| `interrupts` | 3 cells，`interrupts[2] == interrupts[0]+1` | GIC PPI：`[<ppi0> <flags> <ppi1>]`，需与 GIC 的 PPI 分配表一致 |
| `reg-private` | APSS per-core 私有窗口基址 | `0x17xxxxxx`（GIC redistributor 每核 0x40000 步进） |
| `l2-cache-id` / `l3-cache-id` | 0 / 1 | 同 cluster 共用 |
| `l2-cache-size` / `l3-cache-size` | 由 SM8475 规格填 | 需实机 `MIDR`/CLIDR 读回确认 |
| `no-aic-ipi-required` | **必须设 1**（Qualcomm GIC 平台没有 AIC） | 设置后不得再定义 `function-ipi_dispatch*`，否则触发最后两条校验 |
| `function-*`（cpu_idle/platform_cache/enable_core/error_handler） | 不设 | 非 Apple 平台由 ArmCpu 提供 |

失败定位顺序（若启用该分支）：
1. `Max CPU count is zero` → `/cpus` 缺 `max_cpus`；
2. `Actual CPU count greater than max` → `max_cpus` 小于节点数；
3. `Missing '%s' property` → 上表缺项；
4. `interrupts[2] not equal to interrupts[0]+1` → PPI 相邻性不满足；
5. `CPU doesn't use AIC IPI's but function-ipi_dispatch defined` → 设了 `no-aic-ipi-required` 却又定义 IPI 函数。

## 5. 多核的真正路径（PSCI）

- `cpus > 1` 时 `devicetree.py` 要求 `/psci` 且 `method` 为 `smc`/`hvc`（现有 `sm8475.dtsi` 已满足）。
- CPU 启动由 UniXNU `ArmCpu`（`drivers/ArmCpu`）负责：`startCPU()` 发 PSCI `CPU_ON`，
  `IOCPUInterruptController` 提供 IPI；GICv3 redistributor 每核唤醒。
- 该板 `ICC_SGI1R_EL1` 不产生 SGI，IPI 走软件 pending 的 SPI（`armcpu-spi-ipi=1`，INTID 1008+core）——
  与 sheng 相同，启用多核时 `kernel_args` 需要 `armcpu-spi-ipi=1`。
- **`ArmCpu::probe()` 对非 boot CPU 要求 boot-arg `sheng-smp=1`，否则直接返回 nullptr**
  （`drivers/ArmCpu/ArmCpu.cpp`）。也就是说 8 核配置若不带 `sheng-smp=1`，cpu1..7 的 nub
  会落到 AppleARMCPU（IOProbeScore 100）手里并触发同一条校验 panic。多核的 boot-args 至少要有
  `sheng-smp=1 armcpu-spi-ipi=1`。
- 判据：`AppleARMCPU-AllCPU-Initialized` 属于 Apple 驱动，K60 走 ArmCpu 后不适用；
  应改用 `armcpu_smp_step[0..7] == 7`（启动完成）与 `armcpu_smp_running`。

## 6. 上机判据（给持机人）

1. `fastboot boot boot.img` 后，屏幕不再出现 `CPU configuration in device tree is invalid @AppleARMCPU.cpp:111`。
2. 内核继续走下一阶段（出现 UFS/AMFI/驱动日志，或换成了**另一条** panic）。
   注意：`AppleARMCPU-BootCPU-Initialized` / `AppleARMCPU-AllCPU-Initialized` 是 **Apple 自己驱动**的标记，
   K60 的 CPU nub 由 UniXNU `ArmCpu`（IOProbeScore 2000）接管，正常情况下这两条**不会**出现——
   它们不是本方案的验收判据，出现反而说明 AppleARMCPU 抢到了 CPU。
3. 若出现新 panic：拍全屏原文（含 `panic(cpu …)`、`pc`、`caller`、`Kernel text base`），不要自行回滚补丁。

## 7. 8 核开启（K60 实际驱动路径，2026-10-29 修订）

### 7.1 前提
`0340` 的 kext 补丁生效后，AppleARMCPU 的设备树校验不再触发；8 核的唯一门槛回到
UniXNU 自己的 `ArmCpu` 驱动。**不需要** `sheng-smp=1` / `armcpu-spi-ipi=1`：那是 sheng
（`drivers/ArmCpu` 通用版）的开关，K60 用的是 device 仓 `drivers/ArmCpu/ArmCpu.cpp`，
它的 `probe()` 恒返回 `nullptr`，由 `ArmDTPlatform` 发布完 CPU nub 后**直接实例化**每个
`ArmCpu`（`new ArmCpu; init(); attach(nub); start(nub)`），不经过 IOKit 匹配。

### 7.2 唯一需要的改动
```toml
[payload]
cpus = 8
```
`scripts/unixnu/devicetree.py` 已经会生成 `max_cpus = 8`、`cpu0..cpu7`（`cpu-id` 0..7、
`state` 首核 `running` 其余 `waiting`、`reg` 取 `sm8475.dtsi` 的 0x000..0x700）。
不需要新增 `interrupts` / `reg-private` / `function-ipi_dispatch`：这些是 AppleARMCPU 的
校验项，绕过校验后没有消费者。

拓扑（可选修正）：`sm8475.dtsi` 目前把 8 个核全标 `cluster-type = "P"`。SM8475 实际是
1×X2 + 3×A710（P）+ 4×A510（E），即 cpu0–3 `P`、cpu4–7 `E`。`ArmCpu::start()` 用它填
`ml_processor_info_t.cluster_type`，只影响调度器分簇，不影响能否起来；先起 8 核再改。

### 7.3 启动顺序（代码事实，`drivers/ArmCpu/ArmCpu.cpp`）
1. boot CPU 的 `start()`：`prepareGic()` → 注册自己 → 遍历 `provider->getProvider()`
   的所有 `device_type=cpu` 子节点，逐个 `new ArmCpu` + `start(nub)`；
2. `if (armcpu_registered != ml_get_cpu_count()) panic("ArmCpu: incomplete CPU registry (%u/%u)")`
   —— **ADT 里有几个 CPU 就必须注册几个**；
3. 建 `IOCPUInterruptController`，为每个 CPU 注册 IRQ handler；
4. `initCPU(true)` → `psci_smp_init()`；
5. 对每个从核 `processor_start()` → `psci_smp_start_cpu()`（PSCI `CPU_ON`，conduit 取自 DT `/psci`）；
6. 从核在 `initCPU(false)` 里 `wakeRedistributor(true)` → `enableGic()` → 置 `kIOCPUStateRunning`
   → `psci_smp_cpu_running()` → `signalCPU(this)`。

### 7.4 验收判据（按出现顺序）
| 期望日志 | 含义 |
|---|---|
| `ArmCpu: CPU 1 MPIDR=0x100 registered` … `CPU 7 MPIDR=0x700 registered` | 8 个 CPU nub 全部注册 |
| `ArmCpu: CPU registered, install interrupt controller` | 注册数 == `ml_get_cpu_count()` |
| `ArmCpu: CPU 1 PSCI start PASS result=0` … `CPU 7 … PASS` | 固件接受了 7 次 `CPU_ON` |
| `cache: 8 CPU(s), 64 bytes CPU cache line size` | 内核看到的 CPU 数（当前单核是 `1 CPU(s)`）——**最硬的判据** |
| `ArmCpu: boot CPU running with GICv3/CNTV …` 之后系统继续走 | 主核未被从核启动流程卡住 |

### 7.5 失败定位
| 现象 | 结论与下一步 |
|---|---|
| `panic: ArmCpu: incomplete CPU registry (N/8)` | 某个 `cpu@X` 没注册：`reg` 与 `ml_get_cpu_number()` 映射不上（检查 dtsi 的 0x000..0x700 是否连续），或 `gCpus[]` 已占用 |
| `ArmCpu: CPU n PSCI start FAIL (offline) result=-…` | 固件（ABL/安全监控）拒绝 `CPU_ON`：核对 `/psci` 的 `method`（smc/hvc）与 PSCI 版本；被固件 parked 的核需要先确认未被 secure world 占用 |
| 从核 `panic: ArmCpu: CPU n redistributor did not wake` | GIC redistributor 的 `redistributor-stride`/`reg` 不匹配该核的 MPIDR（SM8475 应为 0x40000） |
| 能起但负载下卡死/`ArmCpu: IRQ drain did not quiesce` | IPI 不达：K60 的 SGI（INTID 0）可能同 sheng 一样不生效，需要移植 sheng 的 SPI IPI 方案（`armcpu-spi-ipi`，SPI 1008+core） |
| 起 8 核后 `ml_get_cpu_count()` 仍为 1 | ADT 的 `/cpus` 没被 `max_cpus`/节点数更新：确认 `board.toml [payload] cpus = 8` 真的传到了 `devicetree.py`（看 payload 的 `kernel.macho.adt` 里 `max_cpus`） |

### 7.6 离线自检（上机前）
```bash
python3 smp/adt_dump.py kernel.macho.adt | sed -n '/\[cpus\]/,/\[arm-io\]/p'
```
应看到 `max_cpus = 0x8` 与 8 个 `cpuN`，每个带 `cpu-id`、`reg`、`cluster-type`。
