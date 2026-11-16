"""
Spaceship Titanic — Training Script with MLflow Tracking
CSL236 End-Term Project
"""

import os
import argparse
import joblib
import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score


class SpaceshipTitanicPipeline:
    """End-to-end inference pipeline bundling preprocessing, encoders, scaler, and classifier."""

    def __init__(self, model, label_encoders, scaler, feature_cols, spend_fences):
        self.model = model
        self.label_encoders = label_encoders
        self.scaler = scaler
        self.feature_cols = feature_cols
        self.spend_fences = spend_fences

    def preprocess_df(self, raw_df: pd.DataFrame) -> pd.DataFrame:
        df = raw_df.copy()

        # 1. Feature Extraction
        cabin_split = df["Cabin"].astype(str).str.split("/", expand=True)
        df["Deck"] = cabin_split[0].replace({"nan": "F", "None": "F"}).fillna("F")
        df["CabinNum"] = pd.to_numeric(cabin_split[1], errors="coerce").fillna(427.0)
        df["Side"] = cabin_split[2].replace({"nan": "S", "None": "S"}).fillna("S")

        # Group features
        df["GroupId"] = df["PassengerId"].astype(str).str.split("_").str[0]
        group_sizes = df.groupby("GroupId")["PassengerId"].transform("count")
        df["GroupSize"] = group_sizes.fillna(1)
        df["IsAlone"] = (df["GroupSize"] == 1).astype(int)

        # 2. Imputation & Boolean conversion
        for col in ["CryoSleep", "VIP"]:
            df[col] = df[col].map({"True": 1, "False": 0, True: 1, False: 0, 1: 1, 0: 0})
            df[col] = df[col].fillna(0).astype(int)

        for col in ["HomePlanet", "Destination", "Deck", "Side"]:
            df[col] = df[col].fillna("Earth" if col == "HomePlanet" else "TRAPPIST-1e" if col == "Destination" else "F" if col == "Deck" else "S")

        # Amenity spending
        spend_cols = ["RoomService", "FoodCourt", "ShoppingMall", "Spa", "VRDeck"]
        for col in spend_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            # If CryoSleep is True, spending is 0
            df.loc[df["CryoSleep"] == 1, col] = df.loc[df["CryoSleep"] == 1, col].fillna(0)
            df[col] = df[col].fillna(0.0)

        df["TotalSpend"] = df[spend_cols].sum(axis=1)
        df["LuxurySpend"] = df["Spa"] + df["VRDeck"]
        df["HasSpend"] = (df["TotalSpend"] > 0).astype(int)

        df["Age"] = pd.to_numeric(df["Age"], errors="coerce").fillna(27.0)
        df["AgeGroup"] = pd.cut(
            df["Age"],
            bins=[-1, 12, 18, 35, 60, 100],
            labels=["Child", "Teen", "YoungAdult", "Adult", "Senior"],
        ).astype(str)

        # Outlier Capping
        for col in spend_cols:
            fence = self.spend_fences.get(col, 2000.0)
            df[col] = df[col].clip(upper=fence)

        # Categorical Encoding
        cat_cols = ["HomePlanet", "Destination", "Deck", "Side", "AgeGroup"]
        for col in cat_cols:
            le = self.label_encoders[col]
            # Use safe mapping with default for unseen values
            classes = {cls: idx for idx, cls in enumerate(le.classes_)}
            df[col] = df[col].astype(str).map(classes).fillna(0).astype(int)

        return df[self.feature_cols]

    def predict(self, raw_df: pd.DataFrame) -> np.ndarray:
        features_df = self.preprocess_df(raw_df)
        scaled_features = self.scaler.transform(features_df)
        return self.model.predict(scaled_features)

    def predict_proba(self, raw_df: pd.DataFrame) -> np.ndarray:
        features_df = self.preprocess_df(raw_df)
        scaled_features = self.scaler.transform(features_df)
        return self.model.predict_proba(scaled_features)


