# 子模块本地补丁

`UniXNU/XnuPrelink` 是 org 只读仓（`Emilelu` 无写权限，也没有 fork）。K60 构建需要它的一处本地改动，
因此以补丁形式随 framework 提交，而不是留在工作区里。

## XnuPrelink-auto-slide.patch

- 对象：`kits/XnuPrelink/emit_prelink.py`
- 基线：`f876e3e docs: document component scope and shared porting workflow`
- 内容：把上游的静态发射器换成一层 **auto-slide wrapper**，补两条 20G81 事实（内核集合需要按
  kernelcache 的 collection slide 平移后再绑定；库条目按 library-only 语义发射）。净变化 +213/−301。
- 应用：

```bash
git -C kits/XnuPrelink checkout f876e3e
git -C kits/XnuPrelink apply ../XnuPrelink-auto-slide.patch
```

应用后 `kits/XnuPrelink` 会显示为 dirty（子模块指针不变），这是预期状态；framework 的
`kits/XnuPrelink` 指针仍指 `f876e3e`，因此**克隆后必须手动打这个补丁**，否则 prelink 阶段会按
上游语义发射、K60 集合的 slide 不被接受。

上游修好后应当：把补丁推到 `UniXNU/XnuPrelink`（需要 org 写权限或 fork + 上游合并），再把指针
bump 到新提交并删除本文件。
