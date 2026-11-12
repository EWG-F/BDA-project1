#!/usr/bin/env bash
# Local Unix Pipe Simulator for all 3 Hadoop Streaming MapReduce Jobs
set -e

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RAW_DATA_DIR="$BASE_DIR/data/raw"
OUTPUT_DIR="$BASE_DIR/data/processed"

mkdir -p "$OUTPUT_DIR"

echo "=========================================================="
echo "TrendScope: Local MapReduce Execution Engine"
echo "=========================================================="

echo "Running MapReduce Job 1: Keyword Frequency Analysis..."
cat "$RAW_DATA_DIR"/*videos.csv | python3 "$BASE_DIR/mapreduce/job1_keyword_frequency/mapper.py" | sort | python3 "$BASE_DIR/mapreduce/job1_keyword_frequency/reducer.py" | sort -k2 -nr | head -n 150 > "$OUTPUT_DIR/mr_job1_raw_output.tsv"
echo "Job 1 complete. Sample output:"
head -n 5 "$OUTPUT_DIR/mr_job1_raw_output.tsv"

echo "Running MapReduce Job 2: Category-wise Statistics..."
cat "$RAW_DATA_DIR"/*videos.csv | python3 "$BASE_DIR/mapreduce/job2_category_stats/mapper.py" | sort | python3 "$BASE_DIR/mapreduce/job2_category_stats/reducer.py" > "$OUTPUT_DIR/mr_job2_raw_output.tsv"
echo "Job 2 complete. Sample output:"
head -n 5 "$OUTPUT_DIR/mr_job2_raw_output.tsv"

echo "Running MapReduce Job 3: Trending Persistence Analysis..."
cat "$RAW_DATA_DIR"/*videos.csv | python3 "$BASE_DIR/mapreduce/job3_trending_persistence/mapper.py" | sort | python3 "$BASE_DIR/mapreduce/job3_trending_persistence/reducer.py" | sort -k8 -nr > "$OUTPUT_DIR/mr_job3_raw_output.tsv"
echo "Job 3 complete. Sample output:"
head -n 5 "$OUTPUT_DIR/mr_job3_raw_output.tsv"

echo "=========================================================="
echo "All 3 MapReduce jobs completed and verified locally!"
echo "=========================================================="
