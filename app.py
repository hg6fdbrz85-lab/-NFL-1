import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="NFL 1st TD Master Edge & Long Shot Hunter", layout="wide")

st.title("🏈 Automated NFL First Touchdown (1st TD) & Opening Script Engine")
st.caption("First TD Board, Opening Drive Script Analytics, Book Discrepancies & Long Shot Lottery Scanner")

# -------------------------------------------------------------
# 1. HELPER FUNCTIONS & DISCREPANCY DETECTOR
# -------------------------------------------------------------
def odds_to_implied(odds_val):
    """Converts American Odds (+120, -115) to Implied Probability (%)"""
    try:
        clean = str(odds_val).replace('+', '').strip()
        if clean == 'N/A' or clean == '':
            return 0.0
        odds = float(clean)
        if odds > 0:
            return round((100.0 / (odds + 100.0)) * 100.0, 1)
        else:
            return round((abs(odds) / (abs(odds) + 100.0)) * 100.0, 1)
    except:
        return 0.0

def is_long_shot(odds_val):
    """Checks if American odds meet or exceed +800 threshold for 1st TD"""
    try:
        clean = str(odds_val).replace('+', '').strip()
        if clean == 'N/A' or clean == '':
            return False
        return float(clean) >= 800.0
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
            return f"☀️️ {temp}°F / {wind}mph"
    except Exception:
        return "Outdoor (Live)"

