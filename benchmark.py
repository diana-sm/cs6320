import sys, os

class Automator:
    def __init__(self):
        #seems like good check but geteuid is default to 0 unless you
        #set it with "setiod()" (can figure this out later)
        # if os.geteuid() != 0:
        #     raise Exception("This script must be run with sudo permissions")
        
        #ASSUME REPO IS ON SAME LEVEL AS OLTPBENCH FOLDER
        os.chdir("./oltpbench")

    def run_data(self, should_load = True):
        if should_load:
            os.system("sudo ./oltpbenchmark -b tpcc -c config/tpcc_config_postgres.xml --create=true --load=" + str(should_load))
        print("about to run benchmark")
        os.system("sudo ./oltpbenchmark -b tpcc -c config/tpcc_config_postgres.xml --create=true --load=" + str(should_load) + " --execute=true -s 5 -o outputfile")


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
        os.system(f"sudo rm {file_path}")
a = Automator()
a.run_data(True)
a.get_throughput()
