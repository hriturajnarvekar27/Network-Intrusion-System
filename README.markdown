# Web Attack Prediction System

## Overview

The **Web Attack Prediction System** is a machine learning-based web application designed to classify network traffic as either `BENIGN` or one of three types of web attacks: `Web Attack – Brute Force`, `Web Attack – Sql Injection`, or `Web Attack – XSS`. The system uses a pre-trained Random Forest model to make predictions based on 85 network traffic features. The application is built with Flask, providing a user-friendly web interface where users can manually input feature values to get predictions.

This project serves as the original implementation, focusing on core functionality without themed UI variations.

## Features

- Predicts web attack types using a Random Forest model.
- Supports manual input of 85 network traffic features via a web form.
- Provides a simple and responsive UI using Bootstrap.
- Includes a script to test predictions programmatically.
- Easy setup with Python and Flask.

## Prerequisites

Before setting up the project, ensure you have the following installed:

- **Python 3.8+**: Required to run the Flask application and scripts.
- **pip**: Python package manager to install dependencies.
- **Git**: To clone the repository.

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/<your-username>/web-attack-prediction.git
   cd web-attack-prediction
   ```

2. **Set Up a Virtual Environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   Install the required Python packages using the `requirements.txt` file (create one if not present):
   ```bash
   pip install -r requirements.txt
   ```
   If `requirements.txt` is not present, install the following packages manually:
   ```bash
   pip install flask pandas numpy scikit-learn==1.5.2 joblib
   ```
   **Note**: The Random Forest model was trained with scikit-learn version 1.5.2. Using a different version may cause compatibility issues.

4. **Obtain the Trained Model**:
   The `random_forest_model.joblib` file is not included in the repository due to its size (as per `.gitignore`). You can either:
   - **Retrain the Model**: Use the training script (not provided in this repo) with your dataset to generate `random_forest_model.joblib`.
   - **Download the Model**: If you have access to the pre-trained model, place it in the root directory of the project.

5. **Start the Flask Application**:
   Run the Flask app:
   ```bash
   python app.py
   ```
   The app will be hosted at `http://127.0.0.1:5000`. Open this URL in your browser.

## Project Structure

Below is the structure of the project:

```
web-attack-prediction/
│
├── app.py                    # Flask application script
├── test_predictions.py       # Script to test predictions programmatically
├── templates/
│   └── index.html            # HTML template for the web interface (basic Bootstrap design)
├── .gitignore                # Git ignore file to exclude unnecessary files
└── README.md                 # This README file
```

**Note**: The following files are not included in the repository but are required for full functionality:
- `random_forest_model.joblib`: The pre-trained Random Forest model.
- `test_data.csv`: Sample test data for testing predictions (can be generated or obtained separately).

## Usage

### Manual Prediction via Web Interface

1. Start the Flask app as described in the setup instructions.
2. Open `http://127.0.0.1:5000` in your browser.
3. You’ll see a form with 85 input fields corresponding to the network traffic features.
4. Enter the values for each feature manually. You can use the demo data provided below for testing.
5. Click the **Predict** button to get the prediction.
6. The predicted class (`BENIGN`, `Web Attack – Brute Force`, `Web Attack – Sql Injection`, or `Web Attack – XSS`) will be displayed below the form.

### Demo Data for Testing

Below is demo data for testing predictions. Each row corresponds to one prediction class. Use these values to manually input into the web form.

