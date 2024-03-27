import mysql.connector
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



def get_table_structure(table_name):
    # use decribe statement to retrieve structure
    describe_table = f'DESCRIBE f1_db.{table_name}'
    cursor.execute(describe_table)
    structureFormat = cursor.fetchall()
    print(f'Structure for {table_name} table:')
    for i in structureFormat:
        print(f'column name: {i[0]} ({i[1]})')


def read_data(table_name):
    read_table = f'SELECT * FROM {table_name}'
    cursor.execute(read_table)
    table_data = cursor.fetchall()
    print(f'{table_name} table:')
    for i in table_data:
        print(i)
    print("*"*70)


# get_table_structure("driver")


# read_data("driver")
# read_data("team")
# read_data("race")
db_connection.close()
