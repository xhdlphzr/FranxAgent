# Copyright (C) 2026 xhdlphzr
# This file is part of FranxAgent.
# FranxAgent is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.
# FranxAgent is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with FranxAgent.  If not, see <https://www.gnu.org/licenses/>.

import json
import os
import heapq
from geopy.distance import distance

# Get current file directory
BASE_DIR = os.path.dirname(__file__)

# Load station data
with open(os.path.join(BASE_DIR, 'station.json'), 'r', encoding='utf-8') as f:
    station_data = json.load(f)

# Build mapping from station name to ID
name_to_id = {}
for sid, info in station_data.items():
    name = info['站点']
    name_to_id[name] = int(sid)

STATION_SIZE = 409

# Load adjacency matrix graph data
graph = []
with open(os.path.join(BASE_DIR, 'graph.txt'), 'r', encoding='utf-8') as f:
    for line in f:
        row = list(map(int, line.strip().split()))
        graph.append(row)

for i in range(STATION_SIZE):
    for j in range(STATION_SIZE):
        if graph[i][j] <= 0:
            graph[i][j] = -1

# Transfer penalty factor (minutes), adjustable
PEAK_PENALTY = 5      # Peak hour transfer penalty
OFF_PEAK_PENALTY = 2  # Off-peak hour transfer penalty

def a_star(start_id, end_id, time, graph, peak_penalty, off_peak_penalty):
    """
    A* algorithm implementation (internal use, depends on station_data)
    """
    # Judge speed (m/h) and penalty based on time
    def now_speed(t):
        return 35000 if (420 <= t < 540) or (1020 <= t < 1140) else 40000

    def now_punishment(t):
        return peak_penalty if (420 <= t < 540) or (1020 <= t < 1140) else off_peak_penalty

    # Heuristic function (straight-line distance/speed)
    def heuristic(idx1, idx2):
        coord1 = (station_data[str(idx1)]['纬度'], station_data[str(idx1)]['经度'])
        coord2 = (station_data[str(idx2)]['纬度'], station_data[str(idx2)]['经度'])
        dis = distance(coord1, coord2).m
        return round(dis / 40000 * 60)  # Fixed speed 40000 m/h

    # Check if transfer is required
    def is_transfer(prev, now, nxt):
        if prev == -1 or nxt == -1:
            return False
        lines_prev = set(station_data[str(prev)]['线路'])
        lines_now = set(station_data[str(now)]['线路'])
        lines_nxt = set(station_data[str(nxt)]['线路'])
        return (lines_prev & lines_now) != (lines_now & lines_nxt)

    # Initialization
    open_list = []
    heapq.heappush(open_list, (heuristic(start_id, end_id), heuristic(start_id, end_id), start_id))
    close_set = set()
    prev = [-1] * (STATION_SIZE + 1)
    g = [float('inf')] * (STATION_SIZE + 1)
    g[start_id] = time

    while open_list:
        f, h, u = heapq.heappop(open_list)
        if f > g[u] + heuristic(u, end_id):
            continue
        if u in close_set:
            continue
        close_set.add(u)

        if u == end_id:
            # Reconstruct path
            path = []
            cur = u
            while cur != -1:
                path.append(station_data[str(cur)]['站点'])
                cur = prev[cur]
            path.reverse()
            return g[end_id], g[end_id] - time, path

        for v in range(1, STATION_SIZE + 1):
            w = graph[u][v]
            if w == -1:
                continue
            travel_time = round(w / now_speed(g[u]) * 60)  # Minutes
            if is_transfer(prev[u], u, v):
                travel_time += now_punishment(g[u])

            new_g = g[u] + travel_time
            if new_g < g[v]:
                g[v] = new_g
                prev[v] = u
                heapq.heappush(open_list, (new_g + heuristic(v, end_id), heuristic(v, end_id), v))

    # No available path
    return None

def execute(start: str, end: str, time: int = None) -> str:
    """
    Query the optimal Beijing subway route from start to end (shortest travel time)
    Parameters:
        start: Starting station name
        end: Destination station name
        time: Departure time (minutes since 00:00 of the day), uses current time by default
    Returns:
        Route plan text
    """
    if start not in name_to_id:
        return f"Starting station not found: {start}"
    if end not in name_to_id:
        return f"Destination station not found: {end}"

    start_id = name_to_id[start]
    end_id = name_to_id[end]

    # Use current local time if no time provided
    if time is None:
        import datetime
        now = datetime.datetime.now()
        time = now.hour * 60 + now.minute

    result = a_star(start_id, end_id, time, graph, PEAK_PENALTY, OFF_PEAK_PENALTY)
    if result is None:
        return f"No route found from {start} to {end}"

    total_minutes, travel_minutes, path = result
    # Format output
    lines = []
    current_line = None
    for i, station in enumerate(path):
        if i == 0:
            lines.append(f"Depart from {station}")
        else:
            # Get the first line of current station
            sid = name_to_id[station]
            station_info = station_data[str(sid)]
            line = station_info['线路'][0] if station_info['线路'] else 'Unknown Line'
            if current_line is None:
                current_line = line
                lines.append(f"Take {line} Line")
            elif line != current_line:
                lines.append(f"Transfer to {line} Line at {station}")
                current_line = line
    lines.append(f"Arrive at {path[-1]}")
    lines.append(f"Total travel time: about {travel_minutes} minutes (including transfers)")
    return "\n".join(lines)