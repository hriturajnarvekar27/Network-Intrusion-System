from flask import Flask, render_template, request
import numpy as np
from joblib import load
import pandas as pd
import logging

# Setup logging
logging.basicConfig(filename='flask_app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

# Load model
try:
    model = load("random_forest_model.joblib")
    logging.info("Model loaded successfully.")
except Exception as e:
    logging.error(f"Failed to load model: {e}")

# Define features
FEATURES = [
    'Flow ID', 'Source IP', 'Source Port', 'Destination IP', 'Destination Port', 'Protocol', 'Timestamp',
    'Flow Duration', 'Total Fwd Packets', 'Total Backward Packets', 'Total Length of Fwd Packets',
    'Total Length of Bwd Packets', 'Fwd Packet Length Max', 'Fwd Packet Length Min', 'Fwd Packet Length Mean',
    'Fwd Packet Length Std', 'Bwd Packet Length Max', 'Bwd Packet Length Min', 'Bwd Packet Length Mean',
    'Bwd Packet Length Std', 'Flow Bytes/s', 'Flow Packets/s', 'Flow IAT Mean', 'Flow IAT Std', 'Flow IAT Max',
    'Flow IAT Min', 'Fwd IAT Total', 'Fwd IAT Mean', 'Fwd IAT Std', 'Fwd IAT Max', 'Fwd IAT Min',
    'Bwd IAT Total', 'Bwd IAT Mean', 'Bwd IAT Std', 'Bwd IAT Max', 'Bwd IAT Min', 'Fwd PSH Flags',
    'Bwd PSH Flags', 'Fwd URG Flags', 'Bwd URG Flags', 'Fwd Header Length', 'Bwd Header Length',
    'Fwd Packets/s', 'Bwd Packets/s', 'Min Packet Length', 'Max Packet Length', 'Packet Length Mean',
    'Packet Length Std', 'Packet Length Variance', 'FIN Flag Count', 'SYN Flag Count', 'RST Flag Count',
    'PSH Flag Count', 'ACK Flag Count', 'URG Flag Count', 'CWE Flag Count', 'ECE Flag Count', 'Down/Up Ratio',
    'Average Packet Size', 'Avg Fwd Segment Size', 'Avg Bwd Segment Size', 'Fwd Avg Bytes/Bulk',
    'Fwd Avg Packets/Bulk', 'Fwd Avg Bulk Rate', 'Bwd Avg Bytes/Bulk', 'Bwd Avg Packets/Bulk',
    'Bwd Avg Bulk Rate', 'Subflow Fwd Packets', 'Subflow Fwd Bytes', 'Subflow Bwd Packets',
    'Subflow Bwd Bytes', 'Init_Win_bytes_forward', 'Init_Win_bytes_backward', 'act_data_pkt_fwd',
    'min_seg_size_forward', 'Active Mean', 'Active Std', 'Active Max', 'Active Min', 'Idle Mean',
    'Idle Std', 'Idle Max', 'Idle Min'
]

@app.route('/')
def home():
    return render_template('index.html', features=FEATURES)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract form data
        input_data = []
        for feature in FEATURES:
            value = request.form.get(feature, '')
            if value == '':
                logging.warning(f"Missing value for feature: {feature}")
                return render_template('index.html', features=FEATURES, error="All fields are required.")
            try:
                input_data.append(float(value))
            except ValueError:
                logging.error(f"Invalid value for feature {feature}: {value}")
                return render_template('index.html', features=FEATURES, error=f"Invalid input for {feature}")

        # Log input data
        logging.debug(f"Input data: {input_data}")

        # Convert to DataFrame
        input_df = pd.DataFrame([input_data], columns=FEATURES)
        logging.debug(f"Input DataFrame: {input_df.to_dict()}")

        # Make prediction
        prediction = model.predict(input_df)[0]
        probabilities = model.predict_proba(input_df)[0]
        prob_dict = {cls: float(prob) for cls, prob in zip(model.classes_, probabilities)}
        logging.info(f"Prediction: {prediction}, Probabilities: {prob_dict}")

        return render_template('index.html', features=FEATURES, prediction=prediction)

    except Exception as e:
        logging.error(f"Prediction error: {e}")
        return render_template('index.html', features=FEATURES, error=str(e))

if __name__ == "__main__":
    app.run(debug=True)