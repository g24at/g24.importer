g24.importer
============

Content importer for g24.

MYSQL
-----

$ mysqldump -u root -p[root_password] --default-character-set=utf8 [database_name] > dumpfilename.sql
$ mysql -uroot -p
mysql> CREATE DATABASE g24_726 DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
mysql> GRANT ALL PRIVILEGES ON g24_726.* TO 'g24_726'@'localhost' IDENTIFIED BY 'g24_726';

$ mysql g24_726 -u g24_726 -p --default-character-set=utf8 < dumpfilename.sql
