import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from google.oauth2.service_account import Credentials
import gspread
import re

st.set_page_config(page_title="S-ACE Cloud Performance Portal", layout="wide", page_icon="🏃‍♂️")

USER_DB = {
    "coaching_staff": {"pass": "sace_elite_2027", "role": "coach", "name": "Head Coach", "gender": "boy", "current_age": 99, "grade": "Staff"},
    "hayden.c": {"pass": "cornelius1269", "role": "athlete", "name": "Haydan-Reese Cornelius", "gender": "girl", "current_age": 18, "grade": 12},
    "chanlynne.b": {"pass": "brown1241", "role": "athlete", "name": "Chanlynne Brown", "gender": "girl", "current_age": 18, "grade": 12},
    "ashrin.f": {"pass": "flink1176", "role": "athlete", "name": "Ashrin Flink", "gender": "boy", "current_age": 18, "grade": 12},
    "clayton.vw": {"pass": "vanwyk1062", "role": "athlete", "name": "Clayton van Wyk", "gender": "boy", "current_age": 18, "grade": 11},
    "charne.k": {"pass": "kayser1198", "role": "athlete", "name": "Charne Kayser", "gender": "girl", "current_age": 17, "grade": 11},
    "mitchell.m": {"pass": "maarman2115", "role": "athlete", "name": "Mitchell Maarman", "gender": "boy", "current_age": 17, "grade": 11},
    "lezario.m": {"pass": "meyer1057", "role": "athlete", "name": "Lezario Meyer", "gender": "boy", "current_age": 17, "grade": 11},
    "sharon.s": {"pass": "september1261", "role": "athlete", "name": "Sharonay September", "gender": "girl", "current_age": 17, "grade": 11},
    "kim.c": {"pass": "cloete1300", "role": "athlete", "name": "Kim Cloete", "gender": "girl", "current_age": 17, "grade": 11},
    "alicia.f": {"pass": "festus1224", "role": "athlete", "name": "Alicia Festus", "gender": "girl", "current_age": 18, "grade": 11},
    "melissa.m": {"pass": "mahone1264", "role": "athlete", "name": "Melissa Mhone", "gender": "girl", "current_age": 16, "grade": 10},
    "shinique.s": {"pass": "samuels2639", "role": "athlete", "name": "Shinique Samuels", "gender": "girl", "current_age": 16, "grade": 10},
    "cairo.dk": {"pass": "deklerk1075", "role": "athlete", "name": "Cairo De Klerk", "gender": "boy", "current_age": 16, "grade": 10},
    "lienke.vh": {"pass": "vanhelsdingen1369", "role": "athlete", "name": "Lienke Van Helsdingen", "gender": "girl", "current_age": 16, "grade": 10},
    "jayden.dt": {"pass": "dutoit1080", "role": "athlete", "name": "Jayden Du Toit", "gender": "boy", "current_age": 16, "grade": 10},
    "kevin.l": {"pass": "loumouamou1139", "role": "athlete", "name": "Kevin Loumouamou", "gender": "boy", "current_age": 15, "grade": 10},
    "elmira.d": {"pass": "doissen1215", "role": "athlete", "name": "Elmira Doysen", "gender": "girl", "current_age": 16, "grade": 10},
    "bea.dv": {"pass": "devilliers2738", "role": "athlete", "name": "Bea De Villiers", "gender": "girl", "current_age": 16, "grade": 10},
    "tyler.vn": {"pass": "vanneel1189", "role": "athlete", "name": "Tyler Van Neel", "gender": "boy", "current_age": 15, "grade": 9},
    "local.lp": {"pass": "poole1118", "role": "athlete", "name": "Liam Poole", "gender": "boy", "current_age": 15, "grade": 9},
    "tamzin.a": {"pass": "amos2801", "role": "athlete", "name": "Tamzin Amos", "gender": "boy", "current_age": 15, "grade": 9},
    "raisha.j": {"pass": "joubert1322", "role": "athlete", "name": "Raisha Joubert", "gender": "girl", "current_age": 15, "grade": 9},
    "shassa.lo": {"pass": "owies1213", "role": "athlete", "name": "Shassa-Lee Owies", "gender": "girl", "current_age": 15, "grade": 9},
    "amber.n": {"pass": "nel1251", "role": "athlete", "name": "Amber Nel", "gender": "girl", "current_age": 15, "grade": 9},
    "faith.b": {"pass": "barbery3053", "role": "athlete", "name": "Faith Barbery", "gender": "girl", "current_age": 15, "grade": 9},
    "tarryn.s": {"pass": "simonse1304", "role": "athlete", "name": "Tarryn Simonse", "gender": "girl", "current_age": 16, "grade": 9},
    "jenique.p": {"pass": "prins1342", "role": "athlete", "name": "Jenique Prins", "gender": "girl", "current_age": 14, "grade": 8},
    "damilleo.a": {"pass": "andoones1114", "role": "athlete", "name": "Damilleo Andoones", "gender": "boy", "current_age": 14, "grade": 8}
}

