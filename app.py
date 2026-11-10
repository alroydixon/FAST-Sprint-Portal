import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from google.oauth2.service_account import Credentials
import gspread

# 1. Page Configuration & Aesthetic Architecture
st.set_page_config(page_title="S-ACE Cloud Performance Portal", layout="wide", page_icon="🏃‍♂️")

# 2. Complete 28-Athlete Roster Matrix (Row-Level Security Authentication Registry)
USER_DB = {
    "coaching_staff": {"pass": "sace_elite_2027", "role": "coach", "name": "Head Coach", "gender": "boy", "current_age": 99, "grade": "Staff"},
    # Grade 12
    "hayden.c": {"pass": "cornelius1269", "role": "athlete", "name": "Haydan-Reese Cornelius", "gender": "girl", "current_age": 18, "grade": 12},
    "chanlynne.b": {"pass": "brown1241", "role": "athlete", "name": "Chanlynne Brown", "gender": "girl", "current_age": 18, "grade": 12},
    "ashrin.f": {"pass": "flink1176", "role": "athlete", "name": "Ashrin Flink", "gender": "boy", "current_age": 18, "grade": 12},
    # Grade 11
    "clayton.vw": {"pass": "vanwyk1062", "role": "athlete", "name": "Clayton van Wyk", "gender": "boy", "current_age": 18, "grade": 11},
    "charne.k": {"pass": "kayser1198", "role": "athlete", "name": "Charne Kayser", "gender": "girl", "current_age": 17, "grade": 11},
    "mitchell.m": {"pass": "maarman2115", "role": "athlete", "name": "Mitchell Maarman", "gender": "boy", "current_age": 17, "grade": 11},
    "lezario.m": {"pass": "meyer1057", "role": "athlete", "name": "Lezario Meyer", "gender": "boy", "current_age": 17, "grade": 11},
    "sharon.s": {"pass": "september1261", "role": "athlete", "name": "Sharonay September", "gender": "girl", "current_age": 17, "grade": 11},
    "kim.c": {"pass": "cloete1300", "role": "athlete", "name": "Kim Cloete", "gender": "girl", "current_age": 17, "grade": 11},
    "alicia.f": {"pass": "festus1224", "role": "athlete", "name": "Alicia Festus", "gender": "girl", "current_age": 18, "grade": 11},
    # Grade 10
    "melissa.m": {"pass": "mahone1264", "role": "athlete", "name": "Melissa Mhone", "gender": "girl", "current_age": 16, "grade": 10},
    "shinique.s": {"pass": "samuels2639", "role": "athlete", "name": "Shinique Samuels", "gender": "girl", "current_age": 16, "grade": 10},
    "cairo.dk": {"pass": "deklerk1075", "role": "athlete", "name": "Cairo De Klerk", "gender": "boy", "current_age": 16, "grade": 10},
    "lienke.vh": {"pass": "vanhelsdingen1369", "role": "athlete", "name": "Lienke Van Helsdingen", "gender": "girl", "current_age": 16, "grade": 10},
    "jayden.dt": {"pass": "dutoit1080", "role": "athlete", "name": "Jayden Du Toit", "gender": "boy", "current_age": 16, "grade": 10},
    "kevin.l": {"pass": "loumouamou1139", "role": "athlete", "name": "Kevin Loumouamou", "gender": "boy", "current_age": 15, "grade": 10},
    "elmira.d": {"pass": "doissen1215", "role": "athlete", "name": "Elmira Doysen", "gender": "girl", "current_age": 16, "grade": 10},
    "bea.dv": {"pass": "devilliers2738", "role": "athlete", "name": "Bea De Villiers", "gender": "girl", "current_age": 16, "grade": 10},
    # Grade 9
    "tyler.vn": {"pass": "vanneel1189", "role": "athlete", "name": "Tyler Van Neel", "gender": "boy", "current_age": 15, "grade": 9},
    "local.lp": {"pass": "poole1118", "role": "athlete", "name": "Liam Poole", "gender": "boy", "current_age": 15, "grade": 9},
    "tamzin.a": {"pass": "amos2801", "role": "athlete", "name": "Tamzin Amos", "gender": "boy", "current_age": 15, "grade": 9},
    "raisha.j": {"pass": "joubert1322", "role": "athlete", "name": "Raisha Joubert", "gender": "girl", "current_age": 15, "grade": 9},
    "shassa.lo": {"pass": "owies1213", "role": "athlete", "name": "Shassa-Lee Owies", "gender": "girl", "current_age": 15, "grade": 9},
    "amber.n": {"pass": "nel1251", "role": "athlete", "name": "Amber Nel", "gender": "girl", "current_age": 15, "grade": 9},
    "faith.b": {"pass": "barbery3053", "role": "athlete", "name": "Faith Barbery", "gender": "girl", "current_age": 15, "grade": 9},
    "tarryn.s": {"pass": "simonse1304", "role": "athlete", "name": "Tarryn Simonse", "gender": "girl", "current_age": 16, "grade": 9},
    # Grade 8
    "jenique.p": {"pass": "prins1342", "role": "athlete", "name": "Jenique Prins", "gender": "girl", "current_age": 14, "grade": 8},
    "damilleo.a": {"pass": "andoones1114", "role": "athlete", "name": "Damilleo Andoones", "gender": "boy", "current_age": 14, "grade": 8}
}

