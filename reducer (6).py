#!/usr/bin/env python3
"""
MapReduce Job 1: Keyword Frequency Analysis - Reducer
Aggregates occurrence counts for each keyword emitted by mappers.
Emits keyword and total count formatted as tab-separated values.
"""

import sys

def main():
    current_word = None
    current_count = 0

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        
        parts = line.split('\t')
        if len(parts) != 2:
            continue
        
        word, count_str = parts
        try:
            count = int(count_str)
        except ValueError:
            continue

        if current_word == word:
            current_count += count
        else:
            if current_word is not None:
                sys.stdout.write(f"{current_word}\t{current_count}\n")
            current_word = word
            current_count = count

    if current_word is not None:
        sys.stdout.write(f"{current_word}\t{current_count}\n")

if __name__ == "__main__":
    main()