WELLNESS_SPREADSHEET_ID = "1P-h0UJgYITHJjgNybBnNopopeA51zDYIUdmPfyZuA8o"
RACE_RESULTS_SPREADSHEET_ID = "1HOJfs2qz-oXPC73JZ0YHuiPFxvsyv3ekgOGl3I-TmkI"

def get_gspread_client():
    scope = ["https://googleapis.com", "https://googleapis.com"]
    creds = Credentials.from_service_account_info(dict(st.secrets["gcp_service_account"]), scopes=scope)
    return gspread.authorize(creds)

@st.cache_data(ttl=15)
def get_raw_sheet_grid():
    try:
        gc = get_gspread_client()
        sheet = gc.open_by_key(RACE_RESULTS_SPREADSHEET_ID).worksheet("Form Responses 1")
        return sheet.get_all_values()
    except Exception as e:
        return [["ERROR", str(e)]]

def fetch_athlete_live_track_data(athlete_name, event_type):
    raw_grid = get_raw_sheet_grid()
    if not raw_grid or len(raw_grid) < 2 or raw_grid[0][0] == "ERROR":
        return None

    headers = [str(h).strip().lower() for h in raw_grid[0]]
    data_rows = raw_grid[1:]

    name_idx = next((i for i, h in enumerate(headers) if "athlete" in h or "name" in h), -1)
    date_idx = next((i for i, h in enumerate(headers) if "date" in h or "timestamp" in h), -1)
    if name_idx == -1:
        return None

    target_kw = "100" if "100M" in event_type else ("200" if "200M" in event_type else ("400" if "400M" in event_type else "jump"))
    event_indices = [i for i, h in enumerate(headers) if target_kw in h]
    if not event_indices:
        return None

    parsed_history = []
    clean_search = athlete_name.lower().strip()

    for row in data_rows:
        if len(row) <= name_idx:
            continue
        row_name = str(row[name_idx]).lower().strip()
        if clean_search == row_name or clean_search in row_name:
            year = 2026
            if date_idx != -1 and len(row) > date_idx:
                year_match = re.search(r'20\d{2}', str(row[date_idx]))
                if year_match:
                    year = int(year_match.group())

            for idx in event_indices:
                if len(row) <= idx:
                    continue
                val_str = str(row[idx]).lower().replace('s', '').replace('m', '').replace(',', '.').strip()
                if val_str and val_str not in ["nan", "0", "0.0", "-"]:
                    try:
                        mark = float(val_str)
                        if mark > 0:
                            parsed_history.append({"Year": year, "Mark": mark})
                    except ValueError:
                        continue

    if not parsed_history:
        return None
    res_df = pd.DataFrame(parsed_history)
    if "jump" in target_kw:
        res_df = res_df.groupby("Year", as_index=False).max()
    else:
        res_df = res_df.groupby("Year", as_index=False).min()
    return res_df.sort_values(by="Year")

