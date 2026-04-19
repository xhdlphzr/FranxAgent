# Copyright (C) 2026 xhdlphzr
# This file is part of FranxAgent.
# FranxAgent is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.
# FranxAgent is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with FranxAgent.  If not, see <https://www.gnu.org/licenses/>.

"""
File Write Tool
Allows the AI to write or append content to a specified file
"""

from pathlib import Path

def execute(path: str, content: str, mode="overwrite") -> str:
    """
    Write or append content to a file

    Args:
        path: Full path of the file
        content: Content to be written
        mode: Write mode, "overwrite" (overwrite) or "append" (append), default is "overwrite"

    Returns:
        Operation result information
    """
    try:
        # Resolve the path and handle user directory symbol (~)
        p = Path(path).expanduser().resolve()

        # Ensure the parent directory exists
        p.parent.mkdir(parents=True, exist_ok=True)

        # Select file opening mode based on the parameter
        flag = 'a' if mode == 'append' else 'w'

        # Write content to the file
        with open(p, flag, encoding='utf-8') as f:
            f.write(content)

        # Return success message
        return f"Successfully {'appended to' if mode=='append' else 'wrote to'} file: {p}"
    except Exception as e:
        return f"Write failed: {e}"
