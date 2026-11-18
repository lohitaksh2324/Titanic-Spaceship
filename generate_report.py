"""
CSL236 End-Term Project Report Generator
Spaceship Titanic Production ML System
Team: Lohitaksh Rastogi (24csu115), Khushi Sharma (24csu101)
Output: Lohitaksh_Rastogi_24csu115.pdf
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.units import cm, mm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib import colors

# ── Color Palette ────────────────────────────────────────────────────────────
NAVY      = HexColor("#0B132B")
TEAL      = HexColor("#0D9488")
DARK_TEAL = HexColor("#0F766E")
SLATE     = HexColor("#0F172A")
MUTED     = HexColor("#475569")
LIGHT_BG  = HexColor("#F8FAFC")
BORDER    = HexColor("#E2E8F0")
EMERALD   = HexColor("#10B981")
CORAL     = HexColor("#E11D48")

OUTPUT_FILE = "Lohitaksh_Rastogi_24csu115.pdf"

def build_styles():
    base = getSampleStyleSheet()

    styles = {
        "title": ParagraphStyle(
            "title", parent=base["Normal"],
            fontSize=28, leading=36, textColor=white,
            fontName="Helvetica-Bold", alignment=TA_CENTER,
            spaceAfter=6
        ),
        "subtitle": ParagraphStyle(
            "subtitle", parent=base["Normal"],
            fontSize=14, leading=20, textColor=HexColor("#CBD5E1"),
            fontName="Helvetica", alignment=TA_CENTER,
            spaceAfter=4
        ),
        "meta": ParagraphStyle(
            "meta", parent=base["Normal"],
            fontSize=11, leading=16, textColor=HexColor("#94A3B8"),
            fontName="Helvetica", alignment=TA_CENTER,
            spaceAfter=3
        ),
        "h1": ParagraphStyle(
            "h1", parent=base["Normal"],
            fontSize=16, leading=22, textColor=NAVY,
            fontName="Helvetica-Bold", spaceBefore=14, spaceAfter=6
        ),
        "h2": ParagraphStyle(
            "h2", parent=base["Normal"],
            fontSize=13, leading=18, textColor=DARK_TEAL,
            fontName="Helvetica-Bold", spaceBefore=10, spaceAfter=4
        ),
        "body": ParagraphStyle(
            "body", parent=base["Normal"],
            fontSize=11, leading=17, textColor=SLATE,
            fontName="Helvetica", spaceAfter=6, alignment=TA_JUSTIFY
        ),
        "bullet": ParagraphStyle(
            "bullet", parent=base["Normal"],
            fontSize=11, leading=17, textColor=SLATE,
            fontName="Helvetica", spaceAfter=4,
            leftIndent=14, bulletIndent=0
        ),
        "code": ParagraphStyle(
            "code", parent=base["Normal"],
            fontSize=9, leading=13, textColor=HexColor("#1E293B"),
            fontName="Courier", spaceAfter=4,
            leftIndent=12, backColor=LIGHT_BG
        ),
        "caption": ParagraphStyle(
            "caption", parent=base["Normal"],
            fontSize=9, leading=13, textColor=MUTED,
            fontName="Helvetica-Oblique", alignment=TA_CENTER, spaceAfter=6
        ),
        "stat": ParagraphStyle(
            "stat", parent=base["Normal"],
            fontSize=22, leading=28, textColor=TEAL,
            fontName="Helvetica-Bold", alignment=TA_CENTER
        ),
        "stat_label": ParagraphStyle(
            "stat_label", parent=base["Normal"],
            fontSize=9, leading=12, textColor=MUTED,
            fontName="Helvetica", alignment=TA_CENTER
        ),
    }
    return styles


def divider(color=TEAL, thickness=1.5):
    return HRFlowable(width="100%", thickness=thickness, color=color, spaceAfter=8, spaceBefore=4)


def section_header(text, styles):
    return [
        Paragraph(text, styles["h1"]),
        divider()
    ]


def build_report():
    doc = SimpleDocTemplate(
        OUTPUT_FILE,
        pagesize=A4,
        topMargin=1.8*cm,
        bottomMargin=1.8*cm,
        leftMargin=2.2*cm,
        rightMargin=2.2*cm,
        title="Spaceship Titanic – CSL236 Project Report",
        author="Lohitaksh Rastogi, Khushi Sharma"
    )

    styles = build_styles()
    story = []
    W = A4[0] - 4.4*cm  # usable width

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 1 — TITLE PAGE
    # ══════════════════════════════════════════════════════════════════════════
    # Dark navy banner
    title_table_data = [[
        Paragraph("Spaceship Titanic<br/>Prediction System", styles["title"])
    ]]
    title_table = Table(title_table_data, colWidths=[W])
    title_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("TOPPADDING",    (0, 0), (-1, -1), 28),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 28),
        ("LEFTPADDING",   (0, 0), (-1, -1), 20),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 20),
        ("ROUNDEDCORNERS", (0, 0), (-1, -1), [8]),
    ]))
    story.append(title_table)
    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph(
        "Production MLOps Binary Classification Pipeline with FastAPI, Docker &amp; Render Cloud",
        styles["subtitle"]
    ))
    story.append(Spacer(1, 0.6*cm))

    # Info table
    info_data = [
        ["Course", "CSL236 — Introduction to AI and Machine Learning"],
        ["Institution", "The NorthCap University"],
        ["Section", "B.Tech CSE — Semester 5"],
        ["Dataset", "Kaggle — Spaceship Titanic (Binary Classification)"],
        ["Live Deployment", "https://titanic-spaceship.onrender.com/"],
        ["GitHub Repository", "https://github.com/lohitaksh2324/Titanic-Spaceship"],
    ]
    info_table = Table(info_data, colWidths=[W*0.28, W*0.72])
    info_table.setStyle(TableStyle([
        ("FONTNAME",  (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME",  (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE",  (0, 0), (-1, -1), 10),
        ("LEADING",   (0, 0), (-1, -1), 15),
        ("TEXTCOLOR", (0, 0), (0, -1), DARK_TEAL),
        ("TEXTCOLOR", (1, 0), (1, -1), SLATE),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [LIGHT_BG, white]),
        ("GRID",      (0, 0), (-1, -1), 0.5, BORDER),
        ("TOPPADDING",    (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 0.6*cm))

    # Team members box
    team_data = [
        [Paragraph("<b>Team Members</b>", ParagraphStyle("th", fontSize=11, fontName="Helvetica-Bold", textColor=white))],
        [Paragraph("Lohitaksh Rastogi — Roll No. 24csu115", ParagraphStyle("tm", fontSize=11, fontName="Helvetica", textColor=white, leading=16))],
        [Paragraph("Khushi Sharma — Roll No. 24csu101", ParagraphStyle("tm2", fontSize=11, fontName="Helvetica", textColor=white, leading=16))],
    ]
    team_table = Table(team_data, colWidths=[W])
    team_table.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  TEAL),
        ("BACKGROUND",    (0, 1), (-1, -1), NAVY),
        ("TOPPADDING",    (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING",   (0, 0), (-1, -1), 14),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 14),
        ("ROUNDEDCORNERS",(0, 0), (-1, -1), [6]),
    ]))
    story.append(team_table)
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 2 — PROBLEM STATEMENT & DATASET + EDA
    # ══════════════════════════════════════════════════════════════════════════
    story += section_header("1. Problem Statement & Dataset", styles)

    story.append(Paragraph(
        "The Spaceship Titanic is a fictional interstellar vessel that, during its maiden voyage near Alpha Centauri, "
        "collided with a hidden spacetime anomaly. The collision transported approximately half the passengers into an "
        "alternate dimension. The objective of this project is to build a production-grade binary classification system "
        "that predicts whether a given passenger was <b>Transported</b> (True) or remained safely aboard (False), using "
        "demographic, spatial, and behavioral features extracted from the ship's passenger manifest.",
        styles["body"]
    ))

    story.append(Paragraph("Dataset Statistics", styles["h2"]))

    # Stat cards row
    stats_data = [[
        Paragraph("8,693", styles["stat"]),
        Paragraph("4,277", styles["stat"]),
        Paragraph("14", styles["stat"]),
        Paragraph("50.4%", styles["stat"]),
    ], [
        Paragraph("Training Records", styles["stat_label"]),
        Paragraph("Test Records", styles["stat_label"]),
        Paragraph("Input Features", styles["stat_label"]),
        Paragraph("Transport Rate", styles["stat_label"]),
    ]]
    stats_table = Table(stats_data, colWidths=[W/4]*4)
    stats_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BG),
        ("GRID",       (0, 0), (-1, -1), 0.5, BORDER),
        ("TOPPADDING",    (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("ROUNDEDCORNERS",(0, 0), (-1, -1), [6]),
    ]))
    story.append(stats_table)
    story.append(Spacer(1, 0.4*cm))

    story.append(Paragraph("Feature Categories", styles["h2"]))
    feat_data = [
        ["Category", "Features", "Description"],
        ["Demographics", "HomePlanet, Age, VIP", "Origin planet, passenger age, VIP flag"],
        ["Spatial Telemetry", "Cabin (Deck/Num/Side)", "Physical cabin coordinates on the ship"],
        ["CryoSleep", "CryoSleep (Boolean)", "Whether passenger was in suspended animation"],
        ["Amenity Spend", "RoomService, FoodCourt, ShoppingMall, Spa, VRDeck", "USD expenditure across 5 ship amenities"],
        ["Target", "Transported (Boolean)", "True = displaced to anomaly | False = safe"],
    ]
    feat_table = Table(feat_data, colWidths=[W*0.22, W*0.4, W*0.38])
    feat_table.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  TEAL),
        ("TEXTCOLOR",     (0, 0), (-1, 0),  white),
        ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTNAME",      (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE",      (0, 0), (-1, -1), 9),
        ("LEADING",       (0, 0), (-1, -1), 13),
        ("BACKGROUND",    (0, -1),(-1, -1), HexColor("#F0FDF4")),
        ("FONTNAME",      (0, -1),(-1, -1), "Helvetica-Bold"),
        ("TEXTCOLOR",     (0, -1),(-1, -1), DARK_TEAL),
        ("ROWBACKGROUNDS",(0, 1), (-1, -2), [white, LIGHT_BG]),
        ("GRID",          (0, 0), (-1, -1), 0.5, BORDER),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
    ]))
    story.append(feat_table)
    story.append(Spacer(1, 0.4*cm))

    story.append(Paragraph("2. EDA Highlights", styles["h1"]))
    story.append(divider())

    eda_findings = [
        ("81.8%", "CryoSleep Transport Rate", "Passengers in suspended animation pods had an 81.8% chance of being transported vs only 32.9% for awake passengers. CryoSleep is the dominant predictor."),
        ("73.4%", "Deck B Vulnerability", "Upper forward decks (B: 73.4%, C: 68.0%) faced direct anomaly exposure. Lower decks showed far lower rates (E: 35.7%, T: 20.0%)."),
        ("+10.4%", "Starboard vs Port Bias", "Starboard-side cabins (55.5% transport rate) faced the initial collision vector, yielding 10.4% higher displacement than Port-side (45.1%)."),
        ("-0.24", "RoomService Correlation", "Amenity spend features show negative correlation with Transported. RoomService (r=-0.24), Spa (r=-0.22), VRDeck (r=-0.21) confirm spenders stayed safe."),
        ("2,624.9", "Top F-Score (HasSpend)", "SelectKBest ANOVA confirms HasSpend as the #1 discriminator (F=2,624.9), followed by CryoSleep (F=2,334.3). Spending behavior is the key signal."),
        ("~2%", "Missing Values Rate", "All 12 non-ID columns had ~2.0–2.5% missing values. Zero duplicate rows. Addressed via domain-specific imputation rules (CryoSleep → $0 spend)."),
    ]

    for stat, title, desc in eda_findings:
        row_data = [[
            Paragraph(f"<b>{stat}</b>", ParagraphStyle("st", fontSize=18, fontName="Helvetica-Bold", textColor=TEAL, alignment=TA_CENTER)),
            Paragraph(f"<b>{title}</b><br/><font color='#475569' size='9'>{desc}</font>",
                      ParagraphStyle("ed", fontSize=10, fontName="Helvetica", leading=15, textColor=SLATE))
        ]]
        row_table = Table(row_data, colWidths=[W*0.18, W*0.82])
        row_table.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), LIGHT_BG),
            ("GRID",          (0, 0), (-1, -1), 0.5, BORDER),
            ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING",    (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("LEFTPADDING",   (0, 0), (-1, -1), 10),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
        ]))
        story.append(row_table)
        story.append(Spacer(1, 0.15*cm))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 3 — SYSTEM ARCHITECTURE
    # ══════════════════════════════════════════════════════════════════════════
    story += section_header("3. System Architecture", styles)

    story.append(Paragraph(
        "The project follows an 8-stage MLOps reference architecture spanning data ingestion, "
        "feature engineering, model training, experiment tracking, API serving, containerization, "
        "automated CI/CD, and cloud deployment with drift monitoring.",
        styles["body"]
    ))
    story.append(Spacer(1, 0.3*cm))

    # Architecture diagram as a styled table (pipeline flow)
    arch_stages = [
        ("1", "Data Ingestion & Validation",
         "train.csv (8,693 rows), test.csv (4,277 rows) from Kaggle.\nPydantic data contract enforced at API layer. HTTP 422 on invalid inputs."),
        ("2", "Exploratory Data Analysis",
         "Target balance check (50.4%/49.6%). Missing value heatmap. Correlation matrix\n(numerical features). Cabin-level and CryoSleep transport rate analysis."),
        ("3", "Feature Engineering",
         "Cabin decomposition (Deck, CabinNum, Side). Group extraction (GroupId, GroupSize,\nIsAlone). Spend aggregation (TotalSpend, LuxurySpend, HasSpend). Age binning (5 groups)."),
        ("4", "Data Preparation",
         "CryoSleep-based $0 spend imputation. Median imputation for numeric. Mode for\ncategorical. IQR Winsorization (Q3+3×IQR). LabelEncoder. MinMaxScaler. 80/20 split."),
        ("5", "Model Training & Tuning",
         "Random Forest (Baseline + Tuned via GridSearchCV 5-fold).\nXGBoost (Baseline + Tuned via GridSearchCV 5-fold). Best: Tuned XGBoost."),
        ("6", "Experiment Tracking",
         "MLflow with SQLite backend (mlflow.db). Logged params, accuracy, ROC-AUC,\nand model artifact (model/model.joblib) across all 4 runs."),
        ("7", "Production API & Serving",
         "FastAPI with GET /health, POST /predict, GET / (UI). Pydantic schema validation.\nRule-based prediction tips. JSON logging to logs/predictions.log."),
        ("8", "Containerization, CI/CD & Cloud",
         "Dockerfile (python:3.11-slim). GitHub Actions CI: checkout → train → pytest.\nRender cloud deployment. drift_check.py for Z-score feature drift monitoring."),
    ]

    for num, title, desc in arch_stages:
        stage_data = [[
            Paragraph(f"<b>{num}</b>", ParagraphStyle("num", fontSize=14, fontName="Helvetica-Bold", textColor=white, alignment=TA_CENTER)),
            Paragraph(f"<b>{title}</b>", ParagraphStyle("st", fontSize=11, fontName="Helvetica-Bold", textColor=DARK_TEAL)),
            Paragraph(desc.replace("\n", "<br/>"), ParagraphStyle("sd", fontSize=9.5, fontName="Helvetica", textColor=SLATE, leading=14)),
        ]]
        stage_table = Table(stage_data, colWidths=[W*0.07, W*0.33, W*0.60])
        stage_table.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (0, 0),  TEAL),
            ("BACKGROUND",    (1, 0), (-1, -1), LIGHT_BG),
            ("GRID",          (0, 0), (-1, -1), 0.5, BORDER),
            ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING",    (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("LEFTPADDING",   (0, 0), (-1, -1), 8),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
        ]))
        story.append(stage_table)
        story.append(Spacer(1, 0.12*cm))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 4 — EXPERIMENTS & MODEL COMPARISON
    # ══════════════════════════════════════════════════════════════════════════
    story += section_header("4. Experiments & Model Comparison", styles)

    story.append(Paragraph(
        "Four model configurations were trained, evaluated on the 1,739-sample validation holdout (20% stratified split), "
        "and tracked in MLflow. The best model was selected based on combined accuracy and ROC-AUC performance.",
        styles["body"]
    ))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("MLflow Experiment Results", styles["h2"]))
    mlflow_data = [
        ["Run Name", "Algorithm", "Key Hyperparameters", "Val Accuracy", "ROC-AUC"],
        ["Baseline_RF", "Random Forest", "n_estimators=100, max_depth=8, min_samples_split=2", "79.36%", "0.8845"],
        ["Tuned_RF", "Random Forest", "n_estimators=200, max_depth=12, min_samples_split=5", "80.33%", "0.8935"],
        ["Baseline_XGB", "XGBoost", "n_estimators=100, max_depth=4, learning_rate=0.08", "80.28%", "0.9046"],
        ["Tuned_XGBoost ★", "XGBoost", "n_estimators=250, max_depth=6, learning_rate=0.03", "81.25%", "0.9087"],
    ]
    mlflow_table = Table(mlflow_data, colWidths=[W*0.17, W*0.16, W*0.42, W*0.13, W*0.12])
    mlflow_table.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  TEAL),
        ("TEXTCOLOR",     (0, 0), (-1, 0),  white),
        ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTNAME",      (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE",      (0, 0), (-1, -1), 9),
        ("LEADING",       (0, 0), (-1, -1), 13),
        ("BACKGROUND",    (0, -1),(-1, -1), HexColor("#F0FDF4")),
        ("FONTNAME",      (0, -1),(-1, -1), "Helvetica-Bold"),
        ("TEXTCOLOR",     (0, -1),(-1, -1), DARK_TEAL),
        ("ROWBACKGROUNDS",(0, 1), (-1, -2), [white, LIGHT_BG]),
        ("GRID",          (0, 0), (-1, -1), 0.5, BORDER),
        ("TOPPADDING",    (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
        ("ALIGN",         (3, 0), (-1, -1), "CENTER"),
    ]))
    story.append(mlflow_table)
    story.append(Spacer(1, 0.4*cm))

    story.append(Paragraph("Best Model: Tuned XGBoost", styles["h2"]))
    story.append(Paragraph(
        "The Tuned XGBoost achieved the highest validation accuracy of <b>81.25%</b> and ROC-AUC of <b>0.9087</b>, "
        "outperforming all Random Forest variants. The low learning rate (0.03) combined with high n_estimators (250) "
        "enabled fine-grained boosting, while max_depth=6 controlled overfitting effectively. The model was serialized "
        "to <b>model/model.joblib</b> as a dictionary containing the fitted classifier, label encoders, MinMaxScaler, "
        "feature column names, and IQR outlier fences.",
        styles["body"]
    ))

    story.append(Paragraph("Final Classification Metrics (Tuned XGBoost on Validation Set)", styles["h2"]))
    metric_data = [
        ["Metric", "Value", "Interpretation"],
        ["Validation Accuracy", "81.25%", "Overall correct predictions on 1,739-sample holdout"],
        ["ROC-AUC Score", "0.9087", "Excellent class-ranking discrimination across all thresholds"],
        ["Precision (Class 1)", "80.42%", "Low false anomaly alarm rate — predictions are reliable"],
        ["Recall (Class 1)", "82.53%", "Captures over 82% of actually transported passengers"],
        ["Kaggle Submission", "4,277 rows", "submission.csv generated: 50.6% True / 49.4% False"],
    ]
    metric_table = Table(metric_data, colWidths=[W*0.3, W*0.2, W*0.5])
    metric_table.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  NAVY),
        ("TEXTCOLOR",     (0, 0), (-1, 0),  white),
        ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTNAME",      (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE",      (0, 0), (-1, -1), 9.5),
        ("LEADING",       (0, 0), (-1, -1), 14),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [LIGHT_BG, white]),
        ("GRID",          (0, 0), (-1, -1), 0.5, BORDER),
        ("TOPPADDING",    (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
        ("FONTNAME",      (1, 1), (1, -1),  "Helvetica-Bold"),
        ("TEXTCOLOR",     (1, 1), (1, -1),  DARK_TEAL),
    ]))
    story.append(metric_table)
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 5 — TESTING, CI & DEPLOYMENT
    # ══════════════════════════════════════════════════════════════════════════
    story += section_header("5. Testing, CI/CD & Deployment", styles)

    story.append(Paragraph("Automated Testing (Pytest — 4 Tests, 4 Passed)", styles["h2"]))
    test_data = [
        ["Test ID", "Name", "What It Verifies", "Expected Result"],
        ["test_1", "Health Check", "GET /health returns 200 with model_loaded=True and timestamp", "HTTP 200 ✓"],
        ["test_2", "UI Loads", "GET / returns HTML with 'SPACESHIP TITANIC' and 'Passenger Manifest'", "HTTP 200 ✓"],
        ["test_3", "Domain Logic", "CryoSleep (Deck B, $0 spend) has higher transport prob than awake luxury spender (Deck E, $6,700 spend)", "prob_cryo > prob_awake ✓"],
        ["test_4a", "Boundary (Age)", "Negative Age=-5.0 rejected by Pydantic (ge=0 constraint)", "HTTP 422 ✓"],
        ["test_4b", "Boundary (Planet)", "Invalid HomePlanet='Jupiter' rejected by Pydantic enum", "HTTP 422 ✓"],
        ["test_4c", "Boundary (Spend)", "Negative RoomService=-250.0 rejected by Pydantic (ge=0)", "HTTP 422 ✓"],
    ]
    test_table = Table(test_data, colWidths=[W*0.11, W*0.18, W*0.56, W*0.15])
    test_table.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  TEAL),
        ("TEXTCOLOR",     (0, 0), (-1, 0),  white),
        ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTNAME",      (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE",      (0, 0), (-1, -1), 8.5),
        ("LEADING",       (0, 0), (-1, -1), 12),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [white, LIGHT_BG]),
        ("GRID",          (0, 0), (-1, -1), 0.5, BORDER),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 7),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 7),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("TEXTCOLOR",     (3, 1), (3, -1),  EMERALD),
        ("FONTNAME",      (3, 1), (3, -1),  "Helvetica-Bold"),
    ]))
    story.append(test_table)
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("Docker Containerization", styles["h2"]))
    story.append(Paragraph(
        "The serving application is packaged in a Docker container using <b>python:3.11-slim</b> as the base image. "
        "A lean <b>requirements-serve.txt</b> (FastAPI, uvicorn, joblib, scikit-learn, xgboost, pydantic, python-multipart) "
        "is used instead of the full training requirements, minimizing image size. The container exposes port 8000 and "
        "runs uvicorn as the ASGI server.", styles["body"]
    ))

    story.append(Paragraph("GitHub Actions CI/CD Pipeline", styles["h2"]))
    ci_steps = [
        ("Trigger", "On every git push to main branch"),
        ("Step 1", "Checkout code from GitHub repository"),
        ("Step 2", "Setup Python 3.11 environment"),
        ("Step 3", "Install dependencies from requirements.txt"),
        ("Step 4", "Run train.py to verify training pipeline executes end-to-end"),
        ("Step 5", "Run pytest tests/ — all 4 tests must pass for deployment"),
    ]
    for step, desc in ci_steps:
        story.append(Paragraph(f"<b>{step}:</b> {desc}", styles["bullet"]))

    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("Cloud Deployment on Render", styles["h2"]))
    deploy_data = [
        ["Parameter", "Value"],
        ["Platform", "Render (Free Tier Web Service)"],
        ["Repository", "https://github.com/lohitaksh2324/Titanic-Spaceship"],
        ["Build Command", "pip install -r requirements-serve.txt"],
        ["Start Command", "uvicorn app:app --host 0.0.0.0 --port 8000"],
        ["Live URL", "https://titanic-spaceship.onrender.com/"],
        ["API Docs (Swagger)", "https://titanic-spaceship.onrender.com/docs"],
        ["Health Check", "https://titanic-spaceship.onrender.com/health"],
    ]
    deploy_table = Table(deploy_data, colWidths=[W*0.3, W*0.7])
    deploy_table.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  NAVY),
        ("TEXTCOLOR",     (0, 0), (-1, 0),  white),
        ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTNAME",      (0, 1), (0, -1),  "Helvetica-Bold"),
        ("FONTNAME",      (1, 1), (1, -1),  "Helvetica"),
        ("FONTSIZE",      (0, 0), (-1, -1), 9.5),
        ("LEADING",       (0, 0), (-1, -1), 14),
        ("TEXTCOLOR",     (0, 1), (0, -1),  DARK_TEAL),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [LIGHT_BG, white]),
        ("GRID",          (0, 0), (-1, -1), 0.5, BORDER),
        ("TOPPADDING",    (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
    ]))
    story.append(deploy_table)

    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("Data Drift Monitoring (drift_check.py)", styles["h2"]))
    story.append(Paragraph(
        "A standalone monitoring script compares incoming prediction feature distributions against the training baseline. "
        "It parses <b>logs/predictions.log</b> (JSON-logged by the FastAPI app) and computes mean, standard deviation, "
        "and <b>Z-scores</b> for each numeric feature. If any feature's Z-score exceeds a threshold (|Z| &gt; 2.0), "
        "the script flags a drift warning, indicating the production data distribution has shifted significantly from "
        "the training distribution and a retraining cycle should be triggered.",
        styles["body"]
    ))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 6 — LIMITATIONS & FUTURE SCOPE
    # ══════════════════════════════════════════════════════════════════════════
    story += section_header("6. Limitations & Future Scope", styles)

    story.append(Paragraph("Current Limitations", styles["h2"]))
    limitations = [
        ("Model Accuracy Ceiling",
         "The Tuned XGBoost achieves 81.25% validation accuracy. The dataset contains inherent noise from the fictional "
         "spacetime anomaly scenario that limits further gains with standard preprocessing. Advanced ensemble stacking "
         "or neural approaches could push beyond this but were outside project scope."),
        ("Render Free Tier Spin-Down",
         "The live deployment runs on Render's free tier, which suspends the container after 15 minutes of inactivity. "
         "The first request after a cold start can take 30–60 seconds while the container restarts."),
        ("No Automated Retraining Trigger",
         "While drift_check.py detects distribution drift via Z-scores, it does not automatically trigger a retraining "
         "pipeline. The drift alert currently only prints a warning message; manual intervention is required."),
        ("Static Model Version",
         "The model.joblib is a fixed artifact. There is no model versioning registry (MLflow Model Registry was not "
         "configured). Rolling back to a previous model version requires manual file replacement."),
        ("MLflow UI Not Exposed",
         "MLflow experiment results are stored in a local SQLite file (mlflow.db) rather than a hosted tracking server. "
         "The visual MLflow dashboard cannot be accessed from the deployed Render environment."),
    ]
    for title, desc in limitations:
        story.append(Paragraph(f"<b>• {title}:</b> {desc}", styles["bullet"]))
        story.append(Spacer(1, 0.1*cm))

    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("Future Scope", styles["h2"]))
    roadmap = [
        ("Automated Retraining Pipeline",
         "Extend drift_check.py to automatically trigger a GitHub Actions workflow whenever |Z| > 2.0, "
         "re-running train.py and replacing the production model artifact."),
        ("SHAP Explainability Integration",
         "Integrate SHAP (SHapley Additive exPlanations) waterfall plots into the web UI so each prediction "
         "comes with a visual breakdown of which features drove the outcome."),
        ("Kubernetes Cluster Scaling",
         "Migrate from Render's single-container free tier to a multi-pod Kubernetes deployment with Redis-based "
         "prediction caching for high-volume telemetry processing."),
        ("MLflow Hosted Tracking Server",
         "Deploy MLflow on a cloud database (PostgreSQL + S3 artifact store) for persistent, queryable experiment "
         "history accessible across team members and deployment environments."),
        ("Real-Time Streaming Predictions",
         "Extend the system to process live passenger telemetry streams using Apache Kafka or AWS Kinesis, "
         "enabling sub-second anomaly detection at scale."),
    ]
    for title, desc in roadmap:
        story.append(Paragraph(f"<b>• {title}:</b> {desc}", styles["bullet"]))
        story.append(Spacer(1, 0.1*cm))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 7 — INDIVIDUAL CONTRIBUTIONS
    # ══════════════════════════════════════════════════════════════════════════
    story += section_header("7. Individual Member Contributions", styles)

    # Member 1 — Lohitaksh
    contrib_data_1 = [[
        Paragraph("<b>Lohitaksh Rastogi</b><br/>Roll No. 24csu115",
                  ParagraphStyle("mn", fontSize=12, fontName="Helvetica-Bold", textColor=white, leading=18)),
        Paragraph("Pipeline Architecture, EDA, Feature Engineering, Model Training &amp; MLflow Tracking",
                  ParagraphStyle("mr", fontSize=10, fontName="Helvetica-Oblique", textColor=HexColor("#CBD5E1"), leading=15)),
    ]]
    h1_table = Table(contrib_data_1, colWidths=[W*0.42, W*0.58])
    h1_table.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), NAVY),
        ("TOPPADDING",    (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("LEFTPADDING",   (0, 0), (-1, -1), 12),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 12),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("ROUNDEDCORNERS",(0, 0), (-1, -1), [6]),
    ]))
    story.append(h1_table)
    story.append(Spacer(1, 0.2*cm))

    lohit_tasks = [
        "Designed end-to-end pipeline architecture following the 8-stage MLOps reference model",
        "Performed full Exploratory Data Analysis: target distribution, missing value analysis, correlation heatmap, "
        "cabin-level transport rates, CryoSleep vs awake comparison, and all 12 EDA charts (PNG outputs)",
        "Engineered all derived features: Cabin decomposition (Deck, CabinNum, Side), Group extraction "
        "(GroupId, GroupSize, IsAlone), spend aggregation (TotalSpend, LuxurySpend, HasSpend), and Age binning",
        "Implemented domain-specific imputation (CryoSleep → $0 spend), IQR Winsorization (Q3+3×IQR), "
        "LabelEncoder, MinMaxScaler, and 80/20 stratified split in spaceship_titanic.ipynb and train.py",
        "Configured and ran GridSearchCV with 5-fold cross-validation for both Random Forest and XGBoost",
        "Set up MLflow experiment tracking with SQLite backend; logged 4 runs with params, metrics, and artifacts",
        "Generated final Kaggle submission.csv (4,277 test predictions) using the best Tuned XGBoost pipeline",
        "Serialized the production model pipeline to model/model.joblib for serving",
    ]
    for task in lohit_tasks:
        story.append(Paragraph(f"• {task}", styles["bullet"]))
    story.append(Spacer(1, 0.4*cm))

    # Member 2 — Khushi
    contrib_data_2 = [[
        Paragraph("<b>Khushi Sharma</b><br/>Roll No. 24csu101",
                  ParagraphStyle("mn2", fontSize=12, fontName="Helvetica-Bold", textColor=white, leading=18)),
        Paragraph("FastAPI Development, Pydantic Contract, Web UI, Testing, Docker &amp; CI/CD",
                  ParagraphStyle("mr2", fontSize=10, fontName="Helvetica-Oblique", textColor=HexColor("#CBD5E1"), leading=15)),
    ]]
    h2_table = Table(contrib_data_2, colWidths=[W*0.42, W*0.58])
    h2_table.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), TEAL),
        ("TOPPADDING",    (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("LEFTPADDING",   (0, 0), (-1, -1), 12),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 12),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("ROUNDEDCORNERS",(0, 0), (-1, -1), [6]),
    ]))
    story.append(h2_table)
    story.append(Spacer(1, 0.2*cm))

    khushi_tasks = [
        "Built the full FastAPI serving application (app.py) with GET /health, POST /predict, and GET / (static UI) endpoints",
        "Designed and implemented the Pydantic data contract (PassengerRequest schema) with field validators for "
        "HomePlanet enum, non-negative spend (ge=0), valid age range, and Cabin regex pattern",
        "Developed the rule-based prediction tips generator (5 domain-logic tips based on CryoSleep, Spend, Deck, Side, Age)",
        "Built the complete sci-fi dark-theme web UI (static/index.html) using vanilla HTML5, CSS3, and JavaScript "
        "with Orbitron font, animated results showing Transported = True/False prominently",
        "Set up JSON logging to logs/predictions.log for all incoming API predictions (input features + prediction outcome)",
        "Wrote and validated the full pytest test suite (tests/test_app.py): 4 tests, 6 test cases, all passing",
        "Wrote the Dockerfile (python:3.11-slim) and lean requirements-serve.txt for production containerization",
        "Configured .github/workflows/ci.yml GitHub Actions pipeline and project documentation (README.md)",
        "Set up Render cloud deployment and managed the GitHub repository (lohitaksh2324/Titanic-Spaceship)",
    ]
    for task in khushi_tasks:
        story.append(Paragraph(f"• {task}", styles["bullet"]))

    story.append(Spacer(1, 0.5*cm))
    divider_line = Table([[""]], colWidths=[W])
    divider_line.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, -1), 1, TEAL),
        ("TOPPADDING",    (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(divider_line)
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        "Live System: https://titanic-spaceship.onrender.com/ &nbsp;&nbsp;|&nbsp;&nbsp; "
        "GitHub: https://github.com/lohitaksh2324/Titanic-Spaceship &nbsp;&nbsp;|&nbsp;&nbsp; "
        "API Docs: https://titanic-spaceship.onrender.com/docs",
        ParagraphStyle("footer", fontSize=9, fontName="Helvetica", textColor=MUTED, alignment=TA_CENTER, leading=14)
    ))

    # ── Build PDF ─────────────────────────────────────────────────────────────
    doc.build(story)
    print(f"Report generated: {OUTPUT_FILE}")


if __name__ == "__main__":
    build_report()
