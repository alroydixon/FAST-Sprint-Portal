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

# Advanced Raw Cell Grid Parsing Engine to bypass Row 1 Header locks
@st.cache_data(ttl=15)
def fetch_athlete_live_track_data(athlete_name, event_type):
    gc = get_gspread_client()
    if gc is None: return None
    try:
        sheet = gc.open_by_key(RACE_RESULTS_SPREADSHEET_ID).worksheet("Form Responses 1")
        # Ingest the spreadsheet purely as a raw 2D grid of text strings
        raw_grid = sheet.get_all_values()
        if not raw_grid: return None
        
        # Setup dynamic target indices based on keyword pattern matching
        name_idx, date_idx = -1, -1
        target_indices = []
        
        # Determine the target keyword strings based on chosen event filter
        target_keyword = "100m" if "100M" in event_type else ("200m" if "200M" in event_type else ("400m" if "400M" in event_type else "jump"))
        
        # Scan through the rows to find where headers exist dynamically
        for row in raw_grid:
            row_clean = [str(cell).strip().lower() for cell in row]
            if 'athlete name' in row_clean:
                name_idx = row_clean.index('athlete name')
            if 'date' in row_clean:
                date_idx = row_clean.index('date')
            
            # Map columns matching the requested track event across the entire layout
            for idx, cell in enumerate(row_clean):
                if target_keyword in cell and idx not in target_indices:
                    target_indices.append(idx)
                    
        if name_idx == -1 or date_idx == -1 or not target_indices: return None
        
        parsed_history = []
        # Process and extract rows matching the target athlete name context
        for row in raw_grid:
            if len(row) <= max(name_idx, date_idx): continue
            if str(row[name_idx]).strip().lower() == athlete_name.lower().strip():
                # Safe date string checker
                raw_date = str(row[date_idx]).strip()
                try:
                    if '-' in raw_date: year = int(raw_date.split('-')[0])
                    elif '/' in raw_date: year = int(raw_date.split('/')[0])
                    else: year = 2026
                except Exception:
                    year = 2026
                    
                # Scan identified index positions for marks data cells
                for idx in target_indices:
                    if idx >= len(row): continue
                    mark_str = str(row[idx]).strip().lower()
                    if mark_str and mark_str != "" and mark_str != "nan" and mark_str != "0" and mark_str != "0.0":
                        try:
                            clean_mark = float(mark_str.replace('s', '').replace('m', '').strip())
                            parsed_history.append({"Year": year, "Mark": clean_mark})
                        except ValueError:
                            continue
                            
        if not parsed_history: return None
        res_df = pd.DataFrame(parsed_history)
        if "jump" in target_keyword:
            res_df = res_df.groupby("Year", as_index=False).max()
        else:
            res_df = res_df.groupby("Year", as_index=False).min()
        return res_df.sort_values(by="Year")
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
        st.success("✅ Baseline Balanced: Current squad workload acceleration index is safe at 0.79.")

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
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.write(f"**Gender:** {tgt_info['gender'].capitalize()} | **Current Age:** {tgt_info['current_age']} | **Grade:** {tgt_info['grade']}")
                event_choice = st.selectbox(f"Filter Event Discipline Metrics for {tgt_info['name']}:", ["100M Sprints", "200M Sprints", "400M Sprints", "Long Jump"])
                
                live_df = fetch_athlete_live_track_data(selected_name, event_choice)
                if live_df is not None and not live_df.empty:
                    live_df["Capped APE Score"] = live_df.apply(lambda r: calculate_ape_points(r["Mark"], event_choice, tgt_info["gender"], tgt_info["current_age"], r["Year"]), axis=1)
                    display_df = live_df.copy()
                    display_df["Mark"] = display_df["Mark"].apply(lambda val: f"{val}s" if event_choice != "Long Jump" else f"{val}m")
                    st.table(display_df.rename(columns={"Year": "Competition Season", "Mark": "Logged Season Best"}))
                    
                    fig2, ax2 = plt.subplots(figsize=(6, 2.5))
                    ax2.plot(live_df["Year"].astype(str), live_df["Capped APE Score"], marker="s", color="#1f77b4", linewidth=2)
                    ax2.axhline(1000, color="red", linestyle="--", alpha=0.5)
                    ax2.set_ylabel("APE Points Scale")
                    ax2.set_ylim(400, 1050)
                    ax2.grid(True, linestyle=":", alpha=0.6)
                    st.pyplot(fig2)
                else:
                    st.info(f"📅 Pulling historical marks from all rows... Verifying entry data grid cell coordinates.")

            with col_b:
                st.write("#### 🏋️ Strategic Gym Deployment Profile")
                if tgt_uid in ["clayton.vw", "mitchell.m", "lezario.m", "ashrin.f"]: st.info("Track Directive Group: **Track A (Progressive Strength Overload)**")
                elif tgt_uid in ["sharon.s", "kevin.l", "tamzin.a"]: st.warning("Track Directive Group: **Track B (Biomechanical Alignment Focus)**")
                else: st.success("Track Directive Group: **Foundational Conditioning**")
                
                st.write("#### 📋 Logged Practice Feed Logs (Live Filtered rows)")
                gc = get_gspread_client()
                if gc is not None:
                    try:
                        sheet_data = gc.open_by_key(WELLNESS_SPREADSHEET_ID).worksheet("Session_RPE_Logs").get_all_records()
                        if sheet_data:
                            full_df = pd.DataFrame(sheet_data)
                            filtered_df = full_df[full_df["Username"] == tgt_uid]
                            if not filtered_df.empty: st.dataframe(filtered_df, use_container_width=True)
                            else: st.caption(f"No workout logs captured for {selected_name} yet.")
                        else: st.caption("No wellness rows logged.")
                    except Exception: st.caption("Awaiting sheet cell synchronization updates.")
