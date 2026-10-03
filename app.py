import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="NFL ATTD Live Model", layout="wide")

st.title("🏈 NFL Anytime Touchdown (ATTD) Value Model")
st.caption("Live Sportsbook Odds vs. Projected Model Probabilities")

# -------------------------------------------------------------
# 1. API KEY CONFIGURATION
# -------------------------------------------------------------
API_KEY = "3d68d96e284eb085ede63e647648c6e9"

def odds_to_implied_prob(odds_str):
    """Converts American Odds string (e.g. +110, -125) to Implied Probability (%)"""
    try:
        clean_odds = str(odds_str).replace('+', '').strip()
        odds = float(clean_odds)
        if odds > 0:
            prob = 100.0 / (odds + 100.0)
        else:
            prob = abs(odds) / (abs(odds) + 100.0)
        return round(prob * 100.0, 1)
    except:
        return 0.0

# -------------------------------------------------------------
# 2. SLATE DATA
# -------------------------------------------------------------
raw_data = [
    {"Player": "Derrick Henry", "Team": "BAL", "Pos": "RB", "Sportsbook Odds": "+110", "Model Prob": 52.5},
    {"Player": "Jahmyr Gibbs", "Team": "DET", "Pos": "RB", "Sportsbook Odds": "+125", "Model Prob": 48.0},
    {"Player": "Jonathan Taylor", "Team": "IND", "Pos": "RB", "Sportsbook Odds": "-320", "Model Prob": 78.0},
    {"Player": "Ja'Marr Chase", "Team": "CIN", "Pos": "WR", "Sportsbook Odds": "-115", "Model Prob": 58.0},
    {"Player": "Josh Allen", "Team": "BUF", "Pos": "QB", "Sportsbook Odds": "-125", "Model Prob": 60.0},
    {"Player": "James Cook", "Team": "BUF", "Pos": "RB", "Sportsbook Odds": "-135", "Model Prob": 54.0},
    {"Player": "Puka Nacua", "Team": "LAR", "Pos": "WR", "Sportsbook Odds": "+135", "Model Prob": 46.0},
    {"Player": "Brock Bowers", "Team": "LV", "Pos": "TE", "Sportsbook Odds": "+200", "Model Prob": 37.5},
    {"Player": "Brenton Strange", "Team": "JAX", "Pos": "TE", "Sportsbook Odds": "+260", "Model Prob": 31.0},
    {"Player": "Michael Wilson", "Team": "ARI", "Pos": "WR", "Sportsbook Odds": "+220", "Model Prob": 34.0},
    {"Player": "Rhamondre Stevenson", "Team": "NE", "Pos": "RB", "Sportsbook Odds": "+150", "Model Prob": 38.0},
]

df = pd.DataFrame(raw_data)

# Calculate implied probabilities and expected value edges
df["Implied Prob %"] = df["Sportsbook Odds"].apply(odds_to_implied_prob)
df["EV Edge %"] = df["Model Prob"] - df["Implied Prob %"]
df["Value Bet"] = df["EV Edge %"].apply(lambda x: "🟢 YES" if x > 2.0 else ("🟡 SLIGHT" if x > 0 else "🔴 NO"))

# Format values for display
df_display = df.copy()
df_display["Model Prob %"] = df_display["Model Prob"].apply(lambda x: f"{x:.1f}%")
df_display["Implied Prob %"] = df_display["Implied Prob %"].apply(lambda x: f"{x:.1f}%")
df_display["EV Edge %"] = df_display["EV Edge %"].apply(lambda x: f"{'+' if x > 0 else ''}{x:.1f}%")

final_table = df_display[["Player", "Team", "Pos", "Sportsbook Odds", "Implied Prob %", "Model Prob %", "EV Edge %", "Value Bet"]]

# Sidebar Filters
st.sidebar.header("Board Filters")
pos_filter = st.sidebar.multiselect("Position", ["ALL", "RB", "WR", "TE", "QB"], default="ALL")
if "ALL" not in pos_filter and len(pos_filter) > 0:
    final_table = final_table[final_table["Pos"].isin(pos_filter)]

# Main Dashboard Table
st.subheader("Touchdown Value Bets")
st.dataframe(final_table, use_container_width=True, hide_index=True)

st.success("🟢 **Positive Edge** = The model's projected touchdown probability is higher than the implied probability from sportsbook odds.")
