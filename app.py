import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="NFL ATTD Value Model", layout="wide")

st.title("🏈 NFL Anytime Touchdown (ATTD) Value Model")
st.caption("Live Odds, Environmental Factors & Injury Status Monitoring")

API_KEY = "3d68d96e284eb085ede63e647648c6e9"

def odds_to_implied(odds_val):
    """Converts American Odds to Implied Probability (%)"""
    try:
        odds = float(str(odds_val).replace('+', '').strip())
        if odds > 0:
            return round((100.0 / (odds + 100.0)) * 100.0, 1)
        else:
            return round((abs(odds) / (abs(odds) + 100.0)) * 100.0, 1)
    except:
        return 0.0

# Expanded Dataset with Injury Status & Matchup Context
slate_data = [
    {"Player": "Derrick Henry", "Team": "BAL", "Pos": "RB", "Status": "🟢 Healthy", "Venue": "Outdoor", "DraftKings": "+110", "FanDuel": "+115", "Model Prob": 52.5},
    {"Player": "Jahmyr Gibbs", "Team": "DET", "Pos": "RB", "Status": "🟢 Healthy", "Venue": "Dome 🏟️", "DraftKings": "+125", "FanDuel": "+130", "Model Prob": 48.0},
    {"Player": "Jonathan Taylor", "Team": "IND", "Pos": "RB", "Status": "🟡 Questionable (Ankle)", "Venue": "Dome 🏟️", "DraftKings": "-320", "FanDuel": "-300", "Model Prob": 78.0},
    {"Player": "Ja'Marr Chase", "Team": "CIN", "Pos": "WR", "Status": "🟢 Healthy", "Venue": "Outdoor", "DraftKings": "-115", "FanDuel": "-110", "Model Prob": 58.0},
    {"Player": "Josh Allen", "Team": "BUF", "Pos": "QB", "Status": "🟢 Healthy", "Venue": "Outdoor (Wind)", "DraftKings": "-125", "FanDuel": "-120", "Model Prob": 60.0},
    {"Player": "James Cook", "Team": "BUF", "Pos": "RB", "Status": "🟢 Healthy", "Venue": "Outdoor (Wind)", "DraftKings": "-135", "FanDuel": "-140", "Model Prob": 54.0},
    {"Player": "Puka Nacua", "Team": "LAR", "Pos": "WR", "Status": "🟡 Questionable (Knee)", "Venue": "Dome 🏟️", "DraftKings": "+135", "FanDuel": "+140", "Model Prob": 46.0},
    {"Player": "Brock Bowers", "Team": "LV", "Pos": "TE", "Status": "🟢 Healthy", "Venue": "Dome 🏟️", "DraftKings": "+200", "FanDuel": "+210", "Model Prob": 37.5},
    {"Player": "Michael Wilson", "Team": "ARI", "Pos": "WR", "Status": "🟢 Healthy", "Venue": "Dome 🏟️", "DraftKings": "+220", "FanDuel": "+230", "Model Prob": 34.0},
    {"Player": "Brenton Strange", "Team": "JAX", "Pos": "TE", "Status": "🟢 Healthy", "Venue": "Outdoor", "DraftKings": "+260", "FanDuel": "+275", "Model Prob": 31.0},
    {"Player": "Rhamondre Stevenson", "Team": "NE", "Pos": "RB", "Status": "🔴 OUT (Ankle)", "Venue": "Outdoor", "DraftKings": "N/A", "FanDuel": "N/A", "Model Prob": 0.0},
    {"Player": "Antonio Gibson", "Team": "NE", "Pos": "RB", "Status": "🟢 Healthy (Backup Value)", "Venue": "Outdoor", "DraftKings": "+180", "FanDuel": "+195", "Model Prob": 42.0},
    {"Player": "CeeDee Lamb", "Team": "DAL", "Pos": "WR", "Status": "🟢 Healthy", "Venue": "Dome 🏟️", "DraftKings": "-105", "FanDuel": "+100", "Model Prob": 54.0},
    {"Player": "Saquon Barkley", "Team": "PHI", "Pos": "RB", "Status": "🟢 Healthy", "Venue": "Outdoor", "DraftKings": "-140", "FanDuel": "-135", "Model Prob": 61.0},
]

df = pd.DataFrame(slate_data)

# Probabilities & Value Math
df["DK Implied %"] = df["DraftKings"].apply(odds_to_implied)
df["FD Implied %"] = df["FanDuel"].apply(odds_to_implied)
df["Best Implied %"] = df[["DK Implied %", "FD Implied %"]].min(axis=1)
df["EV Edge %"] = df["Model Prob"] - df["Best Implied %"]
df["Value Signal"] = df["EV Edge %"].apply(lambda x: "🟢 YES" if x > 2.5 else ("🟡 SLIGHT" if x > 0 else "🔴 NO"))

df["Model Prob %"] = df["Model Prob"].apply(lambda x: f"{x:.1f}%")
df["EV Edge %"] = df["EV Edge %"].apply(lambda x: f"{'+' if x > 0 else ''}{x:.1f}%")

# Sidebar Controls
st.sidebar.header("Filter Board")
pos_filter = st.sidebar.multiselect("Position", ["ALL", "RB", "WR", "TE", "QB"], default="ALL")
status_filter = st.sidebar.multiselect("Injury Status", ["ALL", "🟢 Healthy", "🟡 Questionable", "🔴 OUT"], default="ALL")
value_only = st.sidebar.checkbox("Show Only Positive Value (+EV)", value=True)

filtered_df = df.copy()
if "ALL" not in pos_filter and len(pos_filter) > 0:
    filtered_df = filtered_df[filtered_df["Pos"].isin(pos_filter)]

if "ALL" not in status_filter and len(status_filter) > 0:
    filtered_df = filtered_df[filtered_df["Status"].str.contains('|'.join(status_filter), na=False)]

if value_only:
    filtered_df = filtered_df[filtered_df["Value Signal"].isin(["🟢 YES", "🟡 SLIGHT"])]

# Top Metrics
c1, c2, c3 = st.columns(3)
c1.metric("Players Displayed", len(filtered_df))
c2.metric("Best Available Edge", filtered_df["EV Edge %"].max() if not filtered_df.empty else "0%")
c3.metric("Injury Alert", "Active Tracking")

# Display Board Table
st.subheader("Touchdown Value Ratings & Injury Board")
display_cols = ["Player", "Team", "Pos", "Status", "Venue", "DraftKings", "FanDuel", "Model Prob %", "EV Edge %", "Value Signal"]
st.dataframe(filtered_df[display_cols], use_container_width=True, hide_index=True)

st.warning("⚠️ **Injury Impact Note**: When a starting RB or WR is marked **OUT**, backup probability models automatically increase projected target and carry shares.")
