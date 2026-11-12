"""
Unit tests for TrendScope Analytics Engine
"""

import unittest
import pandas as pd
from src.analytics_engine import (
    compute_kpi_summary,
    get_category_analytics,
    get_channel_leaderboard,
    get_top_videos,
    get_regional_summary
)

class TestAnalyticsEngine(unittest.TestCase):
    def setUp(self):
        self.sample_df = pd.DataFrame({
            'video_id': ['v1', 'v2', 'v3'],
            'title': ['Vid 1', 'Vid 2', 'Vid 3'],
            'channel_title': ['Ch A', 'Ch B', 'Ch A'],
            'category_name': ['Music', 'Gaming', 'Music'],
            'country': ['US', 'IN', 'US'],
            'country_name': ['United States', 'India', 'United States'],
            'views': [1000, 2000, 3000],
            'likes': [100, 200, 300],
            'dislikes': [5, 10, 15],
            'comment_count': [10, 20, 30],
            'engagement_rate': [11.0, 11.0, 11.0],
            'like_ratio': [95.2, 95.2, 95.2]
        })

    def test_kpi_summary(self):
        kpis = compute_kpi_summary(self.sample_df)
        self.assertEqual(kpis['total_videos'], 3)
        self.assertEqual(kpis['total_views'], 6000)
        self.assertEqual(kpis['total_likes'], 600)
        self.assertEqual(kpis['total_comments'], 60)
        self.assertEqual(kpis['unique_channels'], 2)

    def test_category_analytics(self):
        cat_df = get_category_analytics(self.sample_df)
        self.assertEqual(len(cat_df), 2)
        music_row = cat_df[cat_df['category_name'] == 'Music'].iloc[0]
        self.assertEqual(music_row['total_views'], 4000)
        self.assertEqual(music_row['video_count'], 2)

    def test_channel_leaderboard(self):
        ch_df = get_channel_leaderboard(self.sample_df)
        self.assertEqual(len(ch_df), 2)
        top_ch = ch_df.iloc[0]
        self.assertEqual(top_ch['channel_title'], 'Ch A')
        self.assertEqual(top_ch['total_views'], 4000)

    def test_regional_summary(self):
        reg_df = get_regional_summary(self.sample_df)
        self.assertEqual(len(reg_df), 2)
        us_row = reg_df[reg_df['country_code'] == 'US'].iloc[0]
        self.assertEqual(us_row['total_views'], 4000)

if __name__ == '__main__':
    unittest.main()
