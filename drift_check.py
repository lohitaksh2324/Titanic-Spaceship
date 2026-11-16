"""
Data Drift Detection Script (Bonus Requirement)
CSL236 End-Term Project

Compares mean and standard deviation of logged prediction inputs against
baseline training data distributions to detect covariate shift / data drift.
"""

import json
import os
import pandas as pd
import numpy as np


def run_drift_check(train_path="data/train.csv", log_path="logs/predictions.log", threshold_std_diff=2.0):
    print("=" * 65)
    print(" SPACESHIP TITANIC — DATA DRIFT MONITORING REPORT")
    print("=" * 65)

    if not os.path.exists(train_path):
        print(f"Error: Training dataset not found at {train_path}")
        return

    if not os.path.exists(log_path) or os.path.getsize(log_path) == 0:
        print(f"Warning: No prediction logs found at {log_path}. Generate predictions first.")
        return

    # Load baseline
    train_df = pd.read_csv(train_path)

    # Load logged inputs
    logged_records = []
    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entry = json.loads(line)
                    logged_records.append(entry["input"])
                except Exception:
                    continue

    if len(logged_records) == 0:
        print("No valid logged requests found.")
        return

    logged_df = pd.DataFrame(logged_records)
    print(f"Baseline Training Samples : {len(train_df):,}")
    print(f"Logged Inference Requests : {len(logged_df):,}\n")

    num_features = ["Age", "RoomService", "FoodCourt", "ShoppingMall", "Spa", "VRDeck"]

    drift_report = []
    drift_detected = False

    for col in num_features:
        if col in logged_df.columns:
            train_col = pd.to_numeric(train_df[col], errors="coerce").dropna()
            logged_col = pd.to_numeric(logged_df[col], errors="coerce").dropna()

            if len(logged_col) == 0:
                continue

            b_mean, b_std = train_col.mean(), train_col.std()
            l_mean, l_std = logged_col.mean(), logged_col.std()

            # Z-score of mean shift relative to baseline standard error
            mean_diff = abs(l_mean - b_mean)
            z_score = mean_diff / (b_std if b_std > 0 else 1.0)
            status = "DRIFT ⚠️" if z_score > threshold_std_diff else "STABLE ✅"
            if z_score > threshold_std_diff:
                drift_detected = True

            drift_report.append({
                "Feature": col,
                "Base Mean": round(b_mean, 2),
                "Log Mean": round(l_mean, 2),
                "Base Std": round(b_std, 2),
                "Log Std": round(l_std, 2),
                "Shift (Z)": round(z_score, 2),
                "Status": status,
            })

    report_df = pd.DataFrame(drift_report)
    print(report_df.to_string(index=False))
    print("\n" + "=" * 65)

    # Check Categorical distribution
    if "HomePlanet" in logged_df.columns:
        print("HomePlanet Distribution Check:")
        base_hp = (train_df["HomePlanet"].value_counts(normalize=True) * 100).round(1).to_dict()
        log_hp = (logged_df["HomePlanet"].value_counts(normalize=True) * 100).round(1).to_dict()
        print(f"  Baseline: {base_hp}")
        print(f"  Logged  : {log_hp}")

    print("=" * 65)
    if drift_detected:
        print("ALERT: Input distribution shift detected! Recommend model re-evaluation.")
    else:
        print("SUCCESS: All feature distributions are within acceptable stability bounds.")
    print("=" * 65)


if __name__ == "__main__":
    run_drift_check()
