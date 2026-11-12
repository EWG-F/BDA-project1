#!/usr/bin/env python3
"""
MapReduce Job 2: Category-wise Statistics - Reducer
Aggregates video counts, views, likes, dislikes, and comments per category.
Calculates average views, average likes, and total engagement rate percentage.
Emits: category_id \t count,total_views,total_likes,total_comments,avg_views,avg_likes,engagement_rate
"""

import sys

def main():
    current_category = None
    count = 0
    total_views = 0
    total_likes = 0
    total_dislikes = 0
    total_comments = 0

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        
        parts = line.split('\t')
        if len(parts) != 2:
            continue
        
        category_id, metrics_str = parts
        try:
            c, v, l, d, cm = map(int, metrics_str.split(','))
        except ValueError:
            continue

        if current_category == category_id:
            count += c
            total_views += v
            total_likes += l
            total_dislikes += d
            total_comments += cm
        else:
            if current_category is not None and count > 0:
                avg_views = round(total_views / count, 2)
                avg_likes = round(total_likes / count, 2)
                engagement = round(((total_likes + total_comments) / total_views * 100), 2) if total_views > 0 else 0.0
                sys.stdout.write(f"{current_category}\t{count},{total_views},{total_likes},{total_comments},{avg_views},{avg_likes},{engagement}\n")
            
            current_category = category_id
            count = c
            total_views = v
            total_likes = l
            total_dislikes = d
            total_comments = cm

    if current_category is not None and count > 0:
        avg_views = round(total_views / count, 2)
        avg_likes = round(total_likes / count, 2)
        engagement = round(((total_likes + total_comments) / total_views * 100), 2) if total_views > 0 else 0.0
        sys.stdout.write(f"{current_category}\t{count},{total_views},{total_likes},{total_comments},{avg_views},{avg_likes},{engagement}\n")

if __name__ == "__main__":
    main()
