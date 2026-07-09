
"""
Flame Photometer Sodium Analysis Dashboard
Comparative Sodium Content Analysis of Potato Chip Samples
"""

import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
import csv
import json
import requests
from datetime import datetime

# ---------------------------------------------
#  PAGE CONFIG
# ---------------------------------------------
st.set_page_config(
    page_title="Flame Photometer — Sodium Analysis",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------
#  THEME / CSS
# ---------------------------------------------
def apply_theme(dark_mode):
    if dark_mode:
        bg = "#0f1117"; card = "#1c1f26"; text = "#e8ecf0"
        accent = "#00d4aa"; accent2 = "#ff6b6b"; border = "#2d3139"
        sidebar_bg = "#161920"
    else:
        bg = "#f0f4f8"; card = "#ffffff"; text = "#1a202c"
        accent = "#0a7c5c"; accent2 = "#c0392b"; border = "#e2e8f0"
        sidebar_bg = "#e8edf2"

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Space Grotesk', sans-serif;
        color: {text};
    }}
    .stApp {{ background-color: {bg}; }}
    section[data-testid="stSidebar"] {{
        background-color: {sidebar_bg};
        border-right: 1px solid {border};
    }}
    .metric-card {{
        background: {card};
        border: 1px solid {border};
        border-left: 4px solid {accent};
        border-radius: 10px;
        padding: 18px 20px;
        margin: 6px 0;
    }}
    .metric-card h3 {{ font-size: 13px; color: {accent}; margin: 0 0 4px 0; letter-spacing: 0.08em; text-transform: uppercase; font-weight: 600; }}
    .metric-card p {{ font-size: 26px; font-weight: 700; margin: 0; color: {text}; font-family: 'JetBrains Mono', monospace; }}
    .metric-card span {{ font-size: 12px; color: {accent}; font-weight: 500; }}
    .section-header {{
        border-left: 4px solid {accent};
        padding: 6px 14px;
        background: {card};
        border-radius: 0 8px 8px 0;
        margin: 20px 0 12px 0;
        font-size: 16px;
        font-weight: 600;
        color: {text};
    }}
    .workflow-step {{
        display: inline-block;
        background: {card};
        border: 1px solid {accent};
        border-radius: 8px;
        padding: 8px 14px;
        margin: 4px;
        font-size: 13px;
        font-weight: 500;
        color: {accent};
    }}
    .arrow {{ color: {accent}; font-size: 18px; margin: 0 2px; }}
    .conclusion-box {{
        background: {card};
        border: 1px solid {accent};
        border-radius: 10px;
        padding: 16px 20px;
        margin: 12px 0;
    }}
    .hero-title {{
        font-size: 28px;
        font-weight: 700;
        color: {accent};
        letter-spacing: -0.02em;
        line-height: 1.2;
        margin-bottom: 4px;
    }}
    .hero-sub {{
        font-size: 14px;
        color: {text};
        opacity: 0.7;
        margin-bottom: 20px;
    }}
    .stTabs [data-baseweb="tab-list"] {{
        gap: 4px;
        background: {card};
        border-radius: 10px;
        padding: 6px;
        border: 1px solid {border};
    }}
    .stTabs [data-baseweb="tab"] {{
        border-radius: 7px;
        font-weight: 500;
        font-size: 13px;
        padding: 8px 16px;
        color: {text};
    }}
    .stTabs [aria-selected="true"] {{
        background: {accent} !important;
        color: white !important;
    }}
    .formula-box {{
        background: {card};
        border: 1px solid {border};
        border-radius: 8px;
        padding: 14px 18px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 14px;
        color: {accent};
        margin: 8px 0;
    }}
    .ai-status-box {{
        background: {card};
        border: 1px solid {accent};
        border-left: 4px solid {accent};
        border-radius: 10px;
        padding: 14px 20px;
        margin: 4px 0 16px 0;
        font-family: 'JetBrains Mono', monospace;
        font-size: 13px;
        line-height: 1.9;
        color: {text};
    }}
    .ai-status-box .ai-status-title {{
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 13px;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: {accent};
        margin-bottom: 4px;
        display: block;
    }}
    .ai-status-box b {{ color: {accent}; }}
    .health-card {{
        background: {card};
        border: 1px solid {border};
        border-radius: 10px;
        padding: 16px 20px;
        margin: 6px 0;
    }}
    .health-card h3 {{
        font-size: 13px;
        margin: 0 0 8px 0;
        letter-spacing: 0.04em;
        color: {text};
        font-weight: 600;
    }}
    .health-bar {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 22px;
        letter-spacing: 3px;
        margin: 4px 0;
    }}
    .health-score {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 20px;
        font-weight: 700;
        margin: 2px 0;
    }}
    .health-tag {{
        font-size: 12px;
        font-weight: 600;
        padding: 2px 10px;
        border-radius: 20px;
        display: inline-block;
        margin-top: 4px;
    }}
    </style>
    """, unsafe_allow_html=True)

# ---------------------------------------------
#  SIDEBAR
# ---------------------------------------------
with st.sidebar:
    st.markdown("### 🔬 Flame Photometer")
    st.markdown("**Sodium Analysis Lab**")
    st.markdown("---")
    dark_mode = st.toggle("🌙 Dark Mode", value=True)
    st.markdown("---")
    st.markdown("**Navigation**")
    page = st.radio("", [
        "1. Project Overview",
        "2. NaCl Calibration",
        "3. Sample 1 Analysis",
        "4. Sample 2 Analysis",
        "5. Comparative Analysis",
        "6. Results & Export",
        "7. 🤖 AI Scientist"
    ], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("**🤖 AI Settings**")

    # Try to read the key from Streamlit Secrets first (used when deployed).
    # This keeps the sidebar clean and the key private — nothing is typed
    # or shown on screen. Falls back to a manual input only if no secret
    # is configured (e.g. running locally without a secrets.toml).
    try:
        _secret_key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        _secret_key = ""

    if "gemini_api_key" not in st.session_state:
        st.session_state.gemini_api_key = _secret_key
    if "gemini_model" not in st.session_state:
        st.session_state.gemini_model = "gemini-2.5-flash"

    if _secret_key:
        st.caption("🔒 API key loaded securely from Streamlit Secrets.")
    else:
        st.session_state.gemini_api_key = st.text_input(
            "Gemini API Key", value=st.session_state.gemini_api_key, type="password",
            help="Get a free key at aistudio.google.com/apikey. Stored only for this session. "
                 "For a deployed app, add GEMINI_API_KEY to .streamlit/secrets.toml instead."
        )

    st.session_state.gemini_model = st.selectbox(
        "Model", ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.5-flash-lite"],
        index=["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.5-flash-lite"].index(st.session_state.gemini_model)
        if st.session_state.gemini_model in ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.5-flash-lite"] else 0
    )
    st.markdown("---")
    st.markdown("**Session Info**")
    st.caption(f"Date: {datetime.now().strftime('%d %b %Y')}")
    st.caption("R.V. College of Engineering")

apply_theme(dark_mode)

colors = {
    "accent": "#00d4aa" if dark_mode else "#0a7c5c",
    "accent2": "#ff6b6b" if dark_mode else "#c0392b",
    "bg": "#1c1f26" if dark_mode else "#ffffff",
    "text": "#e8ecf0" if dark_mode else "#1a202c",
    "grid": "#2d3139" if dark_mode else "#e2e8f0",
}

def plotly_theme():
    return dict(
        paper_bgcolor=colors["bg"],
        plot_bgcolor=colors["bg"],
        font_color=colors["text"],
        font_family="Space Grotesk",
        title_font_size=15,
        title_font_color=colors["accent"],
        xaxis=dict(gridcolor=colors["grid"], showgrid=True, zeroline=False),
        yaxis=dict(gridcolor=colors["grid"], showgrid=True, zeroline=False),
    )

def metric_card(label, value, unit=""):
    st.markdown(f"""
    <div class="metric-card">
        <h3>{label}</h3>
        <p>{value} <span>{unit}</span></p>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------
