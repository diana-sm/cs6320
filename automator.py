from connectors.benchmark import OLTPAutomator
from connectors.database import PGConn
import os
import time

p = PGConn(suppress_logging=True)
a = OLTPAutomator(suppress_logging=True)
#reset to start from clean slate
p.reset()

#========
#should reinit periodically, but not every run (this can take several minutes to do depending on scale factor, which we will want to set reasonably high-- should probably wait for every 20th+ run or something)
#because this example script just does 2 runs, I put it outside the loop and leave it commented most of the time-- with more iterations, it should be factored into the loop somehow
start_time = time.time()
a.reinit_database()
print("Reinit time:", time.time() - start_time)
#========

params = dict()

params = {"effective_cache_size", "work_mem", "maintenance_work_mem",
"effective_io_concurrency", "default_statistics_target", "random_page_cost",
"autovacuum_scale_factor", "autovacuum_vacuum_threshold", "vacuum_cost_limit",
"vacuum_cost_delay"}

for i in params:
  


start_time = time.time()

for p in param_lst:
  for i in ['"128 kB"', '"256 kB"', '"512 kB"', '"1 GB"', '"2 GB"', '"4 GB"', '"8 GB"']:
      #TODO: decide on better intervals (I just went with powers of two)

      
      p.param_set(p, i)
      p.restart()

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