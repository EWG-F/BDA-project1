"""
TrendScope - NLP & Sentiment Analysis Engine
Provides sentiment classification (Positive/Negative/Neutral), text tokenization,
n-gram analysis, hashtag extraction, and word cloud generation.
"""

import re
from collections import Counter
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    vader_analyzer = SentimentIntensityAnalyzer()
except ImportError:
    vader_analyzer = None

STOP_WORDS = {
    "the", "and", "a", "to", "of", "in", "is", "for", "that", "this", "it",
    "on", "with", "as", "at", "by", "from", "be", "or", "an", "are", "from",
    "video", "official", "new", "hd", "special", "part", "vs", "full", "2024",
    "all", "how", "what", "why", "when", "who", "which", "my", "your", "our",
    "me", "we", "us", "he", "she", "they", "them", "his", "her", "their", "so",
    "no", "not", "but", "if", "out", "up", "down", "about", "into", "over", "after",
    "youtube", "trending", "viral", "ep", "teaser", "trailer", "live"
}

def clean_text(text):
    """
    Cleans raw text strings by stripping URLs, special chars, and redundant spaces.
    """
    if not isinstance(text, str):
        return ""
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'[^\w\s#@]', ' ', text)
    return text.strip().lower()

def analyze_sentiment_single(text):
    """
    Calculates compound sentiment score and classifies text as Positive, Negative, or Neutral.
    """
    if not isinstance(text, str) or not text.strip():
        return {"compound": 0.0, "sentiment": "Neutral", "pos": 0.0, "neu": 1.0, "neg": 0.0}
    
    if vader_analyzer:
        scores = vader_analyzer.polarity_scores(text)
        compound = scores['compound']
        if compound >= 0.05:
            label = "Positive"
        elif compound <= -0.05:
            label = "Negative"
        else:
            label = "Neutral"
        return {
            "compound": compound,
            "sentiment": label,
            "pos": scores['pos'],
            "neu": scores['neu'],
            "neg": scores['neg']
        }
    else:
        # High-performance rule-based fallback
        pos_words = {"love", "best", "great", "amazing", "awesome", "win", "epic", "good", "happy", "fun", "perfect"}
        neg_words = {"bad", "fail", "terrible", "worst", "hate", "issue", "mistake", "dark", "danger", "warning", "dead"}
        words = set(clean_text(text).split())
        pos_cnt = len(words & pos_words)
        neg_cnt = len(words & neg_words)
        if pos_cnt > neg_cnt:
            return {"compound": 0.4, "sentiment": "Positive", "pos": 0.5, "neu": 0.5, "neg": 0.0}
        elif neg_cnt > pos_cnt:
            return {"compound": -0.4, "sentiment": "Negative", "pos": 0.0, "neu": 0.5, "neg": 0.5}
        return {"compound": 0.0, "sentiment": "Neutral", "pos": 0.1, "neu": 0.8, "neg": 0.1}

def batch_sentiment_analysis(df, column_name='title'):
    """
    Applies sentiment analysis across a DataFrame column.
    """
    if column_name not in df.columns or df.empty:
        df['sentiment'] = 'Neutral'
        df['sentiment_score'] = 0.0
        return df
    
    results = [analyze_sentiment_single(text) for text in df[column_name].fillna('')]
    df['sentiment'] = [r['sentiment'] for r in results]
    df['sentiment_score'] = [r['compound'] for r in results]
    return df

def extract_top_keywords(df, column_name='title', top_n=50):
    """
    Extracts frequency distribution of meaningful keywords.
    """
    counter = Counter()
    for text in df[column_name].dropna():
        cleaned = clean_text(text)
        tokens = re.findall(r'[a-z0-9]{3,}', cleaned)
        for t in tokens:
            if t not in STOP_WORDS and not t.isdigit():
                counter[t] += 1
    return pd.DataFrame(counter.most_common(top_n), columns=['keyword', 'frequency'])

def extract_hashtags(df, column_name='tags', top_n=30):
    """
    Extracts hashtags and trending topic tags.
    """
    tag_counter = Counter()
    for raw_tags in df[column_name].dropna():
        if isinstance(raw_tags, str):
            # Split pipe or commas
            tokens = [t.strip().replace('"', '').lower() for t in raw_tags.split('|')]
            for t in tokens:
                if t and t not in STOP_WORDS and len(t) > 2 and not t.isdigit():
                    tag_counter[t] += 1
    return pd.DataFrame(tag_counter.most_common(top_n), columns=['hashtag', 'frequency'])

def generate_ngrams(df, column_name='title', n=2, top_n=20):
    """
    Generates N-Gram frequency counts (Bigrams / Trigrams).
    """
    ngram_counter = Counter()
    for text in df[column_name].dropna():
        tokens = [w for w in clean_text(text).split() if w not in STOP_WORDS and len(w) > 2]
        for i in range(len(tokens) - n + 1):
            ngram = " ".join(tokens[i:i+n])
            ngram_counter[ngram] += 1
    return pd.DataFrame(ngram_counter.most_common(top_n), columns=['ngram', 'count'])

def generate_wordcloud_figure(df, column_name='title', colormap='magma'):
    """
    Generates Matplotlib figure containing rendered Word Cloud.
    """
    text = " ".join([clean_text(str(t)) for t in df[column_name].dropna()])
    if not text.strip():
        text = "TrendScope BigData YouTube Analytics Trends Viral Content"
        
    wc = WordCloud(
        width=1000,
        height=500,
        background_color='#0f172a',
        colormap=colormap,
        stopwords=STOP_WORDS,
        max_words=100,
        random_state=42
    ).generate(text)
    
    fig, ax = plt.subplots(figsize=(10, 5), facecolor='#0f172a')
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')
    plt.tight_layout(pad=0)
    return fig
