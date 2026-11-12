#!/usr/bin/env python3
"""
MapReduce Job 3: Trending Persistence Analysis - Mapper
Extracts video_id, trending_date, title, channel_title, category_id, views, likes.
Emits: video_id \t trending_date,category_id,views,likes,channel_title,title
"""

import sys
import csv

def main():
    reader = csv.reader(sys.stdin)
    for row in reader:
        if not row or len(row) < 9:
            continue
        if row[0].strip().lower() == "video_id":
            continue
        
        try:
            video_id = row[0].strip()
            trending_date = row[1].strip()
            title = row[2].replace('\t', ' ').replace('\n', ' ').strip()
            channel_title = row[3].replace('\t', ' ').replace('\n', ' ').strip()
            category_id = str(row[4]).strip()
            views = int(row[7])
            likes = int(row[8])
            
            # Emit key \t value
            sys.stdout.write(f"{video_id}\t{trending_date},{category_id},{views},{likes},{channel_title}:::{title}\n")
        except (ValueError, IndexError):
            continue

if __name__ == "__main__":
    main()
