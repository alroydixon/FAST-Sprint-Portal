import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from google.oauth2.service_account import Credentials
import gspread

# 1. Page Configuration & Aesthetic Setup
st.set_page_config(page_title="S-ACE Cloud Performance Portal", layout="wide", page_icon="🏃‍♂️")

# 2. Complete Roster Database Registry (Row-Level Security Authentication Matrix)
USER_DB = {
    "coaching_staff": {"pass": "sace_elite_2027", "role": "coach", "name": "Head Coach", "gender": "N/A", "current_age": 99},
    # Grade 12
    "hayden.c": {"pass": "cornelius1269", "role": "athlete", "name": "Hayden Cornelius", "gender": "girl", "current_age": 18, "grade": 12},
    "chanlynne.b": {"pass": "brown1241", "role": "athlete", "name": "Chanlynne Brown", "gender": "girl", "current_age": 18, "grade": 12},
    "ashrin.f": {"pass": "flink1176", "role": "athlete", "name": "Ashrin Flink", "gender": "boy", "current_age": 18, "grade": 12},
    # Grade 11
    "clayton.vw": {"pass": "vanwyk1062", "role": "athlete", "name": "Clayton van Wyk", "gender": "boy", "current_age": 18, "grade": 11},
    "charne.k": {"pass": "kayser1198", "role": "athlete", "name": "Charne Kayser", "gender": "girl", "current_age": 17, "grade": 11},
    "mitchell.m": {"pass": "maarman2115", "role": "athlete", "name": "Mitchell Maarman", "gender": "boy", "current_age": 17, "grade": 11},
    "lezario.m": {"pass": "meyer1057", "role": "athlete", "name": "Lezario Meyer", "gender": "boy", "current_age": 17, "grade": 11},
    "sharon.s": {"pass": "september1261", "role": "athlete", "name": "Sharon September", "gender": "girl", "current_age": 17, "grade": 11},
    "kim.c": {"pass": "cloete1300", "role": "athlete", "name": "Kim Cloete", "gender": "girl", "current_age": 17, "grade": 11},
    "alicia.f": {"pass": "festus1224", "role": "athlete", "name": "Alicia Festus", "gender": "girl", "current_age": 18, "grade": 11},
    # Grade 10
    "melissa.m": {"pass": "mahone1264", "role": "athlete", "name": "Melissa Mahone", "gender": "girl", "current_age": 16, "grade": 10},
    "shinique.s": {"pass": "samuels2639", "role": "athlete", "name": "Shinique Samuels", "gender": "girl", "current_age": 16, "grade": 10},
    "cairo.dk": {"pass": "deklerk1075", "role": "athlete", "name": "Cairo de Klerk", "gender": "boy", "current_age": 16, "grade": 10},
    "lienke.vh": {"pass": "vanhelsdingen1369", "role": "athlete", "name": "Lienke Van Helsdingen", "gender": "girl", "current_age": 16, "grade": 10},
    "jayden.dt": {"pass": "dutoit1080", "role": "athlete", "name": "Jayden Du Toit", "gender": "boy", "current_age": 16, "grade": 10},
    "kevin.l": {"pass": "loumouamou1139", "role": "athlete", "name": "Kevin Loumouamou", "gender": "boy", "current_age": 15, "grade": 10},
    "elmira.d": {"pass": "doissen1215", "role": "athlete", "name": "Elmira Doissen", "gender": "girl", "current_age": 16, "grade": 10},
    "bea.dv": {"pass": "devilliers2738", "role": "athlete", "name": "Bea De Villiers", "gender": "girl", "current_age": 16, "grade": 10},
    # Grade 9
    "tyler.vn": {"pass": "vanneel1189", "role": "athlete", "name": "Tyler van Neel", "gender": "boy", "current_age": 15, "grade": 9},
    "local.lp": {"pass": "poole1118", "role": "athlete", "name": "Liam Poole", "gender": "boy", "current_age": 15, "grade": 9},
    "tamzin.a": {"pass": "amos2801", "role": "athlete", "name": "Tamzin Amos", "gender": "boy", "current_age": 15, "grade": 9},
    "raisha.j": {"pass": "joubert1322", "role": "athlete", "name": "Raisha Joubert", "gender": "girl", "current_age": 15, "grade": 9},
    "shassa.lo": {"pass": "owies1213", "role": "athlete", "name": "Shassa Lee Owies", "gender": "girl", "current_age": 15, "grade": 9},
    "amber.n": {"pass": "nel1251", "role": "athlete", "name": "Amber Nel", "gender": "girl", "current_age": 15, "grade": 9},
    "faith.b": {"pass": "barbery3053", "role": "athlete", "name": "Faith Barbery", "gender": "girl", "current_age": 15, "grade": 9},
    "tarryn.s": {"pass": "simonse1304", "role": "athlete", "name": "Tarryn Simonse", "gender": "girl", "current_age": 16, "grade": 9},
    # Grade 8
    "jenique.p": {"pass": "prins1342", "role": "athlete", "name": "Jenique Prins", "gender": "girl", "current_age": 14, "grade": 8},
    "damilleo.a": {"pass": "andoones1114", "role": "athlete", "name": "Damilleo Andoones", "gender": "boy", "current_age": 14, "grade": 8}
}

