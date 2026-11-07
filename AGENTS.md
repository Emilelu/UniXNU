See docs/.

# 提交规范（铁则）

遵循 [feflow/git-commit-style-guide](https://github.com/feflow/git-commit-style-guide)：

```
<type>(<scope>): <subject>

<body>

<footer>
```

- `type` 取 `feat` / `fix` / `docs` / `style` / `refactor` / `perf` / `test` / `build` / `ci` / `chore` / `revert` 之一。
- `scope` 可选，写受影响模块，例如 `xnu`、`userland`、`uefi`、`readme`、`series`。
- `subject` 说清做了什么：英文、祈使式、不超过 50 字符、结尾不加句号。
- `body` 说明**为什么**这样改以及影响面，每行不超过 72 字符；`footer` 写 `BREAKING CHANGE:` 或关联 issue。
- 一次提交只做一件事；代码与文档分成两个提交，同一 PR 里提交。
- 提交者固定为 `Emilelu <kimiuso@vip.qq.com>`，不要使用临时或占位身份。
- 已发布的历史不重写；确需修正（例如作者信息错误）时先说明再强推。

## 分支与上游同步

- `main` 只接收经过验证的合并：本体改动一律开 `feat/` `fix/` `docs/` `chore/` 等分支，
  验证通过再合入 `main`。
- `.github/workflows/sync-upstream.yml` 每天把 `UniXNU/UniXNU` 的 `main` 合并到
  `chore/upstream-sync-<日期>` 分支并开 PR；它不直接写 `main`。
- 上游原有的分支名保持不动，只整理本 fork 自己的分支。

## 工作区与发布（铁则）

这两条优先于本文件其余内容；违反一次就会丢掉无法恢复的工作。

1. **非临时文件不许放 `/tmp`。** 补丁、`series`、构建脚本、笔记，以及任何被结果引用的产物，
   都放在仓库里或 `E:\k60-work` 下。`/tmp` 会无声无息被清空：2026-11-07 一次清理删掉了
   `/tmp/usb-cdc-mainline`，一整天做的内核补丁只剩编译后的 `macho`。不是明确可丢弃的东西，
   不要建在那里。
2. **源码必须先纳入 git 并 push，再进入下一步。** 补丁、脚本、文档写出来不算完成，
   提交到分支并推到 fork 才算完成。`git status` 不允许带着源码改动跨过一次构建，
   构建树也不允许成为某个补丁的唯一副本。只存在于临时 worktree 的工作等于没做，
   没 push 的补丁等于不存在。

每次构建前的检查：`git status --porcelain` 为空，且当前分支与远端齐平。

3. **遇到问题先查参考仓库的解决方案，禁止瞎猜瞎搞。** `UniXNU-pong` 是同 SoC（SM8475）
   最接近的先行实现：出现故障先读它的 `board.toml`、`userland/`、`scripts/` 和
   `migration/` 笔记；`ios-sweet-k60` 是 iOS 16 用户态的先行记录；`UniXNU-sheng` 与
   `UniXNU` 文档补齐其余。提出的方案必须写出它来自哪个文件哪一行，或者明确声明
   「没有找到先行实现」。反例（2026-11-07）：App cryptex 缺失被凭空说成「加一个
   `[userdata] windows` 条目」，而 pong 的真实做法是把 AppOS 放进 OS、并替换悬空别名
   （`userland/build-ipados18.py:260 drop_restore_app_alias`）。
