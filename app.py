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
