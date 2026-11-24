# 接手说明（框架层（framework））

本仓库是 K60（Redmi K60 / mondrian / SM8475）iOS 27 移植的框架层（framework）。

**职责**：unixnu CLI、组件目录（components.toml）、profile（arch/soc/os）、共享构建脚本与 kit（XnuPrelink、VerifiedRoot、ArmSmmu4K 等）。K60 的 SoC/OS/设备 profile 都从这里解析。

移植总方案、启动链、当前状态与已知缺口：
https://github.com/Emilelu/UniXNU-mondrian/blob/main/docs/engineering/PORTING-PLAN.md

构建/上机工作流、铁则与八步流程：
https://github.com/Emilelu/UniXNU-mondrian/blob/main/docs/engineering/WORKFLOW.md

## 本仓库的入口

- 上游：https://github.com/Emilelu/UniXNU
- 设备仓库：https://github.com/Emilelu/UniXNU-mondrian
- SoC 仓库：https://github.com/Emilelu/UniXNU-sm8475-common
- 固件仓库：https://github.com/Emilelu/uefi-mondrian

## 状态（2026-11-25）

K60 的 27 stage-0 已能构建、能打包、内核能在屏幕上打印文本；根存储与 unixnu 分区镜像已就位。
剩余工作是 prelink 未映射槽（AMFI/apfs/sandbox）、显示 framebuffer provider 与 GPU Metal 帧路径。
本仓库已归档，代码保持只读；接手者请从上面的方案文档开始。
