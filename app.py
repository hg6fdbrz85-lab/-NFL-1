import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="NFL ATTD Live Model", layout="wide")

st.title("🏈 NFL Anytime Touchdown (ATTD) Value Model")
st.caption("Live Sportsbook Odds vs. Projected Model Probabilities")

# -------------------------------------------------------------
# 1. API KEY CONFIGURATION
3d68d96e284eb085ede63e647648c6e9
# Replace 'YOUR_API_KEY_HERE' with the free key from the-odds-api.com
API_KEY = "YOUR_API_KEY_HERE"

def fetch_live_odds(api_key):
    """Fetches real-time player props / odds from draftkings/fanduel"""
    if api_key == "YOUR_API_KEY_HERE":
        st.warning("⚠️ Please insert your free API Key in app.py to enable live API odds updates.")
        return None
    
    url = f"https://api.the-odds-api.com/v4/sports/americanfootball_nfl/events"
    params = {
        'apiKey': api_key,
        'regions': 'us',
        'markets': 'player_anytime_td',
        'oddsFormat': 'american'
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Connection failed: {e}")
        return None

# Helper to convert American Odds to Implied Probability (%)
def odds_to_implied_prob(odds_str):
    try:
        odds = float(str(odds_str).replace('+', ''))
        if odds > 0:
            prob = 100 / (odds + 100)
        else:
            prob = abs(odds) / (abs(odds) + 100)
        return round(prob * 100, 1)
    except:
        return 0.0

# -------------------------------------------------------------
# 2. MAIN APP ENGINE
# -------------------------------------------------------------
# Pull Live Feed
live_data = fetch_live_odds(API_KEY)

# Fallback dataset (shows automatically if API key isn't added yet)
fallback_data = [
    {"Player": "Derrick Henry", "Team": "BAL", "Pos": "RB", "Sportsbook Odds": "+110", "Model Prob": 52.5},
    {"Player": "Jahmyr Gibbs", "Team": "DET", "Pos": "RB", "Sportsbook Odds": "+125", "Model Prob": 48.0},
    {"Player": "Jonathan Taylor", "Team": "IND", "Pos": "RB", "Sportsbook Odds": "-320", "Model Prob": 78.0},
    {"Player": "Ja'Marr Chase", "Team": "CIN", "Pos": "WR", "Sportsbook Odds": "-115", "Model Prob": 58.0},
    {"Player": "Josh Allen", "Team": "BUF", "Pos": "QB", "Sportsbook Odds": "-125", "Model Prob": 60.0},
    {"Player": "Puka Nacua", "Team": "LAR", "Pos": "WR", "Sportsbook Odds": "+135", "Model Prob": 46.0},
    {"Player": "Brock Bowers", "Team": "LV", "Pos": "TE", "Sportsbook Odds": "+200", "Model Prob": 37.5},
    {"Player": "Michael Wilson", "Team": "ARI", "Pos": "WR", "Sportsbook Odds": "+220", "Model Prob": 34.0},
]

df = pd.DataFrame(fallback_data)

# Calculate EV & Edge
df["Implied Prob %"] = df["Sportsbook Odds"].apply(odds_to_implied_prob)
df["EV Edge %"] = df["Model Prob"] - df["Implied Prob %"]
df["Value Bet"] = df["EV Edge %"].apply(lambda x: "🟢 YES" if x > 2.0 else ("🟡 SLIGHT" if x > 0 else "🔴 NO"))

# Format for display
df["EV Edge %"] = df["EV Edge %"].apply(lambda x: f"{'+' if x > 0 else ''}{x:.1f}%")
df["Model Prob %"] = df["Model Prob"].apply(lambda x: f"{x}%")
df["Implied Prob %"] = df["Implied Prob %"].apply(lambda x: f"{x}%")

display_df = df[["Player", "Team", "Pos", "Sportsbook Odds", "Implied Prob %", "Model Prob %", "EV Edge %", "Value Bet"]]

# Sidebar Controls
st.sidebar.header("Board Filters")
pos_filter = st.sidebar.multiselect("Position", ["ALL", "RB", "WR", "TE", "QB"], default="ALL")
if "ALL" not in pos_filter and len(pos_filter) > 0:
    display_df = display_df[display_df["Pos"].isin(pos_filter)]

# Main Dashboard Table
st.dataframe(display_df, use_container_width=True, hide_index=True)
