# Copyright (C) 2026 xhdlphzr, zhiziwj
# This file is part of FranxAgent.
# FranxAgent is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.
# FranxAgent is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with FranxAgent.  If not, see <https://www.gnu.org/licenses/>.

"""
String Similarity Calculation Tool
Calculate the similarity of two strings using the rolling hash algorithm (window size 3 bytes)
"""

def execute(text1: str, text2: str) -> str:
    """
    Calculate the similarity of two strings

    Args:
        text1: The first string
        text2: The second string

    Returns:
        Similarity percentage in the format "XX.XX%"
    """
    # Base number and window size
    base = 131
    window_size = 3

    def rolling_hashes(s: str, w: int):
        """
        Calculate the rolling hash value set of a string

        Args:
            s: Input string
            w: Window size

        Returns:
            List of hash values
        """
        if len(s) < w:
            return []
        h = 0
        p = 1
        # Precompute base to the power of w
        for i in range(w):
            p *= base
        res = []
        for i, ch in enumerate(s):
            # Update the hash value
            h = h * base + ord(ch)
            if i >= w:
                # Remove the contribution of characters outside the window
                h -= ord(s[i - w]) * p
            if i >= w - 1:
                # Record the window hash value
                res.append(h)
        return res

    # Calculate the hash value sets of the two strings
    v1 = rolling_hashes(text1, window_size)
    v2 = rolling_hashes(text2, window_size)

    # If the length of either string is less than the window size, return 0%
    if not v1 or not v2:
        return "0.00%"

    # Convert to sets and calculate common hash values
    set1 = set(v1)
    set2 = set(v2)
    common = set1 & set2
    same = len(common)

    # Calculate similarity: 2 * common elements / total number of elements
    total = len(v1) + len(v2)
    similarity = 2.0 * same / total if total > 0 else 0.0

    # Return percentage
    return f"{similarity*100:.2f}%"