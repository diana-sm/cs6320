import sys, os

class Automator:
    def __init__(self):
        if os.geteuid() != 0:
            raise Exception("This script must be run with sudo permissions")
        #ASSUME REPO IS ON SAME LEVEL AS OLTPBENCH FOLDER
        os.system("sudo -u cd ..")
        os.system("sudo -u cd oltpbench/")

    def run_data(self, should_load = True):
        if should_load:
            os.system("sudo -u ./oltpbenchmark -b tpcc -c config/tpcc_config_postgres.xml --create=true --load=" + str(should_load))
        os.system("sudo -u ./oltpbenchmark -b tpcc -c config/tpcc_config_postgres.xml --create=true --load=" + str(should_load) + " --execute=true -s 5 -o outputfile")


    def get_throughput():
        #CHANGE PATH BASED ON WHERE YOU WANT TO USE IT
        #TODO AUTOMATE THIS
        script_dir = os.path.dirname("/results")
        file_path = os.path.join(script_dir, 'outputfile.6.res')
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

a = Automator()
a.run_data(False)
a.get_throughput()