def prepare_training_data(data_path="data/train.csv"):
    df = pd.read_csv(data_path)

    # Cabin components
    cabin_split = df["Cabin"].str.split("/", expand=True)
    df["Deck"] = cabin_split[0].fillna("F")
    df["CabinNum"] = pd.to_numeric(cabin_split[1], errors="coerce")
    df["CabinNum"] = df["CabinNum"].fillna(df["CabinNum"].median())
    df["Side"] = cabin_split[2].fillna("S")

    # Group components
    df["GroupId"] = df["PassengerId"].str.split("_").str[0]
    df["GroupSize"] = df.groupby("GroupId")["PassengerId"].transform("count")
    df["IsAlone"] = (df["GroupSize"] == 1).astype(int)

    # Boolean mapping & imputation
    for col in ["CryoSleep", "VIP"]:
        df[col] = df[col].map({"True": 1, "False": 0, True: 1, False: 0})
        df[col] = df[col].fillna(0).astype(int)

    for col in ["HomePlanet", "Destination", "Deck", "Side"]:
        df[col] = df[col].fillna(df[col].mode()[0])

    spend_cols = ["RoomService", "FoodCourt", "ShoppingMall", "Spa", "VRDeck"]
    for col in spend_cols:
        df.loc[df["CryoSleep"] == 1, col] = df.loc[df["CryoSleep"] == 1, col].fillna(0)
        df[col] = df[col].fillna(df[col].median())

    df["TotalSpend"] = df[spend_cols].sum(axis=1)
    df["LuxurySpend"] = df["Spa"] + df["VRDeck"]
    df["HasSpend"] = (df["TotalSpend"] > 0).astype(int)

    df["Age"] = df["Age"].fillna(df["Age"].median())
    df["AgeGroup"] = pd.cut(
        df["Age"],
        bins=[-1, 12, 18, 35, 60, 100],
        labels=["Child", "Teen", "YoungAdult", "Adult", "Senior"],
    ).astype(str)

    # Outlier capping fences
    spend_fences = {}
    for col in spend_cols:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        fence = q3 + 3.0 * iqr
        spend_fences[col] = float(fence)
        df[col] = df[col].clip(upper=fence)

    # Encoders
    cat_cols = ["HomePlanet", "Destination", "Deck", "Side", "AgeGroup"]
    label_encoders = {}
    for col in cat_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        label_encoders[col] = le

    drop_cols = ["PassengerId", "Name", "Cabin", "GroupId", "Transported"]
    feature_cols = [c for c in df.columns if c not in drop_cols]

    X = df[feature_cols].copy()
    y = df["Transported"].astype(int).values

    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y, label_encoders, scaler, feature_cols, spend_fences


def train_single_run(model_type, n_estimators, max_depth, learning_rate=0.05, save_model=False):
    X_scaled, y, label_encoders, scaler, feature_cols, spend_fences = prepare_training_data()
    X_train, X_val, y_train, y_val = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42, stratify=y
    )

    if model_type == "random_forest":
        model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=42,
            n_jobs=-1,
        )
    else:
        model = XGBClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            learning_rate=learning_rate,
            eval_metric="logloss",
            random_state=42,
        )

    with mlflow.start_run(run_name=f"{model_type}_n{n_estimators}_d{max_depth}"):
        model.fit(X_train, y_train)
        val_pred = model.predict(X_val)
        val_proba = model.predict_proba(X_val)[:, 1]

        acc = float(accuracy_score(y_val, val_pred))
        prec = float(precision_score(y_val, val_pred))
        rec = float(recall_score(y_val, val_pred))
        f1 = float(f1_score(y_val, val_pred))
        auc = float(roc_auc_score(y_val, val_proba))

        # Log parameters
        mlflow.log_param("algorithm", model_type)
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("max_depth", max_depth)
        mlflow.log_param("learning_rate", learning_rate if model_type == "xgboost" else None)

        # Log metrics
        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("precision", prec)
        mlflow.log_metric("recall", rec)
        mlflow.log_metric("f1_score", f1)
        mlflow.log_metric("roc_auc", auc)

        print(
            f"[{model_type.upper()}] n_est={n_estimators}, max_depth={max_depth} -> "
            f"Acc: {acc:.4f}, F1: {f1:.4f}, AUC: {auc:.4f}"
        )

        if save_model:
            os.makedirs("model", exist_ok=True)
            artifacts = {
                "model": model,
                "label_encoders": label_encoders,
                "scaler": scaler,
                "feature_cols": feature_cols,
                "spend_fences": spend_fences,
            }
            joblib.dump(artifacts, "model/model.joblib")
            mlflow.log_artifact("model/model.joblib")
            print("Saved serialized best model pipeline to model/model.joblib ✅")

        return acc, f1, auc


def main():
    parser = argparse.ArgumentParser(description="Spaceship Titanic MLflow Training Script")
    parser.add_argument("--model_type", type=str, default="xgboost", choices=["xgboost", "random_forest"])
    parser.add_argument("--n_estimators", type=int, default=200)
    parser.add_argument("--max_depth", type=int, default=6)
    parser.add_argument("--learning_rate", type=float, default=0.05)
    parser.add_argument("--run_all_experiments", action="store_true", help="Run 3+ configurations across 2 algorithms")
    args = parser.parse_args()

    # Set SQLite backend for MLflow tracking
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    mlflow.set_experiment("spaceship-titanic-predictor")

    if args.run_all_experiments:
        print("=== Running Stage 2 Experiment Tracking (Comparing 2 Algorithms, 4 Runs) ===")
        # Run 1: Baseline Random Forest
        train_single_run("random_forest", n_estimators=100, max_depth=8)
        # Run 2: Tuned Random Forest
        train_single_run("random_forest", n_estimators=200, max_depth=12)
        # Run 3: Baseline XGBoost
        train_single_run("xgboost", n_estimators=100, max_depth=4, learning_rate=0.08)
        # Run 4: Best Model (Tuned XGBoost) -> Saved to model/model.joblib
        train_single_run("xgboost", n_estimators=250, max_depth=6, learning_rate=0.03, save_model=True)
        print("\nAll experiments tracked in SQLite backend (mlflow.db) successfully! ✅")
    else:
        # Run single configuration from CLI args
        train_single_run(
            args.model_type,
            args.n_estimators,
            args.max_depth,
            args.learning_rate,
            save_model=True,
        )


if __name__ == "__main__":
    main()
