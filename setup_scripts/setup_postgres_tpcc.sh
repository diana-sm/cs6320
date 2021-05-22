echo "====dropping old dbs===="

sudo -u postgres psql -c 'DROP DATABASE tpcctemplate;'
sudo -u postgres psql -c 'DROP DATABASE tpcc;'

echo "====creating new dbs===="

sudo -u postgres psql -c 'CREATE DATABASE tpcctemplate;'

cd ../oltpbench

echo "====loading template dbs===="

sudo ./oltpbenchmark -b tpcc -c ../configs/tpcc_config_postgres_template.xml --create=true --load=true

echo "====copying templates to live===="

sudo -u postgres psql -c 'CREATE DATABASE tpcc WITH TEMPLATE tpcctemplate;'

cd ../setup_scripts
