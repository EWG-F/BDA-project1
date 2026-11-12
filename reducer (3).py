#!/usr/bin/env python3
"""
MapReduce Job 3: Trending Persistence Analysis - Reducer
Aggregates video records across days to compute consecutive trending days,
peak views, peak likes, and overall persistence score.
Emits: video_id \t title,channel_title,category_id,trending_days_count,peak_views,peak_likes,persistence_score
"""

import sys

def main():
    current_video_id = None
    dates = set()
    peak_views = 0
    peak_likes = 0
    title = ""
    channel = ""
    category_id = ""

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        
        parts = line.split('\t')
        if len(parts) != 2:
            continue
        
        v_id, data_str = parts
        try:
            meta, text_info = data_str.split(':::')
            meta_parts = meta.split(',')
            t_date = meta_parts[0]
            cat_id = meta_parts[1]
            views = int(meta_parts[2])
            likes = int(meta_parts[3])
            ch_name = meta_parts[4]
            t_title = text_info
        except (ValueError, IndexError):
            continue

        if current_video_id == v_id:
            dates.add(t_date)
            if views > peak_views:
                peak_views = views
                peak_likes = likes
            if t_title:
                title = t_title
            if ch_name:
                channel = ch_name
            if cat_id:
                category_id = cat_id
        else:
            if current_video_id is not None and dates:
                days_count = len(dates)
                p_score = round(days_count * 20.0 + (peak_views / 1000000.0) * 2.5, 2)
                sys.stdout.write(f"{current_video_id}\t{title}\t{channel}\t{category_id}\t{days_count}\t{peak_views}\t{peak_likes}\t{p_score}\n")
            
            current_video_id = v_id
            dates = {t_date}
            peak_views = views
            peak_likes = likes
            title = t_title
            channel = ch_name
            category_id = cat_id

    if current_video_id is not None and dates:
        days_count = len(dates)
        p_score = round(days_count * 20.0 + (peak_views / 1000000.0) * 2.5, 2)
        sys.stdout.write(f"{current_video_id}\t{title}\t{channel}\t{category_id}\t{days_count}\t{peak_views}\t{peak_likes}\t{p_score}\n")

if __name__ == "__main__":
    main()
