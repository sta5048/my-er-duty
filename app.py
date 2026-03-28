import streamlit as st
import datetime
import os

st.set_page_config(page_title="을지 응급실 근무", layout="wide")

# CSS: 모바일에서도 절대 줄바꿈 되지 않도록 강제 설정
st.markdown("""
    <style>
    /* 상단 버튼과 하단 근무표 공통 컨테이너 */
    .flex-row {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important; /* 절대 밑으로 안 내려가게 함 */
        gap: 5px;
        width: 100%;
        margin-bottom: 10px;
    }
    .flex-item {
        flex: 1 !important;
        min-width: 0 !important; /* 폭이 좁아져도 유지 */
    }
    .team-box { 
        border: 1px solid #ddd; 
        padding: 8px; 
        border-radius: 5px; 
        background-color: #f9f9f9;
    }
    .duty-title { font-size: 1rem; font-weight: bold; margin-top: 8px; margin-bottom: 2px; }
    .name-text { font-size: 0.85rem; margin-bottom: 1px; }
    .D { color: #28a745; } .E { color: #fd7e14; } .N { color: #dc3545; }
    
    /* 버튼 스타일 가로 고정 */
    div[data-testid="column"] {
        flex: 1 1 0% !important;
        min-width: 0px !important;
    }
    div.stButton > button {
        width: 100%;
        padding: 5px 0px !important;
        font-size: 13px !important;
        white-space: nowrap;
    }
    </style>
    """, unsafe_allow_html=True)

def load_duty(selected_date):
    filename = f"data/duty_{selected_date.year}_{selected_date.month:02d}.csv"
    if not os.path.exists(filename): return None
    with open(filename, "r", encoding="utf-8") as f:
        return [line.strip().split(",") for line in f if line.strip()]

st.title("📅 ER 근무 조회")

if 'target_date' not in st.session_state:
    st.session_state.target_date = datetime.date.today()

# 1. 버튼 영역 (st.columns를 쓰되 CSS로 가로 고정)
btn_col1, btn_col2, btn_col3 = st.columns(3)
with btn_col1:
    if st.button("⬅️ 어제"):
        st.session_state.target_date -= datetime.timedelta(days=1)
        st.rerun()
with btn_col2:
    if st.button("오늘 📍"):
        st.session_state.target_date = datetime.date.today()
        st.rerun()
with btn_col3:
    if st.button("내일 ➡️"):
        st.session_state.target_date += datetime.timedelta(days=1)
        st.rerun()

selected_date = st.date_input("날짜 선택", st.session_state.target_date)
st.session_state.target_date = selected_date

day = selected_date.day
duty_list = load_duty(selected_date)

# --- 데이터 처리 및 화면 출력 ---
if duty_list:
    teams = {"비외상": {"D":[], "E":[], "N":[], "S":[], "hmj":None}, 
             "외상": {"D":[], "E":[], "N":[], "S":[], "hmj":None}}

    for row in duty_list[1:]:
        if len(row) > day:
            raw_name, work = row[0], row[day]
            if not work or work in ['OF', 'OFF', '']: continue
            team_key = "외상" if "*" in raw_name else "비외상"
            clean_name = raw_name.replace("*", "")
            target = teams[team_key]
            if work == 'D': target["D"].append(clean_name)
            elif work == 'E': target["E"].append(clean_name)
            elif work == 'N': target["N"].append(clean_name)
            elif work == 'S': target["S"].append(clean_name)
            elif "홍민정" in clean_name: target["hmj"] = work

    # 2. 근무표 영역 (HTML 컨테이너로 가로 배치 강제)
    left_content = ""
    right_content = ""

    for team_label in ["비외상", "외상"]:
        t = teams[team_label]
        html = f"<div class='team-box'><b>🏥 {team_label}</b>"
        for shift, label in [("D", "Day"), ("E", "Eve"), ("N", "Night")]:
            html += f"<p class='duty-title {shift}'>{label}</p>"
            if shift == "D":
                if t["S"]: html += "".join([f"<p class='name-text'>🚩<b>S:{s}</b></p>" for s in t["S"]])
                if t["hmj"]: html += f"<p class='name-text'>✨<b>홍민정:{t['hmj']}</b></p>"
            html += "".join([f"<p class='name-text'>{i+1}. {n}</p>" for i, n in enumerate(t[shift])])
        html += "</div>"
        
        if team_label == "비외상": left_content = html
        else: right_content = html

    st.markdown(f"""
        <div class="flex-row">
            <div class="flex-item">{left_content}</div>
            <div class="flex-item">{right_content}</div>
        </div>
        """, unsafe_allow_html=True)

else: # if duty_list와 수직 위치를 맞춰야 함
    st.error(f"⚠️ {selected_date.year}년 {selected_date.month}월 데이터가 없습니다.")
