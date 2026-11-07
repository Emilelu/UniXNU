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
