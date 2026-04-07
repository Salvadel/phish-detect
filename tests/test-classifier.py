"""
PhishDetect - test_classifier.py
CS 455 - Spring 2026

Basic unit tests for the PhishDetect classifier.
Tests cover feature extraction correctness and model prediction.

Must be run with Pytest from the project root directory:
    pytest tests/test-classifier.py
"""

import os
import sys
import joblib
import pytest

# Add src/ to path so we can import from main.py
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from main import extract_features, get_verdict, get_signals

# PATH TO MODEL --------------------------------------------------------------

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "phishdetect.pkl")

# FEATURE EXTRACTION TEST ----------------------------------------------------
class TestFeatureExtraction:

    def test_urgency_keywords_detected(self):
        """Email with urgency language should flag urgency feature."""
        email = "Your account has been suspended. Please verify immediately."
        features = extract_features(email)
        assert features[0] == 1, "urgency_keywords should be 1"

    def test_no_urgency_in_normal_email(self):
        """Normal email should not flag urgency feature."""
        email = "Hi John, here are the meeting notes from today."
        features = extract_features(email)
        assert features[0] == 0, "urgency_keywords should be 0"

    def test_credential_keywords_detected(self):
        """Email asking for credentials should flag credential feature."""
        email = "Please enter your username and password to continue."
        features = extract_features(email)
        assert features[1] == 1, "credential_keywords should be 1"

    def test_url_count_correct(self):
        """URL count should match number of URLs in email."""
        email = "Click here: http://example.com and here: http://another.com"
        features = extract_features(email)
        assert features[2] == 2, "url_count should be 2"

    def test_no_urls_in_plain_email(self):
        """Email with no URLs should have url_count of 0."""
        email = "Hi, just checking in. Hope you are doing well."
        features = extract_features(email)
        assert features[2] == 0, "url_count should be 0"

    def test_ip_address_url_detected(self):
        """Email with raw IP URL should flag ip_address_url feature."""
        email = "Login here: http://192.168.1.1/login"
        features = extract_features(email)
        assert features[5] == 1, "ip_address_url should be 1"

    def test_threat_keywords_detected(self):
        """Email with threat language should flag threat feature."""
        email = "Your account will be terminated due to a violation."
        features = extract_features(email)
        assert features[7] == 1, "threat_keywords should be 1"

    def test_exclamation_count_capped_at_3(self):
        """Exclamation count should be capped at 3."""
        email = "Act now!!!!!!!!!!!!"
        features = extract_features(email)
        assert features[6] <= 3, "exclamation_count should be capped at 3"

    def test_empty_email_returns_zeros(self):
        """Empty input should return all zeros without crashing."""
        features = extract_features("")
        assert features == [0, 0, 0, 0, 0, 0, 0, 0], "empty email should return all zeros"

    def test_feature_vector_length(self):
        """Feature vector should always have exactly 8 features."""
        email = "Some random email text."
        features = extract_features(email)
        assert len(features) == 8, "feature vector must have exactly 8 elements"


# VERDICT THREASHOLD TESTS ---------------------------------------------------------

class TestVerdictThresholds:

    def test_high_confidence_is_phishing(self):
        """Confidence >= 60% should return PHISHING."""
        assert get_verdict(0.60) == "PHISHING"
        assert get_verdict(0.95) == "PHISHING"

    def test_medium_confidence_is_uncertain(self):
        """Confidence between 41–59% should return UNCERTAIN."""
        assert get_verdict(0.41) == "UNCERTAIN"
        assert get_verdict(0.55) == "UNCERTAIN"

    def test_low_confidence_is_legitimate(self):
        """Confidence below 40% should return LEGITIMATE."""
        assert get_verdict(0.39) == "LEGITIMATE"
        assert get_verdict(0.10) == "LEGITIMATE"

    def test_exact_boundary_60(self):
        """Exactly 60% should be PHISHING not UNCERTAIN."""
        assert get_verdict(0.60) == "PHISHING"

    def test_exact_boundary_40(self):
        """Exactly 40% should be LEGITIMATE not UNCERTAIN."""
        assert get_verdict(0.40) == "LEGITIMATE"


# SIGNAL DETECTION TESTS ---------------------------------------------------------

class TestSignalDetection:

    def test_signals_returned_for_phishing_email(self):
        """Phishing email should return at least one signal."""
        email = "URGENT: verify your password immediately! http://192.168.1.1"
        signals = get_signals(email)
        assert len(signals) > 0
        assert signals != ["No strong signals detected"]

    def test_no_signals_for_clean_email(self):
        """Clean email should return no strong signals."""
        email = "Hi, attached are the meeting notes. Let me know if you have questions."
        signals = get_signals(email)
        assert signals == ["No strong signals detected"]


# MODEL INTEGRATION TESTS ---------------------------------------------------------

class TestModelIntegration:

    def test_model_file_exists(self):
        """Trained model file should exist at models/phishdetect.pkl."""
        assert os.path.exists(MODEL_PATH), "phishdetect.pkl not found — run train.py first"

    def test_model_loads_successfully(self):
        """Model should load without errors."""
        model = joblib.load(MODEL_PATH)
        assert model is not None

    def test_model_predicts_on_valid_input(self):
        """Model should return a prediction for a valid feature vector."""
        model = joblib.load(MODEL_PATH)
        features = extract_features("Your account is suspended. Verify now.")
        prediction = model.predict([features])
        assert prediction[0] in [0, 1], "prediction must be 0 or 1"

    def test_model_returns_probability(self):
        """Model should return probabilities between 0 and 1."""
        model = joblib.load(MODEL_PATH)
        features = extract_features("Click here to verify your account.")
        proba = model.predict_proba([features])[0]
        assert 0.0 <= proba[0] <= 1.0
        assert 0.0 <= proba[1] <= 1.0
        assert abs(proba[0] + proba[1] - 1.0) < 0.001, "probabilities must sum to 1"

    def test_obvious_phishing_classified_correctly(self):
        """A clearly phishing email should be classified as phishing."""
        model = joblib.load(MODEL_PATH)
        email = "URGENT: Your account suspended! Verify password immediately! http://192.168.1.1/login terminated!!!"
        features = extract_features(email)
        proba = model.predict_proba([features])[0]
        assert proba[1] >= 0.5, "obvious phishing email should have >= 50% phishing confidence"

    def test_obvious_legit_classified_correctly(self):
        """A clearly legitimate email should not be classified as phishing."""
        model = joblib.load(MODEL_PATH)
        email = "Hi team, the quarterly report is attached. Please review before Friday."
        features = extract_features(email)
        proba = model.predict_proba([features])[0]
        assert proba[1] < 0.70, "clean email should not have high phishing confidence"