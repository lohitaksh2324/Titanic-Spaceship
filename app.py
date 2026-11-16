"""
Spaceship Titanic — FastAPI Prediction Service
CSL236 End-Term Project
"""

import os
import json
import logging
from datetime import datetime
from typing import Literal, Optional, List
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, field_validator
# ── Configure Logging ──────────────────────────────────────────────────────────
os.makedirs("logs", exist_ok=True)
LOG_FILE = "logs/predictions.log"

logger = logging.getLogger("spaceship_titanic")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
file_handler.setFormatter(logging.Formatter("%(message)s"))
if not logger.handlers:
    logger.addHandler(file_handler)


# ── Load Model at Startup (Outside request handler) ───────────────────────────
MODEL_PATH = "model/model.joblib"
if not os.path.exists(MODEL_PATH):
    raise RuntimeError(f"Model file not found at {MODEL_PATH}. Please run train.py first.")

artifacts = joblib.load(MODEL_PATH)
model = artifacts["model"]
label_encoders = artifacts["label_encoders"]
scaler = artifacts["scaler"]
feature_cols = artifacts["feature_cols"]
spend_fences = artifacts["spend_fences"]
print("Model pipeline loaded successfully at startup! ✅")


def preprocess_input(raw_df: pd.DataFrame) -> pd.DataFrame:
    df = raw_df.copy()

    # 1. Feature Extraction
    cabin_split = df["Cabin"].astype(str).str.split("/", expand=True)
    df["Deck"] = cabin_split[0].replace({"nan": "F", "None": "F"}).fillna("F")
    df["CabinNum"] = pd.to_numeric(cabin_split[1], errors="coerce").fillna(427.0)
    df["Side"] = cabin_split[2].replace({"nan": "S", "None": "S"}).fillna("S")

    df["GroupId"] = df["PassengerId"].astype(str).str.split("_").str[0]
    df["GroupSize"] = 1
    df["IsAlone"] = 1

    # 2. Imputation & Boolean conversion
    for col in ["CryoSleep", "VIP"]:
        df[col] = df[col].map({"True": 1, "False": 0, True: 1, False: 0, 1: 1, 0: 0})
        df[col] = df[col].fillna(0).astype(int)

    for col in ["HomePlanet", "Destination", "Deck", "Side"]:
        default_val = "Earth" if col == "HomePlanet" else "TRAPPIST-1e" if col == "Destination" else "F" if col == "Deck" else "S"
        df[col] = df[col].fillna(default_val)

    # Amenity spending
    spend_cols = ["RoomService", "FoodCourt", "ShoppingMall", "Spa", "VRDeck"]
    for col in spend_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df.loc[df["CryoSleep"] == 1, col] = 0.0
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
        fence = spend_fences.get(col, 2000.0)
        df[col] = df[col].clip(upper=fence)

    # Categorical Encoding
    cat_cols = ["HomePlanet", "Destination", "Deck", "Side", "AgeGroup"]
    for col in cat_cols:
        le = label_encoders[col]
        classes = {cls: idx for idx, cls in enumerate(le.classes_)}
        df[col] = df[col].astype(str).map(classes).fillna(0).astype(int)

    return df[feature_cols]


# ── FastAPI App Setup ─────────────────────────────────────────────────────────
app = FastAPI(
    title="Spaceship Titanic Predictor API",
    description="Validated production-style ML inference API predicting passenger transport following spacetime anomaly collision.",
    version="1.0.0",
)

if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")


# ── Pydantic Request & Response Schemas (Data Contract Enforcement) ───────────
class PassengerRequest(BaseModel):
    PassengerId: str = Field(
        default="0001_01",
        description="Unique passenger ID in format gggg_pp",
        pattern=r"^\d{4}_\d{2}$",
    )
    HomePlanet: Literal["Earth", "Europa", "Mars"] = Field(
        ..., description="Planet of departure: Earth, Europa, or Mars"
    )
    CryoSleep: bool = Field(
        ..., description="Whether passenger was placed in suspended animation"
    )
    Cabin: str = Field(
        default="B/0/P",
        description="Cabin identifier in format Deck/Num/Side (e.g. B/0/P)",
        pattern=r"^[A-Za-z]/[0-9]+/[A-Za-z]$",
    )
    Destination: Literal["TRAPPIST-1e", "55 Cancri e", "PSO J318.5-22"] = Field(
        ..., description="Intended destination planet"
    )
    Age: float = Field(
        ..., ge=0.0, le=120.0, description="Age of passenger (0.0 to 120.0)"
    )
    VIP: bool = Field(
        default=False, description="Whether passenger paid for VIP service"
    )
    RoomService: float = Field(
        default=0.0, ge=0.0, le=50000.0, description="RoomService expenditure (>= 0)"
    )
    FoodCourt: float = Field(
        default=0.0, ge=0.0, le=50000.0, description="FoodCourt expenditure (>= 0)"
    )
    ShoppingMall: float = Field(
        default=0.0, ge=0.0, le=50000.0, description="ShoppingMall expenditure (>= 0)"
    )
    Spa: float = Field(
        default=0.0, ge=0.0, le=50000.0, description="Spa expenditure (>= 0)"
    )
    VRDeck: float = Field(
        default=0.0, ge=0.0, le=50000.0, description="VRDeck expenditure (>= 0)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "PassengerId": "0001_01",
                "HomePlanet": "Europa",
                "CryoSleep": True,
                "Cabin": "B/0/P",
                "Destination": "55 Cancri e",
                "Age": 28.0,
                "VIP": False,
                "RoomService": 0.0,
                "FoodCourt": 0.0,
                "ShoppingMall": 0.0,
                "Spa": 0.0,
                "VRDeck": 0.0,
            }
        }


