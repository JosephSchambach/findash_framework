import pymysql
import pandas as pd

class SQLContext:
    def __init__(self, host, port, user, password, database, logger):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.logger = logger
        self._connect()

    def _connect(self):
        try:
            self.connection = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.logger.log("SQL connection established.")
        except Exception as e:
            self.logger.log(f"Failed to connect to SQL: {e}")
            raise e

    def execute(self, query, data=None):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, data)
                self.connection.commit()
                return cursor.fetchall()
        except Exception as e:
            self.logger.log(f"Error executing query: {e}")
            raise e
        
    def pandas_write(self, df, table_name):
        try:
            df.to_sql(table_name, self.connection, if_exists='append', index=False)
            self.logger.log(f"Data written to {table_name} successfully.")
        except Exception as e:
            self.logger.log(f"Error writing to SQL: {e}")
            raise e
        
    def pandas_select(self, query, data=None):
        try:
            df = pd.read_sql(query, self.connection, params=data)
            return df
        except Exception as e:
            self.logger.log(f"Error reading SQL: {e}")
            raise e
