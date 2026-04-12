# 贡献指南（skills 分支）

感谢你对 FranxAgent Skills 的兴趣！我们欢迎任何实用的技能文件，帮助 AI 更好地完成特定领域任务。

## 许可证

本分支中的所有技能文件必须采用 **GNU Free Documentation License 1.3** 或更高版本发布。  
提交技能即表示您同意以该许可证授权。

## 如何贡献

### 1. Fork 仓库
访问 [FranxAgent 仓库](https://github.com/xhdlphzr/FranxAgent)，切换到 `skills` 分支（或直接 Fork 整个仓库）。

### 2. 克隆你的 Fork 到本地
```bash
git clone https://github.com/你的用户名/FranxAgent.git
cd FranxAgent
git checkout skills
```

### 3. 创建新分支
```bash
git checkout -b add-技能名
```

### 4. 添加技能文件
在根目录下创建一个 `.md` 文件（文件名建议使用英文，如 `research_workflow.md`）。  
文件应包含：

- **标题**：一级标题，如 `# 科研工作流程`
- **概述**：说明技能的作用
- **免责声明**（可选）：如涉及特定风险
- **主体**：清晰的步骤、规则或示例，使用 Markdown 层级组织
- **使用建议**：告诉用户如何利用该技能
- **许可证声明**：在文件头部添加简化版权声明（见下文）

#### 许可证声明示例
```markdown
<!--
Copyright (C) 2026 你的名字
See the file COPYING for copying conditions.
-->
```

### 5. 本地测试（可选）
你可以将文件复制到 FranxAgent 主项目的 `skills/` 文件夹，启动主程序，观察是否被正常加载（控制台会打印已加载的技能列表）。

### 6. 提交改动
```bash
git add 你的技能文件.md
git commit -m "添加 [技能名] 技能"
```
如需添加共同作者，请使用 `Co-authored-by`（见下文）。

### 7. 推送并创建 Pull Request
```bash
git push origin add-技能名
```
在 GitHub 上创建 Pull Request，**目标分支选择 `skills`**。  
在描述中说明技能的用途、适用场景。

### 8. 等待审查
维护者会审查内容的合理性、格式规范等。如有修改建议，会在 PR 中反馈。

## 共同作者（Co-authored-by）
如果有多人合作，请在提交信息末尾添加：
```
Co-authored-by: 伙伴用户名 <伙伴邮箱>
```
每个贡献者独占一行。

## 技能要求
- 内容实用，避免空洞或重复。
- 遵守法律法规，不包含侵权或敏感内容。
- 文件编码 UTF-8。

## 其他贡献方式
- 报告问题：在 GitHub Issues 中创建，注明“skills 分支”。
- 改进现有技能：直接修改文件并提交 PR。

## 感谢
每一份技能都让 FranxAgent 更强大。期待你的贡献！