<!--
Copyright (C) 2026 xhdlphzr
This file is part of FranxAgent.
FranxAgent is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.
FranxAgent is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FranxAgent.  If not, see <https://www.gnu.org/licenses/>.
-->

### beijing_subway — 北京地铁换乘助手
- **用途**：根据出发时间，规划北京地铁从起始站到目的地的最优换乘路线（最短出行时间）。自动适配早晚高峰的速度差异及换乘时间惩罚。
- **输入参数**：
    - `start`：**字符串**，起始站名称，例如：`"西直门"`
    - `end`：**字符串**，目的站名称，例如：`"北京南站"`
    - `time`：**整数 | None**，可选，出发时间（从当日 00:00 起计算的分钟数）。如未提供，则使用系统当前时间。
- **输出**：自然语言路线规划，包括途经线路、换乘站点和总出行时间（单位：分钟）。
- **依赖与文件**：
    - 必需库：`geopy`。如未安装，请运行 `pip install geopy`。
    - 数据文件：`station.json`、`graph.txt`。这些文件必须与 `tool.py` 放在同一目录下。
- **运营规则**：
    - 早高峰：07:00–09:00（420–540 分钟）
    - 晚高峰：17:00–19:00（1020–1140 分钟）
    - 高峰速度：35km/h，换乘惩罚：5 分钟
    - 平峰速度：40km/h，换乘惩罚：2 分钟
    - 可调参数：修改 `tool.py` 中的 `PEAK_PENALTY` / `OFF_PEAK_PENALTY`
- **范围限制**：仅支持北京地铁。数据文件需定期更新以与最新地铁线路保持一致。