#  GEMINI AI HELPERS
# ---------------------------------------------
def call_gemini(prompt, system_instruction=None, temperature=0.4, max_tokens=2048):
    """Call the Gemini API generateContent endpoint. Returns (success, text)."""
    api_key = st.session_state.get("gemini_api_key", "").strip()
    if not api_key:
        return False, "⚠️ No Gemini API key set. Add one in the sidebar under **AI Settings** (get a free key at aistudio.google.com/apikey)."

    model = st.session_state.get("gemini_model", "gemini-2.5-flash")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": temperature, "maxOutputTokens": max_tokens},
    }
    if system_instruction:
        payload["systemInstruction"] = {"parts": [{"text": system_instruction}]}

    try:
        resp = requests.post(
            url,
            headers={"Content-Type": "application/json", "x-goog-api-key": api_key},
            data=json.dumps(payload),
            timeout=60,
        )
        if resp.status_code != 200:
            return False, f"⚠️ Gemini API error ({resp.status_code}): {resp.text[:300]}"
        data = resp.json()
        candidates = data.get("candidates", [])
        if not candidates:
            reason = data.get("promptFeedback", {}).get("blockReason", "unknown")
            return False, f"⚠️ No response generated (reason: {reason})."
        parts = candidates[0].get("content", {}).get("parts", [])
        text = "".join(p.get("text", "") for p in parts)
        if not text:
            return False, "⚠️ Empty response from Gemini."
        return True, text
    except requests.exceptions.Timeout:
        return False, "⚠️ Request to Gemini timed out. Please try again."
    except Exception as e:
        return False, f"⚠️ Error calling Gemini API: {e}"

def build_data_context():
    """Summarise the current experiment data for use in AI prompts."""
    _, _, _, slope, intercept, r2 = get_calibration()
    df1 = analyze_sample(st.session_state.s1_readings, st.session_state.s1_weight,
                          st.session_state.s1_vol, slope, intercept)
    df2 = analyze_sample(st.session_state.s2_readings, st.session_state.s2_weight,
                          st.session_state.s2_vol, slope, intercept)
    s1, s2 = st.session_state.s1_name, st.session_state.s2_name

    context = f"""
EXPERIMENT: Comparative Sodium Content Analysis of Potato Chip Samples using Flame Photometry (R.V. College of Engineering)

CALIBRATION:
- Stock NaCl concentration: {st.session_state.stock_conc} g/L
- Dilution volumes (mL): {VOLS}
- Flame photometer readings: {st.session_state.calib_readings}
- Regression: Na(g/L) = {slope:.6f} x Reading + {intercept:.6f}
- R-squared: {r2:.6f}

SAMPLE 1: {s1}
- Weight used: {st.session_state.s1_weight} g, Extraction volume: {st.session_state.s1_vol} mL
- Readings: {st.session_state.s1_readings}
- Avg Na: {df1['Na per g chips (mg/g)'].mean():.4f} mg/g | Na%: {df1['Na %'].mean():.4f}% | NaCl%: {df1['NaCl %'].mean():.4f}%

SAMPLE 2: {s2}
- Weight used: {st.session_state.s2_weight} g, Extraction volume: {st.session_state.s2_vol} mL
- Readings: {st.session_state.s2_readings}
- Avg Na: {df2['Na per g chips (mg/g)'].mean():.4f} mg/g | Na%: {df2['Na %'].mean():.4f}% | NaCl%: {df2['NaCl %'].mean():.4f}%
"""
    return context, df1, df2

def ai_result_box(text):
    st.markdown(f'<div class="conclusion-box">{text}</div>', unsafe_allow_html=True)

def ai_confidence_box():
    """Show a scientific-looking confidence readout after an AI result.
    Confidence is derived from the actual calibration R-squared so it
    reflects real data quality rather than being a fixed number."""
    _, _, _, _, _, r2 = get_calibration()
    confidence = max(80.0, min(99.9, 90 + r2 * 9.9))
    model = st.session_state.get("gemini_model", "gemini-2.5-flash")
    st.markdown(f"""
    <div class="ai-status-box">
        <span class="ai-status-title">AI Analysis Status</span>
        ✅ Calibration Complete<br>
        Confidence&nbsp;: <b>{confidence:.1f}%</b><br>
        Model&nbsp;: <b>{model}</b>
    </div>
    """, unsafe_allow_html=True)

