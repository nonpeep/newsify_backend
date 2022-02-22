import os
import json
 
from flask import Flask, request
 
from transformers import  pipeline

model_name = "deepset/roberta-base-squad2"
model = pipeline('question-answering', model='./model', tokenizer='./model')
 
app = Flask(__name__)

 
@app.route('/predict', methods=['POST'])
def predict():
   return model(request.json)
  
if __name__ == "__main__":
   app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))