import mysql.connector
from exceptions import InternalServerIssue

class Database:
    @classmethod
    def get_db_conn(cls):
        try:
            paranuaradb = mysql.connector.connect(
            host='localhost',
            user='paranuara',
            passwd='paranuara',
            database='paranuara',
            auth_plugin='mysql_native_password'
            )
        except:
            raise InternalServerIssue('Error connecting to the MySQL db')

        return paranuaradb
