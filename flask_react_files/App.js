import React, { useState } from "react";
import "./FishForm.css";

const FishForm = () => {
  const [formData, setFormData] = useState({
    Weight: "",
    Length1: "",
    Length2: "",
    Length3: "",
    Height: "",
    Width: "",
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };
  const [species, setspecies] = useState("");
  const handleSubmit = async (e) => {
    console.log(formData);
    e.preventDefault();
    try {
      const response = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });
      const data = await response.json();
      console.log("Response from backend:", data);
      setspecies(data?.species);
    } catch (error) {
      console.error("Error submitting data:", error);
    }
  };

  return (
    <div className="form-container">
      <h2>Fish Data Form</h2>
      <form onSubmit={handleSubmit}>
        {Object.keys(formData).map((key) => (
          <div key={key} className="form-group">
            <label>{key}:</label>
            <input
              type="text"
              name={key}
              value={formData[key]}
              onChange={handleChange}
              required
            />
          </div>
        ))}
        <button type="submit" className="submit-btn">
          Submit
        </button>
        <label className="species">{species}</label>
      </form>
    </div>
  );
};

export default FishForm;