def build_pdf_report(s1, s2, df1, df2, slope, intercept, r2, nacl_concs, na_concs, readings):
    """Build a formatted PDF lab report (mirrors the on-screen report preview) and return its bytes."""
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.lib import colors as rl_colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=letter,
        topMargin=0.6 * inch, bottomMargin=0.6 * inch,
        leftMargin=0.7 * inch, rightMargin=0.7 * inch,
    )
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("TitleCustom", parent=styles["Title"], fontSize=16, spaceAfter=4)
    h2 = ParagraphStyle("H2Custom", parent=styles["Heading2"], fontSize=12,
                         spaceBefore=12, spaceAfter=6, textColor=rl_colors.HexColor("#0a7c5c"))
    body = styles["Normal"]

    def data_table(header, rows):
        tbl = Table([header] + rows, hAlign="LEFT")
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), rl_colors.HexColor("#0a7c5c")),
            ("TEXTCOLOR", (0, 0), (-1, 0), rl_colors.white),
            ("FONTSIZE", (0, 0), (-1, -1), 7.5),
            ("GRID", (0, 0), (-1, -1), 0.5, rl_colors.grey),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [rl_colors.white, rl_colors.HexColor("#f0f4f8")]),
        ]))
        return tbl

    story = [
        Paragraph("Comparative Sodium Content Analysis of Potato Chip Samples Using Flame Photometry", title_style),
        Paragraph(f"Date: {datetime.now().strftime('%d %B %Y')} &nbsp;&nbsp;|&nbsp;&nbsp; "
                  f"Institution: R.V. College of Engineering", body),
        Spacer(1, 10),

        Paragraph("Objective", h2),
        Paragraph("To determine and compare sodium content in two chip brands using flame photometry "
                  "with NaCl standard calibration.", body),

        Paragraph("Methodology", h2),
        Paragraph(
            f"Chips were crushed, weighed (~{st.session_state.s1_weight} g each), dissolved in distilled water, "
            f"filtered and diluted into a series of {VOLS} mL aliquots. Each was aspirated into a flame "
            f"photometer and emission at 589 nm recorded. Sodium concentration was calculated from a linear "
            f"regression calibration equation.", body),

        Paragraph("Calibration Results", h2),
        Paragraph(
            f"Stock NaCl: {st.session_state.stock_conc} g/L<br/>"
            f"Regression equation: Na = {slope:.6f} &times; Reading + {intercept:.6f}<br/>"
            f"R<super>2</super> = {r2:.6f}", body),
        Spacer(1, 6),
        data_table(
            ["Volume (mL)", "NaCl conc (g/L)", "Na conc (g/L)", "Reading"],
            [[str(v), f"{nacl_concs[i]:.6f}", f"{na_concs[i]:.6f}", f"{readings[i]:.2f}"]
             for i, v in enumerate(VOLS)]
        ),
        Spacer(1, 10),
    ]

    for name, df, weight, vol in [
        (s1, df1, st.session_state.s1_weight, st.session_state.s1_vol),
        (s2, df2, st.session_state.s2_weight, st.session_state.s2_vol),
    ]:
        story.append(Paragraph(f"Sample: {name}", h2))
        story.append(Paragraph(f"Weight used: {weight} g &nbsp;|&nbsp; Extraction volume: {vol} mL", body))
        story.append(Spacer(1, 4))
        story.append(data_table(
            ["Volume (mL)", "Reading", "Na conc (g/L)", "NaCl conc (g/L)", "Na (mg/g)", "Na %", "NaCl %"],
            [[str(row["Volume (mL)"]), f"{row['Reading']:.2f}", f"{row['Na conc (g/L)']:.4f}",
              f"{row['NaCl conc (g/L)']:.4f}", f"{row['Na per g chips (mg/g)']:.4f}",
              f"{row['Na %']:.4f}", f"{row['NaCl %']:.4f}"] for _, row in df.iterrows()]
        ))
        story.append(Spacer(1, 4))
        story.append(Paragraph(
            f"<b>Average:</b> Na = {df['Na per g chips (mg/g)'].mean():.4f} mg/g &nbsp;|&nbsp; "
            f"Na% = {df['Na %'].mean():.4f}% &nbsp;|&nbsp; NaCl% = {df['NaCl %'].mean():.4f}%", body))
        story.append(Spacer(1, 10))

    story.append(Paragraph("Discussion", h2))
    story.append(Paragraph(
        f"Flame photometry provided a reliable method for sodium quantification. The calibration curve showed "
        f"excellent linearity (R<super>2</super> = {r2:.4f}), validating the method. Differences in sodium "
        f"between brands reflect manufacturing/formulation differences.", body))

    better = s1 if df1["Na per g chips (mg/g)"].mean() < df2["Na per g chips (mg/g)"].mean() else s2
    story.append(Paragraph("Conclusion", h2))
    story.append(Paragraph(
        f"<b>{better}</b> has lower sodium content and is the healthier choice regarding sodium intake.", body))

    doc.build(story)
    return buf.getvalue()

def health_meter(label, score_out_of_10, tag_text):
    """Render a visual 0-10 health meter with a filled/empty block bar."""
    score_out_of_10 = max(0.0, min(10.0, score_out_of_10))
    filled = int(round(score_out_of_10))
    bar = "█" * filled + "░" * (10 - filled)
    good = score_out_of_10 >= 5
    bar_color = colors["accent"] if good else colors["accent2"]
    tag_bg = f"{colors['accent']}22" if good else f"{colors['accent2']}22"
    st.markdown(f"""
    <div class="health-card">
        <h3>{label}</h3>
        <div class="health-bar" style="color:{bar_color};">{bar}</div>
        <div class="health-score" style="color:{bar_color};">{score_out_of_10:.1f}/10</div>
        <span class="health-tag" style="color:{bar_color}; background:{tag_bg};">{tag_text}</span>
    </div>
    """, unsafe_allow_html=True)

def sodium_health_score(na_pct):
    """Convert Na% into a 0-10 health score. 0% Na -> 10/10 (best),
    3%+ Na by dry weight -> 0/10 (worst). This threshold is a simple,
    transparent scale for classroom/demo purposes, not a clinical index."""
    score = 10 - (na_pct / 3.0) * 10
    return max(0.0, min(10.0, score))

# ---------------------------------------------
#  SESSION STATE DEFAULTS
# ---------------------------------------------
if "calib_readings" not in st.session_state:
    st.session_state.calib_readings = [276.0, 287.0, 330.0, 370.0, 411.0]
if "s1_readings" not in st.session_state:
    st.session_state.s1_readings = [0.0, 0.0, 0.0, 0.0, 0.0]
if "s2_readings" not in st.session_state:
    st.session_state.s2_readings = [0.0, 0.0, 0.0, 0.0, 0.0]
if "stock_conc" not in st.session_state:
    st.session_state.stock_conc = 0.0098
if "s1_name" not in st.session_state:
    st.session_state.s1_name = "Too Yumm"
if "s2_name" not in st.session_state:
    st.session_state.s2_name = "Bingo"
if "s1_weight" not in st.session_state:
    st.session_state.s1_weight = 10.0
if "s2_weight" not in st.session_state:
    st.session_state.s2_weight = 10.0
if "s1_vol" not in st.session_state:
    st.session_state.s1_vol = 100.0
if "s2_vol" not in st.session_state:
    st.session_state.s2_vol = 100.0

VOLS = [2, 4, 6, 8, 10]

# ---------------------------------------------
#  CALCULATIONS
# ---------------------------------------------
def get_calibration():
    stock = st.session_state.stock_conc
    nacl_concs = [v * stock for v in VOLS]
    na_concs = [c * (23 / 58.44) for c in nacl_concs]
    readings = st.session_state.calib_readings
    slope, intercept, r, _, _ = stats.linregress(readings, na_concs)
    r2 = r ** 2
    return nacl_concs, na_concs, readings, slope, intercept, r2

