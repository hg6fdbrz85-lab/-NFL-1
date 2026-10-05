import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="NFL Touchdown Edge Hunter", layout="wide")
st.title("🏈 NFL Touchdown Prop & 1st TD Hunter")
st.caption("Standalone Board: Automated Schedule-Aware Anytime TD, Multi-TD & Full Statistical Projections (MNF)")

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
    
    # Full dataset with every single original metric and your correct MNF odds
    data = [
        {
            "Player": "Bijan Robinson", "Team": "ATL", "Pos": "RB", "Opponent": "@ NO", "Status": "🟢 Active",
            "Game Total": 47.5, "Spread": "+2.5", "Is Fav": False, "EPA Factor": +1.5,
            "Base Sim Prob": 68.0, "Inside 5 Touches": 6, "Def RZ Rank": "#20 (Mid)",
            "Anytime TD (DK)": "-210", "2+ TDs (DK)": "+380", "1st TD (DK)": "+245"
        },
        {
            "Player": "Drake London", "Team": "ATL", "Pos": "WR", "Opponent": "@ NO", "Status": "🟢 Active",
            "Game Total": 47.5, "Spread": "+2.5", "Is Fav": False, "EPA Factor": +1.0,
            "Base Sim Prob": 45.0, "Inside 5 Touches": 3, "Def RZ Rank": "#18 (Mid)",
            "Anytime TD (DK)": "+115", "2+ TDs (DK)": "+750", "1st TD (DK)": "+800"
        },
        {
            "Player": "Chris Olave", "Team": "NO", "Pos": "WR", "Opponent": "vs ATL", "Status": "🟢 Active",
            "Game Total": 47.5, "Spread": "-2.5", "Is Fav": True, "EPA Factor": +1.2,
            "Base Sim Prob": 44.0, "Inside 5 Touches": 2, "Def RZ Rank": "#22 (Weak)",
            "Anytime TD (DK)": "+125", "2+ TDs (DK)": "+850", "1st TD (DK)": "+900"
        },
        {
            "Player": "Alvin Kamara", "Team": "NO", "Pos": "RB", "Opponent": "vs ATL", "Status": "🟢 Active",
            "Game Total": 47.5, "Spread": "-2.5", "Is Fav": True, "EPA Factor": +1.8,
            "Base Sim Prob": 42.0, "Inside 5 Touches": 5, "Def RZ Rank": "#15 (Mid)",
            "Anytime TD (DK)": "+140", "2+ TDs (DK)": "+800", "1st TD (DK)": "+950"
        }
    ]
    return pd.DataFrame(data), today_str

if "td_slate" not in st.session_state:
    st.session_state.td_slate, st.session_state.td_date = get_todays_td_slate()

# Sidebar Schedule & Full Data Editor
st.sidebar.header("TD Schedule & Manager")
st.sidebar.info(f"📅 Active Date: {st.session_state.td_date}")

with st.sidebar.expander("🛠 Edit Touchdown Slate"):
    st.session_state.td_slate = st.data_editor(st.session_state.td_slate, num_rows="dynamic", use_container_width=True)
    if st.button("Save TD Board"): st.rerun()

# Full Mathematical Pipeline
df = st.session_state.td_slate.copy()
df["Sim Prob"] = df["Base Sim Prob"] + df["EPA Factor"]
df["DK Implied %"] = df["Anytime TD (DK)"].apply(odds_to_implied)
df["EV_Edge_Num"] = df["Sim Prob"] - df["DK Implied %"]
df["Value Signal"] = df["EV_Edge_Num"].apply(lambda x: "🟢 YES" if x > 2.5 else ("🟡 SLIGHT" if x > 0 else "🔴 NO"))

df["Sim Prob %"] = df["Sim Prob"].apply(lambda x: f"{x:.1f}%")
df["EV Edge %"] = df["EV_Edge_Num"].apply(lambda x: f"{'+' if x > 0 else ''}{x:.1f}%")

st.subheader("Monday Night Football — Full Touchdown & Analytics Board")
st.dataframe(
    df[[
        "Player", "Team", "Pos", "Opponent", "Game Total", "Spread", 
        "Anytime TD (DK)", "2+ TDs (DK)", "1st TD (DK)", 
        "Sim Prob %", "EV Edge %", "Value Signal", 
        "Inside 5 Touches", "Def RZ Rank", "EPA Factor"
    ]], 
    use_container_width=True, 
    hide_index=True
)