#### Part 1: Flow ID to Flow IAT Min
| Label                   | Flow ID | Source IP | Source Port | Destination IP | Destination Port | Protocol | Timestamp | Flow Duration | Total Fwd Packets | Total Backward Packets | Total Length of Fwd Packets | Total Length of Bwd Packets | Fwd Packet Length Max | Fwd Packet Length Min | Fwd Packet Length Mean | Fwd Packet Length Std | Bwd Packet Length Max | Bwd Packet Length Min | Bwd Packet Length Mean | Bwd Packet Length Std | Flow Bytes/s | Flow Packets/s | Flow IAT Mean | Flow IAT Std | Flow IAT Max | Flow IAT Min |
|-------------------------|---------|-----------|-------------|----------------|------------------|----------|-----------|---------------|-------------------|------------------------|-----------------------------|-----------------------------|-----------------------|-----------------------|------------------------|-----------------------|-----------------------|-----------------------|------------------------|-----------------------|--------------|----------------|---------------|--------------|--------------|--------------|
| BENIGN                  | 62015   | 1261      | 51885.0     | 1599           | 53.0             | 17.0     | 181       | 76978.0       | 2.0               | 2.0                    | 78.0                        | 206.0                       | 39.0                  | 39.0                  | 39.0                   | 0.0                   | 103.0                 | 103.0                 | 103.0                  | 0.0                   | 3689.365793  | 51.96289849    | 25659.33333   | 44436.34082  | 76970.0      | 4.0          |
| Web Attack – Brute Force| 4022    | 845       | 44380.0     | 1601           | 80.0             | 6.0      | 196       | 5185118.0     | 7.0               | 7.0                    | 1022.0                      | 2321.0                      | 372.0                 | 0.0                   | 146.0                  | 184.0787875           | 1047.0                | 0.0                   | 331.5714286            | 439.6592837           | 644.7297824  | 2.700034985    | 398855.2308   | 1372180.71   | 4963956.0    | 4.0          |
| Web Attack – Sql Injection | 3698    | 845       | 36196.0     | 1601           | 80.0             | 6.0      | 40        | 5006127.0     | 4.0               | 4.0                    | 447.0                       | 530.0                       | 447.0                 | 0.0                   | 111.75                 | 223.5                 | 530.0                 | 0.0                   | 132.5                  | 265.0                 | 195.1608499  | 1.59804176     | 715161.0      | 1889619.815  | 5000415.0    | 4.0          |
| Web Attack – XSS        | 4024    | 845       | 44382.0     | 1601           | 80.0             | 6.0      | 198       | 1000000.0     | 8.0               | 6.0                    | 800.0                       | 600.0                       | 200.0                 | 0.0                   | 100.0                  | 150.0                 | 300.0                 | 0.0                   | 100.0                  | 200.0                 | 1400.0       | 14.0           | 83333.3333    | 300000.0     | 900000.0     | 4.0          |

#### Part 2: Fwd IAT Total to Bwd IAT Min
| Fwd IAT Total | Fwd IAT Mean | Fwd IAT Std | Fwd IAT Max | Fwd IAT Min | Bwd IAT Total | Bwd IAT Mean | Bwd IAT Std | Bwd IAT Max | Bwd IAT Min |
|---------------|--------------|-------------|-------------|-------------|---------------|--------------|-------------|-------------|-------------|
| 4.0           | 4.0          | 0.0         | 4.0         | 4.0         | 4.0           | 4.0          | 0.0         | 4.0         | 4.0         |
| 221162.0      | 36860.33333  | 56141.02125 | 141434.0    | 4.0         | 5185004.0     | 864167.3333  | 2027593.314 | 5001548.0   | 879.0       |
| 5712.0        | 1904.0       | 2168.235227 | 4266.0      | 4.0         | 5005996.0     | 1668665.333  | 2885896.206 | 5001011.0   | 1407.0      |
| 100000.0      | 12500.0      | 20000.0     | 40000.0     | 4.0         | 900000.0      | 180000.0     | 500000.0    | 900000.0    | 400.0       |

#### Part 3: Fwd PSH Flags to Packet Length Variance
| Fwd PSH Flags | Bwd PSH Flags | Fwd URG Flags | Bwd URG Flags | Fwd Header Length | Bwd Header Length | Fwd Packets/s | Bwd Packets/s | Min Packet Length | Max Packet Length | Packet Length Mean | Packet Length Std | Packet Length Variance |
|---------------|---------------|---------------|---------------|-------------------|-------------------|---------------|---------------|-------------------|-------------------|--------------------|-------------------|------------------------|
| 0.0           | 0.0           | 0.0           | 0.0           | 64.0              | 64.0              | 25.98144925   | 25.98144925   | 39.0              | 103.0             | 64.6               | 35.05424368       | 1228.8                 |
| 0.0           | 0.0           | 0.0           | 0.0           | 232.0             | 232.0             | 1.350017492   | 1.350017492   | 0.0               | 1047.0            | 222.8666667        | 331.3239387       | 109775.5524            |
| 0.0           | 0.0           | 0.0           | 0.0           | 136.0             | 136.0             | 0.79902088    | 0.79902088    | 0.0               | 530.0             | 108.5555556        | 216.4053552       | 46831.27778            |
| 0.0           | 0.0           | 0.0           | 0.0           | 256.0             | 192.0             | 8.0           | 6.0           | 0.0               | 300.0             | 150.0              | 200.0             | 100000.0               |

