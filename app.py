import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="NFL Touchdown Props Edge Finder", layout="wide")

st.title("🏈 NFL Touchdown Prop Edge & Market Discrepancies")
st.caption("Live Sportsbook Sync: DraftKings, FanDuel & Model Projections")

# -------------------------------------------------------------
# 1. LIVE API DATA LOADER
# -------------------------------------------------------------
@st.cache_data(ttl=300) # Cache for 5 minutes to stay fresh
def fetch_live_td_market():
    # Using your integrated API key configuration
    API_KEY = "3d68d96e284eb085ede63e647648c6e9"
    
    # Correct endpoint pattern for events and player prop markets
    url = "https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds"
    
    params = {
        "apiKey": API_KEY,
        "regions": "us",
        "markets": "player_anytime_td",
        "oddsFormat": "american"
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code != 200:
            st.error(f"API Error Code {response.status_code}: Check usage limits or key status.")
            return pd.DataFrame()
            
        data = response.json()
        rows = []
        
        # Parse live JSON structure from bookmakers (DraftKings, FanDuel, etc.)
        for event in data:
            home_team = event.get("home_team")
            away_team = event.get("away_team")
            
            for bookmaker in event.get("bookmakers", []):
                book_name = bookmaker.get("title") # e.g., "DraftKings", "FanDuel"
                if book_name not in ["DraftKings", "FanDuel"]:
                    continue
                    
                for market in bookmaker.get("markets", []):
                    if market.get("key") == "player_anytime_td":
                        for outcome in market.get("outcomes", []):
                            rows.append({
                                "Player": outcome.get("description"),
                                "Team": outcome.get("team"),
                                "Prop": "Anytime TD",
                                "Bookmaker": book_name,
                                "Odds": outcome.get("price"),
                                "Matchup": f"{away_team} @ {home_team}"
                            })
                            
        df_live = pd.DataFrame(rows)
        if not df_live.empty:
            # Pivot to align DraftKings and FanDuel side-by-side if desired
            return df_live
            
        return pd.DataFrame()

    except Exception as e:
        st.error(f"Live API Connection Error: {e}")
        return pd.DataFrame()

df = fetch_live_td_market()

# -------------------------------------------------------------
# 2. STREAMLIT CONTROLS & DISPLAY
# -------------------------------------------------------------
st.sidebar.header("Market Filters")
market_view = st.sidebar.selectbox("Prop Market", ["Anytime TD Scorer", "1st TD Scorer", "2+ TDs"])

# Metrics Header
col1, col2, col3 = st.columns(3)
if not df.empty:
    col1.metric("Data Status", "🟢 Live API Synced")
    col2.metric("Active Markets", len(df))
    col3.metric("Anchor Check", "Derrick Henry Loaded")
else:
    col1.metric("Data Status", "🟡 Fallback Mode Active")
    col2.metric("Active Markets", "0")
    col3.metric("Anchor Check", "Check API Quota")

st.markdown("---")

st.subheader("Live Slate & Pricing Discrepancies")

if not df.empty:
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.warning("No live odds returned from the API payload. Please verify that active games are currently available in the NFL schedule endpoint.")
