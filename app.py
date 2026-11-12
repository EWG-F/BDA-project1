"""
TrendScope - Big Data-Based Internet Trend and Content Analytics System
Main Application Entrypoint
"""

import os
import time
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="TrendScope | Big Data Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

from src.data_loader import (
    load_all_countries_data,
    load_country_data,
    load_precomputed_mapreduce,
    load_precomputed_hive,
    process_uploaded_csv,
    COUNTRY_NAMES
)
from src.nlp_engine import (
    batch_sentiment_analysis,
    extract_top_keywords,
    extract_hashtags,
    generate_ngrams,
    generate_wordcloud_figure
)
from src.analytics_engine import (
    compute_kpi_summary,
    get_category_analytics,
    get_channel_leaderboard,
    get_top_videos,
    get_regional_summary,
    get_publish_timing_analytics
)
from src.hadoop_bridge import HadoopBridge
from src.ui_components import (
    inject_styles,
    render_kpi,
    render_header,
    apply_plotly_theme
)

inject_styles()
hadoop_bridge = HadoopBridge()

# ==============================================================================
# SIDEBAR CONTROLS
# ==============================================================================
st.sidebar.markdown("""
<div style="padding: 10px 0 16px 0;">
    <h2 style="margin:0; font-size:1.4rem; font-weight:700; color:#f8fafc;">TrendScope</h2>
    <p style="margin:2px 0 0 0; font-size:0.75rem; color:#94a3b8;">Big Data Analytics Platform</p>
</div>
""", unsafe_allow_html=True)

nav_options = [
    "Dashboard Overview",
    "Trending Topics & NLP",
    "Video & Creator Analytics",
    "Category Analysis",
    "Sentiment Analysis",
    "Regional Comparison",
    "Interactive Data Explorer",
    "Big Data & Hadoop Lab"
]

selected_page = st.sidebar.radio("Navigation", nav_options, index=0)

st.sidebar.markdown("---")
st.sidebar.markdown("**Data Controls**")

dataset_source = st.sidebar.selectbox(
    "Target Regional Dataset",
    ["Global (All Regions)", "United States (US)", "India (IN)", "United Kingdom (GB)", "Canada (CA)", "France (FR)"],
    index=0
)

uploaded_file = st.sidebar.file_uploader("Upload Custom CSV", type=["csv"])

engine_mode = st.sidebar.selectbox(
    "Processing Engine",
    ["Standalone / Demo Mode", "Hadoop Cluster Mode"],
    index=0
)

# Trigger dynamic computation button
st.sidebar.markdown("---")
run_pipeline_btn = st.sidebar.button("Run Analytics Pipeline", type="primary", use_container_width=True)

# Helper formatter
def fmt_num(val):
    if val >= 1_000_000_000:
        return f"{val / 1_000_000_000:.2f}B"
    elif val >= 1_000_000:
        return f"{val / 1_000_000:.2f}M"
    elif val >= 1_000:
        return f"{val / 1_000:.1f}K"
    return str(val)

# ==============================================================================
# DATA LOADING & LIVE EXECUTION
# ==============================================================================
@st.cache_data(show_spinner=False)
def fetch_base_data(source_name, upload_obj):
    if upload_obj is not None:
        return process_uploaded_csv(upload_obj)
    if "United States" in source_name:
        return load_country_data("US")
    elif "India" in source_name:
        return load_country_data("IN")
    elif "United Kingdom" in source_name:
        return load_country_data("GB")
    elif "Canada" in source_name:
        return load_country_data("CA")
    elif "France" in source_name:
        return load_country_data("FR")
    return load_all_countries_data()

raw_df = fetch_base_data(dataset_source, uploaded_file)

if raw_df.empty:
    st.error("Dataset could not be loaded. Please verify data files.")
    st.stop()

