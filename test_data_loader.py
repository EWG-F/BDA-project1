"""
Unit tests for TrendScope Data Loader
"""

import unittest
import os
import pandas as pd
from src.data_loader import (
    load_category_mappings,
    load_country_data,
    load_all_countries_data,
    load_precomputed_mapreduce,
    load_precomputed_hive
)

class TestDataLoader(unittest.TestCase):
    def test_category_mappings(self):
        cat_map = load_category_mappings("US")
        self.assertIsInstance(cat_map, dict)
        self.assertIn(10, cat_map)
        self.assertEqual(cat_map[10], "Music")

    def test_load_country_data(self):
        df_us = load_country_data("US")
        self.assertFalse(df_us.empty)
        self.assertIn('views', df_us.columns)
        self.assertIn('likes', df_us.columns)
        self.assertIn('engagement_rate', df_us.columns)
        self.assertIn('category_name', df_us.columns)
        self.assertTrue((df_us['views'] >= 0).all())

    def test_load_all_countries(self):
        df_all = load_all_countries_data()
        self.assertFalse(df_all.empty)
        unique_countries = df_all['country'].unique()
        for c in ["US", "IN", "GB", "CA", "FR"]:
            self.assertIn(c, unique_countries)

    def test_precomputed_files(self):
        mr1, mr2, mr3 = load_precomputed_mapreduce()
        self.assertFalse(mr1.empty)
        self.assertFalse(mr2.empty)
        self.assertFalse(mr3.empty)
        
        h_ch, h_reg = load_precomputed_hive()
        self.assertFalse(h_ch.empty)
        self.assertFalse(h_reg.empty)

if __name__ == '__main__':
    unittest.main()
