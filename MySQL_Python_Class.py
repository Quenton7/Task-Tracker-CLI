import mysql.connector
import configparser
import os

class MySQLDatabase:
    def __init__(self, config_file):
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Configuration file '{config_file}' not found.")
    
        config = configparser.ConfigParser()
        config.read(config_file)
    
        if 'mysql' not in config:
            raise KeyError("Missing [mysql] section in the configuration file.")
    
        try:
            self.host = config['mysql']['host']
            self.user = config['mysql']['user']
            self.password = config['mysql']['password']
            self.database = config['mysql']['database']
        except KeyError as e:
            raise KeyError(f"Missing key in [mysql] section: {e}")
    
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            # Connect to MySQL server without specifying the database
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            self.cursor = self.connection.cursor()
            print("Connected to MySQL server.")
            # Check if the database exists
            self.cursor.execute(f"SHOW DATABASES LIKE '{self.database}'")
            result = self.cursor.fetchone()
            if not result:
                print(f"Database '{self.database}' does not exist. Creating it...")
                self.cursor.execute(f"CREATE DATABASE {self.database}")
                print(f"Database '{self.database}' created successfully.")
            # Reconnect to the specific database
            self.connection.database = self.database
            print(f"Connected to database '{self.database}'.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")


    def create_table(self, table_name, columns):
        try:
            column_definitions = ', '.join([f"{col} {dtype}" for col, dtype in columns.items()])
            create_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_definitions});"
            self.cursor.execute(create_query)
            print(f"Table {table_name} created successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def insert_data(self, table_name, data):
        try:
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['%s'] * len(data))
            insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            self.cursor.execute(insert_query, tuple(data.values()))
            self.connection.commit()
            print(f"Data inserted into {table_name}.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def view_data(self, table_name):
        try:
            select_query = f"SELECT * FROM {table_name};"
            self.cursor.execute(select_query)
            results = self.cursor.fetchall()
            for row in results:
                print(row)
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def update_data(self, table_name, data, condition):
        try:
            set_clause = ', '.join([f"{col} = %s" for col in data.keys()])
            update_query = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
            self.cursor.execute(update_query, tuple(data.values()))
            self.connection.commit()
            print(f"Data updated in {table_name}.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def delete_data(self, table_name, condition):
        try:
            delete_query = f"DELETE FROM {table_name} WHERE {condition};"
            self.cursor.execute(delete_query)
            self.connection.commit()
            print(f"Data deleted from {table_name}.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def disconnect(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("Disconnected from database.")
        else:
            print("No active connection.")

if __name__ == "__main__":
    """ 1. Initialize the class
        2. Connect to the database
        3. Create a table
        4. Insert data into the table
        5. View data from the table
        6. Update data in the table
        7. View updated data from the table
        8. Delete data from the table
        9. Disconnect from the database
    """

    script_dir = os.path.dirname(__file__)  # Directory of the current script
    config_file_path = os.path.join(script_dir, 'Configuration file/config.ini')

    db = MySQLDatabase(config_file=config_file_path)
    db.connect()
    db.create_table('users', {'id': 'INT AUTO_INCREMENT PRIMARY KEY', 'name': 'VARCHAR(100)', 'age': 'INT'})
    db.insert_data('users', {'name': 'Alice', 'age': 30})
    db.view_data('users')
    db.update_data('users', {'age': 31}, "name = 'Alice'")
    db.view_data('users')
    db.delete_data('users', "name = 'Alice'")
    db.disconnect()
