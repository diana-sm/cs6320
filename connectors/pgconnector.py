import os

class PGConn:
    def __init__(self):
        if os.geteuid() != 0:
            raise Exception("This script must be run with sudo permissions")

    def param_set(self, name, value):
        query = "'ALTER SYSTEM SET {} = {};'".format(name, value)
        os.system("sudo -u postgres psql -c " + query)
        os.system("sudo -u postgres psql -c 'SELECT pg_reload_conf();'")

    def restart(self):
        os.system("sudo su - root -c 'systemctl stop postgresql'")
        os.system("sudo su - root -c 'systemctl start postgresql'")