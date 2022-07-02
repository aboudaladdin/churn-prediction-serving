# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 17:43:46 2022
@description: Serving machine learning model with flask web service
- following Alexey ch5 deployment chapter
@author: Aboud
"""

import pickle 
import os
import numpy as np
from flask import Flask, request, jsonify


## load our model
with open('churn-model.bin',mode='rb') as model_file:
    dict_victor, model = pickle.load(model_file)


## predict single client
def predict_single_client(client, dv, model):
    X = dv.transform([client])
    y_pred = model.predict_proba(X)[:, 1]
    return y_pred[0]

## initiate our flask web service
app = Flask('churn')

@app.route('/', methods = ['GET'])
def home():
    return 'Welcome to Churn prediction, use /predict with json body'
	
@app.route('/ping', methods = ['GET'])
def ping():
    return 'PONG2'


@app.route('/predict', methods = ['POST'])
def predict():
    customer = request.get_json()
    prediction = predict_single_client(customer, dict_victor, model)
    
    churn = prediction >= 0.5 
    result = { 
                'churn_probability': float(prediction), 
                'churn': bool(churn), 
                } 
    return jsonify(result)


if __name__ == '__main__':
    port = os.environ.get("PORT", 9696)
    app.run(debug = False, host='0.0.0.0', port = port)
    