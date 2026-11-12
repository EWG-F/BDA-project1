-- ==============================================================================
-- TrendScope - Apache Hive DDL Specification
-- Database: trendscope
-- ==============================================================================

CREATE DATABASE IF NOT EXISTS trendscope
COMMENT 'TrendScope Big Data Internet Trend and Content Analytics Warehouse'
LOCATION '/user/hive/warehouse/trendscope.db';

USE trendscope;

-- 1. Staging / External Raw Table
CREATE EXTERNAL TABLE IF NOT EXISTS youtube_raw_videos (
    video_id STRING,
    trending_date STRING,
    title STRING,
    channel_title STRING,
    category_id INT,
    publish_time STRING,
    tags STRING,
    views BIGINT,
    likes BIGINT,
    dislikes BIGINT,
    comment_count BIGINT,
    thumbnail_link STRING,
    comments_disabled BOOLEAN,
    ratings_disabled BOOLEAN,
    video_error_or_removed BOOLEAN,
    description STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
   "separatorChar" = ",",
   "quoteChar"     = "\"",
   "escapeChar"    = "\\"
)
STORED AS TEXTFILE
LOCATION '/trendscope/raw/combined/'
TBLPROPERTIES ("skip.header.line.count"="1");

-- 2. Partitioned ORC Managed Table for Production Query Optimization
CREATE TABLE IF NOT EXISTS trending_videos (
    video_id STRING,
    trending_date STRING,
    title STRING,
    channel_title STRING,
    category_id INT,
    publish_time TIMESTAMP,
    tags STRING,
    views BIGINT,
    likes BIGINT,
    dislikes BIGINT,
    comment_count BIGINT,
    thumbnail_link STRING,
    comments_disabled BOOLEAN,
    ratings_disabled BOOLEAN,
    video_error_or_removed BOOLEAN,
    description STRING,
    engagement_rate DOUBLE
)
COMMENT 'Cleaned, structured trending videos partitioned by country'
PARTITIONED BY (country STRING)
STORED AS ORC
TBLPROPERTIES (
    "orc.compress"="SNAPPY",
    "orc.create.index"="true",
    "transactional"="false"
);

-- 3. Category Lookup Table
CREATE TABLE IF NOT EXISTS video_categories (
    category_id INT,
    category_name STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE;

-- 4. Analytical Pre-Aggregated Summary Table: Category Performance
CREATE TABLE IF NOT EXISTS category_performance (
    category_id INT,
    category_name STRING,
    country STRING,
    total_videos BIGINT,
    total_views BIGINT,
    total_likes BIGINT,
    total_comments BIGINT,
    avg_views DOUBLE,
    avg_likes DOUBLE,
    avg_engagement_rate DOUBLE
)
STORED AS ORC;

-- 5. Analytical Pre-Aggregated Summary Table: Channel Leaderboard
CREATE TABLE IF NOT EXISTS channel_leaderboard (
    channel_title STRING,
    country STRING,
    unique_videos BIGINT,
    total_views BIGINT,
    total_likes BIGINT,
    total_comments BIGINT,
    avg_engagement_rate DOUBLE,
    channel_rank INT
)
STORED AS ORC;

-- 6. Analytical Pre-Aggregated Summary Table: Trending Persistence
CREATE TABLE IF NOT EXISTS video_persistence_stats (
    video_id STRING,
    title STRING,
    channel_title STRING,
    category_name STRING,
    country STRING,
    trending_days_count INT,
    peak_views BIGINT,
    peak_likes BIGINT,
    persistence_score DOUBLE
)
STORED AS ORC;
