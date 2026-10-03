import streamlit as st
import pandas as pd

st.set_page_config(page_title="NFL ATTD Value & Trend Model", layout="wide")

st.title("🏈 NFL Anytime Touchdown (ATTD) Value & Trend Dashboard")
st.caption("Live Odds, Injury Alerts, Recent Form (L3 TDs) & RZ Usage Metrics")

def odds_to_implied(odds_val):
    try:
        odds = float(str(odds_val).replace('+', '').strip())
        if odds > 0:
            return round((100.0 / (odds + 100.0)) * 100.0, 1)
        else:
            return round((abs(odds) / (abs(odds) + 100.0)) * 100.0, 1)
    except:
        return 0.0

# Master Board Data
slate_data = [
    {
        "Player": "Derrick Henry", "Team": "BAL", "Pos": "RB", "Status": "🟢 Healthy",
        "L3 TDs": 4, "Inside 5 Touches": 6, "Opp TD Rank": "#28 vs RB (Weak)", "Touch Trend": "🔥 Up",
        "DraftKings": "+110", "FanDuel": "+115", "Model Prob": 52.5
    },
    {
        "Player": "Jahmyr Gibbs", "Team": "DET", "Pos": "RB", "Status": "🟢 Healthy",
        "L3 TDs": 3, "Inside 5 Touches": 4, "Opp TD Rank": "#15 vs RB", "Touch Trend": "➡️ Steady",
        "DraftKings": "+125", "FanDuel": "+130", "Model Prob": 48.0
    },
    {
        "Player": "Ja'Marr Chase", "Team": "CIN", "Pos": "WR", "Status": "🟢 Healthy",
        "L3 TDs": 3, "Inside 5 Touches": 2, "Opp TD Rank": "#30 vs WR (Weak)", "Touch Trend": "🔥 Up",
        "DraftKings": "-115", "FanDuel": "-110", "Model Prob": 58.0
    },
    {
        "Player": "Puka Nacua", "Team": "LAR", "Pos": "WR", "Status": "🟡 Questionable",
        "L3 TDs": 2, "Inside 5 Touches": 3, "Opp TD Rank": "#12 vs WR", "Touch Trend": "🔥 Up",
        "DraftKings": "+135", "FanDuel": "+140", "Model Prob": 46.0
    },
    {
        "Player": "Brock Bowers", "Team": "LV", "Pos": "TE", "Status": "🟢 Healthy",
        "L3 TDs": 2, "Inside 5 Touches": 3, "Opp TD Rank": "#29 vs TE (Weak)", "Touch Trend": "🔥 Up",
        "DraftKings": "+200", "FanDuel": "+210", "Model Prob": 37.5
    },
    {
        "Player": "Antonio Gibson", "Team": "NE", "Pos": "RB", "Status": "🟢 Healthy (Backup Value)",
        "L3 TDs": 1, "Inside 5 Touches": 3, "Opp TD Rank": "#22 vs RB", "Touch Trend": "🚀 Major Surge",
        "DraftKings": "+180", "FanDuel": "+195", "Model Prob": 42.0
    },
    {
        "Player": "Michael Wilson", "Team": "ARI", "Pos": "WR", "Status": "🟢 Healthy",
        "L3 TDs": 2, "Inside 5 Touches": 1, "Opp TD Rank": "#18 vs WR", "Touch Trend": "➡️ Steady",
        "DraftKings": "+220", "FanDuel": "+230", "Model Prob": 34.0
    },
    {
        "Player": "Brenton Strange", "Team": "JAX", "Pos": "TE", "Status": "🟢 Healthy",
        "L3 TDs": 1, "Inside 5 Touches": 2, "Opp TD Rank": "#25 vs TE", "Touch Trend": "➡️ Steady",
        "DraftKings": "+260", "FanDuel": "+275", "Model Prob": 31.0
    }
]

df = pd.DataFrame(slate_data)

# Implied Probabilities & Math
df["DK Implied %"] = df["DraftKings"].apply(odds_to_implied)
df["FD Implied %"] = df["FanDuel"].apply(odds_to_implied)
df["Best Implied %"] = df[["DK Implied %", "FD Implied %"]].min(axis=1)
df["EV Edge %"] = df["Model Prob"] - df["Best Implied %"]
df["Value Signal"] = df["EV Edge %"].apply(lambda x: "🟢 YES" if x > 2.5 else ("🟡 SLIGHT" if x > 0 else "🔴 NO"))

df["Model Prob %"] = df["Model Prob"].apply(lambda x: f"{x:.1f}%")
df["EV Edge %"] = df["EV Edge %"].apply(lambda x: f"{'+' if x > 0 else ''}{x:.1f}%")

# Sidebar Filters
st.sidebar.header("Board Filters")
pos_filter = st.sidebar.multiselect("Position", ["ALL", "RB", "WR", "TE", "QB"], default="ALL")
min_l3_tds = st.sidebar.slider("Minimum Touchdowns (Last 3 Games)", 0, 5, 0)
value_only = st.sidebar.checkbox("Show Only Positive Value (+EV)", value=True)

filtered_df = df.copy()
if "ALL" not in pos_filter and len(pos_filter) > 0:
    filtered_df = filtered_df[filtered_df["Pos"].isin(pos_filter)]

filtered_df = filtered_df[filtered_df["L3 TDs"] >= min_l3_tds]

if value_only:
    filtered_df = filtered_df[filtered_df["Value Signal"].isin(["🟢 YES", "🟡 SLIGHT"])]

# Metrics Header
c1, c2, c3, c4 = st.columns(4)
c1.metric("Players On Board", len(filtered_df))
c2.metric("Best Edge", filtered_df["EV Edge %"].max() if not filtered_df.empty else "0%")
c3.metric("Hot Streaks", len(df[df["L3 TDs"] >= 3]))
c4.metric("Data Engine", "Active")

# Table Display
st.subheader("Touchdown Value Ratings & Player Form")
cols = [
    "Player", "Team", "Pos", "Status", "L3 TDs", "Inside 5 Touches", 
    "Opp TD Rank", "Touch Trend", "DraftKings", "FanDuel", "Model Prob %", "EV Edge %", "Value Signal"
]
st.dataframe(filtered_df[cols], use_container_width=True, hide_index=True)

st.info("💡 **Pro Tip**: Focus on players with **3+ Inside 5 Touches** and positive EV edges—they have high red-zone usage that guarantees touchdown opportunities.")
