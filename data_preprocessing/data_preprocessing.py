import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
from sklearn.cluster import KMeans
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from imblearn.under_sampling import RandomUnderSampler
import logging
import sys

# sys.path.append('logger')
# import logger_config
from logger import logger_config

class Preprocessing:
    def __init__(self, dataFrame):
        self.data = dataFrame

    def binaryEncode(self):
        logging.info("Started binary encoding of features")
        try:
            columns = ['Smoking', 'AlcoholDrinking', 'Stroke', 'DiffWalking', 'PhysicalActivity', 
                        'Asthma', 'KidneyDisease', 'SkinCancer']
            for col in columns:
                self.data[col] = self.data[col].apply(lambda x: 1 if x=="Yes" else 0)
            self.data['Sex'] = self.data['Sex'].apply(lambda x: 1 if x=="Female" else 0) 
            try:
                self.data['HeartDisease'] = self.data['HeartDisease'].apply(lambda x: 1 if x=="Yes" else 0)
            except: 
                pass

            logging.info("Successfully completed binary Encoding of variable.")
            
        except Exception as e:
            logging.error("Error while binary encoding features.\n" + str(e))
            raise e
            
    def ordinalMap(self, val):
        if val == "Poor":
            return 0
        elif val == "Fair":
            return 1
        elif val == "Good":
            return 2
        elif val == "Very good":
            return 3
        else:
            return 4
            
    def ordinalEncode(self):
        logging.info("Started Ordinal Encoding.")
        try:
            self.data['GenHealth'] = list(map(self.ordinalMap, self.data['GenHealth']))
            logging.info("Successfully completed Ordinal Encoding.")
            
        except Exception as e:
            logging.error("Error while ordinal Encoding.\n" + str(e))
            raise e

    def oneHotEncode(self):
        logging.info("Started One Hot Encoding")
        try:
            column = ["AgeCategory", "Race", "Diabetic"]
            enc = OneHotEncoder()
            features = enc.fit_transform(self.data[column]).toarray()
            labels = ['18_24', '25_29', '30_34', '35_39', '40_44', '45_49', '50_54', '55_59', '60_64', '65_69', '70_74', '75_79', 
                    '80_more', 'American_Indian', 'Asian', 'Black', 'Hispanic', 'Other', 'White', 'No', 'Borderline_Diabetes',
                    'Yes', 'During_Pregnancy']

            feature_df = pd.DataFrame(features, columns=labels)
            with open("Resources/OneHotEncoder.pickle", "wb") as file:
                pickle.dump(enc, file)
            
            feature_df.drop(['80_more', 'American_Indian', 'Borderline_Diabetes'], axis=1, inplace=True)
            self.data.drop(['AgeCategory', 'Race', 'Diabetic'], axis=1, inplace=True)
            self.data = pd.concat([self.data, feature_df], axis=1)
            logging.info("Successfullly one Hot encoded features.")
            
        except Exception as e:
            logging.error("Error while One hot Encoding.\n" + str(e))
            raise e

    def oneHotEncodeTest(self):
        logging.info("Started One Hot Encoding of Test data.")
        try:
            column = ["AgeCategory", "Race", "Diabetic"]
            with open("Resources/OneHotEncoder.pickle", "rb") as file:
                oneHotEnc = pickle.load(file)
                features = oneHotEnc.transform(self.data[column]).toarray()
                labels = ['18_24', '25_29', '30_34', '35_39', '40_44', '45_49', '50_54', '55_59', '60_64', '65_69', '70_74', '75_79', 
                    '80_more', 'American_Indian', 'Asian', 'Black', 'Hispanic', 'Other', 'White', 'No', 'Borderline_Diabetes',
                    'Yes', 'During_Pregnancy']

                feature_df = pd.DataFrame(features, columns=labels)
                feature_df.drop(['80_more', 'American_Indian', 'Borderline_Diabetes'], axis=1, inplace=True)
                self.data.drop(['AgeCategory', 'Race', 'Diabetic'], axis=1, inplace=True)
                self.data = pd.concat([self.data, feature_df], axis=1)
                logging.info("Successfullly one Hot encoded features.")
                    
        except Exception as e:
            logging.error("Error while one hot encoding Test data.\n" + str(e))
            raise e
            
    def removeOutlier(self):
        q = self.data['BMI'].quantile(0.9998)
        self.data = self.data[self.data['BMI'] < q]

    def createClusters(self):
        CLUSTER = 4
        temp = self.data.drop('HeartDisease', axis=1)

        kmeans = KMeans(n_clusters=CLUSTER, init='k-means++', random_state=124)
        clusters = kmeans.fit_predict(temp)
        with open('Resources/Kmeans.pickle', 'wb') as file:
            pickle.dump(kmeans, file)
        
        clusters = clusters.reshape(-1, 1)
        self.data['cluster'] = clusters
        return self.data, CLUSTER

    def createClustersTest(self):
        CLUSTER = 4
        try:
            temp = self.data.drop('HeartDisease', axis=1)
        except:
            temp = self.data
        
        with open('Resources/Kmeans.pickle', 'rb') as file:
            kmeans = pickle.load(file)
        
        clusters = kmeans.predict(temp)
        self.data['cluster'] = clusters
        return self.data


    def getXAndY(self):
        x = self.data.drop(['HeartDisease', 'cluster'], axis=1)
        y = self.data['HeartDisease']
        return x, y

    def getX(self, data):
        x = data.drop('cluster', axis=1)
        return x

    def standardizeX(self, x):
        sc = StandardScaler()
        xNew = sc.fit_transform(x)
        with open("Resources/StandardScaler.pickle", "wb") as file:
            pickle.dump(sc, file)
        return xNew

    def standardizeXTest(self, x):
        with open("Resources/StandardScaler.pickle", "rb") as file:
            standardScaler = pickle.load(file)
        xNew = standardScaler.transform(x)
        # print(xNew[0])
        return xNew

    def underSample(self, x, y):
        underSample = RandomUnderSampler(random_state=25)
        xUnder, yUnder = underSample.fit_resample(x, y)
        return xUnder, yUnder
    
    
if __name__ == '__main__':
    df = pd.read_csv('TrainingInput/InputFile.csv')
    a = Preprocessing(df)
    a.binaryEncode()
    print(1)
    a.ordinalEncode()
    print(2)
    a.oneHotEncode()
    print(3)
    a.removeOutlier()
    print(4)
    a.createClusters()
    print(5)
    x, y = a.getXAndY()
    print(6)
    x = a.standardizeX(x)
    print(7)
    x, y = a.underSample(x, y)
    print(8)
