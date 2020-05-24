#!/bin/bash
pip install --upgrade pip
pip install flask mysql-connector-python mock pytest

mysql.service start

# Create user and schema
mysql -uroot < create_database.sql

# Populate database tables with resources data
python loadresources.py