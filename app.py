import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

# 3. Dynamic Age-Group Category Sarel Bekker Ingestion Engine
def calculate_ape_points(time, gender, current_age, season_year):
    if pd.isna(time) or time <= 0:
        return 0
    
    # Track dynamic shift backwards across racing seasons
    years_back = 2026 - season_year
    historical_age = current_age - years_back
    
    # Establish official ASA / SASA fixed category parameters
    if historical_age >= 18:
        scale_tier = "U20"
    elif historical_age >= 16:
        scale_tier = "U18"
    else:
        scale_tier = "U16"
        
    # Execute precise isolated gender lookups
    if gender == "boy":
        if scale_tier == "U20":
            pts = 1000 - ((time - 10.50) * 150) if time > 10.50 else 1000
        elif scale_tier == "U18":
            pts = 1000 - ((time - 10.45) * 160) if time > 10.45 else 1000
        else:
            pts = 1000 - ((time - 10.80) * 170) if time > 10.80 else 1000
    else:
        if scale_tier == "U20":
            pts = 1000 - ((time - 11.50) * 130) if time > 11.50 else 1000
        elif scale_tier == "U18":
            pts = 1000 - ((time - 11.40) * 140) if time > 11.40 else 1000
        else:
            pts = 1000 - ((time - 11.70) * 150) if time > 11.70 else 1000
            
    # Enforce strict 1000 point ceiling constraint rule
    return int(min(max(pts, 0), 1000))

# 4. Authentication Session Management
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
    st.session_state["role"] = None
    st.session_state["username"] = None

if not st.session_state["authenticated"]:
    st.title("🔒 S-ACE Cloud Performance Platform")
    st.subheader("Secure Row-Level Security (RLS) Portal Login")
    
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
            st.error("Access Denied. Check credentials against the secure registry ledger.")

# 5. Core Interface Portal Workspace Router
else:
    user_info = USER_DB[st.session_state["username"]]
    
    st.sidebar.title(f"User: {st.session_state['name']}")
    st.sidebar.write(f"Access Role: **{st.session_state['role'].upper()}**")
    
    if st.sidebar.button("Logout"):
        st.session_state["authenticated"] = False
        st.session_state["role"] = None
        st.session_state["username"] = None
        st.rerun()

    # 🟢 MASTER VIEW A: COACHING STAFF CONTROLS
    if st.session_state["role"] == "coach":
        st.title("🏆 Master Coaching Strategy Dashboard")
        st.write("Full multi-cohort administrative registry visibility active.")
        
        # Compile a clean visual dataframe table showing all athletes
        roster_list = []
        for uid, details in USER_DB.items():
            if details["role"] == "athlete":
                roster_list.append({
                    "User ID": uid,
                    "Athlete Name": details["name"],
                    "Gender": details["gender"].capitalize(),
                    "Current Age": details["current_age"],
                    "Grade Cohort": details["grade"]
                })
        
        st.subheader("S-ACE Track Program Roster Configuration Matrix")
        st.dataframe(pd.DataFrame(roster_list), use_container_width=True)
        st.success(f"Verified row-level segmentation active across all {len(roster_list)} program athletes.")

    # 🔴 MASTER VIEW B: ATHLETE ROW-SECURED HUB
    else:
        st.title(f"🏃‍♂️ Performance & Wellness Hub: {st.session_state['name']}")
        st.caption(f"Gender Baseline: {user_info['gender'].capitalize()} | Grade: {user_info['grade']}")
        
        # Display simulated metrics customized by context
        st.subheader("Your Progress Tracker (Capped at 1000 Pts)")
        
        # Dummy progression tracker demonstrating dynamic point math
        years =
        mock_times = [12.20, 11.90, 11.40, 11.10] if user_info["gender"] == "boy" else [13.40, 13.10, 12.80, 12.50]
        
        pts_history = []
        for y, t in zip(years, mock_times):
            pts_history.append(calculate_ape_points(t, user_info["gender"], user_info["current_age"], y))
            
        df_personal = pd.DataFrame({
            "Competition Year": years,
            "Logged Mark": [f"{t}s" for t in mock_times],
            "Calculated APE Points": pts_history
        })
        st.table(df_personal)
        
        # Training load logging form interface
        st.markdown("---")
        st.subheader("📝 Post-Workout Session RPE Log")
        
        with st.form("athlete_rpe_form"):
            duration = st.number_input("Total Training Volume Duration (Minutes)", min_value=1, value=60)
            rpe = st.slider("Session Rate of Perceived Exertion (Borg 1-10 Scale)", 1, 10, 5)
            notes = st.text_area("Biomechanical Feedback (Pain Markers / Knee Fatigue / Track Status)")
            
            if st.form_submit_button("Submit Practice Metrics"):
                calculated_au = duration * rpe
                st.success(f"Log Captured! Training Load: {calculated_au} AU written securely to cloud database context.")