# 3. Secure Google API Integration Handshake
def get_gspread_client():
    try:
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
        return gspread.authorize(creds)
    except Exception:
        return None

WELLNESS_SPREADSHEET_ID = "1P-h0UJgYITHJjgNybBnNopopeA51zDYIUdmPfyZuA8o"

def write_rpe_to_google_sheets(username, name, duration, rpe_value, load, notes):
    gc = get_gspread_client()
    if gc is None:
        return False, "API Authentication Keys not configured in Cloud Secrets Vault yet."
    try:
        sheet = gc.open_by_key(WELLNESS_SPREADSHEET_ID).worksheet("Session_RPE_Logs")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([timestamp, username, name, duration, rpe_value, load, notes])
        return True, "Success"
    except Exception as e:
        return False, str(e)

# 4. APE Engine Calculations
def calculate_ape_points(mark, gender, current_age, season_year, event_type):
    if pd.isna(mark) or mark <= 0: return 0
    years_back = 2026 - season_year
    historical_age = current_age - years_back
    scale_tier = "U20" if historical_age >= 18 else ("U18" if historical_age >= 16 else "U16")
    
    if event_type == "Long Jump":
        # Metric calculation for long jump distances where further is higher scoring
        if gender == "boy":
            pts = ((mark - 4.0) * 150) + 400
        else:
            pts = ((mark - 3.5) * 160) + 450
    elif "Hurdles" in event_type:
        # Hurdle formulas based on time values
        if gender == "boy":
            pts = 1000 - ((mark - 13.80) * 140) if mark > 13.80 else 1000
        else:
            pts = 1000 - ((mark - 14.00) * 135) if mark > 14.00 else 1000
    else: # Default Sprints (100M/200M standard formulas)
        if gender == "boy":
            if scale_tier == "U20": pts = 1000 - ((mark - 10.50) * 150) if mark > 10.50 else 1000
            elif scale_tier == "U18": pts = 1000 - ((mark - 10.45) * 160) if mark > 10.45 else 1000
            else: pts = 1000 - ((mark - 10.80) * 170) if mark > 10.80 else 1000
        else:
            if scale_tier == "U20": pts = 1000 - ((mark - 11.50) * 130) if mark > 11.50 else 1000
            elif scale_tier == "U18": pts = 1000 - ((mark - 11.40) * 140) if mark > 11.40 else 1000
            else: pts = 1000 - ((mark - 11.70) * 150) if mark > 11.70 else 1000
            
    return int(min(max(pts, 0), 1000))

