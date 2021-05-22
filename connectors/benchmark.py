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

        #if the parameter is not sufficient to run the benchmark (i.e. not enough mem), oltpbench will error out and not produce a results file
        #if this is the case, then we assume the worst and say that throughput was infinitely awful.
        if not os.path.isfile(file_path):
            return -10000000.0

        with open(file_path, "r") as f:
            all_lines = f.readlines()
            res = all_lines[-1].split(",")[1]
            f.close()
            print(res)
            return(float(res))

    # this function BOTH drops the tables AND creates new ones, so it can basically just be used every x times we run the benchmark
    # setting "--clear=true" has some issues-- the db is inferred to have no type so it kind of just crashes...
    # the good news is that the create flag already did this for us, see oltpbench/build/com/oltpbenchmark/benchmarks/tpcc/ddls/tpcc-postgres-ddl.sql

    # NOTE: use this function sparingly, as it does take some time to finish.... We definitely don't want to reinit for every single benchmark run


if __name__ == "__main__":
    a = OLTPAutomator()

    #a.reinit_database()
    a.run_data()
    a.get_throughput()