# -------------------------------------------------------------
# 3. EXPANDED 1ST TD MASTER SLATE
# -------------------------------------------------------------
@st.cache_data(ttl=3600)
def load_nfl_1std_board():
    data = [
        # --- CHALK 1ST TD PLAYS ---
        {
            "Player": "Derrick Henry", "Team": "BAL", "Pos": "RB", "Opponent": "vs TEN", "Status": "🟢 Active",
            "Game Total": 47.5, "Spread": "-6.5", "Is Fav": True, "Opening Script Target Rate": "28% (High Rush Script)",
            "1st Drive RedZone %": "42%", "Base 1st TD Sim %": 18.5,
            "DraftKings": "+450", "FanDuel": "+475"
        },
        {
            "Player": "Ja'Marr Chase", "Team": "CIN", "Pos": "WR", "Opponent": "vs JAX", "Status": "🟢 Active",
            "Game Total": 48.0, "Spread": "-3.0", "Is Fav": True, "Opening Script Target Rate": "38% (Primary Script)",
            "1st Drive RedZone %": "35%", "Base 1st TD Sim %": 16.0,
            "DraftKings": "+550", "FanDuel": "+525"
        },
        {
            "Player": "CeeDee Lamb", "Team": "DAL", "Pos": "WR", "Opponent": "@ HOU", "Status": "🟢 Active",
            "Game Total": 47.0, "Spread": "-1.5", "Is Fav": True, "Opening Script Target Rate": "40% (Alpha Focus)",
            "1st Drive RedZone %": "30%", "Base 1st TD Sim %": 15.2,
            "DraftKings": "+600", "FanDuel": "+575"
        },
        {
            "Player": "Jahmyr Gibbs", "Team": "DET", "Pos": "RB", "Opponent": "@ CAR", "Status": "🟢 Active",
            "Game Total": 49.5, "Spread": "-3.5", "Is Fav": True, "Opening Script Target Rate": "24% (Explosive)",
            "1st Drive RedZone %": "38%", "Base 1st TD Sim %": 14.8,
            "DraftKings": "+650", "FanDuel": "+700"
        },
        
        # --- MID-TIER & SCRIPT VALUE PLAYS ---
        {
            "Player": "Braelon Allen", "Team": "NYJ", "Pos": "RB", "Opponent": "@ CHI", "Status": "🚀 Lead RB (Breece Out)",
            "Game Total": 42.0, "Spread": "+2.5", "Is Fav": False, "Opening Script Target Rate": "30% (Goal-Line Focus)",
            "1st Drive RedZone %": "45%", "Base 1st TD Sim %": 12.5,
            "DraftKings": "+800", "FanDuel": "+850"
        },
        {
            "Player": "Jalen Hurts", "Team": "PHI", "Pos": "QB", "Opponent": "vs LAR", "Status": "🟢 Active",
            "Game Total": 46.5, "Spread": "-2.5", "Is Fav": True, "Opening Script Target Rate": "Tush Push Core",
            "1st Drive RedZone %": "50%", "Base 1st TD Sim %": 13.0,
            "DraftKings": "+750", "FanDuel": "+725"
        },
        {
            "Player": "Josh Allen", "Team": "BUF", "Pos": "QB", "Opponent": "vs NE", "Status": "🟢 Active",
            "Game Total": 45.0, "Spread": "-7.0", "Is Fav": True, "Opening Script Target Rate": "Design Rush Focus",
            "1st Drive RedZone %": "40%", "Base 1st TD Sim %": 12.0,
            "DraftKings": "+800", "FanDuel": "+750"
        },

        # --- HIGH-ODDS / LONG SHOT LOTTERY TICKETS (+1000 OR MORE) ---
        {
            "Player": "Brock Bowers", "Team": "LV", "Pos": "TE", "Opponent": "vs KC", "Status": "🟢 Active",
            "Game Total": 43.5, "Spread": "+3.5", "Is Fav": False, "Opening Script Target Rate": "32% (Script Safety)",
            "1st Drive RedZone %": "25%", "Base 1st TD Sim %": 8.5,
            "DraftKings": "+1100", "FanDuel": "+1000"
        },
        {
            "Player": "Khalil Shakir", "Team": "BUF", "Pos": "WR", "Opponent": "vs NE", "Status": "🟢 Active",
            "Game Total": 45.0, "Spread": "-7.0", "Is Fav": True, "Opening Script Target Rate": "22% (Slot Leak)",
            "1st Drive RedZone %": "18%", "Base 1st TD Sim %": 6.8,
            "DraftKings": "+1400", "FanDuel": "+1250"
        },
        {
            "Player": "Tucker Kraft", "Team": "GB", "Pos": "TE", "Opponent": "vs CHI", "Status": "🟢 Active",
            "Game Total": 44.0, "Spread": "-3.0", "Is Fav": True, "Opening Script Target Rate": "20% (Play-Action)",
            "1st Drive RedZone %": "22%", "Base 1st TD Sim %": 6.0,
            "DraftKings": "+1500", "FanDuel": "+1600"
        },
        {
            "Player": "Ray Davis", "Team": "BUF", "Pos": "RB", "Opponent": "vs NE", "Status": "🟢 Active",
            "Game Total": 45.0, "Spread": "-7.0", "Is Fav": True, "Opening Script Target Rate": "15% (Early Change-up)",
            "1st Drive RedZone %": "30%", "Base 1st TD Sim %": 5.5,
            "DraftKings": "+1800", "FanDuel": "+1650"
        },
        {
            "Player": "DeMario Douglas", "Team": "NE", "Pos": "WR", "Opponent": "@ BUF", "Status": "🟢 Active",
            "Game Total": 45.0, "Spread": "+7.0", "Is Fav": False, "Opening Script Target Rate": "35% (Catch-up Script)",
            "1st Drive RedZone %": "15%", "Base 1st TD Sim %": 4.8,
            "DraftKings": "+2000", "FanDuel": "+2200"
        },
        {
            "Player": "Breece Hall", "Team": "NYJ", "Pos": "RB", "Opponent": "@ CHI", "Status": "🔴 OUT (Quad)",
            "Game Total": 42.0, "Spread": "+2.5", "Is Fav": False, "Opening Script Target Rate": "0%",
            "1st Drive RedZone %": "0%", "Base 1st TD Sim %": 0.0,
            "DraftKings": "N/A", "FanDuel": "N/A"
        }
    ]
    return pd.DataFrame(data)

df = load_nfl_1std_board()

# Live Weather Integration
df["Live Weather"] = df["Team"].apply(get_stadium_weather)

# Calculations
df["Implied Score"] = df.apply(lambda r: calc_implied_team_total(r["Game Total"], r["Spread"], r["Is Fav"]), axis=1)
df["DK Implied %"] = df["DraftKings"].apply(odds_to_implied)
df["FD Implied %"] = df["FanDuel"].apply(odds_to_implied)
df["Best Implied %"] = df[["DK Implied %", "FD Implied %"]].min(axis=1)