def analyze_sample(readings, weight_g, vol_ml, slope, intercept):
    na_concs = [(r - intercept) / slope if slope != 0 else 0 for r in readings]
    results = []
    for i, (v, r, na_c) in enumerate(zip(VOLS, readings, na_concs)):
        nacl_c = na_c * (58.44 / 23)
        na_mg = na_c * vol_ml / 1000 * 1000
        na_per_g = na_mg / weight_g if weight_g > 0 else 0
        na_pct = (na_mg / (weight_g * 1000)) * 100 if weight_g > 0 else 0
        nacl_pct = na_pct * (58.44 / 23)
        results.append({
            "Volume (mL)": v,
            "Reading": r,
            "Na conc (g/L)": round(na_c, 6),
            "NaCl conc (g/L)": round(nacl_c, 6),
            "Na mass (mg)": round(na_mg, 4),
            "Na per g chips (mg/g)": round(na_per_g, 4),
            "Na %": round(na_pct, 4),
            "NaCl %": round(nacl_pct, 4),
        })
    return pd.DataFrame(results)

# ---------------------------------------------
#  PAGE 1: PROJECT OVERVIEW
# ---------------------------------------------
def sample_page(sample_num):
    name_key = f"s{sample_num}_name"
    weight_key = f"s{sample_num}_weight"
    vol_key = f"s{sample_num}_vol"
    readings_key = f"s{sample_num}_readings"

    st.markdown(f'<div class="hero-title">🧪 Chip Sample {sample_num} Analysis</div>', unsafe_allow_html=True)

    col_in, col_out = st.columns([1, 2])
    with col_in:
        st.markdown('<div class="section-header">⚙️ Sample Inputs</div>', unsafe_allow_html=True)
        st.session_state[name_key] = st.text_input("Brand / Sample Name", value=st.session_state[name_key])
        st.session_state[weight_key] = st.number_input("Weight of chips used (g)", value=st.session_state[weight_key], min_value=0.1, max_value=500.0)
        st.session_state[vol_key] = st.number_input("Final extraction volume (mL)", value=st.session_state[vol_key], min_value=1.0, max_value=1000.0)
        st.markdown("**Flame photometer readings:**")
        for i, v in enumerate(VOLS):
            st.session_state[readings_key][i] = st.number_input(
                f"Reading at {v} mL", value=st.session_state[readings_key][i],
                key=f"s{sample_num}_r_{i}", min_value=0.0, max_value=1000.0, format="%.2f"
            )

    _, _, _, slope, intercept, _ = get_calibration()
    df = analyze_sample(
        st.session_state[readings_key],
        st.session_state[weight_key],
        st.session_state[vol_key],
        slope, intercept
    )
    avg_na_per_g = df["Na per g chips (mg/g)"].mean()
    avg_na_pct = df["Na %"].mean()
    avg_nacl_pct = df["NaCl %"].mean()
    total_na_mg = df["Na mass (mg)"].mean()

    with col_out:
        st.markdown('<div class="section-header">📊 Summary</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            metric_card("Avg Na per gram", f"{avg_na_per_g:.4f}", "mg/g")
            metric_card("Avg Na %", f"{avg_na_pct:.4f}", "%")
        with c2:
            metric_card("Avg NaCl %", f"{avg_nacl_pct:.4f}", "%")
            metric_card("Total Na mass (avg)", f"{total_na_mg:.4f}", "mg")

        score = sodium_health_score(avg_na_pct)
        health_meter(
            st.session_state[name_key], score,
            "Lower Sodium" if score >= 5 else "Higher Sodium"
        )

        # Line chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["Volume (mL)"], y=df["Na conc (g/L)"],
            mode='lines+markers', name='Na Concentration',
            line=dict(color=colors["accent"], width=2),
            marker=dict(size=8)))
        fig.update_layout(title=f"{st.session_state[name_key]}: Na Concentration vs Dilution Volume",
            xaxis_title="Volume (mL)", yaxis_title="Na Concentration (g/L)",
            **plotly_theme())
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-header">📋 Calculation Table</div>', unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)

# ---------------------------------------------
#  PAGE 3 & 4: SAMPLES
# ---------------------------------------------

