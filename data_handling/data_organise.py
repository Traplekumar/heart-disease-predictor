import sys
import os
import shutil
import logging

# sys.path.append('logger')
# import logger_config
from logger import logger_config

class DataframeOrganise:
    def __init__(self):
        self.badDataPath = "BadRawData"
        self.goodDataPath = "GoodRawData"
        self.rawDataPath = "RawData"

    def moveBadData(self, file):
        logging.info("Moving bad files to Bad Raw Data Directory")
        try:
            oldFilePath = os.path.join(self.rawDataPath, file)
            newFilePath = os.path.join(self.badDataPath, file)
            shutil.copy(oldFilePath, newFilePath)
            # os.remove(oldFilePath)

        except Exception as e:
            logging.error("Error while bad raw data to BadRawData folder\n"  + str(e))
            raise e
    
    def moveGoodData(self, file):
        logging.info("Moving good files to Good Raw Data Directory")
        try:
            oldFilePath = os.path.join(self.rawDataPath, file)
            newFilePath = os.path.join(self.goodDataPath, file)
            shutil.copy(oldFilePath, newFilePath)
            # os.remove(oldFilePath)
        
        except Exception as e:
            logging.error("Error while moving good raw data ot GoodRawData folder\n"  + str(e))
            raise e

if __name__ == '__main__':
    # pass
    x = DataframeOrganise()
    x.moveGoodData("heart_2020_cleaned.csv")