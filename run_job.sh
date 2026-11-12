#!/usr/bin/env bash
# Hadoop Streaming Runner for Job 2: Category-wise Statistics

INPUT_DIR=${1:-"/trendscope/raw/"}
OUTPUT_DIR=${2:-"/trendscope/output/job2_category_stats"}
HADOOP_STREAMING_JAR=${HADOOP_STREAMING_JAR:-"$HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar"}

echo "=== Running Hadoop Streaming Job 2: Category Statistics ==="
echo "Input: $INPUT_DIR"
echo "Output: $OUTPUT_DIR"

hdfs dfs -rm -r -f "$OUTPUT_DIR" 2>/dev/null || true

hadoop jar $HADOOP_STREAMING_JAR \
    -input "$INPUT_DIR" \
    -output "$OUTPUT_DIR" \
    -mapper "python3 mapper.py" \
    -reducer "python3 reducer.py" \
    -file mapper.py \
    -file reducer.py

echo "=== Job 2 Completed Successfully! ==="
