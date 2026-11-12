-- ==============================================================================
-- TrendScope - Apache Hive Data Ingestion and Partition Population
-- ==============================================================================

USE trendscope;

-- Enable dynamic partitioning
SET hive.exec.dynamic.partition=true;
SET hive.exec.dynamic.partition.mode=nonstrict;
SET hive.optimize.sort.dynamic.partition=true;

-- Insert Category Mapping Reference Data
INSERT OVERWRITE TABLE video_categories VALUES
(1, 'Film & Animation'),
(2, 'Autos & Vehicles'),
(10, 'Music'),
(15, 'Pets & Animals'),
(17, 'Sports'),
(19, 'Travel & Events'),
(20, 'Gaming'),
(22, 'People & Blogs'),
(23, 'Comedy'),
(24, 'Entertainment'),
(25, 'News & Politics'),
(26, 'Howto & Style'),
(27, 'Education'),
(28, 'Science & Technology'),
(29, 'Nonprofits & Activism');

-- Ingest Raw Country Partitions with Transformation & Metric Calculations
-- In production, execute LOAD DATA or INSERT statements per country:

-- US Partition
-- LOAD DATA INPATH '/trendscope/raw/USvideos.csv' OVERWRITE INTO TABLE youtube_raw_videos;
-- INSERT INTO TABLE trending_videos PARTITION (country = 'US')
-- SELECT 
--     video_id, trending_date, title, channel_title, category_id,
--     from_unixtime(unix_timestamp(publish_time, "yyyy-MM-dd'T'HH:mm:ss.SSS'Z'")),
--     tags, views, likes, dislikes, comment_count, thumbnail_link,
--     comments_disabled, ratings_disabled, video_error_or_removed, description,
--     ROUND(((likes + comment_count) / CAST(views AS DOUBLE)) * 100, 2) AS engagement_rate
-- FROM youtube_raw_videos;

-- Populate Pre-Aggregated Category Performance
INSERT OVERWRITE TABLE category_performance
SELECT 
    t.category_id,
    COALESCE(c.category_name, 'Unknown') AS category_name,
    t.country,
    COUNT(t.video_id) AS total_videos,
    SUM(t.views) AS total_views,
    SUM(t.likes) AS total_likes,
    SUM(t.comment_count) AS total_comments,
    ROUND(AVG(t.views), 2) AS avg_views,
    ROUND(AVG(t.likes), 2) AS avg_likes,
    ROUND(AVG(t.engagement_rate), 2) AS avg_engagement_rate
FROM trending_videos t
LEFT JOIN video_categories c ON t.category_id = c.category_id
GROUP BY t.category_id, c.category_name, t.country;

-- Populate Channel Leaderboard with Rank Window Functions
INSERT OVERWRITE TABLE channel_leaderboard
SELECT 
    channel_title,
    country,
    COUNT(DISTINCT video_id) AS unique_videos,
    SUM(views) AS total_views,
    SUM(likes) AS total_likes,
    SUM(comment_count) AS total_comments,
    ROUND(AVG(engagement_rate), 2) AS avg_engagement_rate,
    DENSE_RANK() OVER (PARTITION BY country ORDER BY SUM(views) DESC) AS channel_rank
FROM trending_videos
GROUP BY channel_title, country;