class PredictionResponse(BaseModel):
    passenger_id: str
    transported: bool
    probability: float
    confidence: str
    tips: List[str]


# ── Rule-Based Tips Generator ─────────────────────────────────────────────────
def generate_user_tips(data: PassengerRequest, transported: bool, proba: float) -> List[str]:
    tips = []

    # Tip 1: CryoSleep impact
    if data.CryoSleep:
        tips.append("CryoSleep pods experienced high harmonic resonance with the anomaly, leading to an 81%+ transport rate.")
    else:
        tips.append("Awake passengers who moved about the ship showed a much lower baseline probability (~33%) of being transported.")

    # Tip 2: Spending impact
    total_spend = data.RoomService + data.FoodCourt + data.ShoppingMall + data.Spa + data.VRDeck
    if total_spend == 0:
        tips.append("Zero amenity expenditure indicates passenger was stationary or in passenger compartments near the primary rift zone.")
    else:
        tips.append(f"Passenger recorded ${total_spend:.0f} across luxury amenities, typical of central deck sections that were shielded from the rift.")

    # Tip 3: Cabin orientation
    side = data.Cabin.split("/")[-1].upper() if "/" in data.Cabin else "S"
    if side == "S":
        tips.append("Starboard (S) cabins faced the initial shockwave vectors, increasing exposure relative to Port (P) cabins.")
    else:
        tips.append("Port (P) cabins were partially occluded by the main hull shielding, lowering localized displacement risk.")

    return tips


# ── API Endpoints ─────────────────────────────────────────────────────────────
@app.get("/", summary="Web UI for Predictions")
def serve_ui():
    """Serves the interactive web UI."""
    index_path = os.path.join("static", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Spaceship Titanic Predictor API is running. Visit /docs for Swagger UI."}


@app.get("/health", summary="Health Check")
def health_check():
    """Returns service health status and confirms model is loaded."""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "service": "spaceship-titanic-predictor",
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.post("/predict", response_model=PredictionResponse, summary="Predict Passenger Transported Status")
def predict(passenger: PassengerRequest):
    """
    Predicts whether a passenger was Transported to an alternate dimension.
    Validates input schema and logs requests to logs/predictions.log for drift monitoring.
    """
    try:
        input_data = {
            "PassengerId": passenger.PassengerId,
            "HomePlanet": passenger.HomePlanet,
            "CryoSleep": passenger.CryoSleep,
            "Cabin": passenger.Cabin,
            "Destination": passenger.Destination,
            "Age": passenger.Age,
            "VIP": passenger.VIP,
            "RoomService": passenger.RoomService,
            "FoodCourt": passenger.FoodCourt,
            "ShoppingMall": passenger.ShoppingMall,
            "Spa": passenger.Spa,
            "VRDeck": passenger.VRDeck,
        }
        df_input = pd.DataFrame([input_data])
        features_df = preprocess_input(df_input)
        scaled_features = scaler.transform(features_df)

        pred_label = bool(model.predict(scaled_features)[0])
        pred_proba = float(model.predict_proba(scaled_features)[0][1])

        confidence = "High" if abs(pred_proba - 0.5) >= 0.25 else "Moderate"
        tips = generate_user_tips(passenger, pred_label, pred_proba)

        # Log for drift checks
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "input": input_data,
            "prediction": pred_label,
            "probability": round(pred_proba, 4),
        }
        logger.info(json.dumps(log_entry))

        return PredictionResponse(
            passenger_id=passenger.PassengerId,
            transported=pred_label,
            probability=round(pred_proba, 4),
            confidence=confidence,
            tips=tips,
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Inference error: {str(e)}",
        )