# 1st TD Edge Calculation (Model Sim % vs Market Implied %)
df["EV_Edge_Num"] = df["Base 1st TD Sim %"] - df["Best Implied %"]
df["Value Signal"] = df["EV_Edge_Num"].apply(lambda x: "🟢 GREAT VALUE" if x > 2.0 else ("🟡 SLIGHT EDGE" if x > 0 else "🔴 NO EDGE"))

# Outlier & Lottery Scanner Tagging
def get_1std_category(row):
    try:
        dk_val = str(row["DraftKings"])
        if is_long_shot(dk_val):
            return "🎯 LOTTERY TICKET (+1000+)"
        
        dk_clean = float(dk_val.replace("+", "").strip())
        fd_clean = float(str(row["FanDuel"]).replace("+", "").strip())
        if abs(dk_clean - fd_clean) >= 75:
            return "⚡ 1ST TD BOOK DISCREPANCY"
        elif row["EV_Edge_Num"] >= 4.0:
            return "🔥 ELITE 1ST TD MODEL EDGE"
    except:
        pass
    return "Standard Board"

df["1st TD Market Tag"] = df.apply(get_1std_category, axis=1)

# Formatted columns for presentation
df["Sim 1st TD %"] = df["Base 1st TD Sim %"].apply(lambda x: f"{x:.1f}%")
df["EV Edge %"] = df["EV_Edge_Num"].apply(lambda x: f"{'+' if x > 0 else ''}{x:.1f}%")

# -------------------------------------------------------------
# 4. STREAMLIT FRONTEND CONTROLS & DISPLAY
# -------------------------------------------------------------
st.sidebar.header("1st TD Strategy Filters")

scratched_players = st.sidebar.multiselect("🚫 Scratch/Remove Players", options=df["Player"].unique(), default=["Breece Hall"])
pos_filter = st.sidebar.multiselect("Position", ["ALL", "RB", "WR", "TE", "QB"], default="ALL")

# Focused Toggles for First TD & Lottery Hunting
lottery_mode = st.sidebar.checkbox("🎯 Show Long Shot Lottery Tickets (+1000 or Higher Only)", value=False)
elite_edge_mode = st.sidebar.checkbox("🔥 Show Elite Model Edges Only", value=False)
weather_alert_only = st.sidebar.checkbox("Show Weather Impact Games Only", value=False)

filtered_df = df[~df["Player"].isin(scratched_players)].copy()

if "ALL" not in pos_filter and len(pos_filter) > 0:
    filtered_df = filtered_df[filtered_df["Pos"].isin(pos_filter)]

if lottery_mode:
    filtered_df = filtered_df[filtered_df["1st TD Market Tag"] == "🎯 LOTTERY TICKET (+1000+)"]

if elite_edge_mode:
    filtered_df = filtered_df[filtered_df["1st TD Market Tag"].isin(["🔥 ELITE 1ST TD MODEL EDGE", "⚡ 1ST TD BOOK DISCREPANCY"])]

if weather_alert_only:
    filtered_df = filtered_df[filtered_df["Live Weather"].str.contains("💨|❄️", na=False)]

top_edge_val = filtered_df["EV_Edge_Num"].max() if not filtered_df.empty else 0.0

# Metrics Header
c1, c2, c3, c4 = st.columns(4)
c1.metric("1st TD Slate Count", len(filtered_df))
c2.metric("Top 1st TD Edge", f"+{top_edge_val:.1f}%" if top_edge_val > 0 else f"{top_edge_val:.1f}%")
c3.metric("Focus Mode", "1st Team Touchdown" if not lottery_mode else "Lottery Tickets (+1000+)")
c4.metric("Injury Scratchpad", f"{len(scratched_players)} Scratched" if scratched_players else "🟢 Clean Board")

# Main Board Display
st.subheader("First Touchdown (1st TD) Script & Value Board")
display_cols = [
    "Player", "Team", "Pos", "DraftKings", "FanDuel", 
    "Sim 1st TD %", "EV Edge %", "Value Signal", "1st TD Market Tag",
    "Status", "Opponent", "Live Weather", "Implied Score", 
    "Opening Script Target Rate", "1st Drive RedZone %"
]
st.dataframe(filtered_df[display_cols], use_container_width=True, hide_index=True)