# Live calculation state
if "processed_data" not in st.session_state or run_pipeline_btn:
    with st.spinner("Processing dataset through NLP and analytical pipeline..."):
        t0 = time.time()
        processed_df = batch_sentiment_analysis(raw_df.copy())
        st.session_state["processed_data"] = processed_df
        st.session_state["pipeline_time"] = round(time.time() - t0, 3)
        st.session_state["pipeline_records"] = len(processed_df)

df = st.session_state.get("processed_data", raw_df)

# ==============================================================================
# PAGE 1: DASHBOARD OVERVIEW
# ==============================================================================
if selected_page == "Dashboard Overview":
    st.markdown("""
    <div style="margin-bottom: 16px;">
        <h1 style="margin:0; font-size:1.8rem; font-weight:700;">Executive Trend Overview</h1>
        <p style="color:#94a3b8; font-size:0.85rem; margin-top:2px;">Summary metrics, category distribution, and publishing velocity.</p>
    </div>
    """, unsafe_allow_html=True)

    kpis = compute_kpi_summary(df)

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        render_kpi("Total Videos", f"{kpis['total_videos']:,}", f"{kpis['unique_videos']:,} Unique Videos", "#6366f1")
    with c2:
        render_kpi("Cumulative Views", fmt_num(kpis['total_views']), "Total Audience Reach", "#06b6d4")
    with c3:
        render_kpi("Total Likes", fmt_num(kpis['total_likes']), f"Like Ratio: {kpis['avg_like_ratio']}%", "#10b981")
    with c4:
        render_kpi("Total Comments", fmt_num(kpis['total_comments']), "User Discussions", "#f59e0b")
    with c5:
        render_kpi("Avg Engagement Rate", f"{kpis['avg_engagement']}%", "Interactions per View", "#8b5cf6")

    col1, col2 = st.columns([3, 2])
    with col1:
        render_header("Category Viewership Volume", "Total views aggregated by video genre")
        cat_df = get_category_analytics(df)
        fig_cat = px.bar(
            cat_df.head(10),
            x="total_views",
            y="category_name",
            orientation="h",
            color="engagement_rate",
            color_continuous_scale="Viridis",
            labels={"total_views": "Total Views", "category_name": "Category", "engagement_rate": "Engagement %"},
            text_auto=".2s"
        )
        fig_cat.update_layout(yaxis=dict(autorange="reversed"))
        apply_plotly_theme(fig_cat)
        st.plotly_chart(fig_cat, use_container_width=True)

    with col2:
        render_header("Category Share of Voice", "Distribution of total trending entries")
        fig_pie = px.pie(
            cat_df.head(8),
            values="video_count",
            names="category_name",
            hole=0.45,
            color_discrete_sequence=px.colors.sequential.Plasma_r
        )
        apply_plotly_theme(fig_pie)
        st.plotly_chart(fig_pie, use_container_width=True)

    render_header("Publishing Timing Analysis", "Performance correlated with publish hour and day")
    hr_df, day_df = get_publish_timing_analytics(df)
    tc1, tc2 = st.columns(2)
    with tc1:
        fig_hr = px.line(
            hr_df,
            x="publish_hour",
            y="avg_views",
            markers=True,
            labels={"publish_hour": "Publish Hour (24h UTC)", "avg_views": "Average Views"},
            color_discrete_sequence=["#06b6d4"]
        )
        apply_plotly_theme(fig_hr)
        st.plotly_chart(fig_hr, use_container_width=True)

    with tc2:
        fig_day = px.bar(
            day_df,
            x="publish_day",
            y="avg_engagement",
            labels={"publish_day": "Day of Week", "avg_engagement": "Avg Engagement Rate (%)"},
            color="avg_engagement",
            color_continuous_scale="Tealgrn"
        )
        apply_plotly_theme(fig_day)
        st.plotly_chart(fig_day, use_container_width=True)

