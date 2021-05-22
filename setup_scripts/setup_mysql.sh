echo "====dropping old dbs===="

sudo mysql -u root -e "DROP DATABASE tpcctemplate;";
sudo mysql -u root -e "DROP DATABASE tpcc;";

echo "====creating new dbs===="

sudo mysql -u root -e "CREATE DATABASE tpcctemplate;";
sudo mysql -u root -e "CREATE DATABASE tpcc;";

cd ../oltpbench

echo "====loading template dbs===="

sudo ./oltpbenchmark -b tpcc -c ../configs/tpcc_config_mysql_template.xml --create=true --load=true

echo "====copying templates to live===="

sudo mysqldump -u root tpcctemplate | sudo mysql -u root tpcc

cd ../setup_scripts
