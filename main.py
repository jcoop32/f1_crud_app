import mysql.connector
import datetime
# import config.py

exitProgram = False



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


db_connection = mysql.connector.connect(host="localhost", user="root", password="thebigdog32", database="f1_db")

# cursor to execute sql queries
cursor = db_connection.cursor()


# executing sql query
# read_driver_table = "SELECT * FROM driver"
# cursor.execute(read_driver_table)

# commit changes
# db_connection.commit()

# close cursor and the connection
# cursor.close()
# db_connection.close()


# Helper Functions
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

def show_all_tables():
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    total = 0
    tables_list = {}
    # print("Tables Avaliable:")
    for i in tables:
        total += 1
        print(f'{total}: {i[0]}')

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
    else:
        print("table doesnt exist")
    print(f'You chose *{table_name}*')
    return table_name

# End helper functions



def create_data():
    # data = [
    # (23, 'Michael Jordan', 'Australia', datetime.date(1959, 4, 17), 14),
    # (24, 'Patrick Williams', 'Mexico', datetime.date(2002, 10, 9), 2)
    # ]
    table_name = user_table_selection()
    try:
        insert_statement = f'INSERT INTO {table_name} ({get_table_structure_for_insert(table_name)}) VALUES ({get_table_s_count(table_name)});'
        cursor.executemany(insert_statement, data)
        db_connection.commit()
        print("Record succesfully added")
    except Exception as err:
        print(err)

def read_data():
    table_name = user_table_selection()
    read_table = f'SELECT * FROM {table_name}'
    cursor.execute(read_table)
    table_data = cursor.fetchall()
    print(f'{table_name} table:')
    for i in table_data:
        print(i)
    print("*"*70)


def update_data():
    table_name = user_table_selection()
    print(f"UPDATE {table_name} SET ")

def delete_data():
    table_name = user_table_selection()
    print(f'DELETE FROM {table_name} WHERE id=2')





# one_data_insert = (16, 'John Cena', 'United States', datetime.date(2002, 7, 1), 15)


# get_table_structure("driver")
# get_table_structure_for_insert('driver')
# create_data('driver', data=data)

# get_table_column_count("driver")

# read_data("driver")
# read_data("team")
# read_data("race")

# show_all_tables()

while (exitProgram == False):
    menu()
