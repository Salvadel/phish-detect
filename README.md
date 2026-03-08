# Phishing Email Detection Expert System

> CS 455 - Artificial Intelligence | Spring 2026  
> Embry-Riddle Aeronautical University - Daytona Beach

A rule-based expert system that analyzes email content and metadata to determine whether an email is likely a phishing attempt, legitimate, or uncertain.

## Team Members

| Name | GitHub Handle |
|------|--------------|
| Salvatore DeLuca | @salvadel |
| Devin Catledge | @(your handle) |
| Logan Velvet | @(your handle) |

## Project Structure

```
phishing-expert-system/
│
├── README.md
├── LICENSE
├── .gitignore
├── requirements.txt
│
├── src/
│   ├── main.py             
│   ├── rules.py             
│   ├── engine.py            
│   └── email_parser.py      
│
├── data/
│   ├── phishing_samples/   
│   └── legit_samples/      
│
├── docs/
│   ├── ontology.md          
│   ├── competency_questions.md
│   └── diagrams/           
│
├── report/
│   └── CS455_Final_Report.pdf
│
└── tests/
    └── test_rules.py        
```

> 📁 [`src/`](src/) &nbsp;·&nbsp;&nbsp;[`data/`](data/) &nbsp;·&nbsp;[`docs/`](docs/)&nbsp;·&nbsp;[`report/`](report/)&nbsp;·&nbsp;[`tests/`](tests/)&nbsp;

## How to Run

No Python installation required. Download the pre-built executable for your operating system from the [Releases](https://github.com/salvadel/phishing-expert-system/releases/latest) tab.

| Operating System | File to download |
|-----------------|-----------------|
| Windows | `PhishDetect.exe` |
| Mac / Linux | `PhishDetect` |

### Windows

1. Download `PhishDetect.exe` from the [Releases](https://github.com/salvadel/phishing-expert-system/releases/latest) tab
2. Double-click `PhishDetect.exe` to run

### Mac / Linux

1. Download `PhishDetect` from the [Releases](https://github.com/salvadel/phishing-expert-system/releases/latest) tab
2. Open a terminal in the download folder and make it executable:

```bash
chmod +x PhishDetect
./PhishDetect
```

## Dependencies

See [`requirements.txt`](requirements.txt) for the full list. Key libraries:

- [`experta`](https://experta.readthedocs.io/en/latest/) — inference engine for the expert system
- [`pytest`](https://docs.pytest.org/en/stable/) — unit testing

## Documentation

- [`docs/ontology.md`](docs/ontology.md) — Full ontology write-up
- [`docs/competency_questions.md`](docs/competency_questions.md) — Competency questions used for evaluation
- [`docs/diagrams/`](docs/diagrams/) — Architecture and hierarchy diagrams
- [`report/CS455_Final_Report.pdf`](report/CS455_Final_Report.pdf) — Final project report

## License

This project is licensed under the MIT License. See [`LICENSE`](LICENSE) for details.