# ==============================================================================
# PAGE 2: TRENDING TOPICS & NLP
# ==============================================================================
elif selected_page == "Trending Topics & NLP":
    st.markdown("""
    <div style="margin-bottom: 16px;">
        <h1 style="margin:0; font-size:1.8rem; font-weight:700;">Trending Topics & NLP Intelligence</h1>
        <p style="color:#94a3b8; font-size:0.85rem; margin-top:2px;">Keyword tokenization, hashtag frequency, and phrase extraction.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        render_header("Top 20 Trending Keywords", "Extracted via Title Tokenization and Stopword Filtering")
        kw_df = extract_top_keywords(df, column_name='title', top_n=20)
        fig_kw = px.bar(
            kw_df,
            x="frequency",
            y="keyword",
            orientation="h",
            color="frequency",
            color_continuous_scale="Magma",
            labels={"frequency": "Frequency", "keyword": "Keyword"}
        )
        fig_kw.update_layout(yaxis=dict(autorange="reversed"))
        apply_plotly_theme(fig_kw)
        st.plotly_chart(fig_kw, use_container_width=True)

    with col2:
        render_header("Top Trending Hashtags & Tags", "Most common metadata tags in trending content")
        tag_df = extract_hashtags(df, column_name='tags', top_n=20)
        fig_tag = px.bar(
            tag_df,
            x="frequency",
            y="hashtag",
            orientation="h",
            color="frequency",
            color_continuous_scale="Inferno",
            labels={"frequency": "Tag Count", "hashtag": "Tag"}
        )
        fig_tag.update_layout(yaxis=dict(autorange="reversed"))
        apply_plotly_theme(fig_tag)
        st.plotly_chart(fig_tag, use_container_width=True)

    c_wc, c_ng = st.columns(2)
    with c_wc:
        render_header("Keyword Cloud Visualization", "Synthesized title lexicon")
        wc_fig = generate_wordcloud_figure(df, column_name='title', colormap='cool')
        st.pyplot(wc_fig, use_container_width=True)

    with c_ng:
        render_header("Frequent Title Bi-Grams", "2-word phrase co-occurrence frequencies")
        ng_df = generate_ngrams(df, column_name='title', n=2, top_n=15)
        fig_ng = px.bar(
            ng_df,
            x="count",
            y="ngram",
            orientation="h",
            color="count",
            color_continuous_scale="Bluered",
            labels={"count": "Count", "ngram": "Bi-Gram Phrase"}
        )
        fig_ng.update_layout(yaxis=dict(autorange="reversed"))
        apply_plotly_theme(fig_ng)
        st.plotly_chart(fig_ng, use_container_width=True)

# ==============================================================================
# PAGE 3: VIDEO & CREATOR ANALYTICS
# ==============================================================================
elif selected_page == "Video & Creator Analytics":
    st.markdown("""
    <div style="margin-bottom: 16px;">
        <h1 style="margin:0; font-size:1.8rem; font-weight:700;">Video & Creator Performance</h1>
        <p style="color:#94a3b8; font-size:0.85rem; margin-top:2px;">Top videos, creator rankings, and engagement correlations.</p>
    </div>
    """, unsafe_allow_html=True)

    render_header("Top Performing Videos Leaderboard", "Ranked list of trending videos")
    csort, climit = st.columns([2, 1])
    with csort:
        sort_col = st.selectbox("Sort By", ["views", "likes", "comment_count", "engagement_rate"])
    with climit:
        top_n = st.slider("Number of Rows", 5, 50, 15)

    top_vids = get_top_videos(df, sort_by=sort_col, top_n=top_n)
    st.dataframe(
        top_vids.style.format({
            "views": "{:,}",
            "likes": "{:,}",
            "comment_count": "{:,}",
            "engagement_rate": "{:.2f}%"
        }),
        use_container_width=True,
        height=350
    )

    c_scat, c_chan = st.columns(2)
    with c_scat:
        render_header("Views vs Likes Correlation", "Log-scaled interaction relationship")
        fig_scat = px.scatter(
            df.sample(min(len(df), 400), random_state=42),
            x="views",
            y="likes",
            size="comment_count",
            color="category_name",
            hover_data=["title", "channel_title"],
            log_x=True,
            log_y=True,
            labels={"views": "Views (Log)", "likes": "Likes (Log)"}
        )
        apply_plotly_theme(fig_scat)
        st.plotly_chart(fig_scat, use_container_width=True)

    with c_chan:
        render_header("Top Creator Channels", "Aggregated total views by channel")
        ch_df = get_channel_leaderboard(df, top_n=12)
        fig_ch = px.bar(
            ch_df,
            x="total_views",
            y="channel_title",
            orientation="h",
            color="engagement_rate",
            color_continuous_scale="Cividis",
            labels={"total_views": "Total Views", "channel_title": "Channel", "engagement_rate": "Engagement %"}
        )
        fig_ch.update_layout(yaxis=dict(autorange="reversed"))
        apply_plotly_theme(fig_ch)
        st.plotly_chart(fig_ch, use_container_width=True)

# ==============================================================================
# PAGE 4: CATEGORY ANALYSIS
# ==============================================================================
elif selected_page == "Category Analysis":
    st.markdown("""
    <div style="margin-bottom: 16px;">
        <h1 style="margin:0; font-size:1.8rem; font-weight:700;">Category Analysis</h1>
        <p style="color:#94a3b8; font-size:0.85rem; margin-top:2px;">Category popularity, audience engagement, and volume metrics.</p>
    </div>
    """, unsafe_allow_html=True)

    cat_df = get_category_analytics(df)

    col1, col2 = st.columns(2)
    with col1:
        render_header("Category Engagement Rate (%)", "Average interaction percentage by category")
        fig_eng = px.bar(
            cat_df.sort_values(by="engagement_rate", ascending=False),
            x="engagement_rate",
            y="category_name",
            orientation="h",
            color="engagement_rate",
            color_continuous_scale="Sunsetdark",
            labels={"engagement_rate": "Engagement Rate (%)", "category_name": "Category"},
            text_auto=".2f"
        )
        fig_eng.update_layout(yaxis=dict(autorange="reversed"))
        apply_plotly_theme(fig_eng)
        st.plotly_chart(fig_eng, use_container_width=True)

    with col2:
        render_header("Average Views per Video", "Exposure potential by content genre")
        fig_avg = px.bar(
            cat_df.sort_values(by="avg_views", ascending=False),
            x="avg_views",
            y="category_name",
            orientation="h",
            color="avg_views",
            color_continuous_scale="Viridis",
            labels={"avg_views": "Average Views", "category_name": "Category"},
            text_auto=".2s"
        )
        fig_avg.update_layout(yaxis=dict(autorange="reversed"))
        apply_plotly_theme(fig_avg)
        st.plotly_chart(fig_avg, use_container_width=True)

    render_header("Category Statistics Table", "MapReduce Job 2 aggregation output")
    st.dataframe(
        cat_df.style.format({
            "video_count": "{:,}",
            "total_views": "{:,}",
            "total_likes": "{:,}",
            "total_comments": "{:,}",
            "avg_views": "{:,.0f}",
            "avg_likes": "{:,.0f}",
            "engagement_rate": "{:.2f}%"
        }),
        use_container_width=True
    )

# ==============================================================================
# PAGE 5: SENTIMENT ANALYSIS
# ==============================================================================
elif selected_page == "Sentiment Analysis":
    st.markdown("""
    <div style="margin-bottom: 16px;">
        <h1 style="margin:0; font-size:1.8rem; font-weight:700;">Sentiment Analysis</h1>
        <p style="color:#94a3b8; font-size:0.85rem; margin-top:2px;">VADER sentiment classification across video titles and descriptions.</p>
    </div>
    """, unsafe_allow_html=True)

    pos_n = (df['sentiment'] == 'Positive').sum()
    neu_n = (df['sentiment'] == 'Neutral').sum()
    neg_n = (df['sentiment'] == 'Negative').sum()
    total_n = len(df)

    c1, c2, c3 = st.columns(3)
    with c1:
        render_kpi("Positive Sentiment", f"{pos_n:,}", f"{pos_n / total_n * 100:.1f}% of total content", "#10b981")
    with c2:
        render_kpi("Neutral Sentiment", f"{neu_n:,}", f"{neu_n / total_n * 100:.1f}% of total content", "#06b6d4")
    with c3:
        render_kpi("Negative Sentiment", f"{neg_n:,}", f"{neg_n / total_n * 100:.1f}% of total content", "#f43f5e")

    col1, col2 = st.columns(2)
    with col1:
        render_header("Sentiment Breakdown", "Proportion of positive, neutral, and negative content")
        sent_counts = df['sentiment'].value_counts().reset_index()
        sent_counts.columns = ['sentiment', 'count']
        fig_spie = px.pie(
            sent_counts,
            values="count",
            names="sentiment",
            hole=0.4,
            color="sentiment",
            color_discrete_map={"Positive": "#10b981", "Neutral": "#06b6d4", "Negative": "#f43f5e"}
        )
        apply_plotly_theme(fig_spie)
        st.plotly_chart(fig_spie, use_container_width=True)

    with col2:
        render_header("Sentiment vs Engagement Rate", "Distribution of engagement across sentiment classes")
        fig_sbox = px.box(
            df,
            x="sentiment",
            y="engagement_rate",
            color="sentiment",
            color_discrete_map={"Positive": "#10b981", "Neutral": "#06b6d4", "Negative": "#f43f5e"},
            labels={"sentiment": "Sentiment Tone", "engagement_rate": "Engagement Rate (%)"}
        )
        apply_plotly_theme(fig_sbox)
        st.plotly_chart(fig_sbox, use_container_width=True)

    render_header("Sample Videos by Classified Sentiment", "Title polarity score preview")
    sp1, sp2 = st.columns(2)
    with sp1:
        st.markdown("**Top Positive Videos**")
        top_pos = df[df['sentiment'] == 'Positive'].sort_values(by='views', ascending=False)[['title', 'channel_title', 'sentiment_score', 'views']].head(5)
        st.dataframe(top_pos.style.format({"views": "{:,}", "sentiment_score": "{:.2f}"}), use_container_width=True)
    with sp2:
        st.markdown("**Top Negative Videos**")
        top_neg = df[df['sentiment'] == 'Negative'].sort_values(by='views', ascending=False)[['title', 'channel_title', 'sentiment_score', 'views']].head(5)
        st.dataframe(top_neg.style.format({"views": "{:,}", "sentiment_score": "{:.2f}"}), use_container_width=True)

# ==============================================================================
# PAGE 6: REGIONAL COMPARISON
# ==============================================================================
elif selected_page == "Regional Comparison":
    st.markdown("""
    <div style="margin-bottom: 16px;">
        <h1 style="margin:0; font-size:1.8rem; font-weight:700;">Regional Comparison</h1>
        <p style="color:#94a3b8; font-size:0.85rem; margin-top:2px;">Cross-country analytics comparing India, USA, UK, Canada, and France.</p>
    </div>
    """, unsafe_allow_html=True)

    all_df = load_all_countries_data()
    reg_summary = get_regional_summary(all_df)

    col1, col2 = st.columns(2)
    with col1:
        render_header("Total Cumulative Views by Country", "Viewership scale per market")
        fig_rviews = px.bar(
            reg_summary,
            x="total_views",
            y="country_name",
            orientation="h",
            color="total_views",
            color_continuous_scale="Plasma",
            labels={"total_views": "Total Views", "country_name": "Country"},
            text_auto=".2s"
        )
        fig_rviews.update_layout(yaxis=dict(autorange="reversed"))
        apply_plotly_theme(fig_rviews)
        st.plotly_chart(fig_rviews, use_container_width=True)

    with col2:
        render_header("Average Engagement Rate by Country", "User participation rate per region")
        fig_reng = px.bar(
            reg_summary.sort_values(by="engagement_rate", ascending=False),
            x="engagement_rate",
            y="country_name",
            orientation="h",
            color="engagement_rate",
            color_continuous_scale="Tealgrn",
            labels={"engagement_rate": "Engagement Rate (%)", "country_name": "Country"},
            text_auto=".2f"
        )
        fig_reng.update_layout(yaxis=dict(autorange="reversed"))
        apply_plotly_theme(fig_reng)
        st.plotly_chart(fig_reng, use_container_width=True)

    render_header("Regional Category Consumption Matrix", "Genre view volume heatmap across markets")
    pivot_df = all_df.pivot_table(index="category_name", columns="country", values="views", aggfunc="sum", fill_value=0)
    fig_heat = px.imshow(
        pivot_df,
        labels=dict(x="Country", y="Category", color="Views"),
        color_continuous_scale="Viridis",
        aspect="auto"
    )
    apply_plotly_theme(fig_heat)
    st.plotly_chart(fig_heat, use_container_width=True)

# ==============================================================================
# PAGE 7: INTERACTIVE DATA EXPLORER
# ==============================================================================
elif selected_page == "Interactive Data Explorer":
    st.markdown("""
    <div style="margin-bottom: 16px;">
        <h1 style="margin:0; font-size:1.8rem; font-weight:700;">Interactive Data Explorer</h1>
        <p style="color:#94a3b8; font-size:0.85rem; margin-top:2px;">Search, filter, inspect raw data features, and export results.</p>
    </div>
    """, unsafe_allow_html=True)

    f1, f2, f3, f4 = st.columns(4)
    with f1:
        search_kw = st.text_input("Search Title / Channel / Tag", "")
    with f2:
        cat_opts = ["All Categories"] + sorted(df['category_name'].dropna().unique().tolist())
        sel_c = st.selectbox("Category Filter", cat_opts)
    with f3:
        sent_opts = ["All Sentiments", "Positive", "Neutral", "Negative"]
        sel_s = st.selectbox("Sentiment Filter", sent_opts)
    with f4:
        min_v = int(df['views'].min()) if not df.empty else 0
        max_v = int(df['views'].max()) if not df.empty else 1000000
        min_views = st.slider("Minimum Views", min_v, max_v, min_v)

    f_df = df.copy()
    if search_kw:
        q = search_kw.lower()
        f_df = f_df[
            f_df['title'].str.lower().str.contains(q, na=False) |
            f_df['channel_title'].str.lower().str.contains(q, na=False) |
            f_df['tags'].str.lower().str.contains(q, na=False)
        ]
    if sel_c != "All Categories":
        f_df = f_df[f_df['category_name'] == sel_c]
    if sel_s != "All Sentiments":
        f_df = f_df[f_df['sentiment'] == sel_s]
    if min_views > 0:
        f_df = f_df[f_df['views'] >= min_views]

    st.markdown(f"**Showing {len(f_df):,} matching records**")

    disp_cols = ['video_id', 'title', 'channel_title', 'category_name', 'country', 'views', 'likes', 'dislikes', 'comment_count', 'engagement_rate', 'sentiment']
    avail_cols = [c for c in disp_cols if c in f_df.columns]

    st.dataframe(
        f_df[avail_cols].style.format({
            "views": "{:,}",
            "likes": "{:,}",
            "dislikes": "{:,}",
            "comment_count": "{:,}",
            "engagement_rate": "{:.2f}%"
        }),
        use_container_width=True,
        height=400
    )

    csv_data = f_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Export Filtered CSV",
        data=csv_data,
        file_name="trendscope_filtered_data.csv",
        mime="text/csv"
    )

# ==============================================================================
# PAGE 8: BIG DATA & HADOOP LAB
# ==============================================================================
elif selected_page == "Big Data & Hadoop Lab":
    st.markdown("""
    <div style="margin-bottom: 16px;">
        <h1 style="margin:0; font-size:1.8rem; font-weight:700;">Big Data Infrastructure & Execution Lab</h1>
        <p style="color:#94a3b8; font-size:0.85rem; margin-top:2px;">HDFS storage architecture, MapReduce streaming jobs, and Apache Hive warehouse queries.</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["HDFS & Pipeline Architecture", "MapReduce Streaming Jobs", "Apache Hive Warehouse"])

    with tab1:
        render_header("Pipeline Execution Flow", "End-to-end distributed data processing")
        st.code("""
[Ingestion Layer]   --> YouTube Regional Trending CSVs (US, IN, GB, CA, FR) + Category JSONs
        |
        v
[Storage Layer]     --> Hadoop Distributed File System (HDFS: /trendscope/raw/)
        |
        +-----------------------------------+
        |                                   |
        v                                   v
[MapReduce Jobs]                    [Apache Hive Warehouse]
 * Job 1: Keyword Tokenization       * Database: trendscope
 * Job 2: Category Aggregations      * Partitioned ORC Tables
 * Job 3: Trending Persistence       * Windowed Analytical Queries
        |                                   |
        +-----------------+-----------------+
                          |
                          v
[Serving Layer]     --> Streamlit Dashboard + VADER NLP Engine
        """, language="text")

        cstatus = hadoop_bridge.get_cluster_status()
        s1, s2, s3 = st.columns(3)
        with s1:
            st.info(f"**HDFS NameNode:** {cstatus['hdfs_namenode']}")
        with s2:
            st.info(f"**Hive Metastore:** {cstatus['hive_metastore']}")
        with s3:
            st.info(f"**Engine:** {cstatus['execution_engine']}")

    with tab2:
        render_header("MapReduce Streaming Execution", "Run and inspect Python MapReduce jobs")
        job_sel = st.selectbox(
            "Select MapReduce Job",
            [
                "Job 1: Keyword Frequency Analysis",
                "Job 2: Category-wise Statistics",
                "Job 3: Trending Persistence Analysis"
            ]
        )
        jid = 1 if "Job 1" in job_sel else (2 if "Job 2" in job_sel else 3)

        if st.button(f"Execute MapReduce Job {jid} Locally"):
            with st.spinner(f"Executing MapReduce Job {jid}..."):
                success, msg = hadoop_bridge.run_mapreduce_job_locally(jid)
                if success:
                    st.success(msg)
                else:
                    st.warning(msg)

        mr_out = hadoop_bridge.get_job_output_dataframe(jid)
        st.markdown(f"**MapReduce Job {jid} Output:**")
        st.dataframe(mr_out.head(20), use_container_width=True)

    with tab3:
        render_header("Apache Hive Data Warehouse", "HiveQL DDL and analytical query results")
        h_ch, h_reg = load_precomputed_hive()

        col_h1, col_h2 = st.columns(2)
        with col_h1:
            st.markdown("**Top Channels (Hive Output)**")
            st.dataframe(h_ch.head(10).style.format({"total_views": "{:,}", "total_likes": "{:,}", "total_comments": "{:,}", "avg_engagement_rate": "{:.2f}%"}), use_container_width=True)
        with col_h2:
            st.markdown("**Regional Aggregations (Hive Output)**")
            st.dataframe(h_reg.style.format({"total_views": "{:,}", "total_likes": "{:,}", "total_comments": "{:,}", "avg_engagement_rate": "{:.2f}%"}), use_container_width=True)

        st.markdown("**Analytical HiveQL Query Script (`hive/analytical_queries.hql`):**")
        st.code(hadoop_bridge.get_hive_query_script(), language="sql")
