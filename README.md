# Database Systems Project

Uses reinforcement learning to determine the optimal configuration of Postgres parameters with respect to the TPCC and TPCH benchmarks.
Parameters configured include:
* effective_cache_size
* default_statistics_target
* random_page_cost
* shared_buffers
* work_mem
* maintenance_work_mem 
* autovacuum_vacuum_scale_factor
* autovacuum_vacuum_threshold
* fsync
* synchronous_commit

## Main Components
* Configs: XML configuration files for TPCC and TPCH benchmarks
* Connectors: API for training script to connect to the database and benchmarks
* Envs: RL environments
* Setup Scripts: scripts for loading TPCC and TPCH data into the database
* parameter.py: classes representing Postgres configuration parameters
* train.py: script for running the RL training and generating predictions using the trained agent
* automator.py: manually tests benchmark performance for different parameter configurations
