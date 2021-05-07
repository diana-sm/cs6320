import os

class PGConn():

    #note you can actually 
    def param_set(self, name, value):
        query = "'ALTER SYSTEM SET {} = {};'".format(name, value)
        os.system("sudo -u postgres psql -c " + query)
        os.system("sudo -u postgres psql -c 'SELECT pg_reload_conf();'")

    def restart(self):
        os.system("sudo su - root -c 'systemctl stop postgresql'")
        os.system("sudo su - root -c 'systemctl start postgresql'")

    def reset(self):
        os.system("sudo -u postgres psql -c 'ALTER SYSTEM RESET ALL;'")
        os.system("sudo -u postgres psql -c 'SELECT pg_reload_conf();'")

class MySQLConn():

    def param_set(self, name, value):
        pass

    def restart(self):
        pass
    
    def reset(self):
        pass

p = PGConn()
#p.param_set("commit_delay", 400)
p.reset()

#can be verified with something like sudo -u postgres psql -c 'SHOW commit_delay';