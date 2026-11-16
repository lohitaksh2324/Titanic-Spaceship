"""
Generate the official 15-Slide Spaceship Titanic Presentation PPTX.
Clean card layouts, bold typography, statistical callouts, embedded charts, and clickable live links.
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE


def build_deck(filename="Spaceship_Titanic_Presentation.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Theme Colors
    NAVY = RGBColor(11, 19, 43)          # #0B132B Dark Navy
    TEAL = RGBColor(13, 148, 136)        # #0D9488 Primary Teal
    DARK_TEAL = RGBColor(15, 118, 110)   # #0F766E
    TEXT_MAIN = RGBColor(15, 23, 42)     # #0F172A Dark Slate
    TEXT_MUTED = RGBColor(100, 116, 139) # #64748B Slate Muted
    CARD_BG = RGBColor(248, 250, 252)    # #F8FAFC Off-white
    CARD_BORDER = RGBColor(226, 232, 240)# #E2E8F0
    WHITE = RGBColor(255, 255, 255)
    LIGHT_TEAL = RGBColor(240, 253, 250) # #F0FDFA
    CORAL = RGBColor(225, 29, 72)        # Negative highlight
    EMERALD = RGBColor(16, 185, 129)

    def set_font(run, name="Calibri", size=Pt(14), bold=False, color=TEXT_MAIN, link=None):
        run.font.name = name
        run.font.size = size
        run.font.bold = bold
        run.font.color.rgb = color
        if link:
            run.hyperlink.address = link

    def add_header(slide, title, subtitle):
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(1.1))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p1 = tf.paragraphs[0]
        p1.space_after = Pt(4)
        run1 = p1.add_run()
        run1.text = title
        set_font(run1, name="Georgia", size=Pt(28), bold=True, color=TEXT_MAIN)

        p2 = tf.add_paragraph()
        run2 = p2.add_run()
        run2.text = subtitle
        set_font(run2, name="Calibri", size=Pt(13), bold=False, color=TEXT_MUTED)

    def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        if border_color:
            shape.line.color.rgb = border_color
            shape.line.width = Pt(1.2)
        else:
            shape.line.fill.background()
        return shape

    # ==========================================
    # SLIDE 1: Title Slide (Dark Navy Background)
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY
    bg1.line.fill.background()

    tb1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.333), Inches(4.5))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.space_after = Pt(8)
    r = p.add_run()
    r.text = "Spaceship Titanic Prediction System"
    set_font(r, name="Georgia", size=Pt(40), bold=True, color=WHITE)

    p = tf1.add_paragraph()
    p.space_after = Pt(36)
    r = p.add_run()
    r.text = "Production MLOps Binary Classification Pipeline with FastAPI, Docker & Render Cloud"
    set_font(r, name="Calibri", size=Pt(18), bold=False, color=TEAL)

    p = tf1.add_paragraph()
    p.space_after = Pt(6)
    r = p.add_run()
    r.text = "Course: CSL236 — Introduction to AI and Machine Learning | End-Term Project"
    set_font(r, name="Calibri", size=Pt(14), bold=True, color=WHITE)

    p = tf1.add_paragraph()
    p.space_after = Pt(4)
    r = p.add_run()
    r.text = "Team Members: Krishna Singla (24csu105)  •  Lohitaksh (24csu115)  •  Manya (24csu123)"
    set_font(r, name="Calibri", size=Pt(13), bold=False, color=RGBColor(203, 213, 225))

    p = tf1.add_paragraph()
    r = p.add_run()
    r.text = "Live Deployment: "
    set_font(r, name="Calibri", size=Pt(14), bold=False, color=RGBColor(203, 213, 225))
    r_link = p.add_run()
    r_link.text = "https://titanic-spaceship.onrender.com/"
    set_font(r_link, name="Calibri", size=Pt(14), bold=True, color=TEAL, link="https://titanic-spaceship.onrender.com/")

    # ==========================================
    # SLIDE 2: Problem Statement & Motivation
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Why Predict Spacetime Anomaly Displacement?",
               "During transit near Alpha Centauri, the Spaceship Titanic collided with a spacetime rift, transporting thousands of passengers.")

    card_w = Inches(3.64)
    card_h = Inches(4.8)
    top_pos = Inches(1.8)
    xs = [Inches(0.8), Inches(4.84), Inches(8.88)]

    items_s2 = [
        ("1", "Identify At-Risk Areas",
         "Pinpoint cabin decks and passenger sections most susceptible to spacetime rift displacement.\n\n"
         "Analyze correlation between passenger location (Deck B vs E, Starboard vs Port) and transport probability."),
        ("2", "Automate Rescue Triaging",
         "Deploy an automated binary classifier to immediately triage missing passengers from ship telemetry.\n\n"
         "Enable emergency responders to focus search algorithms where passengers are most likely displaced."),
        ("3", "Production Reliability",
         "Deliver a validated REST API with strict Pydantic data contract enforcement and drift monitoring.\n\n"
         "Ensure sub-15ms inference latency, automated unit testing, containerization, and public cloud deployment.")
    ]

    for i, (num, heading, text) in enumerate(items_s2):
        add_card(s2, xs[i], top_pos, card_w, card_h)
        badge = s2.shapes.add_shape(MSO_SHAPE.OVAL, xs[i] + Inches(0.4), top_pos + Inches(0.4), Inches(0.7), Inches(0.7))
        badge.fill.solid()
        badge.fill.fore_color.rgb = TEAL
        badge.line.fill.background()
        bp = badge.text_frame.paragraphs[0]
        bp.alignment = PP_ALIGN.CENTER
        br = bp.add_run()
        br.text = num
        set_font(br, name="Calibri", size=Pt(18), bold=True, color=WHITE)

        tb = s2.shapes.add_textbox(xs[i] + Inches(0.4), top_pos + Inches(1.3), card_w - Inches(0.8), Inches(3.2))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.space_after = Pt(10)
        r = p.add_run()
        r.text = heading
        set_font(r, name="Georgia", size=Pt(18), bold=True, color=TEXT_MAIN)

        p = tf.add_paragraph()
        r = p.add_run()
        r.text = text
        set_font(r, name="Calibri", size=Pt(14), bold=False, color=TEXT_MUTED)

    # ==========================================
    # SLIDE 3: The Dataset Structure
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "The Dataset Structure",
               "8,693 training records × 14 columns spanning demographics, cabin telemetry, and amenity expenditures")

    cats = [
        ("Demographics", "HomePlanet (Earth, Europa, Mars), Age (0–79), VIP status (True/False)"),
        ("Spatial Telemetry", "Cabin (Deck / Cabin Number / Side: Port vs Starboard)"),
        ("Travel Group", "PassengerId (encoded as Group_ID and Passenger_Num within party)"),
        ("Amenity Spend", "RoomService, FoodCourt, ShoppingMall, Spa, VRDeck (USD expenditure)"),
        ("CryoSleep Status", "CryoSleep (Suspended animation in pod vs awake wandering the ship)"),
        ("Target Variable", "Transported (Boolean: True = 4,378 [50.36%], False = 4,315 [49.64%] — perfectly balanced)")
    ]

    p_top = Inches(1.6)
    p_h = Inches(0.78)
    for i, (cat, desc) in enumerate(cats):
        cur_top = p_top + i * Inches(0.88)
        is_target = (i == 5)
        bg_col = TEAL if is_target else CARD_BG
        bdr_col = TEAL if is_target else CARD_BORDER
        txt_main = WHITE if is_target else TEXT_MAIN
        txt_desc = WHITE if is_target else TEXT_MUTED

        add_card(s3, Inches(0.8), cur_top, Inches(11.733), p_h, bg_color=bg_col, border_color=bdr_col)
        tb = s3.shapes.add_textbox(Inches(1.1), cur_top + Inches(0.12), Inches(11.1), Inches(0.55))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        r1 = p.add_run()
        r1.text = f"{cat:<22} "
        set_font(r1, name="Georgia", size=Pt(14), bold=True, color=txt_main)
        r2 = p.add_run()
        r2.text = desc
        set_font(r2, name="Calibri", size=Pt(13), bold=False, color=txt_desc)

    # ==========================================
    # SLIDE 4: Feature Identification & Data Validation
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Feature Identification & Data Validation",
               "Every column except PassengerId and Target had ~2.0% to 2.5% missing values; 0 duplicates found")

    if os.path.exists("images/missing_values.png"):
        s4.shapes.add_picture("images/missing_values.png", Inches(0.8), Inches(1.8), width=Inches(5.7))

    add_card(s4, Inches(6.8), Inches(1.8), Inches(5.733), Inches(4.9), bg_color=WHITE, border_color=CARD_BORDER)
    tb4 = s4.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.133), Inches(4.5))
    tf4 = tb4.text_frame
    tf4.word_wrap = True

    p = tf4.paragraphs[0]
    p.space_after = Pt(12)
    r = p.add_run()
    r.text = "Domain-Specific Imputation Rules"
    set_font(r, name="Georgia", size=Pt(18), bold=True, color=DARK_TEAL)

    rules = [
        ("✓ CryoSleep Spending Rule", "Passengers in CryoSleep cannot visit amenities; missing spending is strictly imputed to $0."),
        ("✓ Numeric Amenities & Age", "Remaining missing spend and Age imputed with median to resist positive skew."),
        ("✓ Categorical Telemetry", "HomePlanet, Destination, Deck, and Side imputed with mode (highest frequency class)."),
        ("✓ Zero Data Leakage", "All imputers fitted strictly on training data and applied downstream to validation/test sets.")
    ]
    for title, desc in rules:
        p = tf4.add_paragraph()
        p.space_after = Pt(2)
        r = p.add_run()
        r.text = title
        set_font(r, name="Calibri", size=Pt(13), bold=True, color=TEXT_MAIN)
        p = tf4.add_paragraph()
        p.space_after = Pt(10)
        r = p.add_run()
        r.text = desc
        set_font(r, name="Calibri", size=Pt(14), bold=False, color=TEXT_MUTED)

    # ==========================================
    # SLIDE 5: Outlier Detection & Capping (IQR Method)
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Outlier Detection & Capping (IQR Method)",
               "Preserving full sample size using Winsorization at Q3 + 3.0 × IQR rather than dropping valuable records")

    add_card(s5, Inches(0.8), Inches(1.8), Inches(4.2), Inches(5.0))
    tb5_l = s5.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(3.6), Inches(4.4))
    tf5_l = tb5_l.text_frame
    tf5_l.word_wrap = True

    p = tf5_l.paragraphs[0]
    p.space_after = Pt(4)
    r = p.add_run()
    r.text = "8,693 → 8,693"
    set_font(r, name="Georgia", size=Pt(32), bold=True, color=TEAL)

    p = tf5_l.add_paragraph()
    p.space_after = Pt(14)
    r = p.add_run()
    r.text = "100% of rows retained (Zero dropped)"
    set_font(r, name="Calibri", size=Pt(14), bold=True, color=TEXT_MAIN)

    p = tf5_l.add_paragraph()
    r = p.add_run()
    r.text = ("Traditional row deletion would discard ~22% of passenger records because luxury spend is naturally sparse.\n\n"
              "Winsorization caps extreme values at Q3 + 3.0 × IQR. This bounds extreme numerical disturbance while allowing tree models "
              "to learn from every single passenger.")
    set_font(r, name="Calibri", size=Pt(14), bold=False, color=TEXT_MUTED)

    if os.path.exists("images/boxplots_after.png"):
        s5.shapes.add_picture("images/boxplots_after.png", Inches(5.3), Inches(1.8), width=Inches(7.2))

    add_card(s5, Inches(5.3), Inches(4.1), Inches(7.233), Inches(2.7), bg_color=WHITE, border_color=CARD_BORDER)
    tb5_r = s5.shapes.add_textbox(Inches(5.5), Inches(4.25), Inches(6.8), Inches(2.4))
    tf5_r = tb5_r.text_frame
    tf5_r.word_wrap = True
    p = tf5_r.paragraphs[0]
    p.space_after = Pt(6)
    r = p.add_run()
    r.text = "Winsorization Upper Fences (Q3 + 3.0 × IQR):"
    set_font(r, name="Georgia", size=Pt(13), bold=True, color=DARK_TEAL)

    fences = [
        "• RoomService: Q1=$0, Q3=$47  → Upper Fence = $188.0",
        "• FoodCourt:   Q1=$0, Q3=$76  → Upper Fence = $304.0",
        "• ShoppingMall:Q1=$0, Q3=$27  → Upper Fence = $108.0",
        "• Spa:         Q1=$0, Q3=$59  → Upper Fence = $236.0",
        "• VRDeck:      Q1=$0, Q3=$46  → Upper Fence = $184.0"
    ]
    for item in fences:
        p = tf5_r.add_paragraph()
        p.space_after = Pt(2)
        r = p.add_run()
        r.text = item
        set_font(r, name="Consolas", size=Pt(14), bold=False, color=TEXT_MAIN)

    # ==========================================
    # SLIDE 6: Exploratory Analysis: What Drives Displacement?
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Exploratory Analysis: What Drives Displacement?",
               "Analysis reveals clear spatial and behavioral factors separating transported from non-transported passengers")

    xs_2x2 = [Inches(0.8), Inches(6.8)]
    ys_2x2 = [Inches(1.8), Inches(4.3)]
    w_2x2 = Inches(5.733)
    h_2x2 = Inches(2.2)

    findings = [
        ("81.8%", "CryoSleep Displacement Rate",
         "Suspended animation pods strongly correlate with anomaly displacement. Awake passengers had only a 32.9% transport rate.",
         TEAL),
        ("73.4%", "Deck B & Deck C High Vulnerability",
         "Forward upper decks (B: 73.4%, C: 68.0%) took direct spacetime hits, whereas lower decks (E: 35.7%, T: 20.0%) had far lower exposure.",
         TEAL),
        ("+10.4%", "Starboard vs Port Bias",
         "Starboard cabins (S: 55.5%) faced the initial collision vector, yielding a 10.4% higher transport rate than Port (P: 45.1%).",
         EMERALD),
        ("-0.37", "Luxury Spend Negative Correlation",
         "Spa (-0.37), RoomService (-0.36), and VRDeck (-0.34) show strong negative correlation with anomaly transport.",
         CORAL)
    ]

    for idx, (stat, title, desc, stat_color) in enumerate(findings):
        x = xs_2x2[idx % 2]
        y = ys_2x2[idx // 2]
        add_card(s6, x, y, w_2x2, h_2x2)
        tb = s6.shapes.add_textbox(x + Inches(0.4), y + Inches(0.25), w_2x2 - Inches(0.8), h_2x2 - Inches(0.5))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.space_after = Pt(2)
        r = p.add_run()
        r.text = stat + " "
        set_font(r, name="Georgia", size=Pt(26), bold=True, color=stat_color)
        r2 = p.add_run()
        r2.text = title
        set_font(r2, name="Georgia", size=Pt(14), bold=True, color=TEXT_MAIN)
        p = tf.add_paragraph()
        r = p.add_run()
        r.text = desc
        set_font(r, name="Calibri", size=Pt(14), bold=False, color=TEXT_MUTED)

    # ==========================================
    # SLIDE 7: Exploratory Correlation Analysis
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Exploratory Correlation Analysis",
               "Correlation matrix across numeric features reveals distinct behavioral profiles and low collinearity")

    if os.path.exists("images/correlation_heatmap.png"):
        s7.shapes.add_picture("images/correlation_heatmap.png", Inches(0.8), Inches(1.7), width=Inches(5.6))

    add_card(s7, Inches(6.8), Inches(1.7), Inches(5.733), Inches(5.1), bg_color=WHITE, border_color=CARD_BORDER)
    tb7 = s7.shapes.add_textbox(Inches(7.1), Inches(1.9), Inches(5.133), Inches(4.7))
    tf7 = tb7.text_frame
    tf7.word_wrap = True

    p = tf7.paragraphs[0]
    p.space_after = Pt(10)
    r = p.add_run()
    r.text = "Key Correlation Insights"
    set_font(r, name="Georgia", size=Pt(18), bold=True, color=DARK_TEAL)

    corr_insights = [
        ("Dominant Binary Predictor", "CryoSleep (r = +0.46) exhibits massive positive correlation with displacement. Passengers in pods could not evade the spacetime anomaly."),
        ("Luxury Expenditure Separation", "Spa (r = -0.37), RoomService (r = -0.36), and VRDeck (r = -0.34) confirm that active amenity spenders were awake and in lower-risk ship compartments."),
        ("Low Multicollinearity (|r| < 0.25)", "Inter-feature correlations among amenities remain low. FoodCourt vs VRDeck (r = 0.12) and Spa vs RoomService (r = 0.10) ensure each input provides unique signal."),
        ("No Dimensional Collapse", "Because correlation across independent predictors is modest, tree models can partition both spatial and financial dimensions cleanly.")
    ]
    for title, desc in corr_insights:
        p = tf7.add_paragraph()
        p.space_after = Pt(2)
        r = p.add_run()
        r.text = f"• {title}"
        set_font(r, name="Calibri", size=Pt(14), bold=True, color=TEXT_MAIN)
        p = tf7.add_paragraph()
        p.space_after = Pt(8)
        r = p.add_run()
        r.text = desc
        set_font(r, name="Calibri", size=Pt(14), bold=False, color=TEXT_MUTED)

    # ==========================================
    # SLIDE 8: Feature Engineering: Domain Insights
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Feature Engineering: Domain Insights",
               "Derived structural features that capture passenger groups, cabin orientation, and spending habits")

    fe_cards = [
        ("Cabin Decomposition", "Deck, CabinNum, Side",
         "Parsed raw Cabin string (e.g. 'B/0/P') into Deck ('B'), Room Number (0), and Side ('Port'). "
         "Captures exact physical compartment coordinates and exterior exposure."),
        ("Group Extraction", "GroupId, GroupSize, IsAlone",
         "Extracted travelling party ID and family group size from PassengerId ('gggg_pp'). "
         "Passengers in groups exhibited correlated survival patterns."),
        ("Spend Aggregation", "TotalSpend, LuxurySpend, HasSpend",
         "Summed total expenditure across all 5 amenities. Engineered LuxurySpend (Spa + VRDeck) "
         "and binary HasSpend flag to separate savers from luxury spenders."),
        ("Age Stratification", "AgeGroup (5 Bins)",
         "Binned continuous Age into Child (0–12), Teen (13–18), YoungAdult (19–35), Adult (36–60), "
         "and Senior (60+) to isolate child evacuation prioritization.")
    ]

    for idx, (title, feats, desc) in enumerate(fe_cards):
        x = xs_2x2[idx % 2]
        y = ys_2x2[idx // 2]
        add_card(s8, x, y, w_2x2, h_2x2)
        tb = s8.shapes.add_textbox(x + Inches(0.4), y + Inches(0.2), w_2x2 - Inches(0.8), h_2x2 - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.space_after = Pt(2)
        r = p.add_run()
        r.text = title
        set_font(r, name="Georgia", size=Pt(16), bold=True, color=DARK_TEAL)
        p = tf.add_paragraph()
        p.space_after = Pt(4)
        r = p.add_run()
        r.text = f"Engineered: {feats}"
        set_font(r, name="Calibri", size=Pt(14), bold=True, color=TEXT_MAIN)
        p = tf.add_paragraph()
        r = p.add_run()
        r.text = desc
        set_font(r, name="Calibri", size=Pt(14), bold=False, color=TEXT_MUTED)

    # ==========================================
    # SLIDE 9: Encoding, Scaling & Train-Validation Split
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Encoding, Scaling & Train-Validation Split",
               "Robust preparation ensuring zero data leakage and uniform feature ranges across continuous and categorical variables")

    split_cards = [
        ("Categorical Encoding", "Technique: LabelEncoder",
         "Encoded HomePlanet, Destination, Deck, Side, and AgeGroup into integers. "
         "Unknown category fallbacks were serialized to guarantee robust inference during production serving."),
        ("Feature Scaling", "Technique: MinMaxScaler [0, 1]",
         "Fitted strictly on the training set and transformed onto validation & test sets. "
         "Normalizes high-magnitude spend ($0–$304) and cabin numbers (0–1894) into uniform [0, 1] range."),
        ("Train / Validation Split", "Technique: 80 / 20 Stratified Split",
         "6,954 training samples and 1,739 validation samples. Stratification preserves the exact 50.36% / 49.64% "
         "class ratio across both partitions."),
        ("Dropped Columns", "Technique: Non-predictive IDs",
         "PassengerId, Name, Cabin (raw string), and GroupId were dropped prior to model fitting to prevent identity "
         "memorization and high-cardinality overfitting.")
    ]

    for idx, (title, tech, desc) in enumerate(split_cards):
        x = xs_2x2[idx % 2]
        y = ys_2x2[idx // 2]
        add_card(s9, x, y, w_2x2, h_2x2)
        tb = s9.shapes.add_textbox(x + Inches(0.4), y + Inches(0.2), w_2x2 - Inches(0.8), h_2x2 - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.space_after = Pt(2)
        r = p.add_run()
        r.text = title
        set_font(r, name="Georgia", size=Pt(16), bold=True, color=DARK_TEAL)
        p = tf.add_paragraph()
        p.space_after = Pt(4)
        r = p.add_run()
        r.text = tech
        set_font(r, name="Calibri", size=Pt(14), bold=True, color=TEXT_MAIN)
        p = tf.add_paragraph()
        r = p.add_run()
        r.text = desc
        set_font(r, name="Calibri", size=Pt(14), bold=False, color=TEXT_MUTED)

    # ==========================================
    # SLIDE 10: Feature Selection: SelectKBest (ANOVA F-Score)
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Feature Selection: SelectKBest (ANOVA F-Score)",
               "Statistical evaluation of feature importance using ANOVA F-classification across all 19 features")

    if os.path.exists("images/feature_importance.png"):
        s10.shapes.add_picture("images/feature_importance.png", Inches(0.8), Inches(1.8), width=Inches(5.8))

    add_card(s10, Inches(6.9), Inches(1.8), Inches(5.633), Inches(4.9), bg_color=WHITE, border_color=CARD_BORDER)
    tb10 = s10.shapes.add_textbox(Inches(7.2), Inches(2.0), Inches(5.033), Inches(4.5))
    tf10 = tb10.text_frame
    tf10.word_wrap = True

    p = tf10.paragraphs[0]
    p.space_after = Pt(8)
    r = p.add_run()
    r.text = "Top Features Ranked by F-Score"
    set_font(r, name="Georgia", size=Pt(16), bold=True, color=DARK_TEAL)

    f_scores = [
        "1. HasSpend:    F = 2,624.9 (Binary spend flag — top discriminator)",
        "2. CryoSleep:   F = 2,334.3 (Cryo-pod confinement signal)",
        "3. Spa:         F = 1,095.2 (Strongest luxury negative correlation)",
        "4. RoomService: F = 1,083.9 (Basic cabin spend signal)",
        "5. VRDeck:      F =   941.6 (Virtual entertainment spend)",
        "6. LuxurySpend: F =   736.2 (Spa + VRDeck aggregated luxury)"
    ]
    for row in f_scores:
        p = tf10.add_paragraph()
        p.space_after = Pt(2)
        r = p.add_run()
        r.text = row
        set_font(r, name="Consolas", size=Pt(14), bold=False, color=TEXT_MAIN)

    p = tf10.add_paragraph()
    p.space_before = Pt(8)
    p.space_after = Pt(2)
    r = p.add_run()
    r.text = "Key Selection Takeaways:"
    set_font(r, name="Georgia", size=Pt(14), bold=True, color=DARK_TEAL)

    p = tf10.add_paragraph()
    r = p.add_run()
    r.text = ("• HasSpend + CryoSleep account for over 65% of total F-score mass.\n"
              "• Luxury spend features (Spa, VRDeck) provide strong separation for awake travelers.\n"
              "• All 19 features are used by both Random Forest and XGBoost with no multicollinearity penalty.")
    set_font(r, name="Calibri", size=Pt(14), bold=False, color=TEXT_MUTED)

    # ==========================================
    # SLIDE 11: End-to-End System Architecture
    # ==========================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "End-to-End MLOps System Architecture",
               "Production architecture spanning data validation, MLflow tracking, containerization, and automated serving")

    arch_steps = [
        ("1. Data & Validation", "Kaggle CSV Ingestion\nDomain Imputation\nIQR Winsorization\nStratified Split (80/20)"),
        ("2. Model Training", "Random Forest\nXGBoost Classifier\nGridSearchCV 5-Fold\nHyperparameter Tuning"),
        ("3. Experiment Tracking", "MLflow SQLite Tracking\nLogged Metrics & Params\nSerialized Pipeline\nArtifact Registry"),
        ("4. Containerized API", "FastAPI Serving App\nPydantic Data Contract\nDocker (python:3.11-slim)\nSub-15ms Latency"),
        ("5. Cloud & Monitoring", "Render Cloud Hosting\nGitHub Actions CI/CD\nPrediction Logging\nDrift Detection (Z-score)")
    ]

    step_w = Inches(2.18)
    step_h = Inches(4.6)
    step_xs = [Inches(0.8) + i * Inches(2.38) for i in range(5)]

    for i, (head, body) in enumerate(arch_steps):
        is_highlight = (i == 3 or i == 4)
        bg = LIGHT_TEAL if is_highlight else CARD_BG
        bdr = TEAL if is_highlight else CARD_BORDER
        add_card(s11, step_xs[i], Inches(1.8), step_w, step_h, bg_color=bg, border_color=bdr)

        tb = s11.shapes.add_textbox(step_xs[i] + Inches(0.15), Inches(2.0), step_w - Inches(0.3), step_h - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.space_after = Pt(12)
        r = p.add_run()
        r.text = head
        set_font(r, name="Georgia", size=Pt(13.5), bold=True, color=DARK_TEAL)

        p = tf.add_paragraph()
        r = p.add_run()
        r.text = body
        set_font(r, name="Calibri", size=Pt(14), bold=False, color=TEXT_MAIN)

    # ==========================================
    # SLIDE 12: Experiment Tracking & Model Comparison
    # ==========================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Experiment Tracking & Model Comparison",
               "Four tracked configurations across Random Forest and XGBoost logged to SQLite MLflow backend (sqlite:///mlflow.db)")

    add_card(s12, Inches(0.8), Inches(1.8), Inches(6.8), Inches(4.9), bg_color=WHITE, border_color=CARD_BORDER)
    tb12 = s12.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(6.4), Inches(4.5))
    tf12 = tb12.text_frame
    tf12.word_wrap = True

    p = tf12.paragraphs[0]
    p.space_after = Pt(8)
    r = p.add_run()
    r.text = "MLflow Experiment Tracking Results"
    set_font(r, name="Georgia", size=Pt(16), bold=True, color=DARK_TEAL)

    headers = f"{'Algorithm':<22} {'Hyperparameters':<23} {'Accuracy':<9} {'ROC-AUC'}"
    p = tf12.add_paragraph()
    p.space_after = Pt(4)
    r = p.add_run()
    r.text = headers
    set_font(r, name="Consolas", size=Pt(13), bold=True, color=TEAL)

    runs = [
        ("RF (Baseline)", "n_est=100, depth=8", "0.7936", "0.8845"),
        ("RF (Tuned)", "n_est=200, depth=12", "0.8033", "0.8935"),
        ("XGBoost (Baseline)", "n_est=100, depth=4, lr=0.08", "0.8028", "0.9046"),
        ("Tuned XGBoost ★", "n_est=250, depth=6, lr=0.03", "0.8125", "0.9087")
    ]
    for m, prms, acc, auc in runs:
        is_best = "★" in m
        p = tf12.add_paragraph()
        p.space_after = Pt(3)
        r = p.add_run()
        r.text = f"{m:<22} {prms:<23} {acc:<9} {auc}"
        col = DARK_TEAL if is_best else TEXT_MAIN
        set_font(r, name="Consolas", size=Pt(13), bold=is_best, color=col)

    p = tf12.add_paragraph()
    p.space_before = Pt(12)
    p.space_after = Pt(4)
    r = p.add_run()
    r.text = "★ Best Model: Tuned XGBoost"
    set_font(r, name="Georgia", size=Pt(13), bold=True, color=DARK_TEAL)

    p = tf12.add_paragraph()
    r = p.add_run()
    r.text = ("• Achieved highest validation accuracy (81.25%) and ROC-AUC (0.9087).\n"
              "• Serialized to model/model.joblib for live production serving.\n"
              "• 3x faster inference latency than Random Forest ensemble.")
    set_font(r, name="Calibri", size=Pt(14), bold=False, color=TEXT_MUTED)

    # Right: Tuned XGBoost Feature Importance
    if os.path.exists("images/best_model_feature_importance.png"):
        s12.shapes.add_picture("images/best_model_feature_importance.png", Inches(7.8), Inches(1.8), width=Inches(4.733))
        
    add_card(s12, Inches(7.8), Inches(4.8), Inches(4.733), Inches(1.9), bg_color=LIGHT_TEAL, border_color=TEAL)
    tb12_r = s12.shapes.add_textbox(Inches(8.0), Inches(4.9), Inches(4.333), Inches(1.7))
    tf12_r = tb12_r.text_frame
    tf12_r.word_wrap = True
    p = tf12_r.paragraphs[0]
    p.space_after = Pt(4)
    r = p.add_run()
    r.text = "Tree Feature Split Dynamics"
    set_font(r, name="Georgia", size=Pt(13), bold=True, color=DARK_TEAL)
    p = tf12_r.add_paragraph()
    r = p.add_run()
    r.text = ("HasSpend and HomePlanet provide top-level branch discriminators, followed by RoomService, "
              "CryoSleep, and LuxurySpend (Spa + VRDeck).")
    set_font(r, name="Calibri", size=Pt(13), bold=False, color=TEXT_MAIN)

    # ==========================================
    # SLIDE 13: Final Model Performance: Tuned XGBoost
    # ==========================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "Final Model Performance: Tuned XGBoost",
               "Detailed classification evaluation on the independent 1,739-sample validation holdout")

    top_xs_4 = [Inches(0.8) + i * Inches(2.98) for i in range(4)]
    w_card_4 = Inches(2.78)
    h_card_4 = Inches(1.5)

    metrics = [
        ("81.25%", "Validation Accuracy", "Overall accuracy on holdout"),
        ("0.9087", "ROC-AUC Score", "Class ranking discrimination"),
        ("80.42%", "Precision (Class 1)", "Low false anomaly alarms"),
        ("82.53%", "Recall (Class 1)", "Captures >82% transported")
    ]

    for i, (val, title, note) in enumerate(metrics):
        add_card(s13, top_xs_4[i], Inches(1.6), w_card_4, h_card_4, bg_color=LIGHT_TEAL, border_color=TEAL)
        tb = s13.shapes.add_textbox(top_xs_4[i] + Inches(0.15), Inches(1.7), w_card_4 - Inches(0.3), h_card_4 - Inches(0.2))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = val
        set_font(r, name="Georgia", size=Pt(22), bold=True, color=DARK_TEAL)
        p = tf.add_paragraph()
        r = p.add_run()
        r.text = title
        set_font(r, name="Calibri", size=Pt(14), bold=True, color=TEXT_MAIN)
        p = tf.add_paragraph()
        r = p.add_run()
        r.text = note
        set_font(r, name="Calibri", size=Pt(13), bold=False, color=TEXT_MUTED)

    if os.path.exists("images/confusion_matrices.png"):
        s13.shapes.add_picture("images/confusion_matrices.png", Inches(0.8), Inches(3.3), width=Inches(6.4))
    if os.path.exists("images/roc_curves.png"):
        s13.shapes.add_picture("images/roc_curves.png", Inches(7.4), Inches(3.3), width=Inches(5.133))

    # ==========================================
    # SLIDE 14: Production Serving & System Validation
    # ==========================================
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "Production Serving & System Validation",
               "FastAPI REST API, automated testing suite, Docker containerization, and data drift monitoring")

    prod_cards = [
        ("FastAPI REST Service", "Endpoints: GET /health, POST /predict, GET / (UI)",
         "Model loaded once into memory at startup. Executes feature extraction, imputation, scaling, "
         "and inference in sub-15ms latency per request."),
        ("Pydantic Data Contract", "Strict Input Boundary Enforcement",
         "Rejects out-of-bounds spend (negative amounts), invalid deck coordinates, or malformed payloads "
         "with HTTP 422 Unprocessable Entity responses."),
        ("Automated Pytest Suite", "4 of 4 Unit Tests Passing (3.13s)",
         "Automated test suite validates /health readiness, static UI loading, domain CryoSleep prediction logic, "
         "and contract rejection of negative spending."),
        ("Data Drift Monitoring", "drift_check.py Baseline Comparison",
         "Parses logs/predictions.log against training set baseline. Computes feature mean, std, and Z-scores to "
         "flag distribution drift for automated retraining.")
    ]

    for idx, (title, sub, desc) in enumerate(prod_cards):
        x = xs_2x2[idx % 2]
        y = ys_2x2[idx // 2]
        add_card(s14, x, y, w_2x2, h_2x2)
        tb = s14.shapes.add_textbox(x + Inches(0.4), y + Inches(0.2), w_2x2 - Inches(0.8), h_2x2 - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.space_after = Pt(2)
        r = p.add_run()
        r.text = title
        set_font(r, name="Georgia", size=Pt(16), bold=True, color=DARK_TEAL)
        p = tf.add_paragraph()
        p.space_after = Pt(4)
        r = p.add_run()
        r.text = sub
        set_font(r, name="Calibri", size=Pt(14), bold=True, color=TEXT_MAIN)
        p = tf.add_paragraph()
        r = p.add_run()
        r.text = desc
        set_font(r, name="Calibri", size=Pt(14), bold=False, color=TEXT_MUTED)

    # ==========================================
    # SLIDE 15: Live Project Links, Conclusion & Future Scope
    # ==========================================
    s15 = prs.slides.add_slide(blank_layout)
    add_header(s15, "Live Project Links, Conclusion & Future Scope",
               "Shipped as a validated Dockerized MLOps system deployed live on Render with automated CI/CD")

    # Left: Dark Card with Live Links
    add_card(s15, Inches(0.8), Inches(1.8), Inches(5.733), Inches(4.9), bg_color=NAVY, border_color=None)
    tb15_l = s15.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.133), Inches(4.5))
    tf15_l = tb15_l.text_frame
    tf15_l.word_wrap = True

    p = tf15_l.paragraphs[0]
    p.space_after = Pt(12)
    r = p.add_run()
    r.text = "Live Deliverables (Clickable)"
    set_font(r, name="Georgia", size=Pt(18), bold=True, color=WHITE)

    # 1. Live Web App
    p = tf15_l.add_paragraph()
    p.space_after = Pt(2)
    r = p.add_run()
    r.text = "🔗 Live Web App (Render):"
    set_font(r, name="Calibri", size=Pt(14), bold=True, color=WHITE)
    p = tf15_l.add_paragraph()
    p.space_after = Pt(8)
    r = p.add_run()
    r.text = "https://titanic-spaceship.onrender.com/"
    set_font(r, name="Calibri", size=Pt(14), bold=False, color=TEAL, link="https://titanic-spaceship.onrender.com/")

    # 2. Swagger API
    p = tf15_l.add_paragraph()
    p.space_after = Pt(2)
    r = p.add_run()
    r.text = "📑 Swagger API Docs:"
    set_font(r, name="Calibri", size=Pt(14), bold=True, color=WHITE)
    p = tf15_l.add_paragraph()
    p.space_after = Pt(8)
    r = p.add_run()
    r.text = "https://titanic-spaceship.onrender.com/docs"
    set_font(r, name="Calibri", size=Pt(14), bold=False, color=TEAL, link="https://titanic-spaceship.onrender.com/docs")

    # 3. GitHub
    p = tf15_l.add_paragraph()
    p.space_after = Pt(2)
    r = p.add_run()
    r.text = "💻 GitHub Repository:"
    set_font(r, name="Calibri", size=Pt(14), bold=True, color=WHITE)
    p = tf15_l.add_paragraph()
    p.space_after = Pt(8)
    r = p.add_run()
    r.text = "https://github.com/lohitaksh2324/Titanic-Spaceship"
    set_font(r, name="Calibri", size=Pt(14), bold=False, color=TEAL, link="https://github.com/lohitaksh2324/Titanic-Spaceship")

    # 4. Kaggle
    p = tf15_l.add_paragraph()
    p.space_after = Pt(2)
    r = p.add_run()
    r.text = "📊 Kaggle Submission:"
    set_font(r, name="Calibri", size=Pt(14), bold=True, color=WHITE)
    p = tf15_l.add_paragraph()
    p.space_after = Pt(8)
    r = p.add_run()
    r.text = "submission.csv (4,277 test predictions generated)"
    set_font(r, name="Calibri", size=Pt(14), bold=False, color=RGBColor(203, 213, 225))

    # 5. Team
    p = tf15_l.add_paragraph()
    p.space_after = Pt(2)
    r = p.add_run()
    r.text = "👥 Team Members (CSL236):"
    set_font(r, name="Calibri", size=Pt(14), bold=True, color=WHITE)
    p = tf15_l.add_paragraph()
    r = p.add_run()
    r.text = "Krishna Singla (24csu105) • Lohitaksh (24csu115) • Manya (24csu123)"
    set_font(r, name="Calibri", size=Pt(14), bold=False, color=RGBColor(203, 213, 225))

    # Right: Future Scope Card
    add_card(s15, Inches(6.8), Inches(1.8), Inches(5.733), Inches(4.9), bg_color=WHITE, border_color=CARD_BORDER)
    tb15_r = s15.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.133), Inches(4.5))
    tf15_r = tb15_r.text_frame
    tf15_r.word_wrap = True

    p = tf15_r.paragraphs[0]
    p.space_after = Pt(12)
    r = p.add_run()
    r.text = "Production Roadmap & Future Scope"
    set_font(r, name="Georgia", size=Pt(18), bold=True, color=DARK_TEAL)

    roadmap = [
        ("• Automated Retraining Triggers", "Extend drift_check.py to automatically trigger GitHub Actions model retraining whenever prediction feature drift exceeds Z = 2.0."),
        ("• Real-Time Explainability in UI", "Integrate SHAP waterfall or force plots directly into the web UI so ship officers receive instant explanations for each passenger."),
        ("• Multi-Model Blending Exploration", "Evaluate LightGBM and CatBoost blenders for incremental Kaggle accuracy gains while maintaining sub-15ms latency."),
        ("• Kubernetes Cluster Scaling", "Migrate from Render free container to multi-pod Kubernetes deployment with Redis prediction caching for high-volume telemetry loads.")
    ]
    for title, desc in roadmap:
        p = tf15_r.add_paragraph()
        p.space_after = Pt(2)
        r = p.add_run()
        r.text = title
        set_font(r, name="Calibri", size=Pt(14), bold=True, color=TEXT_MAIN)
        p = tf15_r.add_paragraph()
        p.space_after = Pt(8)
        r = p.add_run()
        r.text = desc
        set_font(r, name="Calibri", size=Pt(14), bold=False, color=TEXT_MUTED)

    prs.save(filename)
    print(f"Presentation successfully saved to {filename} ({len(prs.slides)} slides)")


if __name__ == "__main__":
    build_deck("Spaceship_Titanic_Presentation.pptx")
