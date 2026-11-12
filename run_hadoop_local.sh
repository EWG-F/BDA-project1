#!/usr/bin/env bash
# Shell execution script for TrendScope Local Big Data Pipeline
set -e

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "Starting TrendScope Local Big Data Pipeline..."
python3 "$BASE_DIR/scripts/hadoop_pipeline.py"
