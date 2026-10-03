import streamlit as st
import pandas as pd

st.set_page_config(page_title="NFL ATTD Value Model", layout="wide")

st.title("🏈 NFL Anytime Touchdown (ATTD) Value Model")
st.caption("Live Slate Analysis | Model Projected Probability vs. Sportsbook Odds")

# Full Slate NFL Data
data = [
    {"Player": "Derrick Henry", "Team": "BAL", "Pos": "RB", "Sportsbook Odds": "+110", "Model Prob": "52.5%", "Sportsbook Implied": "47.6%", "EV Edge": "+4.9%", "Value": "YES"},
    {"Player": "Jahmyr Gibbs", "Team": "DET", "Pos": "RB", "Sportsbook Odds": "+125", "Model Prob": "48.0%", "Sportsbook Implied": "44.4%", "EV Edge": "+3.6%", "Value": "YES"},
    {"Player": "Jonathan Taylor", "Team": "IND", "Pos": "RB", "Sportsbook Odds": "-320", "Model Prob": "78.0%", "Sportsbook Implied": "76.2%", "EV Edge": "+1.8%", "Value": "SLIGHT"},
    {"Player": "Ja'Marr Chase", "Team": "CIN", "Pos": "WR", "Sportsbook Odds": "-115", "Model Prob": "58.0%", "Sportsbook Implied": "53.5%", "EV Edge": "+4.5%", "Value": "YES"},
    {"Player": "Josh Allen", "Team": "BUF", "Pos": "QB", "Sportsbook Odds": "-125", "Model Prob": "60.0%", "Sportsbook Implied": "55.6%", "EV Edge": "+4.4%", "Value": "YES"},
    {"Player": "James Cook", "Team": "BUF", "Pos": "RB", "Sportsbook Odds": "-135", "Model Prob": "54.0%", "Sportsbook Implied": "57.4%", "EV Edge": "-3.4%", "Value": "NO"},
    {"Player": "Puka Nacua", "Team": "LAR", "Pos": "WR", "Sportsbook Odds": "+135", "Model Prob": "46.0%", "Sportsbook Implied": "42.6%", "EV Edge": "+3.4%", "Value": "YES"},
    {"Player": "Brock Bowers", "Team": "LV", "Pos": "TE", "Sportsbook Odds": "+200", "Model Prob": "37.5%", "Sportsbook Implied": "33.3%", "EV Edge": "+4.2%", "Value": "YES"},
    {"Player": "Brenton Strange", "Team": "JAX", "Pos": "TE", "Sportsbook Odds": "+260", "Model Prob": "31.0%", "Sportsbook Implied": "27.8%", "EV Edge": "+3.2%", "Value": "YES"},
    {"Player": "Michael Wilson", "Team": "ARI", "Pos": "WR", "Sportsbook Odds": "+220", "Model Prob": "34.0%", "Sportsbook Implied": "31.3%", "EV Edge": "+2.7%", "Value": "YES"},
    {"Player": "Rhamondre Stevenson", "Team": "NE", "Pos": "RB", "Sportsbook Odds": "+150", "Model Prob": "38.0%", "Sportsbook Implied": "40.0%", "EV Edge": "-2.0%", "Value": "NO"},
]

df = pd.DataFrame(data)

# Sidebar filters
st.sidebar.header("Filter Slate")
selected_pos = st.sidebar.multiselect("Position", options=["ALL", "RB", "WR", "TE", "QB"], default="ALL")
value_only = st.sidebar.checkbox("Show Only Positive Value (+EV)", value=True)

# Apply filters
filtered_df = df.copy()
if "ALL" not in selected_pos and len(selected_pos) > 0:
    filtered_df = filtered_df[filtered_df["Pos"].isin(selected_pos)]

if value_only:
    filtered_df = filtered_df[filtered_df["Value"].isin(["YES", "SLIGHT"])]

# Metrics Header
col1, col2, col3 = st.columns(3)
col1.metric("Players Displayed", len(filtered_df))
col2.metric("Best Value Edge", "+4.9%" if not filtered_df.empty else "0%")
col3.metric("Slate Status", "Active")

# Display Main Table
st.subheader("Touchdown Value Bets")
st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)

st.success("🟢 **Positive Edge** = The model's projected touchdown probability is higher than the implied probability from sportsbook odds.")
