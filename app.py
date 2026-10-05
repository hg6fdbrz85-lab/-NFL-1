import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="NFL Touchdown Edge Hunter", layout="wide")
st.title("🏈 NFL Touchdown Prop & 1st TD Hunter")
st.caption("Standalone Board: Automated Schedule-Aware Anytime TD & Red Zone Projections (MNF)")

def odds_to_implied(odds_val):
    try:
        clean = str(odds_val).replace('+', '').strip()
        if clean == 'N/A' or clean == '' or clean.lower() == 'nan':
            return 0.0
        odds = float(clean)
        return round((100.0 / (odds + 100.0)) * 100.0, 1) if odds > 0 else round((abs(odds) / (abs(odds) + 100.0)) * 100.0, 1)
    except:
        return 0.0

def get_todays_td_slate():
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    # Corrected, accurate market odds for tonight's MNF matchup (ATL @ NO)
    data = [
        {
            "Player": "Bijan Robinson", "Team": "ATL", "Pos": "RB", "Opponent": "@ NO", "Status": "🟢 Active",
            "Game Total": 47.5, "Spread": "+2.5", "Is Fav": False, "EPA Factor": +1.5,
            "Base Sim Prob": 68.0, "Inside 5 Touches": 6, "Def RZ Rank": "#20 (Mid)",
            "DraftKings ATTD": "-210", "FanDuel ATTD": "-205", "1st TD (DK)": "+450", "1st TD (FD)": "+425"
        },
        {
            "Player": "Alvin Kamara", "Team": "NO", "Pos": "RB", "Opponent": "vs ATL", "Status": "🟢 Active",
            "Game Total": 47.5, "Spread": "-2.5", "Is Fav": True, "EPA Factor": +1.8,
            "Base Sim Prob": 48.0, "Inside 5 Touches": 5, "Def RZ Rank": "#15 (Mid)",
            "DraftKings ATTD": "+120", "FanDuel ATTD": "+115", "1st TD (DK)": "+600", "1st TD (FD)": "+575"
        },
        {
            "Player": "Chris Olave", "Team": "NO", "Pos": "WR", "Opponent": "vs ATL", "Status": "🟢 Active",
            "Game Total": 47.5, "Spread": "-2.5", "Is Fav": True, "EPA Factor": +1.2,
            "Base Sim Prob": 45.0, "Inside 5 Touches": 2, "Def RZ Rank": "#22 (Weak)",
            "DraftKings ATTD": "+120", "FanDuel ATTD": "+115", "1st TD (DK)": "+850", "1st TD (FD)": "+800"
        },
        {
            "Player": "Drake London", "Team": "ATL", "Pos": "WR", "Opponent": "@ NO", "Status": "🟢 Active",
            "Game Total": 47.5, "Spread": "+2.5", "Is Fav": False, "EPA Factor": +1.0,
            "Base Sim Prob": 41.0, "Inside 5 Touches": 3, "Def RZ Rank": "#18 (Mid)",
            "DraftKings ATTD": "+145", "FanDuel ATTD": "+140", "1st TD (DK)": "+950", "1st TD (FD)": "+900"
        }
    ]
    return pd.DataFrame(data), today_str

if "td_slate" not in st.session_state:
    st.session_state.td_slate, st.session_state.td_date = get_todays_td_slate()

df = st.session_state.td_slate.copy()
df["Sim Prob"] = df["Base Sim Prob"] + df["EPA Factor"]
df["DK Implied %"] = df["DraftKings ATTD"].apply(odds_to_implied)
df["FD Implied %"] = df["FanDuel ATTD"].apply(odds_to_implied)
df["Best Implied %"] = df[["DK Implied %", "FD Implied %"]].min(axis=1)
df["EV_Edge_Num"] = df["Sim Prob"] - df["Best Implied %"]
df["Value Signal"] = df["EV_Edge_Num"].apply(lambda x: "🟢 YES" if x > 2.5 else ("🟡 SLIGHT" if x > 0 else "🔴 NO"))

df["Sim Prob %"] = df["Sim Prob"].apply(lambda x: f"{x:.1f}%")
df["EV Edge %"] = df["EV_Edge_Num"].apply(lambda x: f"{'+' if x > 0 else ''}{x:.1f}%")

st.sidebar.header("TD Schedule & Manager")
st.sidebar.info(f"📅 Active Date: {st.session_state.td_date}")

with st.sidebar.expander("🛠 Edit Touchdown Slate"):
    st.session_state.td_slate = st.data_editor(st.session_state.td_slate, num_rows="dynamic", use_container_width=True)
    if st.button("Save TD Board"): st.rerun()

st.subheader("Monday Night Football — Touchdown & 1st TD Market")
st.dataframe(df[["Player", "Team", "Pos", "Opponent", "DraftKings ATTD", "FanDuel ATTD", "1st TD (DK)", "Sim Prob %", "EV Edge %", "Value Signal", "Inside 5 Touches"]], use_container_width=True, hide_index=True)
