import os
import logging
import sys
import shutil

# sys.path.append('logger')
# import logger_config
from logger import logger_config

class DirHandling:
    def __init__(self):
        self.basePath = os.getcwd()
        self.goodDataPath = os.path.join(self.basePath, 'GoodRawData')
        self.badDataPath = os.path.join(self.basePath, 'BadRawData')
        self.SQLDataPath = os.path.join(self.basePath, 'SQLData')
        self.trainingInputPath = os.path.join(self.basePath, 'TrainingInput')
        self.modelPath = os.path.join(self.basePath, 'TrainedModel')
        self.resources = os.path.join(self.basePath, 'Resources')
        
    def createDirectories(self):
        logging.info("Creating necessary directories.")
        try:
            os.makedirs(self.goodDataPath)
            logging.info("Successfully created GoodRawData folder.")
            os.makedirs(self.badDataPath)
            logging.info("Successfully created BadRawData folder.")
            os.makedirs(self.SQLDataPath)
            logging.info("Successfully created SQLData folder.")
            os.makedirs(self.trainingInputPath)
            logging.info("Successfully created TrainingInput folder.")
            os.makedirs(self.resources)
            logging.info("Successfully created Resources folder.")
            os.makedirs(self.modelPath)
            logging.info("Successfully created Trained Model folder")
            
        except Exception as e:
            logging.error("Error while creating necessary directories.\n" + str(e))
            raise e

    def deleteDirectories(self):
        logging.info("Deleting directories.")
        try:
            shutil.rmtree(self.goodDataPath)
            logging.info("Successfully deleted GoodRawData folder.")
            shutil.rmtree(self.badDataPath)
            logging.info("Successfully deleted BadRawData folder.")
            shutil.rmtree(self.SQLDataPath)
            logging.info("Successfully deleted SQLData folder.")
            shutil.rmtree(self.trainingInputPath)
            logging.info("Successfully deleted TrainingInput folder.")
            shutil.rmtree(self.resources)
            logging.info("Successfully deleted Resources folder.")
            shutil.rmtree(self.modelPath)
            logging.info("Successfully deleted Trained Model folder.")
        
        except Exception as e:
            logging.error("Error while deleting directories.\n" + str(e))
            raise e



if __name__  == '__main__':
    x = DirHandling()
    x.createDirectories()
    # x.deleteDirectories()