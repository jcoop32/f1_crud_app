import mysql.connector
import helper_functions
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()

exit_program = False

# connection to db
# may need to change params to connect to your local db
db_connection = mysql.connector.connect(host="localhost", user="root", password=os.getenv("pass"), database="f1_db")

# cursor to execute sql queries
cursor = db_connection.cursor()

# menu interface for user
def menu():
    userChoice = input('Command: (c)reate, (r)ead, (u)pdate, (d)elete, (a)dvanced queries, e(x)it: ')
    if (userChoice == 'c'):
        create_data()
    elif (userChoice == 'r'):
        read_data()
    elif (userChoice == 'u'):
        update_data()
    elif (userChoice == 'd'):
        delete_data()
    elif (userChoice == 'a'):
        advanced_queries()
    elif (userChoice == 'x'):
        print('User quit')
        db_connection.close()
        global exit_program
        exit_program = True
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

#completed
def create_data():
    table_name = helper_functions.user_table_selection()
    helper_functions.read_table_param(table_name)
    data = helper_functions.user_create_loop(table_name)
    try:
        insert_statement = f"""INSERT INTO {table_name}
        ({helper_functions.get_table_structure_for_insert(table_name)})
        VALUES ({helper_functions.get_table_s_count(table_name)});"""
        cursor.execute(insert_statement, data)
        db_connection.commit()
        print("Record succesfully added")
    except Exception as err:
        print(err)

# this is complete
def read_data():
    table_name = helper_functions.user_table_selection()
    read_table_statement = helper_functions.read_table_statement(table_name)
    cursor.execute(read_table_statement)
    table_data = cursor.fetchall()
    print(f'{table_name} table ({helper_functions.get_table_record_count(table_name)} items):')
    print(f'({helper_functions.get_table_structure(table_name)})')
    for i in table_data:
        print(i)
    print("*"*70)

# completed
def update_data():
    table_name = helper_functions.user_table_selection()
    print("Here is the table you have chosen to update:")
    helper_functions.read_table_param(table_name)
    record_id = int(input(f"Which record ({table_name}_id) would you like to change?: "))
    helper_functions.get_table_structure(table_name)
    new_data = helper_functions.user_update_loop(table_name, record_id)
    # print(f"UPDATE {table_name} SET {new_data} WHERE {table_name}_id={record_id}")
    try:
        update_data = helper_functions.update_table_structure_selector(table_name, record_id)
        cursor.execute(update_data, new_data)
        db_connection.commit()
        print(f"Succesfully Updated record id {record_id}")
    except Exception as err:
        print(err)

# this is complete
def delete_data():
    table_name = helper_functions.user_table_selection()
    helper_functions.read_table_param(table_name)
    table_record_count = helper_functions.get_table_record_count(table_name)
    user_selection = int(input("Select ID from record to be deleted (first digit in row): "))
    try:
        delete_statement = f'DELETE FROM {table_name} WHERE {table_name}_id={user_selection}'
        if (user_selection > table_record_count or user_selection < 1):
            print("Record does not exist")
        cursor.execute(delete_statement)
        db_connection.commit()
        print("Record Deleted Successfully")
    except Exception as err:
        print(err)


def advanced_queries():
    print("1: Foreign Drivers query")
    print("2: Driver Team and Nationality query")
    print("3: Calculate the percent rank of the drivers by points")
    print("4: Find the quartile of the circuits based on lengths")
    user_input = int(input("Which query would you like to perform?: "))
    if (user_input == 1):
        return helper_functions.foreignDrivers()
    elif (user_input == 2):
        return helper_functions.driverTeamAndNationality()
    elif (user_input == 3):
        return helper_functions.list_driver_percent_ranks()
    elif (user_input == 4):
        return helper_functions.list_circuit_quartiles()
    else:
        print("Input out of range")


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

# loop for menu
while (exit_program == False):
    menu()
