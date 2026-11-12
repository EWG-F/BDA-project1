#!/usr/bin/env bash
# TrendScope: Shell runner to execute Hive schemas and analytics queries
set -e

HIVE_BIN=${HIVE_BIN:-"hive"}
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=========================================================="
echo "TrendScope: Initializing Apache Hive Data Warehouse"
echo "=========================================================="

if ! command -v "$HIVE_BIN" &> /dev/null; then
    echo "[INFO] Hive CLI not detected in local PATH."
    echo "[INFO] In production or Hadoop mode, ensure Hive server/CLI is running."
    echo "[INFO] TrendScope Hadoop Bridge emulates HiveQL transformations seamlessly in Demo mode."
    exit 0
fi

echo "1. Creating database and tables..."
$HIVE_BIN -f "$BASE_DIR/create_tables.hql"

echo "2. Ingesting partitions..."
$HIVE_BIN -f "$BASE_DIR/load_data.hql"

echo "3. Executing analytical queries..."
$HIVE_BIN -f "$BASE_DIR/analytical_queries.hql"

echo "=== Hive Pipeline Executed Successfully! ==="
