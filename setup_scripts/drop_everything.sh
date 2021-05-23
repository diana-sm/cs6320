sudo -u postgres psql -c 'DROP DATABASE tpcc;'
sudo -u postgres psql -c 'DROP DATABASE tpcctemplate;'
sudo -u postgres psql -c 'DROP DATABASE tpch;'
sudo -u postgres psql -c 'DROP DATABASE tpchtemplate;'
sudo mysql -u root -e "DROP DATABASE tpcctemplate;";
sudo mysql -u root -e "DROP DATABASE tpcc;";