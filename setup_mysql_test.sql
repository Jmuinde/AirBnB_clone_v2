-- script to prepare a MYSQL test server for the project 

-- create the database
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- create the user to administer the database
CREATE USER IF  NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';

-- give the user full control over the database
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost'; 

-- give select privileges on the database performance_schema
GRANT SELECT on performance_schema.* TO 'hbnb_test'@'localhost';

