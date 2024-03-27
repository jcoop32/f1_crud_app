import mysql.connector
import datetime
# import config.py

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
# End helper functions



def create_data(table_name, data):
    try:
        insert_statement = f'INSERT INTO {table_name} ({get_table_structure_for_insert(table_name)}) VALUES ({get_table_s_count(table_name)});'
        cursor.executemany(insert_statement, data)
        db_connection.commit()
        print("Record succesfully added")
    except Exception as err:
        print(err)

def read_data(table_name):
    read_table = f'SELECT * FROM {table_name}'
    cursor.execute(read_table)
    table_data = cursor.fetchall()
    print(f'{table_name} table:')
    for i in table_data:
        print(i)
    print("*"*70)


data = [
    (21, 'Ja Morant', 'Germany', datetime.date(2000, 3, 15), 1),
    (22, 'Miles Morales', 'France', datetime.date(1999, 5, 15), 7)
    ]


# dataa = (16, 'John Cena', 'United States', datetime.date(2002, 7, 1), 15)
# dataTest = [{
#     'driver_id': 16,
#     "name": "John Cena",
#     "nationality": "United States",
#     "birth_date": datetime.date(2002, 7, 1),
#     "team_id": 15
# }]

# get_table_structure("driver")
# get_table_structure_for_insert('driver')
# create_data('driver', data=data)

# get_table_column_count("driver")

read_data("driver")
# read_data("team")
# read_data("race")
db_connection.close()
