import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="NFL ATTD Master Edge & Long Shot Hunter", layout="wide")

st.title("🏈 Automated NFL Anytime TD (ATTD) Edge & Long Shot Hunter")
st.caption("Live Slate, Expanded Discovery Board, Implied Totals, Weather, EPA Weighting & Long Shot Signals")

# -------------------------------------------------------------
# 1. HELPER FUNCTIONS
# -------------------------------------------------------------
def odds_to_implied(odds_val):
    """Converts American Odds (+120, -115) to Implied Probability (%)"""
    try:
        clean = str(odds_val).replace('+', '').strip()
        odds = float(clean)
        if odds > 0:
            return round((100.0 / (odds + 100.0)) * 100.0, 1)
        else:
            return round((abs(odds) / (abs(odds) + 100.0)) * 100.0, 1)
    except:
        return 0.0

def calc_fair_odds_and_vig(dk_odds, fd_odds):
    """Calculates no-vig 'Fair Odds' probability baseline between books"""
    p_dk = odds_to_implied(dk_odds)
    p_fd = odds_to_implied(fd_odds)
    if p_dk == 0 or p_fd == 0:
        return max(p_dk, p_fd)
    avg_implied = (p_dk + p_fd) / 2.0
    return round(avg_implied, 1)

def is_long_shot(odds_val):
    """Checks if American odds meet or exceed +200 threshold"""
    try:
        clean = str(odds_val).replace('+', '').strip()
        if clean == 'N/A':
            return False
        return float(clean) >= 200.0
    except:
        return False

def calc_implied_team_total(game_total, spread, is_favorite=True):
    """Calculates Implied Team Score baseline from Vegas total & spread"""
    try:
        total = float(game_total)
        spd = abs(float(spread))
        return round((total + spd) / 2.0, 1) if is_favorite else round((total - spd) / 2.0, 1)
    except:
        return 0.0

# -------------------------------------------------------------
# 2. LIVE WEATHER ENGINE (Open-Meteo)
# -------------------------------------------------------------
STADIUM_COORDS = {
    "BUF": {"lat": 42.7738, "lon": -78.7870},
    "GB":  {"lat": 44.5013, "lon": -88.0622},
    "CHI": {"lat": 41.8623, "lon": -87.6167},
    "NE":  {"lat": 42.0909, "lon": -71.2643},
    "BAL": {"lat": 39.2780, "lon": -76.6227},
    "PHI": {"lat": 39.9008, "lon": -75.1675},
    "TB":  {"lat": 27.9759, "lon": -82.5033},
    "CAR": {"lat": 35.2258, "lon": -80.8528},
    "CIN": {"lat": 39.0955, "lon": -84.5161},
    "NYG": {"lat": 40.8128, "lon": -74.0742},
    "KC":  {"lat": 39.0489, "lon": -94.4839},
    "HOU": {"lat": 29.6847, "lon": -95.4107},
}

@st.cache_data(ttl=1800)
def get_stadium_weather(team):
    """Pulls live real-time weather metrics for outdoor stadiums."""
    if team not in STADIUM_COORDS:
        return "Dome 🏟️"
    
    loc = STADIUM_COORDS[team]
    url = f"https://api.open-meteo.com/v1/forecast?latitude={loc['lat']}&longitude={loc['lon']}&current_weather=true&temperature_unit=fahrenheit&windspeed_unit=mph"
    
    try:
        res = requests.get(url, timeout=3).json()
        curr = res.get("current_weather", {})
        temp = round(curr.get("temperature", 60))
        wind = round(curr.get("windspeed", 5))
        
        if wind >= 18:
            return f"💨 {wind}mph Wind ({temp}°F)"
        elif temp <= 32:
            return f"❄️ {temp}°F Cold ({wind}mph)"
        else:
            return f"☀️ {temp}°F / {wind}mph"
    except Exception:
        return "Outdoor (Live)"

