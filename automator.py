from connectors.benchmark import OLTPAutomator
from connectors.database import PGConn
import os
import time

p = PGConn(suppress_logging=True)
a = OLTPAutomator(suppress_logging=True)
#reset to start from clean slate
p.reset()

#========
#reinits are fast now (sub-10 seconds)
start_time = time.time()
p.reinit_database()
print("Reinit time:", time.time() - start_time)
#========

param_dict = {
    "effective_cache_size": ['"4 GB"', '"8 GB"', '"16 GB"'],
    "work_mem": ['"64 kB"', '"128 kB"', '"256 kB"', '"512 kB"', '"1 MB"', '"2 MB"', '"4 MB"', '"8 MB"', '"16 MB"', '"1 GB"', '"2 GB"', '"4 GB"', '"8 GB"', '"16 GB"'],
    "maintenance_work_mem": ['"1 MB"', '"2 MB"', '"4 MB"', '"8 MB"', '"16 MB"'],
    "effective_io_concurrency": ['"1"', '"10"', '"100"', '"500"', '"1000"'],
    "default_statistics_target": ['"1"', '"10"', '"100"', '"500"', '"1000"', '"5000"', '"10000"'],
    "random_page_cost": ['"1.0"', '"2.0"', '"3.0"', '"4.0"'],
    "autovacuum_scale_factor": ['"0"', '"0.5"', '"1"'],
    "autovacuum_vacuum_threshold": ['"0"', '"1"', '"10"', '"100"', '"500"', '"1000"', '"5000"', '"10000"'],
    "vacuum_cost_limit": ['"0 ms"', '"1 ms"', '"10 ms"', '"100 ms"', '"500 ms"', '"1000 ms"'],
    "vacuum_cost_delay": ['"0 ms"', '"1 ms"', '"10 ms"', '"100 ms"', '"500 ms"', '"1000 ms"']
}

for param, metrics in param_dict.items():
    start_time = time.time()
    for m in metrics:
        p.param_set(param, m)

        a.run_data()
        print(a.get_throughput())
    # restart after every set of param has fully iterated through its list of metrics
    # reinit after every param is done going through its metrics
    p.restart()
    p.reinit_database()
    print("Reinit time:", time.time() - start_time)

print("Benchmark time:", time.time() - start_time)

p.reset()
