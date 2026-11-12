"""
TrendScope - Analytics Engine Module
Performs statistical aggregations, KPI computations, category breakdowns,
channel performance analysis, and regional cross-comparisons.
"""

import pandas as pd
import numpy as np

def compute_kpi_summary(df):
    """
    Computes high-level executive KPI metrics.
    """
    if df.empty:
        return {
            "total_videos": 0,
            "unique_videos": 0,
            "total_views": 0,
            "total_likes": 0,
            "total_comments": 0,
            "avg_engagement": 0.0,
            "avg_like_ratio": 0.0,
            "unique_channels": 0
        }
        
    t_vids = len(df)
    u_vids = df['video_id'].nunique() if 'video_id' in df.columns else t_vids
    t_views = df['views'].sum()
    t_likes = df['likes'].sum()
    t_comm = df['comment_count'].sum()
    avg_eng = round(((t_likes + t_comm) / t_views * 100), 2) if t_views > 0 else 0.0
    avg_like_r = round(df['like_ratio'].mean(), 2) if 'like_ratio' in df.columns else 0.0
    u_ch = df['channel_title'].nunique() if 'channel_title' in df.columns else 0
    
    return {
        "total_videos": t_vids,
        "unique_videos": u_vids,
        "total_views": t_views,
        "total_likes": t_likes,
        "total_comments": t_comm,
        "avg_engagement": avg_eng,
        "avg_like_ratio": avg_like_r,
        "unique_channels": u_ch
    }

def get_category_analytics(df):
    """
    Aggregates metrics by category.
    """
    if df.empty or 'category_name' not in df.columns:
        return pd.DataFrame()
        
    cat_df = df.groupby('category_name').agg(
        video_count=('views', 'count'),
        total_views=('views', 'sum'),
        total_likes=('likes', 'sum'),
        total_comments=('comment_count', 'sum'),
        avg_views=('views', 'mean'),
        avg_likes=('likes', 'mean')
    ).reset_index()
    
    cat_df['engagement_rate'] = (
        ((cat_df['total_likes'] + cat_df['total_comments']) / cat_df['total_views'].replace(0, 1)) * 100
    ).round(2)
    cat_df['avg_views'] = cat_df['avg_views'].round(0)
    cat_df['avg_likes'] = cat_df['avg_likes'].round(0)
    
    return cat_df.sort_values(by='total_views', ascending=False)

def get_channel_leaderboard(df, top_n=20):
    """
    Aggregates channel statistics and ranks channels by total viewership.
    """
    if df.empty or 'channel_title' not in df.columns:
        return pd.DataFrame()
        
    ch_df = df.groupby('channel_title').agg(
        unique_videos=('video_id', 'nunique'),
        total_views=('views', 'sum'),
        total_likes=('likes', 'sum'),
        total_comments=('comment_count', 'sum')
    ).reset_index()
    
    ch_df['engagement_rate'] = (
        ((ch_df['total_likes'] + ch_df['total_comments']) / ch_df['total_views'].replace(0, 1)) * 100
    ).round(2)
    
    return ch_df.sort_values(by='total_views', ascending=False).head(top_n)

def get_top_videos(df, sort_by='views', top_n=20):
    """
    Returns top performing videos based on selected metric.
    """
    if df.empty:
        return pd.DataFrame()
        
    cols = ['title', 'channel_title', 'category_name', 'country', 'views', 'likes', 'comment_count', 'engagement_rate', 'publish_time']
    avail_cols = [c for c in cols if c in df.columns]
    
    # Deduplicate by video_id to show peak record
    if 'video_id' in df.columns:
        dedup_df = df.sort_values(by=sort_by, ascending=False).drop_duplicates(subset=['video_id'])
    else:
        dedup_df = df.sort_values(by=sort_by, ascending=False)
        
    return dedup_df[avail_cols].head(top_n)

def get_regional_summary(df):
    """
    Compares metrics across countries.
    """
    if df.empty or 'country_name' not in df.columns:
        return pd.DataFrame()
        
    reg_df = df.groupby('country_name').agg(
        country_code=('country', 'first'),
        total_records=('views', 'count'),
        unique_videos=('video_id', 'nunique'),
        total_views=('views', 'sum'),
        total_likes=('likes', 'sum'),
        total_comments=('comment_count', 'sum'),
        avg_views=('views', 'mean')
    ).reset_index()
    
    reg_df['engagement_rate'] = (
        ((reg_df['total_likes'] + reg_df['total_comments']) / reg_df['total_views'].replace(0, 1)) * 100
    ).round(2)
    reg_df['avg_views'] = reg_df['avg_views'].round(0)
    
    return reg_df.sort_values(by='total_views', ascending=False)

def get_publish_timing_analytics(df):
    """
    Analyzes best publishing hours and days of the week.
    """
    if df.empty or 'publish_hour' not in df.columns:
        return pd.DataFrame(), pd.DataFrame()
        
    hour_df = df.groupby('publish_hour').agg(
        video_count=('views', 'count'),
        avg_views=('views', 'mean'),
        avg_engagement=('engagement_rate', 'mean')
    ).reset_index().sort_values(by='publish_hour')
    hour_df['avg_views'] = hour_df['avg_views'].round(0)
    hour_df['avg_engagement'] = hour_df['avg_engagement'].round(2)
    
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_df = df.groupby('publish_day').agg(
        video_count=('views', 'count'),
        avg_views=('views', 'mean'),
        avg_engagement=('engagement_rate', 'mean')
    ).reindex(day_order).dropna().reset_index()
    day_df['avg_views'] = day_df['avg_views'].round(0)
    day_df['avg_engagement'] = day_df['avg_engagement'].round(2)
    
    return hour_df, day_df
