# Copyright (C) 2026 xhdlphzr
# This file is part of FranxAgent.
# FranxAgent is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.
# FranxAgent is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with FranxAgent.  If not, see <https://www.gnu.org/licenses/>.

"""
File Content Reading Tool
Allows the AI to read the content of a specified file
"""

from pathlib import Path
import json
import base64
import time
from openai import OpenAI
from markitdown import MarkItDown

def read(path: str) -> str:
    """
    Read file content

    Args:
        path: Full path of the file

    Returns:
        File content, returns error message if an error occurs
    """
    try:
        # Resolve the path and handle user directory symbol (~)
        p = Path(path).expanduser().resolve()

        # Check if the file exists
        if not p.exists():
            return f"Error: File does not exist - {p}"

        # Check if the path is a file
        if not p.is_file():
            return f"Error: Path is not a file - {p}"

        # Read file content
        with open(p, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except PermissionError:
        return f"Error: No permission to read the file - {path}"
    except Exception as e:
        return f"An error occurred while reading the file: {str(e)}"
    
def _get_config():
    """Read ett tool configuration from config.json"""
    config_path = Path(__file__).parent.parent.parent / "config.json"
    if not config_path.exists():
        raise FileNotFoundError("config.json not found")
    with open(config_path, 'r', encoding='utf-8') as f:
        full_config = json.load(f)
    tool_cfg = full_config.get("tools", {}).get("ett", {})
    return {
        "api_key": tool_cfg.get("api_key", full_config.get("api_key")),
        "base_url": "https://open.bigmodel.cn/api/paas/v4",
        "model": tool_cfg.get("model", "glm-4.6v-flash"),
        "temperature": tool_cfg.get("temperature", full_config.get("temperature", 0.8)),
        "thinking": tool_cfg.get("thinking", full_config.get("thinking", False)),
        "max_retries": tool_cfg.get("max_retries", 5),
    }

def _encode_local_file(path: str) -> str:
    """Convert local file to data URL"""
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    ext = Path(path).suffix.lower()
    mime_map = {
        ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png",
        ".gif": "image/gif", ".mp4": "video/mp4", ".webm": "video/webm"
    }
    mime = mime_map.get(ext, "application/octet-stream")
    return f"data:{mime};base64,{data}"

def ett(urls: str) -> str:
    cfg = _get_config()
    prompt = "Please describe the following content in detail"
    if urls.endswith(('.jpg', '.png', '.gif', '.jpeg')):
        ftype = "image_url"
    if urls.endswith(('.mp4', '.webm')):
        ftype = "video_url"
    client = OpenAI(api_key=cfg["api_key"], base_url=cfg["base_url"])

    # Parse URLs
    url_list = [u.strip() for u in urls.split(",") if u.strip()]
    processed_urls = []
    for url in url_list:
        if url.startswith(("http://", "https://")):
            processed_urls.append(url)
        else:
            try:
                print("Encoding local file to base64, large files may take time please wait...")
                data_url = _encode_local_file(url)
                processed_urls.append(data_url)
            except Exception as e:
                return f"Failed to process local file: {e}"

    # Build content structure
    content = []
    for u in processed_urls:
        if ftype == "image_url":
            content.append({"type": "image_url", "image_url": {"url": u}})
        elif ftype == "video_url":
            content.append({"type": "video_url", "video_url": {"url": u}})
    content.append({"type": "text", "text": prompt})
    messages = [{"role": "user", "content": content}]

    max_retries = cfg["max_retries"]
    base_delay = 2

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=cfg["model"],
                messages=messages,
                temperature=cfg["temperature"],
                stream=False,
                timeout=60.0,   # Request timeout | 超时
                extra_body={"thinking": {"type": "disabled"}} if not cfg["thinking"] else None
            )
            return response.choices[0].message.content
        except Exception as e:
            error_msg = str(e)
            # Judge temporary errors: 429、500、timeout or rate limit keywords
            if any(code in error_msg for code in ["429", "500", "timed out", "timeout"]) or "rate" in error_msg.lower() or "too many" in error_msg.lower():
                if attempt < max_retries - 1:
                    wait = base_delay * (2 ** attempt)
                    print(f"Temporary API error, retry after {wait} seconds...")
                    time.sleep(wait)
                    continue
                else:
                    return "Analysis failed: API busy or timeout, please try again later. Copy content as text or screenshot to retry."
            else:
                return f"Analysis failed: {e}"

    return "Analysis failed: Maximum retries exceeded, please try again later."

def execute(path: str) -> str:
    if path.endswith(('.pdf', '.docx', '.pptx', '.xlsx', '.xls', '.doc', '.ppt', '.csv')):
        try:
            return MarkItDown().convert(path).text_content
        except Exception as e:
            return f"Failed to convert file to Markdown: {e}"
    elif path.endswith(('.jpg', '.png', '.gif', '.mp4', '.webm', '.jpeg')):
        return ett(path)
    else:
        return read(path)