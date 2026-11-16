# 🚀 Spaceship Titanic — Production ML System

[![CI Pipeline](https://github.com/USER/spaceship-titanic-mlops/actions/workflows/ci.yml/badge.svg)](https://github.com/USER/spaceship-titanic-mlops/actions)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688.svg)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-python:3.11--slim-2496ED.svg)](https://www.docker.com/)

An end-to-end production-style Machine Learning system built for the **CSL236 — Introduction to AI and Machine Learning** course (The NorthCap University). This project predicts whether a passenger aboard the Spaceship Titanic was **Transported** to an alternate dimension following a spacetime anomaly collision, following the 8-stage MLOps reference architecture.

---

## 1. Problem Statement & Dataset

- **Problem Type:** Binary Classification
- **Target Variable:** `Transported` (Boolean: `True` if passenger was displaced into alternate dimension, `False` otherwise)
- **Dataset Source:** [Kaggle — Spaceship Titanic Competition](https://www.kaggle.com/competitions/spaceship-titanic)
- **Dataset Size:** 8,693 training records (14 initial attributes), 4,277 test records

---

## 2. Mandatory Data Contract

Every input feature received by the REST API is strictly validated against the following data contract. Any out-of-range value or invalid type is rejected with **HTTP 422 Unprocessable Entity**.

| Feature | Type | Allowed Range / Values | Why It Matters |
| :--- | :--- | :--- | :--- |
| `PassengerId` | string | Regex `^\d{4}_\d{2}$` (e.g. `0001_01`) | Identifies traveling group and individual group position. |
| `HomePlanet` | string | `{'Earth', 'Europa', 'Mars'}` | Planet of departure; Europa passengers show higher transport rates. |
| `CryoSleep` | bool | `{True, False}` | Passengers in suspended animation pods have an 81%+ transport rate. |
| `Cabin` | string | Regex `^[A-Za-z]/[0-9]+/[A-Za-z]$` (e.g. `B/0/P`) | Encodes Deck (`A`–`T`), Cabin Number, and Side (`P` vs `S`). |
| `Destination` | string | `{'TRAPPIST-1e', '55 Cancri e', 'PSO J318.5-22'}` | Destination port of disembarkation. |
| `Age` | float | `0.0 – 120.0` | Passenger age; children under 13 have 0 amenity expenditures. |
| `VIP` | bool | `{True, False}` | VIP suite passengers; Earth has zero VIPs. |
| `RoomService` | float | `≥ 0.0` (max 50,000.0) | Basic amenity expenditure; high spend strongly correlates with remaining safe. |
| `FoodCourt` | float | `≥ 0.0` (max 50,000.0) | Dining amenity expenditure. |
| `ShoppingMall` | float | `≥ 0.0` (max 50,000.0) | Retail amenity expenditure. |
| `Spa` | float | `≥ 0.0` (max 50,000.0) | Luxury amenity spend; negatively correlated with transport. |
| `VRDeck` | float | `≥ 0.0` (max 50,000.0) | Virtual entertainment spend; negatively correlated with transport. |
| **`Transported` (Target)** | **bool** | **`{True, False}`** | **Ground truth prediction label.** |

---

## 3. Repository Structure

```text
aiml project/
├── data/
│   ├── train.csv                # Training dataset (8,693 rows)
│   └── test.csv                 # Kaggle test dataset (4,277 rows)
├── images/                      # EDA and model evaluation plots
│   ├── target_distribution.png
│   ├── missing_values.png
│   ├── categorical_vs_target.png
│   ├── numerical_distributions.png
│   ├── correlation_heatmap.png
│   ├── boxplots_before.png
│   ├── boxplots_after.png
│   ├── feature_importance.png
│   ├── confusion_matrices.png
│   ├── roc_curves.png
│   └── best_model_feature_importance.png
├── model/
│   └── model.joblib             # Serialized best model pipeline (preprocessor + model)
├── static/
│   └── index.html               # Sci-fi themed interactive prediction UI
├── tests/
│   └── test_app.py              # Automated pytest suite (4 tests passing)
├── .github/workflows/
│   └── ci.yml                   # GitHub Actions automated CI pipeline
├── app.py                       # FastAPI serving application + Pydantic schema
├── train.py                     # Training script with MLflow tracking (SQLite backend)
├── drift_check.py               # Data drift detection script (Bonus)
├── Dockerfile                   # Lean production image (python:3.11-slim)
├── requirements.txt             # Full training & dev environment
├── requirements-serve.txt       # Lean serving runtime (no MLflow/pytest)
├── .gitignore                   # Excludes venv/, __pycache__/, mlruns/
└── README.md                    # Project documentation
```

---

## 4. MLflow Experiment Tracking Results

All experiments are tracked using an **SQLite backend** (`sqlite:///mlflow.db`) under experiment `spaceship-titanic-predictor`.

| Run # | Algorithm | Hyperparameters | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| 1 | Random Forest (Baseline) | `n_estimators=100, max_depth=8` | 0.7936 | 0.7812 | 0.8146 | 0.7975 | 0.8845 |
| 2 | Random Forest (Tuned) | `n_estimators=200, max_depth=12` | 0.8033 | 0.8032 | 0.8037 | 0.8034 | 0.8935 |
| 3 | XGBoost (Baseline) | `n_estimators=100, max_depth=4, lr=0.08` | 0.8028 | 0.7891 | 0.8226 | 0.8054 | 0.9046 |
| **4** | **XGBoost (Tuned Best)** | **`n_estimators=250, max_depth=6, lr=0.03`** | **0.8125** | **0.8042** | **0.8253** | **0.8146** | **0.9087** |

### Why We Chose Tuned XGBoost
1. **Superior Discrimination:** Tuned XGBoost achieved the highest validation accuracy (**81.25%**) and the highest ROC-AUC (**0.9087**), outperforming Random Forest by nearly 1% absolute accuracy and +0.015 AUC.
2. **Handling Non-Linear Interactions:** Gradient boosted decision trees with depth 6 effectively capture interactions between cryogenic pod status and individual amenity spend levels.
3. **Generalization:** Tested across cross-validation folds with balanced precision (0.8042) and recall (0.8253).

---

## 5. Local Setup & Execution Guide

### Local Environment
```bash
# 1. Create and activate virtual environment
python3 -m venv venv
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
# On macOS/Linux:
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run training and log all experiments to MLflow SQLite backend
python train.py --run_all_experiments

# 4. Launch MLflow UI to view experiment dashboard
mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5000

# 5. Run the automated test suite
pytest -v --tb=short

# 6. Launch the FastAPI application locally
uvicorn app:app --reload --port 8000
```
Open [http://localhost:8000](http://localhost:8000) for the UI or [http://localhost:8000/docs](http://localhost:8000/docs) for the interactive Swagger API docs.

---

## 6. Docker Build & Deployment

The Docker image is built from `python:3.11-slim` using **`requirements-serve.txt` only** (keeping image size lean by omitting MLflow, pytest, and development tools).

```bash
# 1. Build Docker image
docker build -t spaceship-titanic-app .

# 2. Run container with restart policy
docker run -d -p 8000:8000 --name spaceship-service --restart unless-stopped spaceship-titanic-app

# 3. Test container health
curl http://localhost:8000/health
```

- **Base Image:** `python:3.11-slim`
- **Estimated Image Size:** ~380 MB (lean serving runtime)
- **Restart Policy:** `--restart unless-stopped`

---

## 7. Automated Testing (Pytest Suite)

Run tests locally:
```bash
pytest -v --tb=short
```

| Test Case | Type | Description | Status |
| :--- | :--- | :--- | :---: |
| `test_1_health_check` | Smoke | Verifies `GET /health` returns HTTP 200 and `status == "healthy"` | **PASSED** ✅ |
| `test_2_ui_loads` | Integration | Verifies `GET /` serves HTML web UI with valid title and manifest form | **PASSED** ✅ |
| `test_3_domain_logic_cryosleep_vs_awake` | Domain Logic | Verifies a CryoSleep passenger with $0 spend has significantly higher transport probability than an awake heavy spender | **PASSED** ✅ |
| `test_4_boundary_validation_expects_422` | Boundary/Security | Verifies negative age, invalid planet name, or negative spend triggers HTTP 422 Unprocessable Entity | **PASSED** ✅ |

---

## 8. Continuous Integration (GitHub Actions)

On every push to `main`, `.github/workflows/ci.yml`:
1. Checks out the code.
2. Sets up Python 3.11.
3. Installs dependencies from `requirements.txt`.
4. Executes `python train.py --run_all_experiments`.
5. Runs `pytest -v --tb=short`.

---

## 9. Drift Monitoring (Bonus Requirement)

Every prediction request is logged in structured JSON Lines format to `logs/predictions.log`. The monitoring script compares the distribution of incoming requests against the training baseline:

```bash
python drift_check.py
```
- Monitors feature means, standard deviations, and Z-score shifts.
- Flags input distribution drift if $|Z| > 2.0$.

---

## 10. Team Information

- **Course:** CSL236 — Introduction to AI and Machine Learning (Semester 5)
- **Institution:** The NorthCap University
- **Team Members & Responsibilities:**
  - Member 1: Pipeline architecture, Feature engineering, Model training & MLflow tracking
  - Member 2: FastAPI development, Pydantic schemas, Web UI & Rule-based tips
  - Member 3: Pytest automation, Docker containerization, CI/CD GitHub Actions & Documentation
