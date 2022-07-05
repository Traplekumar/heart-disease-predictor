from flask import Flask, request, render_template, url_for, redirect
from flask_cors import CORS, cross_origin
from sklearn.exceptions import SkipTestWarning
from predict_from_model import Predictor
import os
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
@cross_origin()
def home():

    if request.method == 'POST':
        bmi = float(request.form['bmi'])
        sleep = float(request.form['sleep'])
        phyHealth = float(request.form['physical_health'])
        mentalHealth = float(request.form['mental_health'])
        race = request.form['race']
        sex = request.form['sex']
        ageCat = request.form['age_category']
        diabetic = request.form['diabetic']
        genHealth = request.form['general_health']
        smoking = request.form['smoking']
        alcohol = request.form['alcohol']
        stroke = request.form['stroke']
        asthma = request.form['asthma']
        kidney = request.form['kidney_disease']
        skinCancer = request.form['skin_cancer']
        phyActivity = request.form['physical_activity']
        walking = request.form['difficult_walking']
        values = [bmi, sleep, phyHealth, mentalHealth, race, sex, 
        ageCat, diabetic, genHealth, smoking, alcohol, stroke, asthma,
        kidney, skinCancer, phyActivity, walking]

        predictor = Predictor()
        values = [bmi, smoking, alcohol, stroke, phyHealth, mentalHealth, walking, sex, 
        ageCat, race, diabetic, phyActivity, genHealth, sleep, asthma, kidney, skinCancer]
        print(values)
        # values = [16.6,'Yes','No','No',3.0,30.0,'No','Female','55-59','White','Yes','Yes','Very good',5.0,'Yes','No','Yes']
        prediction = predictor.predict(values)
        return render_template('prediction.html', predValue=prediction)
    else:
        return render_template("home.html")

if __name__ ==  '__main__':
    app.run(debug=True)