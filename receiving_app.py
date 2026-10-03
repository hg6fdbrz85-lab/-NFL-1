import streamlit as st
import pandas as pd

st.set_page_config(page_title="NFL Receiving Props Master Edge", layout="wide")

st.title("📈 NFL Receiving Yards & Receptions Edge Finder")
st.caption("Dedicated Workspace: Target Shares, Route Participation, Line Discrepancy & Yards Over/Under Model")

# -------------------------------------------------------------
# 1. HELPER FUNCTIONS
# -------------------------------------------------------------
def calc_implied_team_total(game_total, spread, is_favorite=True):
    """Calculates Implied Team Score baseline from Vegas total & spread"""
    try:
        total = float(game_total)
        spd = abs(float(spread))
        return round((total + spd) / 2.0, 1) if is_favorite else round((total - spd) / 2.0, 1)
    except:
        return 0.0

# -------------------------------------------------------------
# 2. DEDICATED RECEIVING MASTER SLATE
# -------------------------------------------------------------
@st.cache_data(ttl=3600)
def load_receiving_board():
    data = [
        {
            "Player": "Ja'Marr Chase", "Team": "CIN", "Pos": "WR", "Opponent": "vs JAX", "Status": "🟢 Active",
            "Game Total": 48.0, "Spread": "-3.0", "Is Fav": True, "QB EPA Factor": +2.0,
            "Target Share %": "34.5%", "Route %": "92%", "Expected Receptions": 7.2, "Model Rec Yards": 88.5,
            "DraftKings Line": "74.5", "FanDuel Line": "78.5", "DK Odds": "-115", "FD Odds": "-110"
        },
        {
            "Player": "CeeDee Lamb", "Team": "DAL", "Pos": "WR", "Opponent": "@ HOU", "Status": "🟢 Active",
            "Game Total": 47.0, "Spread": "-1.5", "Is Fav": True, "QB EPA Factor": +1.2,
            "Target Share %": "36.2%", "Route %": "94%", "Expected Receptions": 7.8, "Model Rec Yards": 92.0,
            "DraftKings Line": "82.5", "FanDuel Line": "80.5", "DK Odds": "-110", "FD Odds": "-115"
        },
        {
            "Player": "Puka Nacua", "Team": "LAR", "Pos": "WR", "Opponent": "@ PHI", "Status": "🟡 Questionable",
            "Game Total": 46.5, "Spread": "+2.5", "Is Fav": False, "QB EPA Factor": +0.5,
            "Target Share %": "31.0%", "Route %": "88%", "Expected Receptions": 6.5, "Model Rec Yards": 76.0,
            "DraftKings Line": "69.5", "FanDuel Line": "73.5", "DK Odds": "-110", "FD Odds": "-110"
        },
        {
            "Player": "Brock Bowers", "Team": "LV", "Pos": "TE", "Opponent": "vs KC", "Status": "🟢 Active",
            "Game Total": 43.5, "Spread": "+3.5", "Is Fav": False, "QB EPA Factor": -1.0,
            "Target Share %": "27.5%", "Route %": "81%", "Expected Receptions": 5.8, "Model Rec Yards": 61.5,
            "DraftKings Line": "52.5", "FanDuel Line": "56.5", "DK Odds": "-115", "FD Odds": "-110"
        },
        {
            "Player": "Khalil Shakir", "Team": "BUF", "Pos": "WR", "Opponent": "vs NE", "Status": "🟢 Active",
            "Game Total": 45.0, "Spread": "-7.0", "Is Fav": True, "QB EPA Factor": +2.5,
            "Target Share %": "21.0%", "Route %": "78%", "Expected Receptions": 4.5, "Model Rec Yards": 54.0,
            "DraftKings Line": "44.5", "FanDuel Line": "48.5", "DK Odds": "-110", "FD Odds": "-115"
        },
        {
            "Player": "DeMario Douglas", "Team": "NE", "Pos": "WR", "Opponent": "@ BUF", "Status": "🟢 Active",
            "Game Total": 45.0, "Spread": "+7.0", "Is Fav": False, "QB EPA Factor": -1.2,
            "Target Share %": "28.0%", "Route %": "82%", "Expected Receptions": 5.5, "Model Rec Yards": 58.0,
            "DraftKings Line": "55.5", "FanDuel Line": "49.5", "DK Odds": "-110", "FD Odds": "-110"
        }
    ]
    return pd.DataFrame(data)

df = load_receiving_board()

# Calculations
df["Implied Score"] = df.apply(lambda r: calc_implied_team_total(r["Game Total"], r["Spread"], r["Is Fav"]), axis=1)

df["DK_Line_Num"] = df["DraftKings Line"].astype(float)
df["FD_Line_Num"] = df["FanDuel Line"].astype(float)

df["Yards Edge (vs DK)"] = df["Model Rec Yards"] - df["DK_Line_Num"]

def get_rec_signal(edge):
    if edge >= 7.0:
        return "🟢 OVER VALUE"
    elif edge <= -7.0:
        return "🔴 UNDER VALUE"
    else:
        return "⚪ FAIR MARKET"

df["Value Signal"] = df["Yards Edge (vs DK)"].apply(get_rec_signal)

# Book Discrepancy Scanner for Yards Lines
df["Line Diff"] = abs(df["DK_Line_Num"] - df["FD_Line_Num"])
df["Outlier Status"] = df["Line Diff"].apply(lambda x: "⚡ LINE DISCREPANCY (4+ Yds)" if x >= 4.0 else "Standard Line")

# Formatted displays
df["Yards Edge Display"] = df["Yards Edge (vs DK)"].apply(lambda x: f"{'+' if x > 0 else ''}{x:.1f} yds")

# -------------------------------------------------------------
# 3. STREAMLIT CONTROLS & DISPLAY
# -------------------------------------------------------------
st.sidebar.header("Receiving Workspace Filters")

pos_filter = st.sidebar.multiselect("Position Filter", ["ALL", "WR", "TE"], default="ALL")
discrepancy_mode = st.sidebar.checkbox("⚡ Show Significant Book Line Gaps Only (4+ Yards)", value=False)
value_over_only = st.sidebar.checkbox("Show Only Strong 'OVER' Edges", value=False)

filtered_df = df.copy()

if "ALL" not in pos_filter and len(pos_filter) > 0:
    filtered_df = filtered_df[filtered_df["Pos"].isin(pos_filter)]

if discrepancy_mode:
    filtered_df = filtered_df[filtered_df["Outlier Status"].str.contains("DISCREPANCY")]

if value_over_only:
    filtered_df = filtered_df[filtered_df["Value Signal"] == "🟢 OVER VALUE"]

top_edge = filtered_df["Yards Edge (vs DK)"].max() if not filtered_df.empty else 0.0

# Metrics Header
c1, c2, c3, c4 = st.columns(4)
c1.metric("Active Pass Catchers", len(filtered_df))
c2.metric("Top Yards Edge", f"+{top_edge:.1f} yds" if top_edge > 0 else f"{top_edge:.1f} yds")
c3.metric("Workspace Type", "Receiving Yards Only")
c4.metric("Status", "🟢 Operational")

# Main Board Display
st.subheader("Receiving Yards & Receptions Worksheet")
display_cols = [
    "Player", "Team", "Pos", "DraftKings Line", "FanDuel Line", 
    "Model Rec Yards", "Yards Edge Display", "Value Signal", "Outlier Status",
    "Opponent", "Target Share %", "Route %", "Expected Receptions"
]
st.dataframe(filtered_df[display_cols], use_container_width=True, hide_index=True)
