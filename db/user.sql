$ mysql -u root -p P9 < P9_2014-02-20.sql 

mysql> CREATE USER 'admin'@'%' IDENTIFIED BY 'password';
mysql> GRANT ALL PRIVILEGES ON *.* TO 'admin'@'%';
mysql> FLUSH PRIVILEGES ;

mysql> show databases;



CREATE DATABASE
IF NOT EXISTS `leading_crm` DEFAULT CHARSET 'utf8mb4' COLLATE 'utf8mb4_unicode_ci';
GRANT ALL ON `leading_crm`.* TO 'admin'@'%';

FLUSH PRIVILEGES ;

