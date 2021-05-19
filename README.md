# cs6330

Run `sudo ./setup_[DBMS].sh` to reset state of databases (REQUIRED ONCE PER SERVER-- to group members, you don't need to do this again for postgres, I've already ran it). See example.py for usage examples.

"Template" databases are used to expedite reiniting the tpcc "clean" database (i.e. no tpcc additions or deletions). However, this means that we will have 4 copies of different databases in use at any given time, each ~2GB in size at scale factor 20. Additionally, this server has a disk size of around 8GB, so it is impossible to load all 4 copies in at the same time. As such, you will need to run a setup script, train + evaluate the RL-derivdd parameters, and then DROP the no longer needed databases as shown below.


### Postgres

sudo -u postgres psql -c 'DROP DATABASE tpcc;'

sudo -u postgres psql -c 'DROP DATABASE tpcctemplate;'

### Mysql

sudo mysql -u root -e "DROP DATABASE tpcctemplate;";

sudo mysql -u root -e "DROP DATABASE tpcc;";