#### Part 4: FIN Flag Count to Down/Up Ratio
| FIN Flag Count | SYN Flag Count | RST Flag Count | PSH Flag Count | ACK Flag Count | URG Flag Count | CWE Flag Count | ECE Flag Count | Down/Up Ratio |
|----------------|----------------|----------------|----------------|----------------|----------------|----------------|----------------|---------------|
| 0.0            | 0.0            | 0.0            | 0.0            | 0.0            | 0.0            | 0.0            | 0.0            | 1.0           |
| 0.0            | 0.0            | 0.0            | 1.0            | 0.0            | 0.0            | 0.0            | 0.0            | 1.0           |
| 0.0            | 0.0            | 0.0            | 1.0            | 0.0            | 0.0            | 0.0            | 0.0            | 1.0           |
| 0.0            | 0.0            | 0.0            | 0.0            | 0.0            | 0.0            | 0.0            | 0.0            | 0.75          |

#### Part 5: Average Packet Size to min_seg_size_forward
| Average Packet Size | Avg Fwd Segment Size | Avg Bwd Segment Size | Fwd Avg Bytes/Bulk | Fwd Avg Packets/Bulk | Fwd Avg Bulk Rate | Bwd Avg Bytes/Bulk | Bwd Avg Packets/Bulk | Bwd Avg Bulk Rate | Subflow Fwd Packets | Subflow Fwd Bytes | Subflow Bwd Packets | Subflow Bwd Bytes | Init_Win_bytes_forward | Init_Win_bytes_backward | act_data_pkt_fwd | min_seg_size_forward |
|---------------------|----------------------|----------------------|--------------------|----------------------|-------------------|--------------------|----------------------|-------------------|---------------------|-------------------|---------------------|-------------------|------------------------|-------------------------|------------------|----------------------|
| 80.75               | 39.0                 | 103.0                | 0.0                | 0.0                  | 0.0               | 0.0                | 0.0                  | 0.0               | 2.0                 | 78.0              | 2.0                 | 206.0             | -1.0                   | -1.0                    | 1.0              | 32.0                 |
| 238.7857143         | 146.0                | 331.5714286          | 0.0                | 0.0                  | 0.0               | 0.0                | 0.0                  | 0.0               | 7.0                 | 1022.0            | 7.0                 | 2321.0            | 29200.0                | 252.0                   | 3.0              | 32.0                 |
| 122.125             | 111.75               | 132.5                | 0.0                | 0.0                  | 0.0               | 0.0                | 0.0                  | 0.0               | 4.0                 | 447.0             | 4.0                 | 530.0             | 29200.0                | 235.0                   | 1.0              | 32.0                 |
| 200.0               | 100.0                | 100.0                | 0.0                | 0.0                  | 0.0               | 0.0                | 0.0                  | 0.0               | 8.0                 | 800.0             | 6.0                 | 600.0             | 29200.0                | 252.0                   | 4.0              | 32.0                 |

#### Part 6: Active Mean to Idle Min
| Active Mean | Active Std | Active Max | Active Min | Idle Mean | Idle Std | Idle Max | Idle Min |
|-------------|------------|------------|------------|-----------|----------|----------|----------|
| 0.0         | 0.0        | 0.0        | 0.0        | 0.0       | 0.0      | 0.0      | 0.0      |
| 0.0         | 0.0        | 0.0        | 0.0        | 0.0       | 0.0      | 0.0      | 0.0      |
| 0.0         | 0.0        | 0.0        | 0.0        | 0.0       | 0.0      | 0.0      | 0.0      |
| 0.0         | 0.0        | 0.0        | 0.0        | 0.0       | 0.0      | 0.0      | 0.0      |

**Expected Predictions**:
- Row 1: `BENIGN`
- Row 2: `Web Attack – Brute Force`
- Row 3: `Web Attack – Sql Injection`
- Row 4: `Web Attack – XSS`

### Programmatic Testing with `test_predictions.py`

The `test_predictions.py` script is designed to test predictions by sending requests to the Flask app and directly using the model. However, it currently relies on hardcoded sample inputs. To use it with the demo data:

1. Start the Flask app in one terminal:
   ```bash
   python app.py
   ```
2. In another terminal, run the test script:
   ```bash
   python test_predictions.py
   ```
3. **Note**: You’ll need to modify `test_predictions.py` to use the demo data above instead of its hardcoded inputs. Update the `SAMPLE_INPUTS` dictionary or load the data dynamically.

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature-name
   ```
3. Make your changes and commit them:
   ```bash
   git commit -m "Add feature-name"
   ```
4. Push to your fork and create a pull request:
   ```bash
   git push origin feature-name
   ```
5. Submit a pull request with a detailed description of your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details (if applicable).

## Contact

For questions or support, please open an issue on GitHub or contact the repository owner.

---
*Last updated: June 17, 2025*