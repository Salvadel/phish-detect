"""
PhishDetect - main.py
CS 455 - Spring 2026

Entry point for PhishDetect. Prompts the user to paste an email,
extracts features, loads the trained model, and returns a verdict.
"""

import os
import re
import joblib

# Paths to model and dataset
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "phishdetect_calibrated.pkl")

# FEATURE EXTRACTION ------------------------------------------------------------------------
# Must match exactly what train.py uses, same features, same order

URGENCY_KEYWORDS = [
    "urgent", "immediately", "suspended", "verify", "expire",
    "act now", "limited time", "account locked", "unusual activity",
    "confirm your", "click here", "update your", "validate", "asap", 
    "last chance", "within 24 hours", "final notice", "required action", 
    "attention required"
]

CREDENTIAL_KEYWORDS = [
    "password", "username", "login", "sign in", "credentials",
    "social security", "bank account", "credit card", "ssn", "pin",
    "account number", "security question", "verification code",
    "otp", "one-time password", "2fa", "two-factor authentication",
    "security code", "cvv", "card number", "routing number", 
    "account details"
]

THREAT_KEYWORDS = [
    "terminated", "legal action", "lawsuit", "permanently",
    "disabled", "unauthorized", "fraud", "violation", "suspend",
    "restrict", "compromised", "breach", "data leak", "identity theft",
    "account closure", "legal consequences", "report to authorities",
    "blocked", "deactivated", "penalty", "fine", "prosecution"
]

SUSPICIOUS_TLDS = [".xyz", ".top", ".club", ".info", ".online", ".site", ".tk", ".ru", ".cn", ".pw", ".gq", ".ml", ".cf"]

def extract_features(text):
    """
    Converts raw email text into a 8-feature numeric vector.
    Must stay in sync with train.py at all times.
    """
    if not isinstance(text, str):
        text = ""

    text_lower = text.lower()
    urls = [url.strip() for url in re.findall(r'http[s]?://[^\s)>\].,]+', text_lower)]

    has_urgency         = int(any(re.search(rf'\b{re.escape(kw)}\b' if " " not in kw else re.escape(kw), text_lower) for kw in URGENCY_KEYWORDS))
    has_credentials     = int(any(re.search(rf'\b{re.escape(kw)}\b' if " " not in kw else re.escape(kw), text_lower) for kw in CREDENTIAL_KEYWORDS))
    url_count           = len(urls)
    has_suspicious_tld = int(any(url.endswith(tld) or f"{tld}/" in url for url in urls for tld in SUSPICIOUS_TLDS))
    has_custom_domain_sender = int(bool(re.search(r'[\w\s]+<[^>]+@(?!gmail\.com|yahoo\.com|outlook\.com|hotmail\.com)[^>]+>', text_lower ))) 
    has_ip_url          = int(bool(re.search(r'http[s]?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', text_lower)))
    exclamation_count   = min(text.count("!"), 3)
    has_threats         = int(any(re.search(rf'\b{re.escape(kw)}\b' if " " not in kw else re.escape(kw), text_lower) for kw in THREAT_KEYWORDS))

    return [
        has_urgency,
        has_credentials,
        url_count,
        has_suspicious_tld,
        has_custom_domain_sender,
        has_ip_url,
        exclamation_count,
        has_threats,
    ]

def get_signals(text):
    """
    Returns a human-readable list of signals detected in the email.
    Used to explain the verdict to the user.
    """
    text_lower = text.lower()
    urls = re.findall(r'http[s]?://\S+', text_lower)
    signals = []

    if any(kw in text_lower for kw in URGENCY_KEYWORDS):
        signals.append("Urgency keywords detected")
    if any(kw in text_lower for kw in CREDENTIAL_KEYWORDS):
        signals.append("Credential-related keywords detected")
    if len(urls) > 0:
        signals.append(f"URLs found in body: {len(urls)}")
    if any(tld in url for url in urls for tld in SUSPICIOUS_TLDS):
        signals.append("Suspicious top-level domain detected in URL")
    if re.search(r'[\w\s]+<[^>]+@(?!.*(?:gmail|yahoo|outlook|hotmail))[^>]+>', text_lower):
        signals.append("Sender domain mismatch detected")
    if re.search(r'http[s]?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', text_lower):
        signals.append("Raw IP address used in URL")
    if text.count("!") > 1:
        signals.append(f"High exclamation mark count: {text.count('!')}")
    if any(kw in text_lower for kw in THREAT_KEYWORDS):
        signals.append("Threat language detected")

    return signals if signals else ["No strong signals detected"]

def get_verdict(confidence):
    """Returns verdict string based on confidence threshold."""
    if confidence >= 0.60:
        return "PHISHING"
    elif confidence <= 0.40:
        return "LEGITIMATE"
    else:
        return "UNCERTAIN"

def print_banner():
    print("\n" + "=" * 50)
    print("  PhishDetect - Phishing Email Classifier")
    print("=" * 50)

def get_email_input():
    """Prompts user to paste email content, reads until END sentinel."""
    print("\nPaste email content below.")
    print("Type END on a new line when finished:\n")
    lines = []
    while True:
        try:
            line = input()
            if line.strip().upper() == "END":
                break
            lines.append(line)
        except EOFError:
            break
    return "\n".join(lines)

# MAIN PROGRAM ------------------------------------------------------------------

def main():
    print_banner()

    # Load trained model
    if not os.path.exists(MODEL_PATH):
        print("\n[ERROR] Model not found. Run python src/train.py first.")
        return

    model = joblib.load(MODEL_PATH)

    while True:
        email_text = get_email_input()

        if not email_text.strip():
            print("\n[!] No input detected. Please paste an email.")
            continue

        # Extract features and predict
        features  = extract_features(email_text)
        proba     = model.predict_proba([features])[0]
        confidence = proba[1]  # probability of being phishing
        verdict   = get_verdict(confidence)
        signals   = get_signals(email_text)

        # Display results
        print("\n" + "─" * 50)
        print("  ANALYSIS RESULTS")
        print("─" * 50)

        print("\n  Signals detected:")
        for signal in signals:
            print(f"    · {signal}")

        print(f"\n  Confidence : {confidence * 100:.1f}%")
        print(f"  Verdict    : {verdict}")

        if verdict == "PHISHING":
            print("\n  This email shows signs of phishing.")
            print("     Do not click links or provide credentials.")
        elif verdict == "UNCERTAIN":
            print("\n  ?  This email has some suspicious signals.")
            print("     Proceed with caution.")
        else:
            print("\n  This email does not appear to be phishing.")

        print("\n" + "─" * 50)

        # Ask to run again
        print("\nAnalyze another email? (y/n): ", end="")
        again = input().strip().lower()
        if again != "y":
            print("\nExiting PhishDetect. Stay safe!\n")
            break

if __name__ == "__main__":
    main()