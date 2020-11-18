CREATE DATABASE IF NOT EXISTS ranger;
CREATE USER 'rangerdba'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON *.* TO 'rangerdba'@'localhost' WITH GRANT OPTION;
CREATE USER 'rangerdba'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON *.* TO 'rangerdba'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;

# create database for oozie
CREATE DATABASE IF NOT EXISTS oozie;
CREATE USER 'oozie'@'%' IDENTIFIED BY 'oozie';
GRANT ALL PRIVILEGES ON oozie.* TO 'oozie'@'%' WITH GRANT OPTION;
CREATE USER 'oozie'@'localhost' IDENTIFIED BY 'oozie';
GRANT ALL PRIVILEGES ON oozie.* TO 'oozie'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;

# create database for hive
CREATE DATABASE IF NOT EXISTS hive;
CREATE USER 'hive'@'%' IDENTIFIED BY 'hive';
GRANT ALL PRIVILEGES ON hive.* TO 'hive'@'%' WITH GRANT OPTION;
CREATE USER 'hive'@'localhost' IDENTIFIED BY 'hive';
GRANT ALL PRIVILEGES ON hive.* TO 'hive'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;

#create user for ranger_kms
CREATE USER 'rangerkms'@'localhost' IDENTIFIED BY 'rangerkms';
GRANT ALL PRIVILEGES ON *.* TO 'rangerkms'@'localhost';
CREATE USER 'rangerkms'@'%' IDENTIFIED BY 'rangerkms';
GRANT ALL PRIVILEGES ON *.* TO 'rangerkms'@'%' WITH GRANT OPTION;
GRANT ALL PRIVILEGES ON *.* TO 'rangerkms'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;
