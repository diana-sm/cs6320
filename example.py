from connectors.benchmark import OLTPAutomator
from connectors.database import PGConn
import os
import time

#EXAMPLE FILE FOR HOW TO USE DATABASE AND BENCHMARK CONNECTORS

p = PGConn(suppress_logging=False)
a = OLTPAutomator(suppress_logging=False)
#reset to start from clean slate
p.reset()

#========
#reinits are fast now
start_time = time.time()
p.reinit_database()
print("Reinit time:", time.time() - start_time)
#========

start_time = time.time()
#NOTE: for some reason kilobytes needs a lowercase "k"-- be careful about this one
for i in ['"128 kB"', '"256 kB"', '"512 kB"', '"1 GB"', '"2 GB"', '"4 GB"', '"8 GB"']:
    #TODO: decide on better intervals (I just went with powers of two)

    
    p.param_set("shared_buffers", i)
    p.restart()

    #can use this line to verify that params were changed successfully
    #os.system("sudo -u postgres psql -c 'SHOW effective_io_concurrency'")

    a.run_data()
    print(a.get_throughput())
print("Benchmark time:", time.time() - start_time)
# reset after done, just in case
p.reset()

