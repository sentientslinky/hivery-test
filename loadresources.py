# Loads the resource files into the database
import mysql.connector
import json
import requests
from io import StringIO
import csv
from database import Database

all_fruits_list_url = 'https://raw.githubusercontent.com/chachasikes/openfood_list/master/data/working/California-Rare-Fruit-List-Sheet1-csv.csv'

try:
    paranuaradb = Database.get_db_conn()
except Exception as e:
    print("Error connecting to mysql DB at localhost "+str(e))
    exit(1)

cursor = paranuaradb.cursor()

import os
import sys
resources_folder = os.path.join(sys.path[0], 'resources')
try:
    with open(os.path.join(resources_folder, 'companies.json')) as json_file:
        companies_json = json.load(json_file)
        sql = 'INSERT INTO companies (company_index, name) VALUES(%s,%s)'
        companies_list = ([(x['index'], x['company']) for x in companies_json])
        cursor.executemany(sql, companies_list)

        paranuaradb.commit()
except Exception as e:
    print("Data error in companies data set:"+e)


# Turns out mysql not only can't defer constraint checks till the end of transaction
# It doesn't even snapshot correctly requiring multiple transactions.

cursor = paranuaradb.cursor()

try:
    with open(os.path.join(resources_folder, 'people.json')) as json_file:
        people_json = json.load(json_file)
        column_jsonname = [
        ('_id', '_id'),
        ('person_index', 'index'), 
        ('has_died', 'has_died'), 
        ('age','age'), 
        ('eye_color','eyeColor'), 
        ('name','name'), 
        ('gender','gender'), 
        ('company_id', 'company_id'), 
        ('email','email'), 
        ('phone','phone')
        ]

        insert_people_sql = 'INSERT INTO people('+ \
        ','.join([x[0] for x in column_jsonname])+ \
        ') VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        print(insert_people_sql)
        people_list =[
            tuple([person[jsonname] for colname,jsonname in column_jsonname])
            for person in people_json
            ]
        cursor.executemany(insert_people_sql, people_list)
        
        paranuaradb.commit()

        insert_friends_sql = "INSERT INTO friends (person_ind, friend_ind) VALUES(%s, %s)"
        friends_list = [(person['index'], friendo['index']) for person in people_json
        for friendo in person['friends']
            ]
        
        cursor.executemany(insert_friends_sql, friends_list)
        paranuaradb.commit()

        insert_foods_sql = "INSERT INTO favourite_foods (person_ind, food_name) VALUES(%s, %s)"

        food_list = [(person['index'], food) for person in people_json
        for food in person['favouriteFood']
        ]
        cursor.executemany(insert_foods_sql, food_list)
        paranuaradb.commit()

    r = requests.get(all_fruits_list_url)
    csv_reader = csv.reader(StringIO(r.text))
    all_fruits = [(str.lower(row[0]),) for row in csv_reader]
    insert_all_fruits = "INSERT INTO all_fruits (fruit_name) VALUES(%s)"
    cursor.executemany(insert_all_fruits, all_fruits)
    paranuaradb.commit()
except Exception as e:
    print("Data error in companies data set")

