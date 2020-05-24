import mysql.connector
import mysql.connector.errors
from exceptions import InvalidPersonIndexException, InvalidCompanyNameException


class PeopleAPI:
    @classmethod
    def get_employees_of_company(cls, dbconn, company_name):
        try:
            cursor = dbconn.cursor()
            ind = cls.get_company_index(dbconn, company_name)
            sql = "SELECT p.name FROM companies c INNER JOIN people p ON c.company_index=p.company_id"+\
                " WHERE c.company_index={ind}".format(ind=ind)
            cursor.execute(sql)
            return [x[0] for x in cursor.fetchall()]
        finally:
            cursor.close()

    @staticmethod
    def get_company_index(dbconn, company_name):
        cursor = dbconn.cursor()
        sql = "SELECT company_index FROM companies WHERE name=%s"
        try:
            cursor.execute(sql, [company_name])
            row = cursor.fetchall()
            if len(row) == 0:
                raise InvalidCompanyNameException('The company name provided was invalid')
            return row[0][0]
        finally:
            #no context manager for the cursor.
            cursor.close()
    
    @staticmethod
    def get_mutual_friends_with_brown_eyes_alive(paranuaradb, person1_index, person2_index):
        cursor = paranuaradb.cursor()
        sql = "SELECT p.name, p.age, p.email FROM people p where p.person_index in "+\
        "(select person_ind from friends where friend_ind={person1}) ".format(person1=person1_index)+\
        "AND p.person_index in "+\
        "(select person_ind from friends where friend_ind={person2}) ".format(person2=person2_index) +\
        "AND has_died=false AND eye_color='brown'"

        try:
            cursor.execute(sql)
            
            return [x[0] for x in cursor.fetchall()]
        finally:
            #no context manager for the cursor.
            cursor.close()
    @staticmethod
    def get_fruits_and_veggies(paranuaradb, person_id):
        cursor = paranuaradb.cursor()
        sql = "SELECT p.name, p.age, food.food_name, " +\
            "CASE WHEN fruit.fruit_name IS NOT NULL THEN 'YES' WHEN food.food_name IS NOT NULL THEN 'NO' ELSE null END AS is_fruit " +\
            "FROM people p LEFT JOIN favourite_foods food ON p.person_index = food.person_ind "+\
            "LEFT JOIN all_fruits fruit ON food.food_name = fruit.fruit_name " +\
            "WHERE p.person_index = {person_id}".format(person_id=person_id)
        
        try:
            cursor.execute(sql)
            all_rows = cursor.fetchall()
            if len(all_rows) == 0:
                raise InvalidPersonIndexException()
            
            return { 'name':all_rows[0][0],
                'fruits': [x[2] for x in all_rows if x[3] == 'YES' ],
                'vegetables': [x[2] for x in all_rows if x[3] == 'NO' ]
                }
        finally:
            #no context manager for the cursor.
            cursor.close()


