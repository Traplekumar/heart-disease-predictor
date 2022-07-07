from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import recall_score
import logging
import sys

# sys.path.append('logger')
# import logger_config
from logger import logger_config

class ModelTraining:
    def __init__(self, xtrain, ytrain, xtest, ytest):
        self.xtrain = xtrain
        self.ytrain = ytrain
        self.xtest = xtest
        self.ytest = ytest

    def logisticRegression(self):
        logging.info("Started training Logistic Regression.")
        try:
            model = LogisticRegression(penalty='l2', max_iter=5000)
            model.fit(self.xtrain, self.ytrain)
            ypred = model.predict(self.xtest)
            recall = recall_score(self.ytest, ypred)
            logging.info(f"successfully trained Logistic Regression.")
            return [model, recall]

        except Exception as e:
            logging.error(f"Error while training Logistic Regression.\n" + str(e))
            raise e
    
    def randomForest(self):
        logging.info("Started training randomForest model.")
        try:
            model = RandomForestClassifier(criterion='entropy', max_depth=16, min_samples_leaf=2, min_samples_split=2, n_estimators=200)
            model.fit(self.xtrain, self.ytrain)
            ypred = model.predict(self.xtest)
            recall = recall_score(self.ytest, ypred)
            logging.info("Successfully trained Random Forest.")
            return [model, recall]
        
        except Exception as e:
            logging.error(f"Error while training Random Forest model.\n" + str(e))
            raise e
        
    def xgboost(self):
        logging.info(f"Started training XGBoost.")
        try:
            model = XGBClassifier(booster='gbtree', eta=0.028, max_depth=8, n_estimators=200, random_state=23)
            model.fit(self.xtrain, self.ytrain)
            ypred = model.predict(self.xtest)
            recall = recall_score(self.ytest, ypred)
            logging.info(f"Successfully trained XGBoost.")
            return [model, recall]
        
        except Exception as e:
            logging.error(f"Error while training XGBoost.\n" + str(e))
            raise e


            