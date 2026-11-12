#!/usr/bin/env python3
"""
MapReduce Job 2: Category-wise Statistics - Mapper
Extracts category_id, views, likes, dislikes, and comments for each record.
Emits: category_id \t 1,views,likes,dislikes,comment_count
"""

import sys
import csv

def main():
    reader = csv.reader(sys.stdin)
    for row in reader:
        if not row or len(row) < 11:
            continue
        # Skip header
        if row[0].strip().lower() == "video_id":
            continue
        
        try:
            category_id = str(row[4]).strip()
            views = int(row[7])
            likes = int(row[8])
            dislikes = int(row[9])
            comments = int(row[10])
            
            # Emit category_id \t 1,views,likes,dislikes,comments
            sys.stdout.write(f"{category_id}\t1,{views},{likes},{dislikes},{comments}\n")
        except (ValueError, IndexError):
            continue

if __name__ == "__main__":
    main()
