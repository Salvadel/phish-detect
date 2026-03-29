"""
PhishDetect - evaluate.py
CS 455 - Spring 2026

Automatically selects 20 evaluation emails (11 phishing, 9 legitimate)
from emails.csv and runs them through the trained model.
Outputs a results table you can copy into your report.
"""

import os
import sys
import joblib 
import pandas as pd

# Add src/ to path so we can import from main.py
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from main import extract_features, get_verdict

# ── PATHS ─────────────────────────────────────────────────────────────────────

DATA_PATH  = os.path.join(os.path.dirname(__file__), "..", "data", "emails.csv")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "phishdetect.pkl")

# ── LOAD DATA AND MODEL ───────────────────────────────────────────────────────

df    = pd.read_csv(DATA_PATH)
model = joblib.load(MODEL_PATH)

# Sample 11 phishing and 9 legitimate emails
phishing  = df[df["label"] == 1].sample(n=11, random_state=42)
legit     = df[df["label"] == 0].sample(n=9,  random_state=42)
test_df   = pd.concat([phishing, legit]).reset_index(drop=True)

# ── RUN EVALUATION ────────────────────────────────────────────────────────────

print("\n" + "=" * 75)
print("  PhishDetect — Evaluation Results")
print("=" * 75)
print(f"  {'#':<4} {'Actual':<12} {'Predicted':<12} {'Confidence':<12} {'Correct':<8} Preview")
print("-" * 75)

correct   = 0
tp = tn = fp = fn = 0

results = []

for i, row in test_df.iterrows():
    text          = row["text"]
    actual_label  = int(row["label"])
    features      = extract_features(text)
    proba         = model.predict_proba([features])[0]
    confidence    = proba[1]
    verdict       = get_verdict(confidence)
    predicted_label = 1 if verdict == "PHISHING" else (0 if verdict == "LEGITIMATE" else -1)

    actual_str    = "Phishing"   if actual_label == 1 else "Legitimate"
    predicted_str = verdict
    is_correct    = (actual_label == 1 and verdict == "PHISHING") or \
                    (actual_label == 0 and verdict == "LEGITIMATE")
    correct_str   = "✅" if is_correct else "❌"
    preview       = str(text)[:35].replace("\n", " ") + "..."

    if is_correct:
        correct += 1
    if actual_label == 1 and verdict == "PHISHING":
        tp += 1
    elif actual_label == 0 and verdict == "LEGITIMATE":
        tn += 1
    elif actual_label == 0 and verdict == "PHISHING":
        fp += 1
    elif actual_label == 1 and verdict == "LEGITIMATE":
        fn += 1

    print(f"  {i+1:<4} {actual_str:<12} {predicted_str:<12} {confidence*100:<11.1f}% {correct_str:<8} {preview}")

    results.append({
        "Email #":      i + 1,
        "Actual":       actual_str,
        "Predicted":    predicted_str,
        "Confidence":   f"{confidence*100:.1f}%",
        "Correct":      "Yes" if is_correct else "No",
        "Preview":      preview
    })

# ── SUMMARY METRICS ───────────────────────────────────────────────────────────

accuracy  = correct / len(test_df)
precision = tp / (tp + fp) if (tp + fp) > 0 else 0
recall    = tp / (tp + fn) if (tp + fn) > 0 else 0
f1        = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

print("\n" + "=" * 75)
print("  SUMMARY METRICS")
print("=" * 75)
print(f"  Total emails tested : {len(test_df)}")
print(f"  Correct predictions : {correct}")
print(f"  Accuracy            : {accuracy*100:.1f}%")
print(f"  Precision           : {precision:.2f}")
print(f"  Recall              : {recall:.2f}")
print(f"  F1 Score            : {f1:.2f}")

print("\n  Confusion Matrix:")
print(f"  ┌─────────────────────────────┐")
print(f"  │              Predicted      │")
print(f"  │         Phishing  Legit     │")
print(f"  │ Actual                      │")
print(f"  │ Phishing   {tp:<6}   {fn:<6}   │")
print(f"  │ Legit      {fp:<6}   {tn:<6}   │")
print(f"  └─────────────────────────────┘")
print(f"\n  TP={tp}  TN={tn}  FP={fp}  FN={fn}")

# ── EXPORT TO CSV ─────────────────────────────────────────────────────────────

results_df = pd.DataFrame(results)
out_path   = os.path.join(os.path.dirname(__file__), "..", "data", "evaluation_results.csv")
results_df.to_csv(out_path, index=False)
print(f"\n  Results saved to: data/evaluation_results.csv")
print("  Copy this into your Google Sheet for the report.\n")