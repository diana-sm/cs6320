import os

class PGConn():
    def __init__(self, suppress_logging = False):
        self.suppress_logging = suppress_logging

    def run_command(self, command):
        os.system(
            "{} {}".format(
                command,
                ("> /dev/null 2>&1" if self.suppress_logging else "")
            )
        )

    def param_set(self, name, value):
        query = "'ALTER SYSTEM SET {} = {};'".format(name, value)
        self.run_command("sudo -u postgres psql -c " + query)
        self.run_command("sudo -u postgres psql -c 'SELECT pg_reload_conf();'")
    
    def show_value(self, name):
       self.run_command("sudo -u postgres psql -c 'show {};'".format(name))

    def restart(self, drop_caches = False):
        self.run_command("sudo su - root -c 'systemctl stop postgresql'")
        if drop_caches:
            self.run_command("sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'")
        self.run_command("sudo su - root -c 'systemctl start postgresql'")

    def reset(self):
        self.run_command("sudo -u postgres psql -c 'ALTER SYSTEM RESET ALL;'")
        #self.run_command("sudo -u postgres psql -c 'SELECT pg_reload_conf();'")
        self.restart() #changed to hard restart becuse some system params need it to be reloaded
    
    def reinit_database(self):
        self.run_command("sudo -u postgres psql -c 'DROP DATABASE tpcc;'")
        self.run_command("sudo -u postgres psql -c 'CREATE DATABASE tpcc WITH TEMPLATE tpcctemplate;'")

class MySQLConn():

    def __init__(self, suppress_logging = False):
        self.suppress_logging = suppress_logging


    def param_set(self, name, value, scope = "PERSIST"):
        #persist is strongest scope level (both changes runtime value and writes to file), but optionally can use a weaker one (not sure why we would need to just yet though)
        query = "'SET {} {} = {};'".format(scope, name, value)
        self.run_command("sudo mysql -u root -e " + query)
        # mysql system variables don't need to be manually reloaded so no extra call here

    def restart(self, drop_caches = False):
        
        if drop_caches:
            self.run_command("sudo service mysql restart")
        self.run_command("sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'")
    
    def reset(self):
        self.run_command("sudo mysql -u root -e 'RESET PERSIST;'")
        self.restart()

        

    def reinit_database(self):
        self.run_command("sudo mysql -u root -e 'DROP DATABASE tpcc;'")
        self.run_command("sudo mysql -u root -e 'CREATE DATABASE tpcc;'")
        self.run_command("sudo mysqldump -u root tpcctemplate | sudo mysql -u root tpcc'")

#============
#==EXAMPLES==
#============
if __name__ == "__main__":
# Postgres
    p = PGConn()
    p.param_set("commit_delay", 400)
    p.reset()

#can be verified with something like sudo -u postgres psql -c 'SHOW commit_delay';

#Mysql
    m = MySQLConn()
    m.param_set("max_connections", 23)
    m.reset()

#sudo mysql -u root -e'select @@global.max_connections';

    pass
