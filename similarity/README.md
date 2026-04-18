<!--
Copyright (C) 2026 xhdlphzr
This file is part of FranxAgent.
FranxAgent is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.
FranxAgent is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FranxAgent.  If not, see <https://www.gnu.org/licenses/>.
-->

### `similarity` - Detect String Similarity | 检测字符串相似度
- **Purpose**
Calculate the similarity between two strings under a fixed sliding window (fixed window size: 3 bytes, based on rolling hash). Suitable for scenarios such as local text duplicate detection and filename comparison.

- **Input**
```json
{
"text1": "First string",
"text2": "Second string"
}
```

Parameter Description:
- `text1`: **string**, required, the first string to be compared
- `text2`: **string**, required, the second string to be compared

- **Output**
Returns a string in the format `"XX.XX%"`, representing the similarity percentage. If the length of either string is less than 3 bytes, it returns `"0.00%"`.

- **Notes**
- Strings are processed as UTF-8 encoded byte sequences: English characters occupy 1 byte, Chinese characters usually occupy 3 bytes, and the window size is fixed at 3 bytes.
- The comparison is based on sets of window hash values; the order of windows is ignored, only the consistency of window content matters.
- Suitable for short text comparison. It can still calculate results for long texts, but may fail to capture long-range patterns.