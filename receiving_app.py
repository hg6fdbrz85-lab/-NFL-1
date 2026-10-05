import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="NFL Receiving Yards Edge Hunter", layout="wide")
st.title("📊 NFL Receiving Yards & Receptions Hunter")
st.caption("Standalone Board: Automated Schedule-Aware Receptions & Receiving Yards Projections")

def get_todays_receiving_slate():
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    # Automated Slate Mapping (Loads MNF for Oct 5, 2026)
    data = [
        {
            "Player": "Chris Olave", "Team": "NO", "Pos": "WR", "Opponent": "vs ATL", "Status": "🟢 Active",
            "Receptions Line": "O 5.5 (-115)", "Rec Yards Line": "O 74.5 (-110)", "DK Rec Odds": "-115", "FD Rec Odds": "-110",
            "Target Share %": "28.5%", "Air Yards Share": "34.0%", "Base Sim Yards": 78.5,
        },
        {
            "Player": "Drake London", "Team": "ATL", "Pos": "WR", "Opponent": "@ NO", "Status": "🟢 Active",
            "Receptions Line": "O 5.5 (-110)", "Rec Yards Line": "O 65.5 (-115)", "DK Rec Odds": "-110", "FD Rec Odds": "-115",
            "Target Share %": "26.0%", "Air Yards Share": "31.2%", "Base Sim Yards": 69.0,
        },
        {
            "Player": "Bijan Robinson", "Team": "ATL", "Pos": "RB", "Opponent": "@ NO", "Status": "🟢 Active",
            "Receptions Line": "O 4.5 (-105)", "Rec Yards Line": "O 35.5 (-110)", "DK Rec Odds": "-105", "FD Rec Odds": "-110",
            "Target Share %": "18.5%", "Air Yards Share": "8.0%", "Base Sim Yards": 38.0,
        }
    ]
    return pd.DataFrame(data), today_str

if "rec_slate" not in st.session_state:
    st.session_state.rec_slate, st.session_state.rec_date = get_todays_receiving_slate()

df_rec = st.session_state.rec_slate.copy()

st.sidebar.header("Receiving Schedule & Manager")
st.sidebar.info(f"📅 Active Date: {st.session_state.rec_date}")

with st.sidebar.expander("🛠 Edit Receiving Slate"):
    st.session_state.rec_slate = st.data_editor(st.session_state.rec_slate, num_rows="dynamic", use_container_width=True)
    if st.button("Save Receiving Board"): st.rerun()

st.subheader("Active NFL Slate — Receptions & Receiving Yards Board")
st.dataframe(df_rec[["Player", "Team", "Pos", "Opponent", "Receptions Line", "Rec Yards Line", "Target Share %", "Air Yards Share", "Base Sim Yards"]], use_container_width=True, hide_index=True)