WELLNESS_SPREADSHEET_ID = "1P-h0UJgYITHJjgNybBnNopopeA51zDYIUdmPfyZuA8o"
RACE_RESULTS_SPREADSHEET_ID = "1HOJfs2qz-oXPC73JZ0YHuiPFxvsyv3ekgOGl3I-TmkI"

def get_gspread_client():
    try:
        scope = ["https://googleapis.com", "https://googleapis.com"]
        creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
        return gspread.authorize(creds)
    except Exception:
        return None

def calculate_ape_points(mark, event, gender, current_age, season_year):
    if pd.isna(mark) or mark <= 0: return 0
    years_back = 2026 - season_year
    historical_age = current_age - years_back
    scale_tier = "U20" if historical_age >= 18 else ("U18" if historical_age >= 16 else "U16")
    
    if "100" in event:
        if gender == "boy": pts = 1000 - ((mark - 10.50) * 150) if mark > 10.50 else 1000
        else: pts = 1000 - ((mark - 11.50) * 130) if mark > 11.50 else 1000
    elif "200" in event:
        if gender == "boy": pts = 1000 - ((mark - 21.20) * 70) if mark > 21.20 else 1000
        else: pts = 1000 - ((mark - 24.00) * 65) if mark > 24.00 else 1000
    elif "400" in event:
        if gender == "boy": pts = 1000 - ((mark - 48.00) * 35) if mark > 48.00 else 1000
        else: pts = 1000 - ((mark - 56.00) * 30) if mark > 56.00 else 1000
    else:
        pts = (mark / 6.50) * 1000 if mark < 6.50 else 1000
        
    return int(min(max(pts, 0), 1000))
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
    st.session_state["role"] = None
    st.session_state["username"] = None

if not st.session_state["authenticated"]:
    st.title("🔒 S-ACE Cloud Performance Portal")
    st.subheader("Row-Level Secured Portal Authorization")
    username = st.text_input("Athlete ID / Coaching Code")
    password = st.text_input("Access Security Password", type="password")
    if st.button("Log In"):
        if username in USER_DB and USER_DB[username]["pass"] == password:
            st.session_state["authenticated"] = True
            st.session_state["role"] = USER_DB[username]["role"]
            st.session_state["username"] = username
            st.session_state["name"] = USER_DB[username]["name"]
            st.rerun()
        else: st.error("Access Denied.")
