-- ==============================================================================
-- TrendScope - Apache Hive Analytical HiveQL Queries
-- Database: trendscope
-- ==============================================================================

USE trendscope;

-- ------------------------------------------------------------------------------
-- QUERY 1: Top 10 High-Growth Viral Videos Across All Regions
-- Objective: Identifies the most viewed videos with strong like-to-view conversion
-- ------------------------------------------------------------------------------
SELECT 
    video_id,
    title,
    channel_title,
    country,
    MAX(views) AS max_views,
    MAX(likes) AS max_likes,
    MAX(comment_count) AS max_comments,
    ROUND((MAX(likes) / CAST(MAX(views) AS DOUBLE)) * 100, 2) AS like_conversion_pct
FROM trending_videos
GROUP BY video_id, title, channel_title, country
ORDER BY max_views DESC
LIMIT 10;

-- ------------------------------------------------------------------------------
-- QUERY 2: Category Popularity and Audience Interaction Breakdown
-- Objective: Aggregates total viewership, engagement, and video volume per category
-- ------------------------------------------------------------------------------
SELECT 
    c.category_name,
    COUNT(t.video_id) AS total_appearances,
    SUM(t.views) AS total_views,
    SUM(t.likes) AS total_likes,
    SUM(t.comment_count) AS total_comments,
    ROUND(AVG(t.views), 0) AS avg_views_per_video,
    ROUND(AVG(t.engagement_rate), 2) AS avg_engagement_rate_pct
FROM trending_videos t
JOIN video_categories c ON t.category_id = c.category_id
GROUP BY c.category_name
ORDER BY total_views DESC;

-- ------------------------------------------------------------------------------
-- QUERY 3: Multi-Day Trending Persistence & Content Longevity Index
-- Objective: Measures how many distinct days videos stayed on the trending chart
-- ------------------------------------------------------------------------------
SELECT 
    video_id,
    title,
    channel_title,
    country,
    COUNT(DISTINCT trending_date) AS trending_days_count,
    MAX(views) AS peak_views,
    MAX(likes) AS peak_likes,
    ROUND(COUNT(DISTINCT trending_date) * 20.0 + (MAX(views) / 1000000.0) * 2.5, 2) AS persistence_score
FROM trending_videos
GROUP BY video_id, title, channel_title, country
HAVING COUNT(DISTINCT trending_date) >= 2
ORDER BY trending_days_count DESC, peak_views DESC
LIMIT 20;

-- ------------------------------------------------------------------------------
-- QUERY 4: Regional Content Consumption & Dominant Categories Comparison
-- Objective: Pivot-like comparison of category view distribution per country
-- ------------------------------------------------------------------------------
SELECT 
    t.country,
    c.category_name,
    COUNT(DISTINCT t.video_id) AS unique_videos,
    SUM(t.views) AS total_category_views,
    ROUND((SUM(t.views) / SUM(SUM(t.views)) OVER (PARTITION BY t.country)) * 100, 2) AS country_view_share_pct
FROM trending_videos t
JOIN video_categories c ON t.category_id = c.category_id
GROUP BY t.country, c.category_name
ORDER BY t.country, total_category_views DESC;

-- ------------------------------------------------------------------------------
-- QUERY 5: Top Performing Channels with Windowed Regional Rank
-- Objective: Evaluates top 5 channels per country using DENSE_RANK() window function
-- ------------------------------------------------------------------------------
WITH ChannelSummary AS (
    SELECT 
        channel_title,
        country,
        COUNT(DISTINCT video_id) AS total_unique_videos,
        SUM(views) AS aggregate_views,
        SUM(likes) AS aggregate_likes,
        ROUND(AVG(engagement_rate), 2) AS avg_engagement_rate,
        DENSE_RANK() OVER (PARTITION BY country ORDER BY SUM(views) DESC) AS rank_in_country
    FROM trending_videos
    GROUP BY channel_title, country
)
SELECT * 
FROM ChannelSummary 
WHERE rank_in_country <= 5
ORDER BY country, rank_in_country;

-- ------------------------------------------------------------------------------
-- QUERY 6: Day-of-Week Publishing Trend vs Average Engagement
-- Objective: Evaluates whether publish day affects trending video velocity
-- ------------------------------------------------------------------------------
SELECT 
    from_unixtime(unix_timestamp(publish_time), 'EEEE') AS publish_day_of_week,
    COUNT(DISTINCT video_id) AS total_published_videos,
    ROUND(AVG(views), 0) AS avg_views,
    ROUND(AVG(likes), 0) AS avg_likes,
    ROUND(AVG(engagement_rate), 2) AS avg_engagement_rate
FROM trending_videos
GROUP BY from_unixtime(unix_timestamp(publish_time), 'EEEE')
ORDER BY avg_views DESC;

-- ------------------------------------------------------------------------------
-- QUERY 7: Controversial Video Detection (High Dislike-to-Like Ratio)
-- Objective: Identifies videos that polarized audience opinion
-- ------------------------------------------------------------------------------
SELECT 
    video_id,
    title,
    channel_title,
    country,
    views,
    likes,
    dislikes,
    ROUND((dislikes / CAST(NULLIF(likes + dislikes, 0) AS DOUBLE)) * 100, 2) AS dislike_ratio_pct
FROM trending_videos
WHERE (likes + dislikes) > 10000
ORDER BY dislike_ratio_pct DESC
LIMIT 15;

-- ------------------------------------------------------------------------------
-- QUERY 8: Regional Macro Overview & Engagement Benchmarks
-- Objective: High-level KPI comparison across India, USA, UK, Canada, France
-- ------------------------------------------------------------------------------
SELECT 
    country,
    COUNT(video_id) AS total_trending_entries,
    COUNT(DISTINCT video_id) AS unique_video_count,
    SUM(views) AS total_country_views,
    SUM(likes) AS total_country_likes,
    SUM(comment_count) AS total_country_comments,
    ROUND(AVG(views), 0) AS avg_views_per_video,
    ROUND(AVG(engagement_rate), 2) AS avg_country_engagement_rate
FROM trending_videos
GROUP BY country
ORDER BY total_country_views DESC;