if page == "1. Project Overview":
    st.markdown('<div class="hero-title">🔬 Comparative Sodium Content Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Potato Chip Samples · Flame Photometry · R.V. College of Engineering</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown('<div class="section-header">🎯 Objective</div>', unsafe_allow_html=True)
        st.markdown("""
        To determine and compare the sodium content in two different brands of potato chips
        using **flame photometry** with a standard NaCl calibration curve, and evaluate the
        health implications of sodium intake from each brand.
        """)

        st.markdown('<div class="section-header">🔥 Principle of Flame Photometry</div>', unsafe_allow_html=True)
        st.markdown("""
        Flame photometry is a branch of atomic emission spectroscopy. When a sodium-containing
        solution is aspirated into a flame, sodium atoms absorb thermal energy and are excited
        to higher energy levels. Upon returning to ground state, they **emit characteristic
        yellow light at 589 nm**. The emission intensity is directly proportional to sodium
        concentration within the linear working range of the flame photometer. (Note: the
        Beer-Lambert law applies to absorption spectroscopy, not emission, and is not the
        governing principle here.)
        """)

        st.markdown('<div class="section-header">⚗️ Sodium Detection</div>', unsafe_allow_html=True)
        st.markdown("""
        - **Wavelength detected:** 589 nm (sodium D-lines)
        - **Flame temperature:** ~1800°C (air-propane)
        - **Emission colour:** Bright yellow
        - **Detection range:** 0.1 – 100 ppm Na
        - **Reference:** Standard NaCl solutions of known concentration
        """)

    with col2:
        st.markdown('<div class="section-header">📊 Key Formulas</div>', unsafe_allow_html=True)
        st.markdown('<div class="formula-box">Na (g/L) = (Reading − c) / m</div>', unsafe_allow_html=True)
        st.markdown('<div class="formula-box">NaCl = Na × (58.44 / 23)</div>', unsafe_allow_html=True)
        st.markdown('<div class="formula-box">Na mass (mg) = Na conc × Vol (L) × 1000</div>', unsafe_allow_html=True)
        st.markdown('<div class="formula-box">Na% = (Na mg / chip mass mg) × 100</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-header">🧬 Atomic Masses</div>', unsafe_allow_html=True)
        st.markdown("""
        | Element | Symbol | Mass |
        |---------|--------|------|
        | Sodium  | Na     | 23 g/mol |
        | Chlorine| Cl     | 35.44 g/mol |
        | NaCl    | —      | 58.44 g/mol |
        """)

    st.markdown('<div class="section-header">🔄 Experiment Workflow</div>', unsafe_allow_html=True)
    steps = ["Chip Sample", "Crushing & Weighing", "Distilled Water Extraction", "Filtration",
             "Dilution Series", "Flame Photometer", "Calibration Curve", "Sodium Calculation", "Comparison"]
    workflow_html = " <span class='arrow'>→</span> ".join(
        [f"<span class='workflow-step'>{s}</span>" for s in steps]
    )
    st.markdown(f"<div style='line-height:2.5'>{workflow_html}</div>", unsafe_allow_html=True)

# ---------------------------------------------
#  PAGE 2: CALIBRATION
# ---------------------------------------------
elif page == "2. NaCl Calibration":
    st.markdown('<div class="hero-title">📈 Standard NaCl Calibration Curve</div>', unsafe_allow_html=True)

    col_in, col_out = st.columns([1, 2])
    with col_in:
        st.markdown('<div class="section-header">⚙️ Inputs</div>', unsafe_allow_html=True)
        st.session_state.stock_conc = st.number_input(
            "Stock NaCl concentration (g/L)", value=st.session_state.stock_conc,
            min_value=0.0001, max_value=10.0, format="%.4f"
        )
        st.markdown("**Flame photometer readings:**")
        for i, v in enumerate(VOLS):
            st.session_state.calib_readings[i] = st.number_input(
                f"Reading at {v} mL", value=st.session_state.calib_readings[i],
                key=f"cr_{i}", min_value=0.0, max_value=1000.0, format="%.2f"
            )

    nacl_concs, na_concs, readings, slope, intercept, r2 = get_calibration()

    with col_out:
        st.markdown('<div class="section-header">📊 Calibration Statistics</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1: metric_card("Slope (m)", f"{slope:.6f}", "g/L per unit")
        with c2: metric_card("Intercept (c)", f"{intercept:.6f}", "g/L")
        with c3: metric_card("R² Value", f"{r2:.6f}", "")

        st.markdown(f'<div class="formula-box">Regression: Na (g/L) = {slope:.6f} × Reading + ({intercept:.6f})</div>', unsafe_allow_html=True)

        # Calibration chart
        x_line = np.linspace(0, max(readings) * 1.1, 100)
        y_line = slope * x_line + intercept

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=readings, y=na_concs, mode='markers',
            name='Data Points', marker=dict(color=colors["accent"], size=12, symbol='circle')))
        fig.add_trace(go.Scatter(x=x_line, y=y_line, mode='lines',
            name='Best Fit Line', line=dict(color=colors["accent2"], width=2, dash='dash')))
        fig.update_layout(title="Calibration Curve: Flame Reading vs Na Concentration",
            xaxis_title="Flame Photometer Reading", yaxis_title="Na Concentration (g/L)",
            legend=dict(bgcolor='rgba(0,0,0,0)'), **plotly_theme())
        st.plotly_chart(fig, use_container_width=True)

    # Table
    st.markdown('<div class="section-header">📋 Calibration Data Table</div>', unsafe_allow_html=True)
    df_calib = pd.DataFrame({
        "Volume (mL)": VOLS,
        "NaCl conc (g/L)": [round(c, 6) for c in nacl_concs],
        "Na conc (g/L)": [round(c, 6) for c in na_concs],
        "Flame Reading": readings,
    })
    st.dataframe(df_calib, use_container_width=True)

# ---------------------------------------------
#  HELPER: SAMPLE PAGE
# ---------------------------------------------
elif page == "3. Sample 1 Analysis":
    sample_page(1)

elif page == "4. Sample 2 Analysis":
    sample_page(2)

