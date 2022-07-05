import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import regex as re
import json
import os
import sys
import logging

# sys.path.append('logger')
# import logger_config
from logger import logger_config

class DataValidation:
    def __init__(self):
        self.schemaPath = "Validation_schema.json"
    
    def fileNameCheck(self, fileName):
        """
        Check if the file name is correct or not.
        Input : Name of the file
        Output : True/False
        """
        logging.info("Checking file name")
        regex = 'heart_patient_[0-9]{8}.csv'
        re.compile(regex)
        if(re.search(regex, fileName)):
            return True
        else:
            return False

    def getValuesFromSchema(self):
        """
        Extracting values from the Schema file for data validation.
        Output : lenght of the Date Stamp, Number of columns and ColumnNames
        """
        logging.info("Extracting values from Validation_schema file")
        try:
            with open(self.schemaPath, 'r') as f:
                dic = json.load(f)
                f.close()

            lengthOfDateStamp = dic['LengthOfDateStamp']
            numberOfColumns = dic['NumberOfColumns']
            columnNamesTypes = dic['ColumnNameType']
            logging.info(f"length of dateStamp : {lengthOfDateStamp}, numbe of columns : {numberOfColumns}, \n" 
                            f"column name and type : {columnNamesTypes}")
            return numberOfColumns, columnNamesTypes

        except Exception as e:
            logging.error(e)
            raise e

    def columnNumberCheck(self, numberOfColumns, data):
        """
        Validates the number of column in dataset to be equal to the specified number of column
        Input : numberOfColumns(from Schema file), dataset
        Output : True/False
        """
        logging.info("Checking number of columns in dataset")
        try:
            columnNumbers = len(data.columns)
            if(columnNumbers == numberOfColumns):
                return True
            else:
                return False
        
        except Exception as e:
            logging.error(e)
            raise e

    def columnNameTypeCheck(self, columnNames, data):
        """
        Checks if the name and type of columns in dataset are same as specified in schema file.
        Input : columnNames(from Schema) and dataset
        Output : True/False 
        """
        logging.info("Checking Column name and type")
        try:
            columns = ['HeartDisease', 'BMI', 'Smoking', 'AlcoholDrinking', 'Stroke',
                        'PhysicalHealth', 'MentalHealth', 'DiffWalking', 'Sex', 'AgeCategory',
                        'Race', 'Diabetic', 'PhysicalActivity', 'GenHealth', 'SleepTime',
                        'Asthma', 'KidneyDisease', 'SkinCancer']
            for col in columns:
                if data[col].dtype != columnNames[col]:
                    return False
            return True

        except Exception as e:
            logging.error(e)
            raise e
            
    def nullValueCheck(self, data):
        """
        Checks if the any column in the dataset contains null values.
        Input : Dataset
        Output : True/False
        """
        logging.info("Checking if data contains null value")
        try:
            return data.isnull().sum().sum() == 0
        
        except Exception as e:
            logging.error(e)
            raise e
    
if __name__ == "__main__":
    x = DataValidation()
    print(x.fileNameCheck("heart_patient_02022022.csv"))
    numberOfColumns, columnNamesTypes = x.getValuesFromSchema()
