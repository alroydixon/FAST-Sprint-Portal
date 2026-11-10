import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from google.oauth2.service_account import Credentials
import gspread
import json

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
        # Load raw flat string configuration line directly, parsing as native python JSON dict
        info_dict = json.loads(st.secrets["raw_json_string"])
        scope = ["https://googleapis.com", "https://googleapis.com"]
        creds = Credentials.from_service_account_info(info_dict, scopes=scope)
        return gspread.authorize(creds)
    except Exception:
        return None

# Horizontal Dashboard Pivot Matrix Processing Engine
@st.cache_data(ttl=15)
def fetch_athlete_live_track_data(athlete_name, event_type):
    gc = get_gspread_client()
    if gc is None: return None
    try:
        sheet = gc.open_by_key(RACE_RESULTS_SPREADSHEET_ID).worksheet("Form Responses 1")
        raw_grid = sheet.get_all_values()
        if not raw_grid: return None
        
        target_discipline = "100m sprint" if "100M" in event_type else ("200m sprint" if "200M" in event_type else ("400m sprint" if "400M" in event_type else "long jump"))
        header_row_idx = -1
        for idx, row in enumerate(raw_grid):
            row_joined = " ".join([str(c).lower().strip() for c in row])
            if "trend" in row_joined and target_discipline in row_joined:
                header_row_idx = idx + 1
                break
                
        if header_row_idx == -1 or header_row_idx >= len(raw_grid): return None
        
        headers = [str(h).strip() for h in raw_grid[header_row_idx]]
        data_rows = raw_grid[header_row_idx + 1:]
        
        name_idx = -1
        for i, h in enumerate(headers):
            if "athlete" in h.lower() or "name" in h.lower():
                name_idx = i
                break
                
        if name_idx == -1: return None
        
        parsed_history = []
        clean_search_name = athlete_name.lower().strip()
        
        for row in data_rows:
            if len(row) <= name_idx: continue
            if str(row[name_idx]).lower().strip() == clean_search_name:
                for col_idx, col_name in enumerate(headers):
                    if "week:" in col_name.lower():
                        try:
                            year_prefix = col_name.split(' ')[0].strip()
                            year = 2000 + int(year_prefix)
                        except Exception:
                            year = 2026
                            
                        mark_str = str(row[col_idx]).strip().lower()
                        if mark_str and mark_str != "" and mark_str != "nan" and mark_str != "0":
                            try:
                                clean_mark = float(mark_str.replace('s', '').replace('m', '').strip())
                                parsed_history.append({"Year": year, "Mark": clean_mark})
                            except ValueError:
                                continue
                                
        if not parsed_history: return None
        res_df = pd.DataFrame(parsed_history)
        if "jump" in target_discipline:
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