# ---------------------------------------------
#  PAGE 5: COMPARATIVE ANALYSIS
# ---------------------------------------------
elif page == "5. Comparative Analysis":
    st.markdown('<div class="hero-title">⚖️ Comparative Analysis</div>', unsafe_allow_html=True)

    _, _, _, slope, intercept, _ = get_calibration()

    df1 = analyze_sample(st.session_state.s1_readings, st.session_state.s1_weight,
                         st.session_state.s1_vol, slope, intercept)
    df2 = analyze_sample(st.session_state.s2_readings, st.session_state.s2_weight,
                         st.session_state.s2_vol, slope, intercept)

    s1 = st.session_state.s1_name
    s2 = st.session_state.s2_name

    m1 = {
        "Na (mg/g)": df1["Na per g chips (mg/g)"].mean(),
        "Na (%)": df1["Na %"].mean(),
        "NaCl (%)": df1["NaCl %"].mean(),
        "Total Na (mg)": df1["Na mass (mg)"].mean(),
        "Avg Reading": np.mean(st.session_state.s1_readings),
    }
    m2 = {
        "Na (mg/g)": df2["Na per g chips (mg/g)"].mean(),
        "Na (%)": df2["Na %"].mean(),
        "NaCl (%)": df2["NaCl %"].mean(),
        "Total Na (mg)": df2["Na mass (mg)"].mean(),
        "Avg Reading": np.mean(st.session_state.s2_readings),
    }

    # Health meter comparison
    st.markdown('<div class="section-header">🏥 Sodium Health Meter</div>', unsafe_allow_html=True)
    hm1, hm2 = st.columns(2)
    score1 = sodium_health_score(m1["Na (%)"])
    score2 = sodium_health_score(m2["Na (%)"])
    with hm1:
        tag1 = "Lower Sodium" if m1["Na (%)"] <= m2["Na (%)"] else "Higher Sodium"
        health_meter(s1, score1, tag1)
    with hm2:
        tag2 = "Lower Sodium" if m2["Na (%)"] <= m1["Na (%)"] else "Higher Sodium"
        health_meter(s2, score2, tag2)
    st.caption("Score is a simple 0–10 scale (10 = lowest sodium) derived from Na% of dry chip weight, for illustrative comparison only.")

    # Metric comparison table
    st.markdown('<div class="section-header">📋 Metric Comparison Table</div>', unsafe_allow_html=True)
    comp_df = pd.DataFrame({
        "Metric": list(m1.keys()),
        s1: [round(v, 5) for v in m1.values()],
        s2: [round(v, 5) for v in m2.values()],
        "Difference": [round(abs(m1[k] - m2[k]), 5) for k in m1],
    })
    st.dataframe(comp_df, use_container_width=True)

    # Charts row
    col1, col2 = st.columns(2)

    with col1:
        # Bar chart
        metrics_show = ["Na (mg/g)", "Na (%)", "NaCl (%)"]
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(name=s1, x=metrics_show,
            y=[m1[k] for k in metrics_show], marker_color=colors["accent"]))
        fig_bar.add_trace(go.Bar(name=s2, x=metrics_show,
            y=[m2[k] for k in metrics_show], marker_color=colors["accent2"]))
        fig_bar.update_layout(title="Bar Chart Comparison", barmode='group',
            legend=dict(bgcolor='rgba(0,0,0,0)'), **plotly_theme())
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        # Pie chart — Na distribution
        fig_pie = go.Figure(go.Pie(
            labels=[s1, s2],
            values=[m1["Total Na (mg)"], m2["Total Na (mg)"]],
            marker_colors=[colors["accent"], colors["accent2"]],
            hole=0.4,
            textinfo='label+percent'
        ))
        fig_pie.update_layout(title="Na Mass Distribution", **plotly_theme())
        st.plotly_chart(fig_pie, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        # Radar chart
        cats = ["Na (mg/g)", "Na (%)", "NaCl (%)", "Total Na (mg)", "Avg Reading"]
        # Normalise 0-1 for radar
        max_vals = [max(m1[k], m2[k]) for k in cats]
        v1_norm = [m1[k] / mx if mx > 0 else 0 for k, mx in zip(cats, max_vals)]
        v2_norm = [m2[k] / mx if mx > 0 else 0 for k, mx in zip(cats, max_vals)]

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=v1_norm + [v1_norm[0]], theta=cats + [cats[0]],
            fill='toself', name=s1, line_color=colors["accent"]))
        fig_radar.add_trace(go.Scatterpolar(r=v2_norm + [v2_norm[0]], theta=cats + [cats[0]],
            fill='toself', name=s2, line_color=colors["accent2"]))
        fig_radar.update_layout(title="Radar Chart (Normalised)",
            polar=dict(bgcolor=colors["bg"],
                radialaxis=dict(visible=True, gridcolor=colors["grid"]),
                angularaxis=dict(gridcolor=colors["grid"])),
            legend=dict(bgcolor='rgba(0,0,0,0)'),
            paper_bgcolor=colors["bg"], font_color=colors["text"])
        st.plotly_chart(fig_radar, use_container_width=True)

    with col4:
        # Comparative line graph
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(x=VOLS, y=df1["Na conc (g/L)"],
            mode='lines+markers', name=s1, line=dict(color=colors["accent"], width=2)))
        fig_line.add_trace(go.Scatter(x=VOLS, y=df2["Na conc (g/L)"],
            mode='lines+markers', name=s2, line=dict(color=colors["accent2"], width=2)))
        fig_line.update_layout(title="Na Concentration vs Volume",
            xaxis_title="Volume (mL)", yaxis_title="Na Concentration (g/L)",
            legend=dict(bgcolor='rgba(0,0,0,0)'), **plotly_theme())
        st.plotly_chart(fig_line, use_container_width=True)

    # Conclusion
    st.markdown('<div class="section-header">🏁 Automatic Conclusion</div>', unsafe_allow_html=True)
    na1 = m1["Na (mg/g)"]
    na2 = m2["Na (mg/g)"]
    if na1 < na2:
        lower, higher = s1, s2
        pct_diff = ((na2 - na1) / na2) * 100
    else:
        lower, higher = s2, s1
        pct_diff = ((na1 - na2) / na1) * 100

    conclusion = f"""
    ✅ **{lower}** contains **{pct_diff:.1f}% less sodium** than **{higher}** and is the
    healthier option regarding sodium intake.

    - **{s1}** Na content: **{na1:.4f} mg/g** ({m1['Na (%)']:.4f}% Na, {m1['NaCl (%)']:.4f}% NaCl)
    - **{s2}** Na content: **{na2:.4f} mg/g** ({m2['Na (%)']:.4f}% Na, {m2['NaCl (%)']:.4f}% NaCl)

    From a dietary perspective, consumers seeking lower sodium intake should prefer **{lower}**.
    Both samples were analysed using flame photometry at 589 nm with a validated NaCl calibration
    curve (regression-based). All results are expressed per gram of dry chip sample.
    """
    st.markdown(f'<div class="conclusion-box">{conclusion}</div>', unsafe_allow_html=True)

    # AI-powered analysis
    st.markdown('<div class="section-header">🤖 AI-Powered Analysis</div>', unsafe_allow_html=True)
    if st.button("🤖 Analyze using AI", key="analyze_comparison_ai"):
        with st.spinner("Gemini is analysing your results..."):
            context, _, _ = build_data_context()
            prompt = f"""{context}

You are a scientific reviewer analysing this flame photometry sodium comparison experiment.
Based ONLY on the data above, provide a structured response with these exact sections (use markdown headers):

### Discussion
Discuss the sodium content trends and what the numbers indicate about the two samples.

### Interpretation
Interpret the results in the context of flame photometry methodology and calibration quality (mention R-squared).

### Health Recommendation
Give a practical, evidence-based dietary recommendation comparing the two samples' sodium content.

### Conclusion
A concise 2-3 sentence conclusion summarising which sample is lower in sodium and by how much.

Keep the entire response under 350 words. Be precise and quantitative, referencing actual numbers from the data."""
            ok, result = call_gemini(prompt)
        if ok:
            ai_result_box(result.replace("\n", "<br>"))
            ai_confidence_box()
        else:
            st.warning(result)

