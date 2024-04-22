import mysql.connector
import os
import datetime
from dotenv import load_dotenv, dotenv_values

load_dotenv()


db_connection = mysql.connector.connect(host="localhost", user="root", password=os.getenv("pass"), database="f1_db")

# cursor to execute sql queries
cursor = db_connection.cursor()
# Helper Functions

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
        table_name = "team"
    elif (user_input > 1 or user_input < 6):
        print("table doesnt exist")
    print(f'You chose *{table_name}*')
    return table_name

# shows the different coloumns for table in param
def get_table_structure(table_name):
    # use decribe statement to retrieve structure
    describe_table = f'DESCRIBE f1_db.{table_name}'
    cursor.execute(describe_table)
    structureFormat = cursor.fetchall()
    end_array = []
    print(f'Structure for {table_name} table:')
    for i in structureFormat:
        # print(f'column name: {i[0]} ({i[1]})')
        end_array.append(f'{i[0]} ({i[1]}): ')
    return end_array

def get_column_names(table_name):
    # use decribe statement to retrieve structure
    describe_table = f'DESCRIBE f1_db.{table_name}'
    cursor.execute(describe_table)
    structureFormat = cursor.fetchall()
    end_array = []
    for i in structureFormat:
        # print(f'column name: {i[0]} ({i[1]})')
        end_array.append(i[0])
    return end_array


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
    print(end_string)

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
    # tables_list = {}
    # print("Tables Avaliable:")
    for i in tables:
        total += 1
        print(f'{total}: {i[0]}')


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


def user_create_loop(table_name):
    user_finished_create_arr = []
    for i in get_table_structure(table_name):
        user_create_input = input(f'{i}')
        if (i == 'driver_id (int): ' or i == 'team_id (int): ' or i == 'circuit_id (int): '
            or i == 'race_id (int): ' or i == 'season_id (int): ' or i == 'result_id (int): ' or i == 'year (int): '):
            user_create_input = int(user_create_input)
        if (i == 'birth_date (date): ' or i == 'date (date): '):
            user_create_input = None
        user_finished_create_arr.append(user_create_input)
    # have to change the data type of user input to the data type in
    # changes arr to tuple for mysql insert format
    arr_to_tuple = tuple(user_finished_create_arr)
    return arr_to_tuple


def user_update_loop(table_name, record_id):
    user_finished_create_arr = []
    for i in get_table_structure(table_name):
        user_create_input = input(f'{i}')
        if (i == f'{table_name}_id (int): '):
            user_create_input = record_id
        if (i == 'team_id (int): '):
            user_create_input = int(user_create_input)
        if (i == 'birth_date (date): '):
            user_create_input = None
        user_finished_create_arr.append(user_create_input)
    # have to change the data type of user input to the data type in
    arr_to_tuple = tuple(user_finished_create_arr)
    return arr_to_tuple

# changes update statement for selected table
def update_table_structure_selector(table_name, record_id):
    update_statement = ''
    if (table_name == "circuit"):
        update_statement = f'UPDATE {table_name} SET {table_name}_id=%s, name=%s, location=%s, length=%s WHERE {table_name}_id={record_id}'
    elif(table_name == "driver"):
        update_statement = f'UPDATE {table_name} SET {table_name}_id=%s, name=%s, nationality=%s, birth_date=%s, team_id=%s WHERE {table_name}_id={record_id}'
    elif(table_name == "race"):
        update_statement = f'UPDATE {table_name} SET {table_name}_id=%s, date=%s, location=%s, circuit_id=%s WHERE {table_name}_id={record_id}'
    elif(table_name == "result"):
        update_statement = f'UPDATE {table_name} SET {table_name}_id=%s, driver_id=%s, race_id=%s, season_id=%s, position=%s, points=%s WHERE {table_name}_id={record_id}'
    elif(table_name == "season"):
        update_statement = f'UPDATE {table_name} SET {table_name}_id=%s, year=%s WHERE {table_name}_id={record_id}'
    elif(table_name == "team"):
        update_statement = f'UPDATE {table_name} SET {table_name}_id=%s, name=%s, country=%s, constructor=%s WHERE {table_name}_id={record_id}'

    return update_statement


# get_column_names("driver")

# returns simple preset select statements
def preset_read_options(table_name):
    column_names = get_column_names(table_name)
    preset_statements = []
    selecting = True
    for i in range(get_table_column_count(table_name)):
        for j in column_names:
            statement =  f'SELECT {j} FROM {table_name}'
            preset_statements.append(statement)
        print(f'[{i+1}]: {preset_statements[i]}')
    while (selecting):
        user_selection = int(input("Which preset select statement would you like to use?: "))
        if (user_selection > get_table_column_count(table_name) or user_selection < 1):
            print("Selection out of range!")
        else:
            selecting = False
            return preset_statements[user_selection-1]

# decides if user wants to use a preset or default select statement
def read_table_statement(table_name):
    default_statement = f'SELECT * FROM {table_name}'
    ask_user_to_use_preset = input("Would you like to use a preset statement? (y/n):")
    if (ask_user_to_use_preset == "y"):
        return preset_read_options(table_name)
    else:
        return default_statement


def read_two_tables(t1, t2):
    read = f'SELECT {t1}_id, name, {t2}_id FROM {t1} UNION SELECT {t2}_id, name, country FROM {t2};'
    cursor.execute(read)
    table_data = cursor.fetchall()
    for i in table_data:
        print(i)

def foreignDrivers():
    query = """
    WITH ForeignDrivers AS (
        SELECT team.team_id, team.name, driver.driver_id
        FROM team
        JOIN driver ON team.team_id = driver.team_id
        WHERE team.country <> driver.nationality
)
    SELECT name AS 'Team Name', COUNT(driver_id) AS 'Foreign Drivers'
    FROM ForeignDrivers
    GROUP BY team_id, name
    ORDER BY 'Foreign Drivers' DESC;
    """
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        if results:
            print(f"{'Team Name':<30} {'Foreign Drivers':<15}")
            print("-" * 45)
            for team_name, count in results:
                print(f"{team_name:<30} {count:<15}")
        else:
            print("No data found on teams with foreign drivers.")
        print("" * 70)
    except Exception as e:
        print(f"An error occurred: {e}")




def driverTeamAndNationality():
    query = """
    SELECT driver.name AS 'Driver Name', driver.nationality, team.name AS 'Team Name'
    FROM driver
    JOIN team ON driver.team_id = team.team_id
    ORDER BY team.name, driver.name;
    """
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        print("Driver Name | Nationality | Team Name")
        print("-" * 40)
        for driver_name, nationality, team_name in results:
            print(f"{driver_name} | {nationality} | {team_name}")
        print("" * 70)
    except Exception as e:
        print(f"An error occurred: {e}")





# read_two_tables("driver",  "team")


# preset_read_options("circuit")

# End helper functions

