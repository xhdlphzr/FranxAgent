<!--
Copyright (C) 2026 xhdlphzr
This file is part of FranxAgent.
FranxAgent is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.
FranxAgent is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FranxAgent.  If not, see <https://www.gnu.org/licenses/>.
-->

### `similarity` — 检测字符串相似度
- **用途**
在固定滑动窗口下计算两个字符串的相似度（固定窗口大小：3 字节，基于滚动哈希）。适用于本地文本去重、文件名比较等场景。

- **输入**
```json
{
"text1": "第一个字符串",
"text2": "第二个字符串"
}
```

参数说明：
- `text1`：**字符串**，必填，要比较的第一个字符串
- `text2`：**字符串**，必填，要比较的第二个字符串

- **输出**
返回格式为 `"XX.XX%"` 的字符串，表示相似度百分比。如果任一字符串的长度不足 3 字节，则返回 `"0.00%"`。

- **备注**
- 字符串按 UTF-8 编码的字节序列处理：英文字符占 1 字节，中文字符通常占 3 字节，窗口大小固定为 3 字节。
- 比较基于窗口哈希值集合，忽略窗口顺序，仅关注窗口内容的一致性。
- 适用于短文本比较。长文本仍可计算结果，但可能无法捕获长距离模式。