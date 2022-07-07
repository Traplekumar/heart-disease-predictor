import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import pickle
from data_handling.database_operations import DbOperation
from data_handling.data_organise import DataframeOrganise
from directory_handling.directory_handling import DirHandling
from data_validation.data_validation import DataValidation
from data_preprocessing.data_preprocessing import Preprocessing
from model_training.model_training import ModelTraining
import logging
import sys

# sys.path.append('logger')
from logger import logger_config

class ValidateDatabaseTrain:
    def __init__(self):
        self.rawDataDirectory = "RawData"
        self.modelDir = "TrainedModel"
        self.columnNamesTypes = {}

    def validate(self):
        logging.info("Starting Raw Data validation")
        try:
            moveRawData = DataframeOrganise()
            validateRawData = DataValidation()
            for file in os.listdir(self.rawDataDirectory):
                if (validateRawData.fileNameCheck(file)):
                    numberOfColumns, colNamesTypes = validateRawData.getValuesFromSchema()
                    self.columnNamesTypes = colNamesTypes
                    filePath = os.path.join(self.rawDataDirectory, file)
                    df = pd.read_csv(filePath)
                    if (validateRawData.columnNumberCheck(numberOfColumns, df) and 
                        validateRawData.columnNameTypeCheck(self.columnNamesTypes, df) and 
                        validateRawData.nullValueCheck(df)):
                            moveRawData.moveGoodData(file)
                    else:
                        moveRawData.moveBadData(file)

                else:
                    moveRawData.moveBadData(file)

            logging.info("Successfully Validated the dataset.")
                        
        except Exception as e:
            logging.error("Error while validating dataset.\n" + str(e))
            raise e
    
    def database(self):
        logging.info("Started creating data from Good Raw Data.")
        try:
            sqliteDb = DbOperation('DatasetCleaned', 'GoodTrainData')
            conn = sqliteDb.dbConnection()
            sqliteDb.createDbTable(self.columnNamesTypes)
            sqliteDb.insertDataIntoTable()
            sqliteDb.createCsvFromTable()

        except Exception as e:
            logging.error("Error while adding Good Raw Data to database.\n" + str(e))
            raise e

    def preprocessTrain(self, filePath='TrainingInput/InputFile.csv'):
        logging.info("Started preprocessing of TRAIN data.")
        try:
            df = pd.read_csv(filePath)
            preTrain = Preprocessing(df)
            preTrain.binaryEncode()
            preTrain.ordinalEncode()
            preTrain.oneHotEncode()
            preTrain.removeOutlier()
            xtrain, ytrain= preTrain.getXAndY()
            x_under, y_under = preTrain.underSample(xtrain, ytrain)
            
            logging.info("Successfully completed preprocessing of TRAIN data.")
            return x_under, y_under
        
        except Exception as e:
            logging.error("Error while preprocessing TRAIN data.\n" + str(e))
            raise e
    
    def preprocessTest(self, filePath='RawData/Testing_Data.csv'):
        logging.info("started proprocessing TEST data.")
        try:
            df = pd.read_csv('RawData/Testing_Data.csv')
            preTest = Preprocessing(df)
            preTest.binaryEncode()
            preTest.ordinalEncode()
            preTest.oneHotEncodeTest()
            xtest, ytest = preTest.getXAndY()

            logging.info("Successfully completed preprocessing of TEST data.")
            return xtest, ytest
        
        except Exception as e:
            logging.error("Error while preprocessing TEST dataset.\n" + str(e))
            raise e
            
    def train(self):
        logging.info("Started Training model on cluster")
        try:
            # directory = DirHandling()
            # # delecting necessary directories that hold data of Previous Run.
            # directory.deleteDirectories()
            # # creating new necessary directories
            # directory.createDirectories()
            # # for train dataset:
            # self.validate()
            # self.database()
            
            x_under, y_under = self.preprocessTrain()
            xtest, ytest = self.preprocessTest()
            
            trainModel = ModelTraining(x_under, y_under, xtest, ytest)

            clf_log = trainModel.logisticRegression()
            clf_ran = trainModel.randomForest()
            clf_xgb = trainModel.xgboost()

            classifiers = [clf_log, clf_ran, clf_xgb]
            bestIndex = np.argmax([clf[1] for clf in classifiers])
            bestModel = classifiers[bestIndex][0]

            logging.info(f"Logistic Regression Score: {clf_log[1]}, Random Forest Score: {clf_ran[1]}, XGBoost Score: {clf_xgb[1]}")
            modelName = str(bestModel).split('(')[0] + '.pickle'
            modelPath = os.path.join(self.modelDir, modelName)
            with open(modelPath, 'wb') as file:
                pickle.dump(bestModel, file)
            
            logging.info("Successfully saved: " + str(modelName))

        except Exception as e:
            logging.error("Error while Training models on clusterd data.\n" + str(e))
            raise e
                
if __name__ == '__main__':
    a = ValidateDatabaseTrain()
    a.train()