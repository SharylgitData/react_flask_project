from flask import Flask, request, jsonify
import pickle
import numpy as np
import pandas as pd
from flask_cors import CORS
# Load the trained model and LabelEncoder
with open("fish_model.pkl", "rb") as file:
    model, label_encoder = pickle.load(file)

app = Flask(__name__)
CORS(app)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get JSON request data
        data = request.get_json()
        
        df = pd.DataFrame([data])
        
        # Ensure input columns match the training data
        expected_columns = ['Weight', 'Length1', 'Length2', 'Length3', 'Height', 'Width']
        df = df[expected_columns]
        
        # Make prediction
        species_idx = model.predict(df)[0]
        species_name = label_encoder.inverse_transform([species_idx])[0]
        
        return jsonify({"species": species_name})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
