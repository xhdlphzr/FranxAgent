# Copyright (C) 2026 xhdlphzr
# This file is part of FranxAI.
# FranxAI is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.
# FranxAI is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with FranxAI.  If not, see <https://www.gnu.org/licenses/>.

"""
Skills 模块：统一工具加载 + MCP 管理 + 自动构建向量知识库
"""

import importlib.util
import sys
import sqlite3
import json
import numpy as np
import time
import threading
from pathlib import Path
from sentence_transformers import SentenceTransformer

# 添加项目根目录到 sys.path 以便导入 src.mcps
PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.mcps import MCPStdioClient

# ---------- 1. 加载内置工具 ----------
SKILLS_ROOT = Path(__file__).parent
TOOLS_DIR = SKILLS_ROOT / 'tools'

_internal_tools = {}
for item in TOOLS_DIR.iterdir():
    if not item.is_dir() or item.name.startswith('__'):
        continue
    tool_name = item.name
    tool_path = item / 'tool.py'
    readme_path = item / 'README.md'

    if not (tool_path.exists() and readme_path.exists()):
        print(f"⚠️ 工具 {tool_name} 缺少 tool.py 或 README.md，跳过")
        continue

    try:
        spec = importlib.util.spec_from_file_location(f"skills.tools.{tool_name}", tool_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[f"skills.tools.{tool_name}"] = module
        spec.loader.exec_module(module)
    except Exception as e:
        print(f"⚠️ 工具 {tool_name} 的 tool.py 导入失败：{e}，跳过")
        continue

    if not hasattr(module, 'execute'):
        print(f"⚠️ 工具 {tool_name} 的 tool.py 未定义 execute 函数，跳过")
        continue

    _internal_tools[tool_name] = module.execute

# ---------- 2. 收集所有 Markdown 文件 ----------
all_md_contents = []
for md_file in SKILLS_ROOT.rglob("*.md"):
    try:
        content = md_file.read_text(encoding='utf-8').strip()
        if content:
            all_md_contents.append(content)
    except Exception as e:
        print(f"⚠️ 读取 Markdown 文件 {md_file} 失败：{e}")

# ---------- 3. MCP 服务器管理 ----------
_mcp_tools = {}
_mcp_clients = []
_mcp_lock = threading.Lock()

def _load_mcp_servers():
    """从配置文件加载 MCP 服务器并启动，将工具描述加入知识库"""
    global _mcp_tools
    config_path = PROJECT_ROOT / "config.json"
    if not config_path.exists():
        return
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except Exception as e:
        print(f"读取配置文件失败: {e}")
        return

    servers = config.get("mcp_servers", [])
    if not servers:
        return

    for server in servers:
        name = server.get("name", "unknown")
        command = server.get("command")
        if not command:
            print(f"跳过 {name}: 缺少 command")
            continue
        args = server.get("args", [])

        try:
            client = MCPStdioClient(command, args)
            client.start()
            time.sleep(0.5)  # 等待子进程就绪
            raw_tools = client.list_tools()
            if not raw_tools:
                print(f"⚠️ {name} 未返回工具，跳过")
                client.close()
                continue

            print(f"已连接 MCP 服务器 {name}，发现 {len(raw_tools)} 个工具")
            _mcp_clients.append(client)
            with _mcp_lock:
                for tool in raw_tools:
                    tool_name = tool["name"]
                    full_name = f"{name}/{tool_name}"
                    description = tool.get("description", "")
                    params = tool.get("inputSchema", {}).get("properties", {})
                    param_str = ", ".join([f"{k} ({v.get('type','any')})" for k, v in params.items()])
                    desc_text = f"工具名称：{full_name}\n功能：{description}\n参数：{param_str}" if param_str else f"工具名称：{full_name}\n功能：{description}"
                    # 将描述加入全局知识库
                    all_md_contents.append(desc_text)

                    # 创建包装函数
                    def make_wrapper(mcp_client, t_name):
                        def wrapper(**kwargs):
                            try:
                                return mcp_client.call_tool(t_name, kwargs)
                            except Exception as e:
                                return f"调用失败: {e}"
                        return wrapper
                    _mcp_tools[full_name] = make_wrapper(client, tool_name)
        except Exception as e:
            print(f"启动 MCP 服务器 {name} 失败: {e}")
            import traceback
            traceback.print_exc()
            continue

# 启动 MCP 服务器（此时 all_md_contents 会追加 MCP 工具描述）
_load_mcp_servers()

# ---------- 4. 向量库构建（自动） ----------
VECTOR_DB_PATH = SKILLS_ROOT / "knowledge.db"
MODEL_NAME = 'all-MiniLM-L12-v2'

def _init_vector_db():
    """创建数据库表（如果不存在）"""
    conn = sqlite3.connect(VECTOR_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vectors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            embedding BLOB NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS metadata (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    conn.commit()
    conn.close()

def _get_current_file_state():
    """获取当前所有 .md 文件的状态（相对路径 -> 修改时间）"""
    state = {}
    for md_file in SKILLS_ROOT.rglob("*.md"):
        try:
            mtime = md_file.stat().st_mtime
            rel_path = str(md_file.relative_to(SKILLS_ROOT))
            state[rel_path] = mtime
        except Exception as e:
            print(f"⚠️ 无法获取文件状态 {md_file}: {e}")
    return state

def _need_rebuild():
    """检查是否需要重建向量库"""
    conn = sqlite3.connect(VECTOR_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM vectors")
    count = cursor.fetchone()[0]
    if count == 0:
        conn.close()
        return True

    cursor.execute("SELECT value FROM metadata WHERE key = 'file_state'")
    row = cursor.fetchone()
    stored_state_json = row[0] if row else None
    conn.close()

    if stored_state_json is None:
        return True

    try:
        stored_state = json.loads(stored_state_json)
    except:
        return True

    current_state = _get_current_file_state()
    return stored_state != current_state

def _rebuild_vector_db():
    """重建向量库"""
    print("正在构建向量知识库...")
    model = SentenceTransformer(MODEL_NAME)
    conn = sqlite3.connect(VECTOR_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM vectors')
    cursor.execute('DELETE FROM metadata')
    for idx, text in enumerate(all_md_contents):
        emb = model.encode(text)
        emb_blob = emb.tobytes()
        cursor.execute(
            "INSERT INTO vectors (text, embedding) VALUES (?, ?)",
            (text, emb_blob)
        )
        if (idx + 1) % 50 == 0:
            print(f"  已处理 {idx+1}/{len(all_md_contents)} 条")
    current_state = _get_current_file_state()
    cursor.execute(
        "INSERT INTO metadata (key, value) VALUES (?, ?)",
        ('file_state', json.dumps(current_state))
    )
    conn.commit()
    conn.close()
    print(f"向量库构建完成，共 {len(all_md_contents)} 条记录。")

_init_vector_db()
if _need_rebuild():
    _rebuild_vector_db()

# ---------- 5. 检索接口 ----------
def search(query: str, k: int = 1):
    """检索与 query 最相似的 k 条知识"""
    conn = sqlite3.connect(VECTOR_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT text, embedding FROM vectors")
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        return []

    model = SentenceTransformer(MODEL_NAME)
    q_emb = model.encode(query)
    scores = []
    for text, emb_blob in rows:
        emb = np.frombuffer(emb_blob, dtype=np.float32)
        dot = np.dot(q_emb, emb)
        norm_q = np.linalg.norm(q_emb)
        norm_d = np.linalg.norm(emb)
        sim = dot / (norm_q * norm_d) if norm_q * norm_d != 0 else 0
        scores.append((sim, text))
    scores.sort(reverse=True, key=lambda x: x[0])
    return [{'text': t} for _, t in scores[:k]]

# ---------- 6. 统一工具调用（内置 + MCP） ----------
def tools(tool_name: str, arguments: dict = None) -> str:
    """
    统一工具调用接口：支持内置工具和 MCP 工具（格式 服务器名/工具名）
    """
    # 先检查是否是 MCP 工具
    if '/' in tool_name:
        with _mcp_lock:
            if tool_name in _mcp_tools:
                try:
                    return _mcp_tools[tool_name](**(arguments or {}))
                except Exception as e:
                    return f"MCP 工具调用失败: {e}"
            else:
                return f"错误：未知 MCP 工具 {tool_name}"
    # 否则尝试内置工具
    if tool_name not in _internal_tools:
        return f"错误：未知工具 {tool_name}"
    try:
        return _internal_tools[tool_name](**(arguments or {}))
    except Exception as e:
        return f"调用失败: {e}"

# 导出工具函数字典（只有一个 tools 函数）
tool_functions = {"tools": tools}

# 工具元数据（描述）
tools_metadata = [
    {
        "type": "function",
        "function": {
            "name": "tools",
            "description": "调用任何可用工具。参数：tool_name (工具名), arguments (JSON 对象)。所有内置工具都通过此工具调用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "tool_name": {
                        "type": "string",
                        "description": "工具名称，如 read、write、command、search、similarity、add_task、del_task、ett、beijing_subway 等。外部 MCP 工具使用 服务器名/工具名 格式。"
                    },
                    "arguments": {
                        "type": "object",
                        "description": "工具参数"
                    }
                },
                "required": ["tool_name"]
            }
        }
    }
]

# 清理函数（供外部调用，例如 atexit）
def cleanup_mcp_clients():
    """关闭所有 MCP 客户端"""
    for client in _mcp_clients:
        try:
            client.close()
        except:
            pass

print("内置工具列表:", list(_internal_tools.keys()))
print(f"MCP 工具数量: {len(_mcp_tools)}")
print(f"知识库已就绪，共 {len(all_md_contents)} 篇文档。")

__all__ = ['tools_metadata', 'tool_functions', 'search', 'cleanup_mcp_clients']