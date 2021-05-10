import sys, os

class OLTPAutomator:
    def __init__(self, suppress_logging = False, benchmark = "tpcc_config_postgres.xml"):
        self.suppress_logging = suppress_logging
        self.benchmark = benchmark
        #ASSUME REPO (AND CALLING SCRIPT) IS ON SAME LEVEL AS OLTPBENCH FOLDER
        os.chdir("./oltpbench")

    def run_command(self, command):
        os.system(
            "{} {}".format(
                command,
                ("> /dev/null 2>&1" if self.suppress_logging else "")
            )
        )

    def run_data(self):
        file_path = os.path.join("./results", 'outputfile.res')
        #I think it makes mroe sense to remove the file before the data run, because that allows us to decouple run_data and get_throughput
        #i.e. if we run run_data twice in a row without doing this, then any following get_throughput calls fail because the file names are messed up
        self.run_command("sudo rm ./results/outputfile*")
        self.run_command("sudo ./oltpbenchmark -b tpcc -c ../configs/{} --execute=true -s 10 -o outputfile".format(self.benchmark)) #-s option should match runtime of benchmark, if we aren't doing fancy sampling window stuff


    def get_throughput(self):
        #CHANGE PATH BASED ON WHERE YOU WANT TO USE IT
        #TODO AUTOMATE THIS
        file_path = os.path.join("./results", 'outputfile.res')
        with open(file_path, "r") as f:
            all_lines = f.readlines()
            res = all_lines[-1].split(",")[1]
            #print(res)
            # while True:
            #     line = f.readline()
            #     if not line:
            #         break
            #     #res = line.strip()
            #     res = line.split(",")
            #     print(res[1])
            f.close()
            return(res)

    # this function BOTH drops the tables AND creates new ones, so it can basically just be used every x times we run the benchmark
    # setting "--clear=true" has some issues-- the db is inferred to have no type so it kind of just crashes...
    # the good news is that the create flag already did this for us, see oltpbench/build/com/oltpbenchmark/benchmarks/tpcc/ddls/tpcc-postgres-ddl.sql

    # NOTE: use this function sparingly, as it does take some time to finish.... We definitely don't want to reinit for every single benchmark run
    def reinit_database(self):
        self.run_command("sudo ./oltpbenchmark -b tpcc -c ../configs/{} --create=true --load=true".format(self.benchmark))

if __name__ == "__main__":
    a = OLTPAutomator()

    a.reinit_database()
    a.run_data()
    a.get_throughput()