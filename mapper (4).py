#!/usr/bin/env python3
"""
MapReduce Job 1: Keyword Frequency Analysis - Mapper
Extracts tokens from video titles and tags, filters stopwords and punctuation,
and emits (keyword, 1) key-value pairs for Hadoop Streaming.
"""

import sys
import csv
import re

STOP_WORDS = {
    "the", "and", "a", "to", "of", "in", "is", "for", "that", "this", "it",
    "on", "with", "as", "at", "by", "from", "be", "or", "an", "are", "from",
    "video", "official", "new", "hd", "special", "part", "vs", "full", "2024",
    "all", "how", "what", "why", "when", "who", "which", "my", "your", "our",
    "me", "we", "us", "he", "she", "they", "them", "his", "her", "their", "so",
    "no", "not", "but", "if", "out", "up", "down", "about", "into", "over", "after"
}

def main():
    reader = csv.reader(sys.stdin)
    for row in reader:
        if not row or len(row) < 7:
            continue
        # Skip CSV header
        if row[0].strip().lower() == "video_id":
            continue
        
        title = row[2] if len(row) > 2 else ""
        tags = row[6] if len(row) > 6 else ""
        
        combined_text = f"{title} {tags.replace('|', ' ').replace('\"', '')}"
        tokens = re.findall(r'[A-Za-z0-9#@]{3,}', combined_text.lower())
        
        for token in tokens:
            token = token.strip()
            if token and token not in STOP_WORDS and not token.isdigit():
                # Emit key \t value
                sys.stdout.write(f"{token}\t1\n")

if __name__ == "__main__":
    main()
