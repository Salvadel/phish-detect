# PhishDetect

A proof-of-concept machine learning classifier that analyzes email content to determine the likelihood it is a phishing attempt. Built as an academic exploration of applying supervised learning to a real-world cybersecurity problem.

> **Scope note:** This is a proof-of-concept project built for educational purposes. It is not intended for production use or as a replacement for enterprise security tools.

---

## Team Members

| Name | GitHub Handle |
|------|--------------|
| Salvatore DeLuca | @Salvas |
| Devin Catledge | @cadetpenguin359 |
| Logan Velvet | @LoganVelvet |

## What It Does

PhishDetect takes a pasted email, extracts a small set of features (URL count, urgency keywords, sender signals), and runs them through a trained Random Forest classifier. It returns a confidence percentage and a verdict: **PHISHING**, **UNCERTAIN**, or **LEGITIMATE**.

## Project Structure

```
phish-detect/
│
├── README.md
├── LICENSE
├── .gitignore
├── requirements.txt
│
├── src/
│   ├── main.py          # Entry point — parsing, feature extraction, prediction
│   └── train.py         # One-time training script, generates phishdetect.pkl
│
├── data/
│   └── emails.csv       # ~60 labeled emails (0 = legitimate, 1 = phishing)
│
├── models/
│   └── phishdetect.pkl  # Trained Random Forest model
│
├── report/
│   └── CS455_Final_Report.pdf
│
└── tests/
    └── test_classifier.py
```

> [`src/`](src/) &nbsp;·&nbsp; [`data/`](data/) &nbsp;·&nbsp; [`models/`](models/) &nbsp;·&nbsp; [`report/`](report/)

## How to Run

### Prerequisites

- Python 3.10 or higher
- pip

### 1. Clone the repository

```bash
git clone https://github.com/YOURUSERNAME/phish-detect.git
cd phish-detect
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Train the model (run once)

```bash
python src/train.py
```

This reads [`data/emails.csv`](data/emails.csv), trains the classifier, and saves the model to `models/phishdetect.pkl`.

### 4. Run PhishDetect

```bash
python src/main.py
```

Paste your email content when prompted, type `END` on a new line, and the classifier will return a verdict.

### 5. Run tests

```bash
pytest tests/
```

## Example Output

```
=== PhishDetect ===
Paste email content below (type END on a new line when done):

Dear user, your account will be suspended. Click here to verify immediately.
END

Analyzing...

Signals detected:
  · Urgency keywords found
  · Suspicious URL count: 2
  · Sender domain mismatch

Confidence: 87% — Verdict: PHISHING
```

## Features Used by the Classifier

The model is trained on 8 hand-engineered features extracted from raw email text:

| Feature | Description |
|---------|-------------|
| `contains_urgency_keywords` | Words like "urgent", "suspended", "immediately" |
| `contains_credential_keywords` | Words like "password", "verify", "login" |
| `url_count` | Number of URLs found in the email body |
| `has_suspicious_tld` | URLs using unusual top-level domains |
| `sender_domain_mismatch` | Display name domain differs from sender domain |
| `has_ip_address_url` | URL uses a raw IP instead of a domain name |
| `exclamation_mark_count` | Number of exclamation marks in the body |
| `contains_threat_keywords` | Words like "terminated", "legal action", "suspended" |

## Limitations

As a proof of concept, PhishDetect has known limitations:

- Trained on ~60 emails — accuracy will vary on real-world volume
- No live URL scanning — relies purely on structural and keyword features
- Copy-paste input only — does not connect to email clients or parse .eml files
- Not tested against adversarial or obfuscated phishing content

## Dependencies

See [`requirements.txt`](requirements.txt) for the full list. Key libraries:

- [`scikit-learn`](https://scikit-learn.org/) — Random Forest classifier
- [`pandas`](https://pandas.pydata.org/) — dataset loading and manipulation
- [`joblib`](https://joblib.readthedocs.io/) — saving and loading the trained model
- [`pytest`](https://docs.pytest.org/en/stable/) — unit testing

## License

This project is licensed under the MIT License. See [`LICENSE`](LICENSE) for details.
