echo "====dropping old dbs===="

sudo -u postgres psql -c 'DROP DATABASE tpch;'
sudo -u postgres psql -c 'DROP DATABASE tpchtemplate;'

echo "====creating new dbs===="

sudo -u postgres psql -c 'CREATE DATABASE tpchtemplate;'

cd ../oltpbench

echo "====loading template dbs===="

sudo ./oltpbenchmark -b tpcc -c ../configs/tpch_config_postgres_template.xml --create=true --load=true

echo "====copying templates to live===="

sudo -u postgres psql -c 'CREATE DATABASE tpch WITH TEMPLATE tpchtemplate;'

cd ../setup_scripts
