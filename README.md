# PhishDetect

> CS 455 – Artificial Intelligence | Spring 2026  
> Embry-Riddle Aeronautical University – Daytona Beach

A proof-of-concept machine learning classifier that analyzes email content to determine the likelihood it is a phishing attempt. Built as an academic exploration of applying supervised learning to a real-world cybersecurity problem.
 
**Scope note:** This is a proof-of-concept project built for educational purposes. It is not intended for production use or as a replacement for enterprise security tools.

---

## Team Members

| Name | GitHub Handle |
|------|--------------|
| Salvatore DeLuca | @(your handle) |
| Devin Catledge | @(your handle) |
| Logan Velvet | @(your handle) |

---

## What It Does

PhishDetect takes a pasted email, extracts a set of features (URLs, sender analysis, keyword signals), and runs them through a trained Random Forest classifier. It returns a confidence percentage and a verdict: **PHISHING**, **UNCERTAIN**, or **LEGITIMATE**.

---

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
│   ├── main.py                  # Entry point
│   ├── email_parser.py          # Extracts raw features from email text
│   ├── feature_extractor.py     # Converts features into ML input vector
│   └── model.py                 # Loads trained model, runs prediction
│
├── data/
│   ├── phishing_samples/        # Sample phishing emails for testing
│   └── legit_samples/           # Legitimate emails for comparison
│
├── models/
│   └── phishdetect.pkl          # Trained Random Forest model
│
├── docs/
│   └── diagrams/                # Architecture diagrams
│
├── report/
│   └── CS455_Final_Report.pdf
│
└── tests/
    └── test_classifier.py       # Basic classifier tests
```

[`src/`](src/) &nbsp;·&nbsp; [`data/`](data/) &nbsp;·&nbsp; [`models/`](models/) &nbsp;·&nbsp; [`docs/`](docs/) &nbsp;·&nbsp; [`report/`](report/)

---

## How to Run

No Python installation required. Download the pre-built executable for your operating system from the [Releases](https://github.com/YOURUSERNAME/phish-detect/releases/latest) tab.

| Operating System | File to download |
|-----------------|-----------------|
| Windows | `PhishDetect.exe` |
| Mac / Linux | `PhishDetect` |

### Windows

1. Download `PhishDetect.exe` from the [Releases](https://github.com/YOURUSERNAME/phish-detect/releases/latest) tab
2. Double-click `PhishDetect.exe` to run

### Mac / Linux

1. Download `PhishDetect` from the [Releases](https://github.com/YOURUSERNAME/phish-detect/releases/latest) tab
2. Open a terminal in the download folder and make it executable:

```bash
chmod +x PhishDetect
./PhishDetect
```

> **Note:** On Mac, if you see a security warning, go to **System Settings → Privacy & Security** and click **Open Anyway**.

---

## Example Output

```
=== PhishDetect ===
Paste email content below (type END on a new line when done):

...

Analyzing email...

Top signals detected:
  · Sender domain mismatch
  · Urgency keywords found in body
  · Suspicious URL flagged by VirusTotal

Confidence: 87% — Verdict: PHISHING
```

---

## Limitations

As a proof of concept, PhishDetect has known limitations:

- Trained on a small dataset — accuracy may degrade on unusual phishing styles
- VirusTotal API requires an internet connection and a free API key
- Not tested against adversarial inputs or obfuscated phishing content
- Copy-paste only — does not parse .eml files or connect to email clients

---

## Dependencies

See [`requirements.txt`](requirements.txt) for the full list. Key libraries:

- [`scikit-learn`](https://scikit-learn.org/) — Random Forest classifier
- [`requests`](https://docs.python-requests.org/) — VirusTotal API calls
- [`python-dotenv`](https://pypi.org/project/python-dotenv/) — API key management
- [`pytest`](https://docs.pytest.org/en/stable/) — unit testing

---

## Documentation

- [`docs/diagrams/`](docs/diagrams/) — Architecture and pipeline diagrams
- [`report/CS455_Final_Report.pdf`](report/CS455_Final_Report.pdf) — Final project report

---

## License

This project is licensed under the MIT License. See [`LICENSE`](LICENSE) for details.
