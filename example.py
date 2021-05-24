from connectors.benchmark import OLTPAutomator
from connectors.database import PGConn
import os
import time
import numpy as np

bench = "tpch"
#EXAMPLE FILE FOR HOW TO USE DATABASE AND BENCHMARK CONNECTORS

p = PGConn(suppress_logging=True)
a = OLTPAutomator(suppress_logging=True, bench = bench, benchmark = bench+"_config_postgres.xml")
#reset to start from clean slate
p.reset()

#========
#reinits are fast now
start_time = time.time()
p.reinit_database(bench=bench)
print("Reinit time:", time.time() - start_time)
#========

throughputs = {}
start_time = time.time()
#NOTE: for some reason kilobytes needs a lowercase "k"-- be careful about this one
#for i in ['"128 kB"', '"256 kB"', '"512 kB"', '"1 GB"', '"2 GB"', '"4 GB"', '"8 GB"']:
for i in ['"8MB"', '"32MB"', '"64MB"', '"128MB"', '"256MB"', '"512MB"', '"1GB"','"2GB"']:
    #TODO: decide on better intervals (I just went with powers of two)

    
    p.param_set("shared_buffers", i)
    p.restart()

    #can use this line to verify that params were changed successfully
    #os.system("sudo -u postgres psql -c 'SHOW effective_io_concurrency'")
    a.run_data()
    if bench == "tpch":
        print(i, a.get_latency())
    else:
        print(i, a.get_throughput())

print("Benchmark time:", time.time() - start_time)
print(throughputs)
# reset after done, just in case
p.reset()
p.restart()
