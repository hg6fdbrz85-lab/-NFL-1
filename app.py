import streamlit as st
import pandas as pd

# 1. Page Title & Setup
st.set_page_config(page_title="NFL TD Value Finder", layout="wide")
st.title("🏈 NFL Anytime Touchdown Value Model")
st.caption("Updated for Weekend Slate | Expected TDs (xTD) vs Sportsbook Odds")

# 2. Sample Data Engine (You can add/change players anytime right here)
data = [
    {"Player": "Derrick Henry", "Team": "BAL", "Pos": "RB", "RZ Touches/Gm": 4.2, "Inside 5 Touches": 1.8, "Opp RZ Def Rank": 22, "DraftKings Odds": "+110"},
    {"Player": "CeeDee Lamb", "Team": "DAL", "Pos": "WR", "RZ Touches/Gm": 2.1, "Inside 5 Touches": 0.4, "Opp RZ Def Rank": 14, "DraftKings Odds": "+140"},
    {"Player": "Travis Kelce", "Team": "KC", "Pos": "TE", "RZ Touches/Gm": 1.8, "Inside 5 Touches": 0.6, "Opp RZ Def Rank": 28, "DraftKings Odds": "+175"},
    {"Player": "A.J. Brown", "Team": "PHI", "Pos": "WR", "RZ Touches/Gm": 1.5, "Inside 5 Touches": 0.2, "Opp RZ Def Rank": 8, "DraftKings Odds": "+160"},
    {"Player": "Jahmyr Gibbs", "Team": "DET", "Pos": "RB", "RZ Touches/Gm": 3.1, "Inside 5 Touches": 1.2, "Opp RZ Def Rank": 19, "DraftKings Odds": "+125"},
]

df = pd.DataFrame(data)

# 3. Model Math: Calculate xTD and Expected Value Probability
df['xTD'] = (df['Inside 5 Touches'] * 0.40) + ((df['RZ Touches/Gm'] - df['Inside 5 Touches']) * 0.10)
df['Model Prob %'] = ((1 - (2.71828 ** -df['xTD'])) * 100).round(1)

# Convert odds string to implied probability %
def odds_to_prob(odds_str):
    val = int(odds_str.replace("+", "").replace("-", ""))
    if "+" in odds_str:
        return round(100 / (val + 100) * 100, 1)
    else:
        return round(val / (val + 100) * 100, 1)

df['Implied Odds %'] = df['DraftKings Odds'].apply(odds_to_prob)
df['Edge (% Points)'] = (df['Model Prob %'] - df['Implied Odds %']).round(1)

# 4. Interactive Web Controls
st.sidebar.header("Filter Options")
selected_pos = st.sidebar.multiselect("Filter Position", options=["RB", "WR", "TE"], default=["RB", "WR", "TE"])
min_edge = st.sidebar.slider("Minimum Model Edge %", min_value=-10.0, max_value=20.0, value=0.0)

filtered_df = df[(df['Pos'].isin(selected_pos)) & (df['Edge (% Points)'] >= min_edge)]

# 5. Display Clean Interactive Table
st.subheader("Today's Top Value Bets (+EV)")
st.dataframe(
    filtered_df[['Player', 'Team', 'Pos', 'DraftKings Odds', 'Model Prob %', 'Implied Odds %', 'Edge (% Points)']],
    use_container_width=True,
    hide_index=True
)

st.success("🟢 Positive Edge = Model probability is higher than the Sportsbook odds!")
