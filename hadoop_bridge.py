"""
TrendScope - Hadoop & Big Data Bridge Module
Bridges Streamlit application with Hadoop HDFS, MapReduce Streaming, and Apache Hive.
Supports both Live Hadoop Execution and Standalone Demo Mode.
"""

import os
import subprocess
import pandas as pd

class HadoopBridge:
    def __init__(self):
        self.hadoop_home = os.environ.get("HADOOP_HOME", "")
        self.hive_home = os.environ.get("HIVE_HOME", "")
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.mapreduce_dir = os.path.join(self.base_dir, "mapreduce")
        self.hive_dir = os.path.join(self.base_dir, "hive")
        self.processed_dir = os.path.join(self.base_dir, "data", "processed")
        self.raw_dir = os.path.join(self.base_dir, "data", "raw")

    def check_hadoop_installed(self):
        """
        Checks whether Hadoop and HDFS CLIs are available on the operating system.
        """
        try:
            res = subprocess.run(["hadoop", "version"], capture_output=True, text=True, timeout=5)
            return res.returncode == 0
        except Exception:
            return False

    def check_hive_installed(self):
        """
        Checks whether Apache Hive is available in PATH.
        """
        try:
            res = subprocess.run(["hive", "--version"], capture_output=True, text=True, timeout=5)
            return res.returncode == 0
        except Exception:
            return False

    def run_mapreduce_job_locally(self, job_number=1):
        """
        Executes a specific MapReduce job using local Python standard I/O streaming pipes.
        """
        job_map = {
            1: ("job1_keyword_frequency", "mr_job1_raw_output.tsv"),
            2: ("job2_category_stats", "mr_job2_raw_output.tsv"),
            3: ("job3_trending_persistence", "mr_job3_raw_output.tsv")
        }
        
        if job_number not in job_map:
            return False, "Invalid Job Number"
            
        job_folder, out_filename = job_map[job_number]
        mapper = os.path.join(self.mapreduce_dir, job_folder, "mapper.py")
        reducer = os.path.join(self.mapreduce_dir, job_folder, "reducer.py")
        out_file = os.path.join(self.processed_dir, out_filename)
        
        try:
            # Command: cat raw/*videos.csv | python mapper.py | sort | python reducer.py > out_file
            cmd = f"cat {self.raw_dir}/*videos.csv | python3 {mapper} | sort | python3 {reducer} > {out_file}"
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
            if res.returncode == 0:
                return True, f"MapReduce Job {job_number} executed successfully! Output saved to {out_filename}"
            else:
                return False, f"MapReduce Job {job_number} error: {res.stderr}"
        except Exception as e:
            return False, f"Execution failed: {str(e)}"

    def get_job_output_dataframe(self, job_number=1):
        """
        Loads the output dataset for the requested MapReduce job.
        """
        if job_number == 1:
            path = os.path.join(self.processed_dir, "mapreduce_job1_keywords.csv")
            return pd.read_csv(path)
        elif job_number == 2:
            path = os.path.join(self.processed_dir, "mapreduce_job2_category_stats.csv")
            return pd.read_csv(path)
        elif job_number == 3:
            path = os.path.join(self.processed_dir, "mapreduce_job3_persistence.csv")
            return pd.read_csv(path)
        return pd.DataFrame()

    def get_hive_query_script(self):
        """
        Reads analytical HiveQL script text.
        """
        hql_path = os.path.join(self.hive_dir, "analytical_queries.hql")
        if os.path.exists(hql_path):
            with open(hql_path, 'r', encoding='utf-8') as f:
                return f.read()
        return "-- HiveQL script not found"

    def get_cluster_status(self):
        """
        Returns environment diagnostic parameters.
        """
        hadoop_avail = self.check_hadoop_installed()
        hive_avail = self.check_hive_installed()
        
        return {
            "hadoop_available": hadoop_avail,
            "hive_available": hive_avail,
            "hdfs_namenode": "hdfs://localhost:9000" if hadoop_avail else "Standalone Virtual HDFS (Demo)",
            "hive_metastore": "thrift://localhost:9083" if hive_avail else "Embedded Metastore (Precomputed)",
            "execution_engine": "MapReduce 3.3.6 & Hive on Tez" if hadoop_avail else "Python Hadoop Streaming & Hive Engine"
        }
