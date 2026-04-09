# PhishDetect

> CS 455 – Artificial Intelligence | Spring 2026  
> Embry-Riddle Aeronautical University – Daytona Beach

A proof-of-concept machine learning classifier that analyzes email content to determine the likelihood that it is a phishing attempt. Built as an academic exploration of applying supervised learning to a real-world cybersecurity problem.

>**Scope note:** This is a proof-of-concept project built for educational purposes. It is not intended for production use or as a replacement for enterprise security tools.

## Team Members

| Name | GitHub Handle |
|------|--------------|
| Salvatore DeLuca | @Salvas |
| Devin Catledge | @cadetpenguin359 |
| Logan Velvet | @LoganVelvet |

## What It Does

PhishDetect takes a pasted email, extracts a set of features (urgency keywords, credential signals, URL patterns), and runs them through a trained Random Forest classifier. The model outputs a **calibrated confidence percentage** and a verdict: **PHISHING**, **UNCERTAIN**, or **LEGITIMATE**.  

- The **UNCERTAIN** verdict is based on a probability range of **41–60%**, which can be adjusted for stricter or more lenient classifications.  
- The model uses **probability calibration** to produce more reliable confidence scores, improving evaluation consistency.

## Results

| Metric | Score |
|--------|-------|
| Evaluation Accuracy | 93.3% |
| Precision | 0.94 |
| Recall | 1.00 |
| F1 Score | 0.97 |

Evaluated against 30 emails entirely separate from the training dataset.  

Evaluated against 30 emails entirely separate from the training dataset.  

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
│   ├── main.py          # Entry point - feature extraction and prediction
│   ├── train.py         # One-time training script, generates phishdetect.pkl
│   └── calibration.py   # Calibrates the Random Forest model
│   └── evaluate.py      # Runs evaluation against held-out test emails
│
├── data/
│   ├── emails.csv               # 100 labeled training emails
│   ├── evaluation_emails.csv    # 30 held-out evaluation emails
│   ├── evaluation_results.csv   # Results from evaluate.py
│
├── models/
│   └── phishdetect.pkl              # Trained Random Forest model
│   └── phishdetect_calibrated.pkl   # Calibrated model
│
└── tests/
    └── test_classifier.py   # 23 feature tests - all passing
```

> [`src/`](src/) &nbsp;·&nbsp; [`data/`](data/) &nbsp;·&nbsp; [`models/`](models/) &nbsp;·&nbsp; [`report/`](report/)

## How to Run

### Prerequisites

- Python 3.10 or higher
- pip

### 1. Clone the repository

```bash
git clone https://github.com/Salvas/phish-detect.git
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

Reads [`data/emails.csv`](data/emails.csv), trains the classifier, and saves the model to `models/phishdetect.pkl`.

### 4. Calibrate the model (run once)

```bash
python src/calibration.py
```

### 5. Run tests

```bash
pytest tests/test_classifier.py -v
```

### 6. Run evaluation

```bash
python src/evaluate.py
```

Runs the model against [`data/evaluation_emails.csv`](data/evaluation_emails.csv) and prints accuracy, precision, recall, F1, and a confusion matrix.

### 7. Run PhishDetect

```bash
python src/main.py
```

Paste your email content when prompted, type `END` on a new line, and the classifier will return a verdict.

## Example Output

```
=== PhishDetect ===
Paste email content below (type END on a new line when done):

Dear user, your account will be suspended. Click here to verify immediately.
END

Analyzing...

Signals detected:
  · Urgency keywords found
  · Credential keywords found
  · Suspicious URL count: 1

Confidence: 87.0% - Verdict: PHISHING
```

## Features Used by the Classifier

The model is trained on 8 hand-engineered features extracted from raw email text:

| Feature | Description |
|---------|-------------|
| `urgency_keywords` | Words like "urgent", "suspended", "immediately" |
| `credential_keywords` | Words like "password", "verify", "login" |
| `url_count` | Number of URLs found in the email body |
| `suspicious_tld` | URLs using unusual top-level domains (.xyz, .top etc.) |
| `domain_mismatch` | Display name domain differs from sender domain |
| `ip_address_url` | URL uses a raw IP instead of a domain name |
| `exclamation_count` | Number of exclamation marks (capped at 3) |
| `threat_keywords` | Words like "terminated", "legal action", "violation" |

## Dataset

Training and evaluation data sourced from two verified datasets:

- **[Nazario Phishing Corpus](https://www.kaggle.com/datasets/naserabdullahalam/phishing-email-dataset)** - verified real-world phishing emails
- **[Enron Email Dataset](https://www.kaggle.com/datasets/naserabdullahalam/phishing-email-dataset)** - legitimate business emails

Training set: 100 emails (55 phishing, 45 legitimate)
Evaluation set: 30 emails (15 phishing, 15 legitimate) - no overlap with training data

## Limitations

As a proof of concept, PhishDetect has known limitations:

- Trained on 100 emails - accuracy will vary on real-world volume
- No live URL scanning - relies purely on structural and keyword features
- Copy-paste input only - does not connect to email clients or parse .eml files
- Not tested against adversarial or obfuscated phishing content
- May struggle with non-English emails or heavily obfuscated spam

## Dependencies

See [`requirements.txt`](requirements.txt) for the full list. Key libraries:

- [`scikit-learn`](https://scikit-learn.org/) - Random Forest classifier
- [`pandas`](https://pandas.pydata.org/) - dataset loading and manipulation
- [`joblib`](https://joblib.readthedocs.io/) - saving and loading the trained model
- [`pytest`](https://docs.pytest.org/en/stable/) - unit testing

## License

This project is licensed under the MIT License. See [`LICENSE`](LICENSE) for details.
