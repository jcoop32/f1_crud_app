import mysql.connector
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()


db_connection = mysql.connector.connect(host="localhost", user="root", password=os.getenv("pass"), database="f1_db")

# cursor to execute sql queries
cursor = db_connection.cursor()
# Helper Functions

# shows the different coloumns for table in param
def get_table_structure(table_name):
    # use decribe statement to retrieve structure
    describe_table = f'DESCRIBE f1_db.{table_name}'
    cursor.execute(describe_table)
    structureFormat = cursor.fetchall()
    print(f'Structure for {table_name} table:')
    for i in structureFormat:
        print(f'column name: {i[0]} ({i[1]})')

# used for insert fuctionality
def get_table_structure_for_insert(table_name):
    # use decribe statement to retrieve structure
    describe_table = f'DESCRIBE f1_db.{table_name}'
    cursor.execute(describe_table)
    structureFormat = cursor.fetchall()
    table_column_count = get_table_column_count(table_name)
    end_string = ''
    for i in range(0, table_column_count):
        # return f'{i[0]},'
        if i < table_column_count - 1:
            # print(f'{structureFormat[i][0]}, ')
            end_string += f'{structureFormat[i][0]}, '
        else:
            # print()
            end_string += f'{structureFormat[i][0]}'
    return end_string

# used for insert functionality
def get_table_column_count(table_name):
    column_count = f'SELECT COUNT(*) FROM information_schema.columns WHERE table_name = "{table_name}";'
    cursor.execute(column_count)
    count = cursor.fetchall()
    s_count = count[0][0]
    return s_count


# get s count for the values in the insert statement
def get_table_s_count(table_name):
    column_count = f'SELECT COUNT(*) FROM information_schema.columns WHERE table_name = "{table_name}";'
    cursor.execute(column_count)
    count = cursor.fetchall()
    s_count = count[0][0]
    end_string = ''
    for i in range(0, s_count):
        if i < s_count - 1:
            # print(f'%s, ', end="")
            end_string += f"%s, "
        else:
            # print(f'%s')
            end_string += f"%s"
    return end_string

# show all tables in db
def show_all_tables():
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    total = 0
    tables_list = {}
    # print("Tables Avaliable:")
    for i in tables:
        total += 1
        print(f'{total}: {i[0]}')

# function for users to select a table (used for each CRUD operation)
def user_table_selection():
    show_all_tables()
    user_input = int(input("Enter table to read/modify from: "))
    if (user_input == 1):
        table_name = "circuit"
    elif(user_input == 2):
        table_name = "driver"
    elif(user_input == 3):
        table_name = "race"
    elif(user_input == 4):
        table_name = "result"
    elif(user_input == 5):
        table_name = "season"
    elif(user_input == 6):
        table_name = "driver"
    elif (user_input > 1 or user_input < 6):
        print("table doesnt exist")
    print(f'You chose *{table_name}*')
    return table_name

# get table count to make sure user is in range for CRUD ops
def get_table_record_count(table_name):
    statement = f"SELECT COUNT(*) FROM {table_name}"
    cursor.execute(statement)
    count = cursor.fetchall()
    return (int(count[0][0]))


def read_table_param(table_name):
    read_table = f'SELECT * FROM {table_name}'
    cursor.execute(read_table)
    table_data = cursor.fetchall()
    print(f'{table_name} table:')
    for i in table_data:
        print(i)
    print("*"*70)

# End helper functions

