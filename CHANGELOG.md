# Changelog

## [v1.0.0](https://github.com/xhdlphzr/FranxAI/releases/tag/v1.0.0)

### Added
- 命令行版本初始发布。

## [v1.0.1](https://github.com/xhdlphzr/FranxAI/releases/tag/v1.0.1)

### Added
- 工具调用能力。
- 人性化交互设计。

## [v1.1.0](https://github.com/xhdlphzr/FranxAI/releases/tag/v1.1.0)

### Added
- 字符串相似度计算工具。

### Fixed
- 工具调用中的若干问题。

## [v1.1.1](https://github.com/xhdlphzr/FranxAI/releases/tag/v1.1.1)

### Fixed
- 编码问题。

## [v1.1.2](https://github.com/xhdlphzr/FranxAI/releases/tag/v1.1.2)

### Fixed
- `command` 工具增加安全限制，禁止直接删除文件。

## [v1.2.0](https://github.com/xhdlphzr/FranxAI/releases/tag/v1.2.0)

### Added
- 对话记忆功能，支持跨会话保留上下文。

## [v1.3.0](https://github.com/xhdlphzr/FranxAI/releases/tag/v1.3.0)

### Added
- 执行工具（原 `execute`）。

### Fixed
- 记忆功能的稳定性。

## [v2.0.0](https://github.com/xhdlphzr/FranxAI/releases/tag/v2.0.0)

### Added
- 网络搜索工具（DuckDuckGo，免费）。
- 全新 Web 界面，支持实时聊天。
- 一键启动脚本（Windows `.bat` / macOS `.sh`）。

### Fixed
- 若干已知问题。

## [v2.1.0](https://github.com/xhdlphzr/FranxAI/releases/tag/v2.1.0)

### Added
- 聊天响应改为流式输出。

## [v2.2.0](https://github.com/xhdlphzr/FranxAI/releases/tag/v2.2.0)

### Added
- 停止生成按钮，可随时中断 AI 回复。

### Fixed
- 优化用户体验细节。

## [v2.3.0](https://github.com/xhdlphzr/FranxAI/releases/tag/v2.3.0)

### Added
- 增加更多可配置参数（温度、最大迭代次数等）。

## [v2.4.0](https://github.com/xhdlphzr/FranxAI/releases/tag/v2.4.0)

### Added
- 多模态理解工具 `ett`，支持图片、视频、文档分析。

## [v2.4.1](https://github.com/xhdlphzr/FranxAI/releases/tag/v2.4.1)

### Fixed
- 记忆功能兼容性问题。

## [v2.5.0](https://github.com/xhdlphzr/FranxAI/releases/tag/v2.5.0)

### Added
- 北京地铁换乘规划工具。
- 切换至 GPL v3 许可证。

## [v3.0.0](https://github.com/xhdlphzr/FranxAI/releases/tag/v3.0.0)

### Added
- MCP 协议支持（stdio 模式），可连接任意 MCP 服务器。
- 项目更名为 FranxAI。

### Fixed
- 重构为“大一统工具”架构，所有内置工具及 MCP 工具统一通过 `tools` 调用，显著降低 token 消耗。

## [v3.1.0](https://github.com/xhdlphzr/FranxAI/releases/tag/v3.1.0)

### Added
- Web 界面中添加定时任务管理（添加、删除、实时执行）。
- 定时任务执行结果通过 SSE 实时推送，支持中途停止。

## [v3.2.0](https://github.com/xhdlphzr/FranxAI/releases/tag/v3.2.0)

### Added
- 技能系统：`skills/` 文件夹下的 Markdown 文件自动合并到系统提示，扩展 AI 知识。

### Fixed
- 代码重构，清理历史遗留问题。

## [v3.2.1](https://github.com/xhdlphzr/FranxAI/releases/tag/v3.2.1)

### Fixed
- macOS 启动脚本兼容性调整。
- 为所有文档添加 GPL 许可声明。

## [v3.2.2](https://github.com/xhdlphzr/FranxAI/releases/tag/v3.2.2)

### Fixed
- 系统提示词优化，增强 AI 行为可控性。

## [v3.2.3](https://github.com/xhdlphzr/FranxAI/releases/tag/v3.2.3)

### Fixed
- 为工具 README 添加类型限制，确保加载稳定。

## [v3.3.0](https://github.com/xhdlphzr/FranxAI/releases/tag/v3.3.0)

### Added
- 后端 Markdown 渲染（`python-markdown`）。
- 前端 KaTeX 数学公式渲染（支持 `$...$` 和 `$$...$$`）。
- 用户消息同样支持 Markdown 和数学公式。

## [v4.0.0](https://github.com/xhdlphzr/FranxAI/releases/tag/v4.0.0)

### Added
- **向量知识库**：统一所有知识源（工具说明、技能文件、MCP 工具描述、对话历史），通过 `sentence-transformers` 自动构建本地向量库，实现语义检索。
- **动态系统提示增强**：每次对话前，根据用户输入从向量库检索最相关的知识片段（数量可配置 `knowledge_k`），动态注入系统提示，大幅降低 token 消耗，同时让 AI 获得精准上下文。
- **对话历史持久化**：将完整对话问答对自动保存到 `skills/memories/` 目录，下次启动时自动纳入知识库，实现跨会话“记忆”检索。
- **统一工具入口**：将内置工具、MCP 工具的管理全部整合到 `skills` 模块，`agent.py` 仅需导入 `tool_functions` 和 `search`，代码更简洁。

### Fixed
- **移除 `memory.txt` 机制**：不再依赖文件摘要，改用向量库检索实现长期记忆。
- **`skills` 模块重构**：`skills/__init__.py` 现在同时负责工具加载、知识收集、向量库构建与检索；原 `tools/` 目录移入 `skills/tools/`，MCP 服务器启动逻辑也迁移至此。
- **配置新增 `knowledge_k`**：默认值 `1`，控制每次检索的知识片段数量。
- 修复了多轮对话中系统提示过于冗长的问题，现在只注入最相关的知识。
- 解决了 MCP 工具描述未加入知识库的遗漏，AI 现在能通过检索发现可用工具。
- 删除 `memory.txt` 相关代码，不再生成或读取该文件。