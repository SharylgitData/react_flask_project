import React, { useState } from "react";
import axios from "axios";

function App() {
  const [input, setInput] = useState({
    Weight: "",
    Length1: "",
    Length2: "",
    Length3: "",
    Height: "",
    Width: "",
  });
  const [prediction, setPrediction] = useState(""); // Holds the predicted species

  const handleChange = (e) => {
    setInput({ ...input, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post("http://127.0.0.1:5000/predict", input);
      setPrediction(response.data.species); // Update UI with prediction
    } catch (error) {
      console.error("Error fetching prediction:", error);
      setPrediction("Error: Unable to get prediction");
    }
  };

  return (
    <div>
      <h1>Fish Market Prediction</h1>
      <form onSubmit={handleSubmit}>
        {Object.keys(input).map((key) => (
          <div key={key}>
            <label>{key}: </label>
            <input
              type="number"
              name={key}
              value={input[key]}
              onChange={handleChange}
              required
            />
          </div>
        ))}
        <button type="submit">Predict</button>
      </form>
      {prediction && <h2>Predicted Fish Species: {prediction}</h2>}
    </div>
  );
}

export default App;