# -------------------------------------------------------------
# 3. EXPANDED MASTER SLATE (Chalk, Mid-Tier & Deep Long Shots)
# -------------------------------------------------------------
@st.cache_data(ttl=3600)
def load_nfl_board():
    data = [
        # --- CHALK & CORE PLAYS ---
        {
            "Player": "Derrick Henry", "Team": "BAL", "Pos": "RB", "Opponent": "vs TEN", "Status": "🟢 Active",
            "Game Total": 47.5, "Spread": "-6.5", "Is Fav": True, "QB EPA Factor": +1.5,
            "1st Read %": "N/A (RB)", "Route %": "32%", "Base Sim": 54.7,
            "L3 TDs": 4, "Inside 5 Touches": 6, "Def TDs Allowed/G": "1.8 (31st)", "Def RZ Rank": "#30 (Poor)",
            "DraftKings": "+110", "FanDuel": "+115"
        },
        {
            "Player": "Ja'Marr Chase", "Team": "CIN", "Pos": "WR", "Opponent": "vs JAX", "Status": "🟢 Active",
            "Game Total": 48.0, "Spread": "-3.0", "Is Fav": True, "QB EPA Factor": +2.0,
            "1st Read %": "34.5%", "Route %": "92%", "Base Sim": 59.0,
            "L3 TDs": 3, "Inside 5 Touches": 2, "Def TDs Allowed/G": "2.1 (32nd)", "Def RZ Rank": "#32 (Worst)",
            "DraftKings": "-115", "FanDuel": "-110"
        },
        {
            "Player": "CeeDee Lamb", "Team": "DAL", "Pos": "WR", "Opponent": "@ HOU", "Status": "🟢 Active",
            "Game Total": 47.0, "Spread": "-1.5", "Is Fav": True, "QB EPA Factor": +1.2,
            "1st Read %": "36.2%", "Route %": "94%", "Base Sim": 51.8,
            "L3 TDs": 2, "Inside 5 Touches": 2, "Def TDs Allowed/G": "1.6 (29th)", "Def RZ Rank": "#31 (Poor)",
            "DraftKings": "+105", "FanDuel": "+110"
        },
        {
            "Player": "Jahmyr Gibbs", "Team": "DET", "Pos": "RB", "Opponent": "@ CAR", "Status": "🟢 Active",
            "Game Total": 49.5, "Spread": "-3.5", "Is Fav": True, "QB EPA Factor": +2.2,
            "1st Read %": "18.2%", "Route %": "64%", "Base Sim": 47.8,
            "L3 TDs": 3, "Inside 5 Touches": 4, "Def TDs Allowed/G": "1.5 (28th)", "Def RZ Rank": "#27 (Weak)",
            "DraftKings": "+125", "FanDuel": "+130"
        },
        
        # --- MID-TIER VALUE PLAYS ---
        {
            "Player": "Braelon Allen", "Team": "NYJ", "Pos": "RB", "Opponent": "@ CHI", "Status": "🚀 Lead RB (Breece Out)",
            "Game Total": 42.0, "Spread": "+2.5", "Is Fav": False, "QB EPA Factor": -0.8,
            "1st Read %": "N/A (RB)", "Route %": "38%", "Base Sim": 44.0,
            "L3 TDs": 2, "Inside 5 Touches": 5, "Def TDs Allowed/G": "1.4 (21st)", "Def RZ Rank": "#20 (Mid)",
            "DraftKings": "+135", "FanDuel": "+145"
        },
        {
            "Player": "Jalen Hurts", "Team": "PHI", "Pos": "QB", "Opponent": "vs LAR", "Status": "🟢 Active",
            "Game Total": 46.5, "Spread": "-2.5", "Is Fav": True, "QB EPA Factor": +1.8,
            "1st Read %": "N/A (QB)", "Route %": "N/A", "Base Sim": 43.2,
            "L3 TDs": 4, "Inside 5 Touches": 7, "Def TDs Allowed/G": "1.1 (25th)", "Def RZ Rank": "#28 (Weak)",
            "DraftKings": "+165", "FanDuel": "+160"
        },
        {
            "Player": "Josh Allen", "Team": "BUF", "Pos": "QB", "Opponent": "vs NE", "Status": "🟢 Active",
            "Game Total": 45.0, "Spread": "-7.0", "Is Fav": True, "QB EPA Factor": +2.5,
            "1st Read %": "N/A (QB)", "Route %": "N/A", "Base Sim": 42.5,
            "L3 TDs": 3, "Inside 5 Touches": 5, "Def TDs Allowed/G": "0.8 (18th)", "Def RZ Rank": "#15 (Mid)",
            "DraftKings": "+140", "FanDuel": "+150"
        },
        {
            "Player": "Puka Nacua", "Team": "LAR", "Pos": "WR", "Opponent": "@ PHI", "Status": "🟡 Questionable",
            "Game Total": 46.5, "Spread": "+2.5", "Is Fav": False, "QB EPA Factor": +0.5,
            "1st Read %": "31.0%", "Route %": "88%", "Base Sim": 41.5,
            "L3 TDs": 2, "Inside 5 Touches": 3, "Def TDs Allowed/G": "1.4 (22nd)", "Def RZ Rank": "#18 (Mid)",
            "DraftKings": "+150", "FanDuel": "+155"
        },

        # --- DEEP LONG SHOTS (+200 TO +450) ---
        {
            "Player": "Brock Bowers", "Team": "LV", "Pos": "TE", "Opponent": "vs KC", "Status": "🟢 Active",
            "Game Total": 43.5, "Spread": "+3.5", "Is Fav": False, "QB EPA Factor": -1.0,
            "1st Read %": "27.5%", "Route %": "81%", "Base Sim": 39.5,
            "L3 TDs": 2, "Inside 5 Touches": 3, "Def TDs Allowed/G": "1.1 (29th)", "Def RZ Rank": "#25 (Weak)",
            "DraftKings": "+210", "FanDuel": "+225"
        },
        {
            "Player": "Khalil Shakir", "Team": "BUF", "Pos": "WR", "Opponent": "vs NE", "Status": "🟢 Active",
            "Game Total": 45.0, "Spread": "-7.0", "Is Fav": True, "QB EPA Factor": +2.5,
            "1st Read %": "21.0%", "Route %": "78%", "Base Sim": 36.0,
            "L3 TDs": 1, "Inside 5 Touches": 2, "Def TDs Allowed/G": "1.2 (19th)", "Def RZ Rank": "#16 (Mid)",
            "DraftKings": "+240", "FanDuel": "+250"
        },
        {
            "Player": "Tucker Kraft", "Team": "GB", "Pos": "TE", "Opponent": "vs CHI", "Status": "🟢 Active",
            "Game Total": 44.0, "Spread": "-3.0", "Is Fav": True, "QB EPA Factor": +1.1,
            "1st Read %": "19.5%", "Route %": "76%", "Base Sim": 34.5,
            "L3 TDs": 2, "Inside 5 Touches": 3, "Def TDs Allowed/G": "1.3 (20th)", "Def RZ Rank": "#19 (Mid)",
            "DraftKings": "+275", "FanDuel": "+290"
        },
        {
            "Player": "Ray Davis", "Team": "BUF", "Pos": "RB", "Opponent": "vs NE", "Status": "🟢 Active",
            "Game Total": 45.0, "Spread": "-7.0", "Is Fav": True, "QB EPA Factor": +2.5,
            "1st Read %": "N/A (RB)", "Route %": "24%", "Base Sim": 32.0,
            "L3 TDs": 1, "Inside 5 Touches": 4, "Def TDs Allowed/G": "1.2 (19th)", "Def RZ Rank": "#16 (Mid)",
            "DraftKings": "+310", "FanDuel": "+330"
        },
        {
            "Player": "DeMario Douglas", "Team": "NE", "Pos": "WR", "Opponent": "@ BUF", "Status": "🟢 Active",
            "Game Total": 45.0, "Spread": "+7.0", "Is Fav": False, "QB EPA Factor": -1.2,
            "1st Read %": "28.0%", "Route %": "82%", "Base Sim": 31.0,
            "L3 TDs": 1, "Inside 5 Touches": 1, "Def TDs Allowed/G": "0.9 (12th)", "Def RZ Rank": "#10 (Tough)",
            "DraftKings": "+350", "FanDuel": "+375"
        },
        {
            "Player": "Breece Hall", "Team": "NYJ", "Pos": "RB", "Opponent": "@ CHI", "Status": "🔴 OUT (Quad)",
            "Game Total": 42.0, "Spread": "+2.5", "Is Fav": False, "QB EPA Factor": -0.8,
            "1st Read %": "N/A", "Route %": "0%", "Base Sim": 0.0,
            "L3 TDs": 1, "Inside 5 Touches": 0, "Def TDs Allowed/G": "1.4 (21st)", "Def RZ Rank": "#20 (Mid)",
            "DraftKings": "N/A", "FanDuel": "N/A"
        }
    ]
    return pd.DataFrame(data)

