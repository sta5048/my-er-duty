import streamlit as st
import datetime
import os

st.set_page_config(page_title="을지 응급실 근무", layout="wide")

# CSS: 버튼과 근무 카드를 모두 가로로 강제 배치
st.markdown("""
    <style>
    /* 공통 컨테이너: 가로 정렬 강제 */
    .flex-container { 
        display: flex; 
        gap: 8px; 
        width: 100%; 
        margin-bottom: 10px;
    }
    /* 버튼과 박스가 동일한 비율로 가로를 채우도록 설정 */
    .flex-item { 
        flex: 1; 
        min-width: 0; 
    }
    
    .team-box { border: 1px solid #ddd; padding: 10px; border-radius: 5px; }
    .duty-title { font-size: 1.1rem; font-weight: bold; margin-bottom: 5px; }
    .name-text { font-size: 0.9rem; margin-bottom: 2px; }
    .D { color: #28a745; } .E { color: #fd7e14; } .N { color: #dc3545; }
    
    /* Streamlit 기본 버튼 스타일 덮어쓰기 (모바일 줄바꿈 방지) */
    div[data-testid="column"] {
        flex: 1 !important;
        min-width: 0px !important;
    }
    div.stButton > button {
        width: 100%;
        padding: 10px 0;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

def load_duty(selected_date):
    filename = f"data/duty_{selected_date.year}_{selected_date.month:02d}.csv"
    if not os.path.exists(filename): return None
    with open(filename, "r", encoding="utf-8") as f:
        return [line.strip().split(",") for line in f if line.strip()]

st.title("📅 ER 근무 조회")

# --- 날짜 제어 로직 ---
if 'target_date' not in st.session_state:
    st.session_state.target_date = datetime.date.today()

# 버튼 3개를 강제로 한 줄에 배치
btn_col1, btn_col2, btn_col3 = st.columns(3)
with btn_col1:
    if st.button("⬅️ 전날"):
        st.session_state.target_date -= datetime.timedelta(days=1)
        st.rerun()
with btn_col2:
    if st.button("오늘 📍"):
        st.session_state.target_date = datetime.date.today()
        st.rerun()
with btn_col3:
    if st.button("담날 ➡️"):
        st.session_state.target_date += datetime.timedelta(days=1)
        st.rerun()

# 날짜 선택기
selected_date = st.date_input("날짜 선택", st.session_state.target_date)
st.session_state.target_date = selected_date

day = selected_date.day
duty_list = load_duty(selected_date)

if duty_list:
    teams = {
        "비외상": {"D": [], "E": [], "N": [], "S": [], "hmj": None},
        "외상": {"D": [], "E": [], "N": [], "S": [], "hmj": None}
    }

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

    left_html = ""
    right_html = ""

    for team_label in ["비외상", "외상"]:
        t = teams[team_label]
        content = f"<div class='team-box'><h4>🏥 {team_label}</h4>"
        for shift, label in [("D", "Day"), ("E", "Eve"), ("N", "Night")]:
            content += f"<p class='duty-title {shift}'>{label}</p>"
            if shift == "D":
                if t["S"]: content += "".join([f"<p class='name-text'>🚩<b>S:{s}</b></p>" for s in t["S"]])
                if t["hmj"]: content += f"<p class='name-text'>✨<b>홍민정:{t['hmj']}</b></p>"
            names = t[shift]
            content += "".join([f"<p class='name-text'>{i+1}. {n}</p>" for i, n in enumerate(names)])
        content += "</div>"
        
        if team_label == "비외상": left_html = content
        else: right_html = content

    # 최종 결과: 근무표도 flex-container를 사용하여 배치
    st.markdown(f"""
        <div class="flex-container">
            <div class="flex-item">{left_html}</div>
            <div class="flex-item">{right_html}</div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.error(f"⚠️ {selected_date.year}년 {selected_date.month}월 데이터 파일이 없습니다.")
