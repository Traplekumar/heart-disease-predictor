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
    def __init__(self, xtrain, ytrain, xtest, ytest, cluster):
        self.xtrain = xtrain
        self.ytrain = ytrain
        self.xtest = xtest
        self.ytest = ytest
        self.cluster = cluster

    def logisticRegression(self):
        logging.info(f"Started training Logistic Regression on cluster => {self.cluster}.")
        try:
            model = LogisticRegression(penalty='none')
            model.fit(self.xtrain, self.ytrain)
            ypred = model.predict(self.xtest)
            # print(self.ytest)
            recall = recall_score(self.ytest, ypred)
            logging.info(f"successfully trained Logistic Regression model on cluster => {self.cluster}.")
            return [model, recall]

        except Exception as e:
            logging.error(f"Error while training Logistic Regression model on cluster => {self.cluster}.\n" + str(e))
            raise e
    
    def randomForest(self):
        logging.info(f"Started training randomForest model on cluster => {self.cluster}")
        try:
            model = RandomForestClassifier(criterion='entropy', max_depth=19, min_samples_leaf=3, min_samples_split=9, n_estimators=100)
            model.fit(self.xtrain, self.ytrain)
            ypred = model.predict(self.xtest)
            recall = recall_score(self.ytest, ypred)
            logging.info(f"Successfully trained Random Forest on cluster => {self.cluster}")
            return [model, recall]
        
        except Exception as e:
            logging.error(f"Error while training Random Forest model on cluster => {self.cluster}.\n" + str(e))
            raise e
        
    def xgboost(self):
        logging.info(f"Started training XGBoost on cluster => {self.cluster}")
        try:
            model = XGBClassifier(booster='gblinear', eta=0.019, max_depth=1, n_estimators=10, random_state=23)
            model.fit(self.xtrain, self.ytrain)
            ypred = model.predict(self.xtest)
            recall = recall_score(self.ytest, ypred)
            logging.info(f"Successfully trained XGBoost on cluster => {self.cluster}")
            return [model, recall]
        
        except Exception as e:
            logging.error(f"Error while training XGBoost on cluster => {self.cluster}.\n" + str(e))
            raise e


            