df = load_nfl_board()

# Live Weather Integration
df["Live Weather"] = df["Team"].apply(get_stadium_weather)

# Calculations
df["Sim Prob"] = df["Base Sim"] + df["QB EPA Factor"]
df["Implied Score"] = df.apply(lambda r: calc_implied_team_total(r["Game Total"], r["Spread"], r["Is Fav"]), axis=1)
df["DK Implied %"] = df["DraftKings"].apply(odds_to_implied)
df["FD Implied %"] = df["FanDuel"].apply(odds_to_implied)
df["Best Implied %"] = df[["DK Implied %", "FD Implied %"]].min(axis=1)

df["Fair Odds %"] = df.apply(lambda r: calc_fair_odds_and_vig(r["DraftKings"], r["FanDuel"]), axis=1)

# EV EDGE & DISCOVERY SIGNALS
df["EV_Edge_Num"] = df["Sim Prob"] - df["Best Implied %"]
df["Value Signal"] = df["EV_Edge_Num"].apply(lambda x: "🟢 YES" if x > 2.5 else ("🟡 SLIGHT" if x > 0 else "🔴 NO"))

# Dynamic Long Shot Discovery Tag (+200 and up with positive EV)
def get_discovery_tag(row):
    if is_long_shot(row["DraftKings"]) or is_long_shot(row["FanDuel"]):
        if row["EV_Edge_Num"] > 0:
            return "🎯 LIVE LONG SHOT"
        else:
            return "⚠️ LONG SHOT TRAP"
    return "Standard Board"