# 5. Authentication Session Management
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

    # 🟢 COACH VIEW
    if st.session_state["role"] == "coach":
        st.title("🏆 Master Coaching Strategy Dashboard")
        
        # Live Feed Monitoring Block
        st.subheader("📋 Recent Team Session RPE Logs & ACWR Analytics")
        gc = get_gspread_client()
        rpe_df = pd.DataFrame()
        
        if gc is not None:
            try:
                sheet_data = gc.open_by_key(WELLNESS_SPREADSHEET_ID).worksheet("Session_RPE_Logs").get_all_records()
                if sheet_data:
                    rpe_df = pd.DataFrame(sheet_data)
                    st.dataframe(rpe_df, use_container_width=True)
            except Exception as e:
                st.error(f"Could not read logs tab: {str(e)}")
        else:
            st.warning("Google Connection not active. Displaying local simulated data models.")
            # Build mock dataset to compute realistic ACWR tracking graphs offline
            dates = [datetime.now() - timedelta(days=i) for i in range(30)]
            rpe_df = pd.DataFrame({
                "Timestamp": [d.strftime("%Y-%m-%d %H:%M:%S") for d in dates],
                "Athlete Name": ["Clayton van Wyk"] * 30,
                "Training_Load_AU": np.random.randint(200, 700, size=30)
            })
            
        if not rpe_df.empty and "Training_Load_AU" in rpe_df.columns:
            st.markdown("---")
            st.subheader("📈 Acute-to-Chronic Workload Ratio (ACWR) Monitor")
            
            # Group and isolate metrics chronologically
            rpe_df["Timestamp"] = pd.to_datetime(rpe_df["Timestamp"])
            rpe_df = rpe_df.sort_values("Timestamp")
            
            # Calculate metrics
            acute_load = rpe_df["Training_Load_AU"].rolling(window=7, min_periods=1).mean()
            chronic_load = rpe_df["Training_Load_AU"].rolling(window=28, min_periods=1).mean()
            acwr = acute_load / chronic_load
            
            fig, ax = plt.subplots(figsize=(10, 3.5))
            ax.plot(rpe_df["Timestamp"], acwr, label="Current ACWR Trend", color="purple", linewidth=2)
            ax.axhline(1.5, color="red", linestyle="--", label="High Risk Boundary (1.5)")
            ax.axhline(1.0, color="green", linestyle=":", label="Optimal Balance (1.0)")
            ax.set_ylabel("Workload Ratio")
            ax.legend(loc="upper left")
            ax.grid(True, linestyle=":", alpha=0.6)
            st.pyplot(fig)
            
            latest_acwr = acwr.iloc[-1]
            if latest_acwr >= 1.5:
                st.error(f"🚨 ALERT: Team Load Spikes Detected! Current ACWR stands at {latest_acwr:.2f}. High risk of soft-tissue or fatigue-induced strain injuries.")
            else:
                st.success(f"✅ Baseline Balanced: Current squad workload acceleration index is safe at {latest_acwr:.2f}.")

        roster_list = [{"User ID": uid, "Athlete Name": det["name"], "Gender": det["gender"].capitalize(), "Current Age": det["current_age"], "Grade": det["grade"]} for uid, det in USER_DB.items() if det["role"] == "athlete"]
        st.subheader("S-ACE Track Program Roster")
        st.dataframe(pd.DataFrame(roster_list), use_container_width=True)

    # 🔴 SECURED ATHLETE PORTAL VIEW WITH EVENT FILTERS
    else:
        st.title(f"🏃‍♂️ Performance & Wellness Hub: {st.session_state['name']}")
        
        # Interactive Event Filter
        selected_event = st.selectbox("Select Competitive Discipline Track to Display:", ["100M Sprint", "200M Sprint", "Hurdles", "Long Jump"])
        
        c1, c2 = st.columns(2)
        with c1:
            st.subheader(f"Progression Trend: {selected_event}")
            years = [2023, 2024, 2025, 2026]
            
            # Dynamically adjust mock numbers matching chosen filter
            if selected_event == "100M Sprint":
                mock_marks = [12.20, 11.90, 11.40, 11.10] if user_info["gender"] == "boy" else [13.40, 13.10, 12.80, 12.50]
                unit = "s"
            elif selected_event == "200M Sprint":
                mock_marks = [25.10, 24.20, 23.10, 22.40] if user_info["gender"] == "boy" else [27.80, 26.50, 25.90, 25.40]
                unit = "s"
            elif selected_event == "Hurdles":
                mock_marks = [15.20, 14.80, 14.50, 14.13] if user_info["gender"] == "boy" else [15.11, 14.80, 14.63, 14.10]
                unit = "s"
            else: # Long Jump
                mock_marks = [5.10, 5.40, 5.65, 5.98] if user_info["gender"] == "boy" else [4.10, 4.30, 4.45, 4.51]
                unit = "m"
                
            pts_history = [calculate_ape_points(m, user_info["gender"], user_info["current_age"], y, selected_event) for y, m in zip(years, mock_marks)]
            
            df_personal = pd.DataFrame({
                "Season": years,
                "Performance Mark": [f"{m}{unit}" for m in mock_marks],
                "Capped APE Score": pts_history
            })
            st.table(df_personal)
            
            # Render individual line trend graphs
            fig, ax = plt.subplots(figsize=(6, 3))
            ax.plot(years, pts_history, marker='o', linewidth=2.5, color="#1f77b4")
            ax.axhline(1000, color="red", linestyle="--", alpha=0.7)
            ax.set_title(f"{selected_event} Point Curve History")
            ax.set_ylim(400, 1050)
            ax.grid(True, linestyle=":", alpha=0.5)
            st.pyplot(fig)

        with c2:
            st.subheader("📝 Post-Workout Session RPE Log")
            with st.form("athlete_rpe_form"):
                duration = st.number_input("Total Training Duration (Minutes)", min_value=1, value=60)
                rpe = st.slider("Session Rate of Perceived Exertion (Borg 1-10 Scale)", 1, 10, 5)
                notes = st.text_area("Biomechanical Feedback (Pain / Knee Fatigue Flags)")
                
                if st.form_submit_button("Submit Practice Metrics"):
                    calculated_au = duration * rpe
                    success, msg = write_rpe_to_google_sheets(st.session_state["username"], st.session_state["name"], duration, rpe, calculated_au, notes)
                    if success:
                        st.success(f"💪 Training Log Saved Directly to Google Sheets! Workload Score: {calculated_au} AU.")
                    else:
                        st.error(f"Sheet Link Interrupted: {msg}")
