import sys, os

class OLTPAutomator:
    def __init__(self, benchmark = "tpcc_config_postgres.xml"):
        self.benchmark = benchmark
        #ASSUME REPO IS ON SAME LEVEL AS OLTPBENCH FOLDER
        os.chdir("../oltpbench")

    def run_data(self):
        print("about to run benchmark")
        os.system("sudo ./oltpbenchmark -b tpcc -c ../configs/{} --execute=true -s 5 -o outputfile".format(self.benchmark))


    def get_throughput(self):
        #CHANGE PATH BASED ON WHERE YOU WANT TO USE IT
        #TODO AUTOMATE THIS
        file_path = os.path.join("./results", 'outputfile.res')
        with open(file_path, "r") as f:
            all_lines = f.readlines()
            res = all_lines[-1].split(",")[1]
            print(res)
            # while True:
            #     line = f.readline()
            #     if not line:
            #         break
            #     #res = line.strip()
            #     res = line.split(",")
            #     print(res[1])
            f.close()
            return(res)
        os.system(f"sudo rm {file_path}")

    # this function BOTH drops the tables AND creates new ones, so it can basically just be used every x times we run the benchmark
    # setting "--clear=true" has some issues-- the db is inferred to have no type so it kind of just crashes...
    # the good news is that the create flag already did this for us, see oltpbench/build/com/oltpbenchmark/benchmarks/tpcc/ddls/tpcc-postgres-ddl.sql
    def reinit_database(self):
        os.system("sudo ./oltpbenchmark -b tpcc -c ../configs/{} --create=true --load=true".format(self.benchmark))

a = OLTPAutomator()

a.reinit_database()
a.run_data()
a.get_throughput()