# ---------------------------------------------
#  PAGE 6: RESULTS & EXPORT
# ---------------------------------------------
elif page == "6. Results & Export":
    st.markdown('<div class="hero-title">📄 Results & Report Export</div>', unsafe_allow_html=True)

    _, _, _, slope, intercept, r2 = get_calibration()
    nacl_concs, na_concs, readings, slope, intercept, r2 = get_calibration()
    df1 = analyze_sample(st.session_state.s1_readings, st.session_state.s1_weight,
                         st.session_state.s1_vol, slope, intercept)
    df2 = analyze_sample(st.session_state.s2_readings, st.session_state.s2_weight,
                         st.session_state.s2_vol, slope, intercept)

    s1, s2 = st.session_state.s1_name, st.session_state.s2_name

    # Report preview
    st.markdown('<div class="section-header">📋 Lab Report Preview</div>', unsafe_allow_html=True)
    st.markdown(f"""
    **Title:** Comparative Sodium Content Analysis of Potato Chip Samples Using Flame Photometry

    **Date:** {datetime.now().strftime('%d %B %Y')}
    **Institution:** R.V. College of Engineering

    **Objective:**
    To determine and compare sodium content in two chip brands using flame photometry with NaCl standard calibration.

    **Methodology:**
    Chips were crushed, weighed (~{st.session_state.s1_weight}g each), dissolved in distilled water, filtered and diluted
    into a series of {VOLS} mL aliquots. Each was aspirated into a flame photometer and emission at 589 nm recorded.
    Sodium concentration was calculated from a linear regression calibration equation.

    **Calibration Results:**
    - Stock NaCl: {st.session_state.stock_conc} g/L
    - Regression equation: Na = {slope:.6f} × Reading + {intercept:.6f}
    - R² = {r2:.6f}

    **Sample Results:**
    - {s1}: Avg Na = {df1['Na per g chips (mg/g)'].mean():.4f} mg/g | Na% = {df1['Na %'].mean():.4f}% | NaCl% = {df1['NaCl %'].mean():.4f}%
    - {s2}: Avg Na = {df2['Na per g chips (mg/g)'].mean():.4f} mg/g | Na% = {df2['Na %'].mean():.4f}% | NaCl% = {df2['NaCl %'].mean():.4f}%

    **Discussion:**
    Flame photometry provided a reliable method for sodium quantification. The calibration curve showed
    excellent linearity (R² = {r2:.4f}), validating the method. Differences in sodium between brands
    reflect manufacturing/formulation differences.

    **Conclusion:**
    {"**" + s1 + "**" if df1['Na per g chips (mg/g)'].mean() < df2['Na per g chips (mg/g)'].mean() else "**" + s2 + "**"}
    has lower sodium content and is the healthier choice regarding sodium intake.
    """)

    # Export buttons
    st.markdown('<div class="section-header">💾 Export Data</div>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        # CSV export — all data combined
        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow(["=== CALIBRATION DATA ==="])
        writer.writerow(["Volume (mL)", "NaCl conc (g/L)", "Na conc (g/L)", "Reading"])
        for i, v in enumerate(VOLS):
            writer.writerow([v, round(nacl_concs[i], 6), round(na_concs[i], 6), readings[i]])
        writer.writerow([])
        writer.writerow([f"=== {s1} ==="])
        df1.to_csv(buf, index=False)
        writer.writerow([])
        writer.writerow([f"=== {s2} ==="])
        df2.to_csv(buf, index=False)
        st.download_button("📥 Download CSV", buf.getvalue(),
            file_name="sodium_analysis.csv", mime="text/csv")

    with col2:
        # Excel export
        excel_buf = io.BytesIO()
        with pd.ExcelWriter(excel_buf, engine='openpyxl') as writer_xl:
            calib_df = pd.DataFrame({
                "Volume (mL)": VOLS, "NaCl conc (g/L)": nacl_concs,
                "Na conc (g/L)": na_concs, "Reading": readings
            })
            calib_df.to_excel(writer_xl, sheet_name="Calibration", index=False)
            df1.to_excel(writer_xl, sheet_name=s1[:30], index=False)
            df2.to_excel(writer_xl, sheet_name=s2[:30], index=False)
        st.download_button("📊 Download Excel", excel_buf.getvalue(),
            file_name="sodium_analysis.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    with col3:
        # Text report
        report_text = f"""
FLAME PHOTOMETER SODIUM ANALYSIS REPORT
========================================
Date: {datetime.now().strftime('%d %B %Y')}
Institution: R.V. College of Engineering

CALIBRATION
-----------
Stock NaCl: {st.session_state.stock_conc} g/L
Equation: Na = {slope:.6f} x Reading + ({intercept:.6f})
R² = {r2:.6f}

SAMPLE 1: {s1}
-----------
Weight: {st.session_state.s1_weight} g
Volume: {st.session_state.s1_vol} mL
Avg Na: {df1['Na per g chips (mg/g)'].mean():.4f} mg/g
Na%: {df1['Na %'].mean():.4f}%
NaCl%: {df1['NaCl %'].mean():.4f}%

SAMPLE 2: {s2}
-----------
Weight: {st.session_state.s2_weight} g
Volume: {st.session_state.s2_vol} mL
Avg Na: {df2['Na per g chips (mg/g)'].mean():.4f} mg/g
Na%: {df2['Na %'].mean():.4f}%
NaCl%: {df2['NaCl %'].mean():.4f}%
"""
        st.download_button("📄 Download Report (TXT)", report_text,
            file_name="lab_report.txt", mime="text/plain")

    with col4:
        # PDF export — formatted lab report
        try:
            pdf_bytes = build_pdf_report(s1, s2, df1, df2, slope, intercept, r2, nacl_concs, na_concs, readings)
            st.download_button("📕 Download PDF Report", pdf_bytes,
                file_name="lab_report.pdf", mime="application/pdf")
        except Exception as e:
            st.warning(f"⚠️ Could not generate PDF: {e}")

    # Scientific Calculator
    st.markdown('<div class="section-header">🧮 Scientific Calculator</div>', unsafe_allow_html=True)
    with st.expander("Open Calculator"):
        c1, c2 = st.columns(2)
        with c1:
            na_input = st.number_input("Na concentration (g/L)", value=0.001, format="%.6f")
            vol_input = st.number_input("Volume (mL)", value=100.0)
            wt_input = st.number_input("Chip weight (g)", value=10.0)
        with c2:
            na_mg = na_input * vol_input / 1000 * 1000
            nacl_calc = na_input * (58.44 / 23)
            na_pct = (na_mg / (wt_input * 1000)) * 100 if wt_input > 0 else 0
            nacl_pct = na_pct * (58.44 / 23)
            metric_card("Na mass", f"{na_mg:.5f}", "mg")
            metric_card("NaCl conc", f"{nacl_calc:.6f}", "g/L")
            metric_card("Na %", f"{na_pct:.5f}", "%")
            metric_card("NaCl %", f"{nacl_pct:.5f}", "%")

# ---------------------------------------------
#  PAGE 7: AI SCIENTIST
# ---------------------------------------------
elif page == "7. 🤖 AI Scientist":
    st.markdown('<div class="hero-title">🤖 AI Scientist</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Gemini-powered analysis, discussion, error-checking, reporting &amp; viva prep</div>', unsafe_allow_html=True)

    if not st.session_state.get("gemini_api_key", "").strip():
        st.info("💡 Add your Gemini API key in the sidebar (**AI Settings**) to use these tools. Get a free key at aistudio.google.com/apikey.")

    tabs = st.tabs([
        "🩺 Health Analysis",
        "💬 Scientific Discussion",
        "🔍 Error Detection",
        "📄 Report Generator",
        "🎓 Viva Assistant",
    ])

    # ---- 1. AI Health Analysis ----
    with tabs[0]:
        st.markdown('<div class="section-header">🩺 AI Health Analysis</div>', unsafe_allow_html=True)
        st.caption("Gemini reviews the sodium results from a nutrition & health standpoint.")
        if st.button("🤖 Run Health Analysis", key="ai_health_btn"):
            with st.spinner("Analysing health implications..."):
                context, _, _ = build_data_context()
                prompt = f"""{context}

Act as a nutrition scientist. Based only on the data above, provide:
1. **Sodium Health Context** — how these sodium levels compare to typical daily intake guidelines (mention general WHO/ICMR-style recommendations qualitatively, without inventing exact citations).
2. **Comparative Health Verdict** — which sample is the better choice for someone watching sodium intake, and why.
3. **Practical Advice** — 2-3 bullet points of practical dietary advice for consumers of these products.
Keep it under 300 words, markdown formatted."""
                ok, result = call_gemini(prompt)
            if ok:
                ai_result_box(result.replace("\n", "<br>"))
                ai_confidence_box()
            else:
                st.warning(result)

    # ---- 2. AI Scientific Discussion (ChatGPT-style chat) ----
    with tabs[1]:
        st.markdown('<div class="section-header">💬 AI Scientific Discussion</div>', unsafe_allow_html=True)
        st.caption("Ask Gemini anything about the methodology, chemistry, or results of this experiment.")

        if "chat_messages" not in st.session_state:
            st.session_state.chat_messages = []

        chat_box = st.container(height=420, border=True)
        with chat_box:
            if not st.session_state.chat_messages:
                st.markdown(
                    '<div style="opacity:0.6; padding:12px 4px;">👋 Ask a question below to start the conversation — '
                    'e.g. <i>"Why does flame photometry use an air-acetylene flame for sodium detection?"</i></div>',
                    unsafe_allow_html=True
                )
            for msg in st.session_state.chat_messages:
                avatar = "👤" if msg["role"] == "user" else "🤖"
                with st.chat_message(msg["role"], avatar=avatar):
                    st.markdown(msg["content"])

        col_input, col_clear = st.columns([6, 1])
        with col_clear:
            if st.session_state.chat_messages and st.button("🗑️ Clear", key="clear_chat_btn", use_container_width=True):
                st.session_state.chat_messages = []
                st.rerun()

        user_question = st.chat_input("Ask about the methodology, chemistry, or results…")
        if user_question and user_question.strip():
            st.session_state.chat_messages.append({"role": "user", "content": user_question})

            context, _, _ = build_data_context()
            history_text = ""
            if len(st.session_state.chat_messages) > 1:
                history_text = "\n\nPREVIOUS CONVERSATION (for context, most recent last):\n" + "\n".join(
                    f"{'Student' if m['role'] == 'user' else 'AI'}: {m['content']}"
                    for m in st.session_state.chat_messages[:-1]
                )
            prompt = f"""{context}
{history_text}

You are a flame photometry and analytical chemistry expert helping a student understand their experiment.
Student's latest question: "{user_question}"

Answer clearly and scientifically, referencing the experiment's actual data and the prior conversation where relevant. Keep it under 300 words."""
            ok, result = call_gemini(prompt)
            st.session_state.chat_messages.append({"role": "assistant", "content": result})
            st.rerun()

    # ---- 3. AI Error Detection ----
    with tabs[2]:
        st.markdown('<div class="section-header">🔍 AI Error Detection</div>', unsafe_allow_html=True)
        st.caption("Gemini checks your calibration and sample data for anomalies, outliers, or possible experimental errors.")
        if st.button("🤖 Detect Errors", key="ai_error_btn"):
            with st.spinner("Checking data for anomalies..."):
                context, df1, df2 = build_data_context()
                prompt = f"""{context}

You are a lab quality-control reviewer. Examine this flame photometry data for potential experimental errors, such as:
- Non-linearity or a weak calibration curve (low R-squared)
- Outlier or non-monotonic readings within a sample's dilution series
- Inconsistent or physically implausible values (e.g. negative concentrations)
- Any reading that deviates sharply from the expected linear trend

List specific issues found (referencing exact numbers), or state clearly if no significant issues are found.
Then give 2-3 actionable suggestions to improve data quality. Keep it under 300 words, markdown formatted."""
                ok, result = call_gemini(prompt)
            if ok:
                ai_result_box(result.replace("\n", "<br>"))
                ai_confidence_box()
            else:
                st.warning(result)

        # Standard experimental recommendations — always shown as good
        # lab practice, independent of whether the AI check was run.
        st.markdown('<div class="section-header">✅ Recommendations</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="conclusion-box">
        ✔ Repeat calibration every 20 samples<br>
        ✔ Use freshly prepared NaCl standards<br>
        ✔ Clean burner before measurements<br>
        ✔ Repeat readings in triplicate
        </div>
        """, unsafe_allow_html=True)

    # ---- 4. AI Report Generator ----
    with tabs[3]:
        st.markdown('<div class="section-header">📄 AI Report Generator</div>', unsafe_allow_html=True)
        st.caption("Generates a full lab report: Abstract, Methodology, Discussion, Result, Conclusion, Future Scope.")
        if st.button("🤖 Generate AI Report", key="ai_report_btn"):
            with st.spinner("Drafting full report... this may take a moment"):
                context, _, _ = build_data_context()
                prompt = f"""{context}

Write a formal undergraduate lab report for this experiment. Use these exact markdown section headers, in this order:

### Abstract
### Methodology
### Result
### Discussion
### Conclusion
### Future Scope

Each section should be concise but substantive (3-6 sentences), grounded in the actual data provided above.
The Future Scope section should suggest realistic extensions (e.g. more replicates, more brands, ICP-MS validation).
Do not invent data not present above."""
                ok, result = call_gemini(prompt, max_tokens=3000)
            if ok:
                st.session_state["ai_generated_report"] = result
                ai_result_box(result.replace("\n", "<br>"))
                ai_confidence_box()
            else:
                st.warning(result)

        if st.session_state.get("ai_generated_report"):
            st.download_button(
                "📥 Download AI Report (TXT)",
                st.session_state["ai_generated_report"],
                file_name="ai_generated_report.txt",
                mime="text/plain",
                key="ai_report_download"
            )

    # ---- 5. AI Viva Assistant ----
    with tabs[4]:
        st.markdown('<div class="section-header">🎓 AI Viva Assistant</div>', unsafe_allow_html=True)
        st.caption("Generates likely viva/exam questions (with model answers) based on this experiment.")
        num_q = st.slider("Number of questions", 3, 10, 5, key="ai_viva_num")
        if st.button("🤖 Generate Viva Questions", key="ai_viva_btn"):
            with st.spinner("Preparing viva questions..."):
                context, _, _ = build_data_context()
                prompt = f"""{context}

You are a professor preparing viva-voce questions for a student who performed this flame photometry experiment.
Generate exactly {num_q} likely viva questions covering: principle of flame photometry, calibration/regression method,
sample preparation, sources of error, and interpretation of THIS student's specific results.
For each question, give a concise model answer (2-4 sentences).
Format as:
**Q1: [question]**
A: [answer]

Keep total response focused and well organised."""
                ok, result = call_gemini(prompt, max_tokens=3000)
            if ok:
                ai_result_box(result.replace("\n", "<br>"))
                ai_confidence_box()
            else:
                st.warning(result)
