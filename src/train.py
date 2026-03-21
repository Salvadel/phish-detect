"""
PhishDetect - train.py
CS 455 - Spring 2026

Run this script once to train the classifier, This file does not need to be rerun 
unless you want to retrain the model with new data or tweak the feature extraction.
"""

import os
import re
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# LOAD THE DATASET -------------------------------------------------------------

DATA_PATH  = os.path.join(os.path.dirname(__file__), "..", "data", "emails.csv")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "phishdetect.pkl")

print("Loading dataset...")
df = pd.read_csv(DATA_PATH)

# Ensure expected columns exist
if "text" not in df.columns or "label" not in df.columns:
    raise ValueError("emails.csv must have 'text' and 'label' columns.")

df = df.dropna(subset=["text", "label"])
print(f"  {len(df)} emails loaded ({df['label'].sum()} phishing, {(df['label']==0).sum()} legitimate)")


# EXTRACT FEATURES ----------------------------------------------------------------

URGENCY_KEYWORDS = [
    "urgent", "immediately", "suspended", "verify", "expire",
    "act now", "limited time", "account locked", "unusual activity",
    "confirm your", "click here", "update your", "validate"
]

CREDENTIAL_KEYWORDS = [
    "password", "username", "login", "sign in", "credentials",
    "social security", "bank account", "credit card", "ssn"
]

THREAT_KEYWORDS = [
    "terminated", "legal action", "lawsuit", "permanently",
    "disabled", "unauthorized", "fraud", "violation"
]

SUSPICIOUS_TLDS = [".xyz", ".top", ".club", ".info", ".online", ".site", ".tk"]


def extract_features(text):
    """
    Converts raw email text into an 8-feature numeric vector.
    Returns a list of 8 numbers the Random Forest can train on.
    """
    if not isinstance(text, str):
        text = ""

    text_lower = text.lower()
    urls = re.findall(r'http[s]?://\S+', text_lower)

    # Feature 1 — urgency keywords present
    has_urgency = int(any(kw in text_lower for kw in URGENCY_KEYWORDS))

    # Feature 2 — credential keywords present
    has_credentials = int(any(kw in text_lower for kw in CREDENTIAL_KEYWORDS))

    # Feature 3 — number of URLs in the email
    url_count = len(urls)

    # Feature 4 — suspicious top-level domain in any URL
    has_suspicious_tld = int(any(tld in url for url in urls for tld in SUSPICIOUS_TLDS))

    # Feature 5 — sender domain mismatch (display name vs domain)
    # Looks for patterns like "PayPal <support@paypa1.com>"
    has_domain_mismatch = int(bool(re.search(
        r'[\w\s]+<[^>]+@(?!.*(?:gmail|yahoo|outlook|hotmail))[^>]+>', text_lower
    )))

    # Feature 6 — URL uses raw IP address instead of domain
    has_ip_url = int(bool(re.search(r'http[s]?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', text_lower)))

    # Feature 7 — exclamation mark count (urgency signal)
    exclamation_count = text.count("!")

    # Feature 8 — threat keywords present
    has_threats = int(any(kw in text_lower for kw in THREAT_KEYWORDS))

    return [
        has_urgency,
        has_credentials,
        url_count,
        has_suspicious_tld,
        has_domain_mismatch,
        has_ip_url,
        exclamation_count,
        has_threats,
    ]


print("Extracting features...")
X = df["text"].apply(extract_features).tolist()
y = df["label"].tolist()
print("  Features extracted for all emails.")


# TRAIN TEST SPLIT ------------------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,      # 80% train, 20% test
    random_state=42,    # fixed seed — same split every run
    stratify=y          # keeps phishing/legit ratio equal in both sets
)

print(f"\nSplit: {len(X_train)} training emails, {len(X_test)} test emails")


# TRAIN THE MODEL ------------------------------------------------------------------

print("\nTraining Random Forest classifier...")
model = RandomForestClassifier(
    n_estimators=100,   # 100 decision trees
    max_depth=10,       # prevents overfitting on small dataset
    random_state=42
)
model.fit(X_train, y_train)
print("  Training complete.")


# EVALUATE THE MODEL ----------------------------------------------------------------

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("\n── Evaluation Results ──────────────────────────────")
print(f"  Accuracy:  {accuracy * 100:.1f}%")
print("\n  Classification Report:")
print(classification_report(y_test, y_pred, target_names=["Legitimate", "Phishing"]))

# Feature importance
feature_names = [
    "urgency_keywords",
    "credential_keywords",
    "url_count",
    "suspicious_tld",
    "domain_mismatch",
    "ip_address_url",
    "exclamation_count",
    "threat_keywords",
]
importances = model.feature_importances_
print("  Feature Importance (for report):")
for name, score in sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True):
    bar = "█" * int(score * 40)
    print(f"    {name:<25} {bar} {score:.3f}")


# SAVE THE MODEL ------------------------------------------------------------------

os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
joblib.dump(model, MODEL_PATH)
print(f"\nModel saved to: {MODEL_PATH}")
print("Run python src/main.py to classify emails.")