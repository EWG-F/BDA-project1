"""
Unit tests for TrendScope MapReduce Job Mappers and Reducers
"""

import unittest
import subprocess
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MR_DIR = os.path.join(BASE_DIR, "mapreduce")

class TestMapReduceJobs(unittest.TestCase):
    def test_job1_keyword_mapper_reducer(self):
        sample_input = "video_id,trending_date,title,channel_title,category_id,publish_time,tags,views,likes,dislikes,comment_count,thumb,c_dis,r_dis,err,desc\nv1,18.01.01,Amazing Python Big Data,Tech,28,2018-01-01T00:00:00Z,\"python\"|\"hadoop\",100,10,1,2,http,False,False,False,desc\n"
        
        mapper = os.path.join(MR_DIR, "job1_keyword_frequency", "mapper.py")
        reducer = os.path.join(MR_DIR, "job1_keyword_frequency", "reducer.py")
        
        cmd = f"echo '{sample_input}' | python3 {mapper} | sort | python3 {reducer}"
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("python", res.stdout)
        self.assertIn("amazing", res.stdout)

    def test_job2_category_mapper_reducer(self):
        sample_input = "video_id,trending_date,title,channel_title,category_id,publish_time,tags,views,likes,dislikes,comment_count,thumb,c_dis,r_dis,err,desc\nv1,18.01.01,Title,Ch,10,2018-01-01T00:00:00Z,tag,1000,100,5,20,http,False,False,False,desc\n"
        
        mapper = os.path.join(MR_DIR, "job2_category_stats", "mapper.py")
        reducer = os.path.join(MR_DIR, "job2_category_stats", "reducer.py")
        
        cmd = f"echo '{sample_input}' | python3 {mapper} | sort | python3 {reducer}"
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("10\t1,1000,100,20,1000.0,100.0,12.0", res.stdout.strip())

    def test_job3_persistence_mapper_reducer(self):
        sample_input = (
            "video_id,trending_date,title,channel_title,category_id,publish_time,tags,views,likes,dislikes,comment_count,thumb,c_dis,r_dis,err,desc\n"
            "v1,18.01.01,Title A,Ch A,10,2018-01-01T00:00:00Z,tag,1000,100,5,20,http,False,False,False,desc\n"
            "v1,18.01.02,Title A,Ch A,10,2018-01-01T00:00:00Z,tag,2000,200,10,40,http,False,False,False,desc\n"
        )
        
        mapper = os.path.join(MR_DIR, "job3_trending_persistence", "mapper.py")
        reducer = os.path.join(MR_DIR, "job3_trending_persistence", "reducer.py")
        
        cmd = f"echo '{sample_input}' | python3 {mapper} | sort | python3 {reducer}"
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("v1\tTitle A\tCh A\t10\t2\t2000\t200", res.stdout.strip())

if __name__ == '__main__':
    unittest.main()
