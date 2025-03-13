from flask import Flask, request, jsonify
import pickle
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load ML Model and Encoder
try:
    with open("fish_market_model.pkl", "rb") as f:
        model = pickle.load(f)  # Load the trained model

    with open("encoder.pkl", "rb") as f:  # Load encoder separately
        encoder = pickle.load(f)
except Exception as e:
    print(f"Error loading model or encoder: {e}")
    model = None
    encoder = None

@app.route("/predict", methods=["POST"])
def predict():
    if model is None or encoder is None:
        return jsonify({"error": "Model or encoder not loaded properly"}), 500

    try:
        data = request.json  # Get JSON input from React
        
        # Ensure required fields exist
        required_fields = ["Weight", "Length1", "Length2", "Length3", "Height", "Width"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400
        
        # Convert input to NumPy array
        features = np.array([
            float(data["Weight"]),
            float(data["Length1"]),
            float(data["Length2"]),
            float(data["Length3"]),
            float(data["Height"]),
            float(data["Width"]),
        ]).reshape(1, -1)

        # ✅ Ensure `model` is actually a model
        if not hasattr(model, "predict"):
            return jsonify({"error": "Loaded model is not valid"}), 500
        
        # Predict fish species
        prediction = model.predict(features)
        species = encoder.inverse_transform(prediction)[0]

        return jsonify({"species": species})
    
    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({"error": f"Unable to make prediction: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
