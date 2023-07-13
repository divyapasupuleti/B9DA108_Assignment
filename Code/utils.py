import json
import mysql.connector

def mysql_connector():
    f = open('config.json')
    data = json.load(f)
    user_name = data['my_sql_cred']['user_name']
    password = data['my_sql_cred']['password']
    database = data['my_sql_cred']['database']
    host = data['my_sql_cred']['host']
    mydb = mysql.connector.connect(
            host=host,
            user=user_name,
            password=password,
            database=database
            )
    mycursor = mydb.cursor()
    return mydb, mycursor




mysql_connector()