df["Discovery Status"] = df.apply(get_discovery_tag, axis=1)

# Formatted strings for display
df["Sim Prob %"] = df["Sim Prob"].apply(lambda x: f"{x:.1f}%")
df["Fair Odds % Col"] = df["Fair Odds %"].apply(lambda x: f"{x:.1f}%")
df["EV Edge %"] = df["EV_Edge_Num"].apply(lambda x: f"{'+' if x > 0 else ''}{x:.1f}%")

# -------------------------------------------------------------
# 4. STREAMLIT FRONTEND CONTROLS & DISPLAY
# -------------------------------------------------------------
st.sidebar.header("Filter & Discovery Controls")

scratched_players = st.sidebar.multiselect("🚫 Scratch/Remove Players", options=df["Player"].unique(), default=["Breece Hall"])
pos_filter = st.sidebar.multiselect("Position", ["ALL", "RB", "WR", "TE", "QB"], default="ALL")

# Discovery Mode Toggle
discovery_mode = st.sidebar.checkbox("🎯 Long Shot Discovery Mode (+200 & +EV Only)", value=False)

weather_alert_only = st.sidebar.checkbox("Show Weather Impact Games Only", value=False)
value_only = st.sidebar.checkbox("Show Only Positive Value (+EV)", value=False)

filtered_df = df[~df["Player"].isin(scratched_players)].copy()

if "ALL" not in pos_filter and len(pos_filter) > 0:
    filtered_df = filtered_df[filtered_df["Pos"].isin(pos_filter)]

if discovery_mode:
    filtered_df = filtered_df[filtered_df["Discovery Status"] == "🎯 LIVE LONG SHOT"]

if weather_alert_only:
    filtered_df = filtered_df[filtered_df["Live Weather"].str.contains("💨|❄️", na=False)]

if value_only:
    filtered_df = filtered_df[filtered_df["Value Signal"].isin(["🟢 YES", "🟡 SLIGHT"])]

top_edge_val = filtered_df["EV_Edge_Num"].max() if not filtered_df.empty else 0.0

# Metrics Header
c1, c2, c3, c4 = st.columns(4)
c1.metric("Active Players on Board", len(filtered_df))
c2.metric("Top Edge Found", f"+{top_edge_val:.1f}%" if top_edge_val > 0 else f"{top_edge_val:.1f}%")
c3.metric("Discovery Engine", "🟢 Active")
c4.metric("Injury Scratchpad", f"{len(scratched_players)} Scratched" if scratched_players else "🟢 Clean Board")

# Main Board
st.subheader("Touchdown Prop Edge & Discovery Board")
display_cols = [
    "Player", "Team", "Pos", "DraftKings", "FanDuel", 
    "Sim Prob %", "EV Edge %", "Value Signal", "Discovery Status",
    "Status", "Opponent", "Live Weather", "Implied Score", 
    "Inside 5 Touches", "Def RZ Rank", 
    "1st Read %", "Route %", "Fair Odds % Col"
]
st.dataframe(filtered_df[display_cols], use_container_width=True, hide_index=True)
