from connectors.benchmark import OLTPAutomator
from connectors.database import PGConn
import os
import time

#why use python file api when os do trick?
os.system("rm throughput_vs_time1.csv")
os.system("touch throughput_vs_time1.csv")

p = PGConn(suppress_logging=True)
a = OLTPAutomator(suppress_logging=True)
#reset to start from clean slate
p.reset()
p.restart()

#========
#should reinit periodically, but not every run (this can take several minutes to do depending on scale factor, which we will want to set reasonably high-- should probably wait for every 20th+ run or something)
#because this example script just does 2 runs, I put it outside the loop and leave it commented most of the time-- with more iterations, it should be factored into the loop somehow
start_time = time.time()
#a.reinit_database()
print("Reinit time:", time.time() - start_time)
#========

start_time = time.time()
for i in range(8638,10000):
    a.run_data()
    tps = a.get_throughput()
    print(i, tps)
    os.system("echo '{},{}' >> ../throughput_vs_time1.csv".format(i, tps))
print("Experiment time:", time.time() - start_time)
# reset after done, just in case
p.reset()

