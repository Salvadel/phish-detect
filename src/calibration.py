"""
PhishDetect - calibration.py
CS 455 - Spring 2026

Calibrates the probabilities of a pre-trained PhishDetect model using sigmoid calibration.
"""

import os
import sys
import joblib
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from main import extract_features
from sklearn.calibration import CalibratedClassifierCV

# PATHS ----------------------------------------------------------------------
DATA_PATH  = os.path.join(os.path.dirname(__file__), "..", "data", "evaluation_emails.csv")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "phishdetect.pkl")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "phishdetect_calibrated.pkl")

# LOAD DATA AND MODEL -------------------------------------------------------
df = pd.read_csv(DATA_PATH)
model = joblib.load(MODEL_PATH)

# CIONVERT EMAILS TO FEATURES ----------------------------------------------------------------
X_cal = df["text"].apply(lambda t: extract_features(t)).tolist()
y_cal = df["label"].tolist()

# CALIBRATE MODEL ---------------------------------------------------------------
# Use cv=None for pre-trained model (modern sklearn)
calibrated_model = CalibratedClassifierCV(estimator=model, method='sigmoid', cv=None)
calibrated_model.fit(X_cal, y_cal)

# SAVE CALIBRATED MODEL ----------------------------------------------------------------
joblib.dump(calibrated_model, OUTPUT_PATH)
print(f"Calibrated model saved to: {OUTPUT_PATH}")