def calculate_ape_points(mark, event, gender, current_age, season_year):
    if pd.isna(mark) or mark <= 0:
        return 0
    if "100" in event:
        if gender == "boy":
            pts = 1000 - ((mark - 10.50) * 150) if mark > 10.50 else 1000
        else:
            pts = 1000 - ((mark - 11.50) * 130) if mark > 11.50 else 1000
    elif "200" in event:
        if gender == "boy":
            pts = 1000 - ((mark - 21.20) * 70) if mark > 21.20 else 1000
        else:
            pts = 1000 - ((mark - 24.00) * 65) if mark > 24.00 else 1000
    elif "400" in event:
        if gender == "boy":
            pts = 1000 - ((mark - 48.00) * 35) if mark > 48.00 else 1000
        else:
            pts = 1000 - ((mark - 56.00) * 30) if mark > 56.00 else 1000
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
        else:
            st.error("Access Denied.")
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
                    st.info("📅 No marks found for this athlete in the selected event.")

                with st.expander("🛠️ Debug: Inspect Raw Google Sheet Data"):
                    grid = get_raw_sheet_grid()
                    st.write(f"**Total rows read:** {len(grid)}")
                    if grid:
                        st.write("**Row 1 Headers:**", grid[0])
                        if len(grid) > 1:
                            st.write("**Row 2 Sample:**", grid[1])

            with col_b:
                st.write("#### 🏋️ Strategic Gym Deployment Profile")
                if tgt_uid in ["clayton.vw", "mitchell.m", "lezario.m", "ashrin.f"]:
                    st.info("Track Directive Group: **Track A (Progressive Strength Overload)**")
                elif tgt_uid in ["sharon.s", "kevin.l", "tamzin.a"]:
                    st.warning("Track Directive Group: **Track B (Biomechanical Alignment Focus)**")
                else:
                    st.success("Track Directive Group: **Foundational Conditioning**")
                
                st.write("#### 📋 Logged Practice Feed Logs (Live Filtered rows)")
                try:
                    gc = get_gspread_client()
                    sheet_data = gc.open_by_key(WELLNESS_SPREADSHEET_ID).worksheet("Session_RPE_Logs").get_all_records()
                    if sheet_data:
                        full_df = pd.DataFrame(sheet_data)
                        filtered_df = full_df[full_df["Username"] == tgt_uid]
                        if not filtered_df.empty:
                            st.dataframe(filtered_df, use_container_width=True)
                        else:
                            st.caption(f"No workout logs captured for {selected_name} yet.")
                    else:
                        st.caption("No wellness rows logged.")
                except Exception as e:
                    st.caption(f"Wellness log feed status: {str(e)}")
    else:
        st.title(f"🏃‍♂️ Performance & Wellness Hub: {st.session_state['name']}")
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Your Multi-Season Progression Metrics")
            personal_event = st.selectbox("Select Event Log View:", ["100M Sprints", "200M Sprints", "400M Sprints", "Long Jump"])
            live_df = fetch_athlete_live_track_data(st.session_state['name'], personal_event)
            if live_df is not None and not live_df.empty:
                live_df["Capped APE Score"] = live_df.apply(lambda r: calculate_ape_points(r["Mark"], personal_event, user_info["gender"], user_info["current_age"], r["Year"]), axis=1)
                st.table(live_df.rename(columns={"Year": "Competition Season", "Mark": "Logged Season Best"}))
                
                fig2, ax2 = plt.subplots(figsize=(6, 2.5))
                ax2.plot(live_df["Year"].astype(str), live_df["Capped APE Score"], marker="s", color="#ff7f0e", linewidth=2)
                ax2.set_ylim(400, 1050)
                ax2.grid(True, linestyle=":")
                st.pyplot(fig2)
            else:
                st.warning("🔍 No marks found for this event.")

        with c2:
            st.subheader("📝 Post-Workout Practice Matrix Capture Form")
            with st.form("athlete_rpe_form"):
                duration = st.number_input("Total Training Duration Volume (Minutes)", min_value=1, value=60)
                rpe = st.slider("Session Rate of Perceived Exertion Intensity (Borg Scale 1-10)", 1, 10, 5)
                notes = st.text_area("Biomechanical Feedback (Pain Markers / Hip Tension / Joint Fatigue)")
                if st.form_submit_button("Submit Workout Metrics"):
                    calculated_au = duration * rpe
                    try:
                        gc = get_gspread_client()
                        sheet = gc.open_by_key(WELLNESS_SPREADSHEET_ID).worksheet("Session_RPE_Logs")
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        sheet.append_row([timestamp, st.session_state["username"], st.session_state["name"], duration, rpe, calculated_au, notes])
                        st.success(f"💪 Workout Logged Live to Sheets Tab! Workload Score: {calculated_au} AU.")
                    except Exception as e:
                        st.error(f"Sheet Append Interrupted: {str(e)}")
