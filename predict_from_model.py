import os
import pandas as pd
import pickle

class Predictor:
    def __init__(self):
        self.modelDirectory = 'TrainedModel'
        self.resources = 'Resources'

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

    def predict(self, valList):
        colName = ['BMI', 'Smoking', 'AlcoholDrinking', 'Stroke', 'PhysicalHealth', 'MentalHealth', 
                    'DiffWalking', 'Sex', 'AgeCategory', 'Race', 'Diabetic', 'PhysicalActivity', 'GenHealth', 'SleepTime', 
                    'Asthma', 'KidneyDisease', 'SkinCancer']

        df = pd.DataFrame(columns = colName)
        df.loc[0] = valList        
        print(df)
        
        ## binary encode
        columns = ['Smoking', 'AlcoholDrinking', 'Stroke', 'DiffWalking', 'PhysicalActivity', 
                        'Asthma', 'KidneyDisease', 'SkinCancer']
        for col in columns:
            df[col] = df[col].apply(lambda x: 1 if x=="Yes" else 0)
        df['Sex'] = df['Sex'].apply(lambda x: 1 if x=="Female" else 0) 

        ## ordinal encode
        df['GenHealth'] = list(map(self.ordinalMap, df['GenHealth']))
            

        ## one Hot Encode
        column = ["AgeCategory", "Race", "Diabetic"]
        with open("Resources/OneHotEncoder.pickle", "rb") as file:
            oneHotEnc = pickle.load(file)
            features = oneHotEnc.transform(df[column]).toarray()
            labels = ['18_24', '25_29', '30_34', '35_39', '40_44', '45_49', '50_54', '55_59', '60_64', '65_69', '70_74', '75_79', 
                '80_more', 'American_Indian', 'Asian', 'Black', 'Hispanic', 'Other', 'White', 'No', 'Borderline_Diabetes',
                'Yes', 'During_Pregnancy']

            feature_df = pd.DataFrame(features, columns=labels)
            feature_df.drop(['80_more', 'White', 'No'], axis=1, inplace=True)
            df.drop(['AgeCategory', 'Race', 'Diabetic'], axis=1, inplace=True)
            df = pd.concat([df, feature_df], axis=1)
        
        xUser = df

        ## Standard Scaler
        # with open("Resources/StandardScaler.pickle", "rb") as file:
        #     standardScaler = pickle.load(file)
        # xNew = standardScaler.transform(df)

        ## make prediction
        for model in os.listdir(self.modelDirectory):
            modelPath = os.path.join(self.modelDirectory, model)
            print(modelPath)
            with open(modelPath, 'rb') as file:
                predModel = pickle.load(file)
                prediction = predModel.predict(xUser)
                return prediction

if __name__ == '__main__':
    x = Predictor()
    values = [32.81,'Yes','No','No',0.0,0.0,'No','Female','60-64','White','No','No','Excellent',8.0,'No','No','No']

    print(x.predict(values))