import pandas as pd

data = pd.read_csv("web_attacks_balanced.csv")
xss_data = data[data["Label"] == "Web Attack – XSS"].drop("Label", axis=1)
for i in range(min(10, len(xss_data))):
    sample = xss_data.iloc[i]
    if len(sample) == 83 and not sample.isna().any():
        print(f"Valid XSS sample at index {i}:")
        print(sample.values.tolist())
        break
else:
    print("No valid XSS sample found in first 10 rows.")