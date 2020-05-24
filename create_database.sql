DROP DATABASE IF EXISTS paranuara;

CREATE DATABASE paranuara;


CREATE USER IF NOT EXISTS paranuara IDENTIFIED BY 'paranuara';

USE paranuara;
GRANT ALL PRIVILEGES ON paranuara.* TO paranuara;


CREATE TABLE companies(
    company_index INT PRIMARY KEY,
    name VARCHAR(40)
);

CREATE TABLE people(
    _id VARCHAR(40),
    person_index int,
    has_died BOOLEAN,
    age int,
    eye_color VARCHAR(10),
    name VARCHAR(90),
    gender VARCHAR(10),
    company_id int,
    email VARCHAR(100),
    phone VARCHAR(100),

    PRIMARY KEY (person_index),
    FOREIGN KEY (company_id) REFERENCES companies(company_index)
);

CREATE TABLE friends(
    person_ind int,
    friend_ind int,
    PRIMARY KEY (person_ind, friend_ind),
    FOREIGN KEY (person_ind) REFERENCES people(person_index),
    FOREIGN KEY (friend_ind) REFERENCES people(person_index)
);

CREATE TABLE favourite_foods(
    person_ind int,
    food_name VARCHAR(30),
    FOREIGN KEY (person_ind) REFERENCES people(person_index)
);

CREATE TABLE all_fruits(
    fruit_name VARCHAR(190)
);