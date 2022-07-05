import pandas as pd
import sqlite3
import os
import csv
import logging
import sys

# sys.path.append('logger')
# import logger_config
from logger import logger_config

class DbOperation:
    def __init__(self, dataBaseName, tableName):
        self.sqlDirectory = "SQLData"
        self.goodDataPath = "GoodRawData"
        self.CSVName = "TrainingInput/InputFile.csv"
        self.dbName = dataBaseName
        self.tableName = tableName

    def dbConnection(self):
        """
        Establish a connection with database
        Input : Name of the database
        Output : connection to database (conn)
        """
        logging.info("Establishing SQLite3 database connection")
        try:
            sqlFilePath = os.path.join(self.sqlDirectory, self.dbName)
            conn = sqlite3.connect(sqlFilePath)
            logging.info("Successfully opened data base: " + str(self.dbName))
            return conn
        
        except Exception as e:
            logging.error("Error while establishing connection with database.\n" + str(e))
            raise e
    
    def createDbTable(self, columnNamesTypes):
        """
        Create table in given database
        Input : Name of database, Column names and type
        """
        conn = self.dbConnection()
        cursor = conn.cursor()
        try:
            cursor.execute(f"SELECT COUNT(name) FROM sqlite_master WHERE type = 'table' AND name = '{self.tableName}'")
            if cursor.fetchone()[0] == 1: # checks if the database is filled
                conn.close()
                logging.info(f"Table '{self.tableName}' already present.")
                logging.info("Database closed Successfully: " + str(self.dbName))
                
            else:
                for key in columnNamesTypes.keys():
                    type = columnNamesTypes[key]
                    if type == 'object':
                        type = 'TEXT'
                    elif type == 'float64':
                        type = 'FLOAT'
                    try:
                        cursor.execute(f"ALTER TABLE {self.tableName} ADD COLUMN {key} {type}")
                    except:
                        cursor.execute(f"CREATE TABLE {self.tableName} ({key} {type})")

                conn.close()
                logging.info("Successfully created Table: " + str(self.tableName))
                logging.info("Database closed Successfully: " + str(self.dbName))
        
        except Exception as e:
            conn.close()
            logging.error("Error while creating Table in database.\n" + str(e))
            logging.info("Database closed Successfully: " + str(self.dbName))
            raise e
    
    def insertDataIntoTable(self):
        """
        Insert data into the given database
        Input : Database name
        """
        conn = self.dbConnection()
        cursor = conn.cursor()
        try:
            logging.info("Adding data in Database Table")
            for file in os.listdir(self.goodDataPath):
                filePath = os.path.join(self.goodDataPath, file)
                df = pd.read_csv(filePath)
                for i in range(df.shape[0]):
                    row = tuple(data for data in df.iloc[i])
                    if i%10000 == 0:
                        print(i, row)
                    cursor.execute(f"INSERT INTO {self.tableName} VALUES {row}")
                
                conn.commit()
                logging.info(f"{file} added successfully in database table")
            
            conn.close()
            logging.info(f"Database closed Successfully: " + str(self.dbName))

        except Exception as e:
            conn.close()
            logging.error("Error while adding data in database Table.\n" + str(e))
            logging.info(f"Database closed Successfully: " + str(self.dbName))
        
    def createCsvFromTable(self):
        """
        Exports CSV file from the given Sqlite database
        Input : File Name
        Output : TrainingInput/InputFile.csv file
        """
        conn = self.dbConnection()
        cursor = conn.cursor()
        try:
            db_df = pd.read_sql_query(f"SELECT * FROM {self.tableName}", conn)
            db_df.to_csv(self.CSVName, index=False)
            conn.close()
            logging.info("Successfully exported CSV file from SQLite Database")
            logging.info(f"Database closed Successfully: " + str(self.dbName))
           
        except Exception as e:
            conn.close()
            logging.error("Error while exproting CSV file from SQLite database.\n" + str(e))
            logging.info(f"Database closed Successfully: " + str(self.dbName))
            raise e
            

if __name__ == '__main__':
    import sys
    sys.path.append('data_validation')
    # print("=================================\n",sys.path, "\n=================================")
    import data_validation
    x = data_validation.DataValidation()
    _, columnNamesTypes = x.getValuesFromSchema()
    y = DbOperation('xyz', 'abc')
    y.createDbTable(columnNamesTypes)
    y.insertDataIntoTable()
    y.createCsvFromTable()