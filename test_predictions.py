import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from joblib import load
import logging

# Setup logging
logging.basicConfig(filename='test_predictions.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Flask app URL
BASE_URL = "http://127.0.0.1:5000"

# Load model for direct testing
try:
    model = load("random_forest_model.joblib")
    logging.info("Model loaded successfully.")
except FileNotFoundError:
    logging.error("Model file 'random_forest_model.joblib' not found.")
    model = None

# Feature names
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

# Demo data with refined XSS sample
DEMO_DATA = {
    "BENIGN": [
        62015, 1261, 51885.0, 1599, 53.0, 17.0, 181, 76978.0, 2.0, 2.0, 78.0, 206.0, 39.0, 39.0, 39.0, 0.0,
        103.0, 103.0, 103.0, 0.0, 3689.365793, 51.96289849, 25659.33333, 44436.34082, 76970.0, 4.0, 4.0, 4.0,
        0.0, 4.0, 4.0, 4.0, 4.0, 0.0, 4.0, 4.0, 0.0, 0.0, 0.0, 0.0, 64.0, 64.0, 25.98144925, 25.98144925,
        39.0, 103.0, 64.6, 35.05424368, 1228.8, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 80.75, 39.0,
        103.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 78.0, 2.0, 206.0, -1.0, -1.0, 1.0, 32.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0
    ],
    "Web Attack – Brute Force": [
        4022, 845, 44380.0, 1601, 80.0, 6.0, 196, 5185118.0, 7.0, 7.0, 1022.0, 2321.0, 372.0, 0.0, 146.0,
        184.0787875, 1047.0, 0.0, 331.5714286, 439.6592837, 644.7297824, 2.700034985, 398855.2308, 1372180.71,
        4963956.0, 4.0, 221162.0, 36860.33333, 56141.02125, 141434.0, 4.0, 5185004.0, 864167.3333, 2027593.314,
        5001548.0, 879.0, 0.0, 0.0, 0.0, 0.0, 232.0, 232.0, 1.350017492, 1.350017492, 0.0, 1047.0, 222.8666667,
        331.3239387, 109775.5524, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 238.7857143, 146.0, 331.5714286,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.0, 1022.0, 7.0, 2321.0, 29200.0, 252.0, 3.0, 32.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0
    ],
    "Web Attack – Sql Injection": [
        3698, 845, 36196.0, 1601, 80.0, 6.0, 40, 5006127.0, 4.0, 4.0, 447.0, 530.0, 447.0, 0.0, 111.75, 223.5,
        530.0, 0.0, 132.5, 265.0, 195.1608499, 1.59804176, 715161.0, 1889619.815, 5000415.0, 4.0, 5712.0, 1904.0,
        2168.235227, 4266.0, 4.0, 5005996.0, 1668665.333, 2885896.206, 5001011.0, 1407.0, 0.0, 0.0, 0.0, 0.0,
        136.0, 136.0, 0.79902088, 0.79902088, 0.0, 530.0, 108.5555556, 216.4053552, 46831.27778, 0.0, 0.0, 0.0,
        1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 122.125, 111.75, 132.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 4.0, 447.0, 4.0,
        530.0, 29200.0, 235.0, 1.0, 32.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    ],
    "Web Attack – XSS": [
        4628.0, 845.0, 52120.0, 1601.0, 80.0, 6.0, 15.0, 5638432.0, 3.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.709417086, 1879477.333, 3254752.687, 5637742.0, 72.0, 5638432.0, 2819216.0, 3985997.695,
        5637742.0, 690.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 104.0, 40.0, 0.532062815, 0.1773542719999999, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.0,
        0.0, 1.0, 0.0, 29200.0, 28960.0, 0.0, 32.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    ]
}

def test_prediction_flask(label, data):
    form_data = {feature: str(value) for feature, value in zip(FEATURES, data)}
    logging.debug(f"Flask input for {label}: {form_data}")
    try:
        response = requests.post(f"{BASE_URL}/predict", data=form_data)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        prediction_div = soup.find('div', class_='alert-success')
        if prediction_div:
            prediction = prediction_div.text.replace("Prediction:", "").strip()
            return prediction, None
        error_div = soup.find('div', class_='alert-danger')
        if error_div:
            error = error_div.text.replace("Error:", "").strip()
            return None, error
        return None, "No prediction or error found in response."
    except requests.RequestException as e:
        return None, f"Request failed: {e}"

def test_prediction_direct(label, data):
    if model is None:
        return None, "Model not loaded."
    try:
        input_data = pd.DataFrame([data], columns=FEATURES)
        logging.debug(f"Direct input for {label}: {input_data.to_dict()}")
        prediction = model.predict(input_data)[0]
        probabilities = model.predict_proba(input_data)[0]
        prob_dict = {cls: float(prob) for cls, prob in zip(model.classes_, probabilities)}
        logging.info(f"Probabilities for {label}: {prob_dict}")
        # Compare XSS and Brute Force features if XSS fails
        if label == "Web Attack – XSS" and prediction != "Web Attack – XSS":
            xss_df = input_data
            bf_df = pd.DataFrame([DEMO_DATA["Web Attack – Brute Force"]], columns=FEATURES)
            diff = (xss_df - bf_df).abs().mean()
            key_features = ['Flow Duration', 'Fwd Packet Length Max', 'Packet Length Variance', 'Flow Bytes/s']
            logging.warning(f"Feature differences for key features: {diff[key_features].to_dict()}")
        return prediction, None
    except Exception as e:
        return None, f"Direct prediction failed: {e}"

def run_tests():
    print("Running prediction tests...\n")
    for label, data in DEMO_DATA.items():
        print(f"Testing label: {label}")
        flask_prediction, flask_error = test_prediction_flask(label, data)
        if flask_prediction:
            flask_status = "PASS" if flask_prediction == label else "FAIL"
            print(f"Flask Prediction: {flask_prediction}")
            print(f"Expected: {label}")
            print(f"Flask Status: {flask_status}")
        else:
            print(f"Flask Error: {flask_error}")
            print(f"Flask Status: FAIL")
        direct_prediction, direct_error = test_prediction_direct(label, data)
        if direct_prediction:
            direct_status = "PASS" if direct_prediction == label else "FAIL"
            print(f"Direct Prediction: {direct_prediction}")
            print(f"Direct Status: {direct_status}")
        else:
            print(f"Direct Error: {direct_error}")
            print(f"Direct Status: FAIL")
        print("\n")

if __name__ == "__main__":
    run_tests()