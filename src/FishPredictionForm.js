import React, { useState } from "react";
import axios from "axios";

function FishPredictionForm() {
    const [features, setFeatures] = useState({
        Weight: "",
        Length1: "",
        Length2: "",
        Length3: "",
        Height: "",
        Width: "",
    });

    const [prediction, setPrediction] = useState("");

    const handleChange = (e) => {
        setFeatures({ ...features, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post("http://127.0.0.1:5000/predict", {
                features: Object.values(features).map(Number), // Convert input to numbers
            });
            setPrediction(response.data.prediction);
        } catch (error) {
            setPrediction("Error: Unable to get prediction");
        }
    };

    return (
        <div>
            <h2>Fish Species Prediction</h2>
            <form onSubmit={handleSubmit}>
                {Object.keys(features).map((key) => (
                    <div key={key}>
                        <label>{key}: </label>
                        <input type="text" name={key} value={features[key]} onChange={handleChange} required />
                    </div>
                ))}
                <button type="submit">Predict</button>
            </form>
            {prediction && <h3>Predicted Fish Species: {prediction}</h3>}
        </div>
    );
}

export default FishPredictionForm;
