import mysql.connector
import datetime
import helper_functions
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()
# import config.py

exitProgram = False

db_connection = mysql.connector.connect(host="localhost", user="root", password=os.getenv("pass"), database="f1_db")

# cursor to execute sql queries
cursor = db_connection.cursor()

def menu():
    userChoice = input('Command: (c)reate, (r)ead, (u)pdate, (d)elete, e(x)it: ')
    if (userChoice == 'c'):
        create_data()
    elif (userChoice == 'r'):
        read_data()
    elif (userChoice == 'u'):
        update_data()
    elif (userChoice == 'd'):
        delete_data()
    elif (userChoice == 'x'):
        print('User quit')
        db_connection.close()
        global exitProgram
        exitProgram = True
    else:
        print('Command not found')

# executing sql query
# read_driver_table = "SELECT * FROM driver"
# cursor.execute(read_driver_table)

# commit changes
# db_connection.commit()

# close cursor and the connection
# cursor.close()
# db_connection.close()

def create_data():
    data = [
    (23, 'Michael Jordan', 'Australia', datetime.date(1959, 4, 17), 14),
    (24, 'Patrick Williams', 'Mexico', datetime.date(2002, 10, 9), 2)
    ]
    table_name = helper_functions.user_table_selection()
    try:
        insert_statement = f"""INSERT INTO {table_name}
        ({helper_functions.get_table_structure_for_insert(table_name)})
        VALUES ({helper_functions.get_table_s_count(table_name)});"""
        cursor.executemany(insert_statement, data)
        db_connection.commit()
        print("Record succesfully added")
    except Exception as err:
        print(err)

def read_data():
    table_name = helper_functions.user_table_selection()
    read_table = f'SELECT * FROM {table_name}'
    cursor.execute(read_table)
    table_data = cursor.fetchall()
    print(f'{table_name} table:')
    for i in table_data:
        print(i)
    print("*"*70)


def update_data():
    table_name = helper_functions.user_table_selection()
    print(f"UPDATE {table_name} SET ")

def delete_data():
    table_name = helper_functions.user_table_selection()
    print(f'DELETE FROM {table_name} WHERE id=2')


# ******** function tests ***********
# one_data_insert = (16, 'John Cena', 'United States', datetime.date(2002, 7, 1), 15)

# get_table_structure("driver")
# get_table_structure_for_insert('driver')

# create_data('driver', data=data)

# get_table_column_count("driver")

# read_data("driver")
# read_data("team")
# read_data("race")

# show_all_tables()
# ********* end function tests ********

while (exitProgram == False):
    menu()