else:
    user_info = USER_DB[st.session_state["username"]]
    st.sidebar.title(f"User: {st.session_state['name']}")
    st.sidebar.write(f"Access Role: **{st.session_state['role'].upper()}**")
    if st.sidebar.button("Logout"):
        st.session_state["authenticated"] = False
        st.session_state["role"] = None
        st.session_state["username"] = None
        st.rerun()

    if st.session_state["role"] == "coach":
        st.title("📈 Acute-to-Chronic Workload Ratio (ACWR) Monitor")
        fig, ax = plt.subplots(figsize=(10, 2.2))
        dates = [f"2026-10-{i}" for i in range(13, 31)] + [f"2026-11-0{i}" for i in range(1, 10)]
        ratios = [1.0, 1.0, 0.99, 1.0, 0.98, 0.96, 0.98, 0.92, 0.99, 1.01, 1.0, 0.96, 0.97, 1.01, 0.94, 0.89, 0.84, 0.80, 0.78, 0.85, 0.86, 0.79]
        ax.plot(dates[:len(ratios)], ratios, color="purple", marker="o", label="Current ACWR Trend", linewidth=2)
        ax.axhline(1.5, color="red", linestyle="--", label="High Risk Boundary (1.5)")
        ax.axhline(1.0, color="green", linestyle=":", label="Optimal Balance (1.0)")
        ax.set_ylim(0.5, 1.7)
        ax.set_ylabel("Workload Ratio")
        ax.legend(loc="upper left")
        plt.xticks(rotation=15)
        st.pyplot(fig)

        st.subheader("S-ACE Track Program Roster")
        roster_list = [{"User ID": uid, "Athlete Name": det["name"], "Gender": det["gender"].capitalize(), "Current Age": det["current_age"], "Grade": det["grade"]} for uid, det in USER_DB.items() if det["role"] == "athlete"]
        st.dataframe(pd.DataFrame(roster_list), use_container_width=True)

        st.markdown("---")
        st.header("🔍 Individual Athlete Explorer & Deep-Dive Metrics")
        athlete_names_mapping = {det["name"]: uid for uid, det in USER_DB.items() if det["role"] == "athlete"}
        selected_name = st.selectbox("Select an Athlete Profile to Deep-Dive Into:", sorted(list(athlete_names_mapping.keys())))
        
        if selected_name:
            tgt_uid = athlete_names_mapping[selected_name]
            tgt_info = USER_DB[tgt_uid]
            st.subheader(f"📊 Personal Ledger Portfolio: {selected_name}")
            
            # 🛠️ LIVE BACKEND DEBUG DIAGNOSTIC STREAM 
            st.write("### 🎛️ Live Google API Connection Diagnostics")
            gc = get_gspread_client()
            if gc is not None:
                try:
                    sheet = gc.open_by_key(RACE_RESULTS_SPREADSHEET_ID).worksheet("Form Responses 1")
                    raw_grid = sheet.get_all_values()
                    
                    st.info(f"📁 **Total Rows Found in Sheet Tab:** {len(raw_grid)}")
                    if len(raw_grid) > 0:
                        st.write(f"🏷️ **Raw Column Headers Discovered (Row 1):** `{raw_grid[0]}`")
                        
                        # Find indices
                        headers_lower = [str(h).strip().lower() for h in raw_grid[0]]
                        name_idx = headers_lower.index('athlete name') if 'athlete name' in headers_lower else -1
                        date_idx = headers_lower.index('date') if 'date' in headers_lower else -1
                        
                        st.write(f"📍 **Index Placement Coordinates:** `Athlete Name Column: {name_idx}` | `Date Column: {date_idx}`")
                        
                        # Look for matches
                        matches = [r for r in raw_grid[1:] if len(r) > name_idx and str(r[name_idx]).strip().lower() == selected_name.lower().strip()]
                        st.warning(f"🎯 **Filtered Athlete Rows Extracted for {selected_name}:** {len(matches)}")
                        if len(matches) > 0:
                            st.write(f"📝 **Sample Captured Row:** `{matches[0]}`")
                except Exception as e:
                    st.error(f"❌ Diagnostic Pipeline Interrupted: {str(e)}")
            else:
                st.error("❌ Google Service Account authentication key missing in Secrets Panel.")
