-- script to prepare a MYSQL server for the project 

-- create the database
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;

-- create the user to administer the database
CREATE USER IF  NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';

-- give the user full control over the database
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost'; 

-- give select privileges on the database performance_schema
GRANT SELECT on performance_schema.* TO 'hbnb_dev'@'localhost';

