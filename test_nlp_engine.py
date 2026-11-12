"""
Unit tests for TrendScope NLP & Sentiment Engine
"""

import unittest
import pandas as pd
from src.nlp_engine import (
    clean_text,
    analyze_sentiment_single,
    batch_sentiment_analysis,
    extract_top_keywords,
    extract_hashtags,
    generate_ngrams
)

class TestNLPEngine(unittest.TestCase):
    def test_clean_text(self):
        sample = "Check out this AWESOME video! https://youtube.com #viral"
        cleaned = clean_text(sample)
        self.assertNotIn("https", cleaned)
        self.assertIn("awesome", cleaned)

    def test_sentiment_single(self):
        pos_res = analyze_sentiment_single("I absolutely love this amazing project!")
        self.assertEqual(pos_res['sentiment'], "Positive")
        self.assertGreater(pos_res['compound'], 0)

        neg_res = analyze_sentiment_single("This terrible bug is the worst disaster.")
        self.assertEqual(neg_res['sentiment'], "Negative")
        self.assertLess(neg_res['compound'], 0)

        neu_res = analyze_sentiment_single("Meeting scheduled for Monday 10am.")
        self.assertEqual(neu_res['sentiment'], "Neutral")

    def test_batch_sentiment(self):
        df = pd.DataFrame({'title': ["Great victory", "Terrible fail", "Standard video"]})
        res_df = batch_sentiment_analysis(df, column_name='title')
        self.assertIn('sentiment', res_df.columns)
        self.assertIn('sentiment_score', res_df.columns)
        self.assertEqual(len(res_df), 3)

    def test_keyword_and_hashtag_extraction(self):
        df = pd.DataFrame({
            'title': ["Python Big Data Analytics", "Python Machine Learning Analytics"],
            'tags': ['"python"|"bigdata"|"analytics"', '"python"|"ai"']
        })
        kw_df = extract_top_keywords(df, top_n=5)
        self.assertFalse(kw_df.empty)
        self.assertEqual(kw_df.iloc[0]['keyword'], 'python')

        tag_df = extract_hashtags(df, top_n=5)
        self.assertFalse(tag_df.empty)
        self.assertEqual(tag_df.iloc[0]['hashtag'], 'python')

if __name__ == '__main__':
    unittest.main()
