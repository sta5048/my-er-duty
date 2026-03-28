import streamlit as st
import datetime
import os

st.set_page_config(page_title="을지 응급실 근무", layout="wide")

# CSS: 모바일에서도 가로 배치를 강제하고 폰트 크기를 살짝 조절함
st.markdown("""
    <style>
    .main-container { display: flex; gap: 10px; width: 100%; }
    .team-box { flex: 1; min-width: 0; border: 1px solid #ddd; padding: 10px; border-radius: 5px; }
    .duty-title { font-size: 1.1rem; font-weight: bold; margin-bottom: 5px; }
    .name-text { font-size: 0.9rem; margin-bottom: 2px; }
    .D { color: #28a745; } .E { color: #fd7e14; } .N { color: #dc3545; }
    /* 버튼 간격 조절 */
    .stButton > button { width: 100%; }
    </style>
    """, unsafe_allow_html=True)

def load_duty(selected_date):
    filename = f"data/duty_{selected_date.year}_{selected_date.month:02d}.csv"
    if not os.path.exists(filename): return None
    with open(filename, "r", encoding="utf-8") as f:
        return [line.strip().split(",") for line in f]

st.title("📅 ER 근무 조회")

# --- 날짜 조절 로직 ---
if 'target_date' not in st.session_state:
    st.session_state.target_date = datetime.date.today()

# 버튼들을 한 줄에 나란히 배치 (3개 컬럼 사용: 버튼, 여백, 버튼)
# [1, 0.2, 1] 비율로 주면 가운데에 살짝 틈이 생깁니다.
col_left, col_mid, col_right = st.columns([1, 0.1, 1])

with col_left:
    if st.button("⬅️ 전날", use_container_width=True):
        st.session_state.target_date -= datetime.timedelta(days=1)
        st.rerun()

with col_right:
    if st.button("다음날 ➡️", use_container_width=True):
        st.session_state.target_date += datetime.timedelta(days=1)
        st.rerun()

# 날짜 선택기 (버튼 아래에 위치)
selected_date = st.date_input("날짜 직접 선택", value=st.session_state.target_date)

if selected_date != st.session_state.target_date:
    st.session_state.target_date = selected_date
    st.rerun()

# 최종 선택된 날짜 정보 사용
current_date = st.session_state.target_date
day = current_date.day
duty_list = load_duty(current_date)
# -------------------------
if duty_list:
    teams = {
        "비외상": {"D": [], "E": [], "N": [], "S": [], "hmj": None},
        "외상": {"D": [], "E": [], "N": [], "S": [], "hmj": None}
    }

    for row in duty_list[1:]:
        if len(row) > day:
            raw_name, work = row[0], row[day]
            team_key = "외상" if "*" in raw_name else "비외상"
            clean_name = raw_name.replace("*", "")
            target = teams[team_key]
            
            if work == 'D': target["D"].append(clean_name)
            elif work == 'E': target["E"].append(clean_name)
            elif work == 'N': target["N"].append(clean_name)
            elif work == 'S': target["S"].append(clean_name)
            elif "홍민정" in clean_name and work != 'OF': target["hmj"] = work

    left_html = ""
    right_html = ""

    for team_label, side_html in [("비외상", "left"), ("외상", "right")]:
        t = teams[team_label]
        content = f"<div class='team-box'><h4>🏥 {team_label}</h4>"
        
        # Day
        content += "<p class='duty-title D'>Day</p>"
        # 문법 오류 수정 지점: f"..." 형태로 따옴표를 정확히 넣었습니다.
        if t["S"]: content += "".join([f"<p class='name-text'>🚩<b>S:{s}</b></p>" for s in t["S"]])
        if t["hmj"]: content += f"<p class='name-text'>✨<b>홍민정:{t['hmj']}</b></p>"
        content += "".join([f"<p class='name-text'>{i+1}. {n}</p>" for i, n in enumerate(t["D"])])
        
        # Eve
        content += "<p class='duty-title E'>Eve</p>"
        content += "".join([f"<p class='name-text'>{i+1}. {n}</p>" for i, n in enumerate(t["E"])])
        
        # Night
        content += "<p class='duty-title N'>Night</p>"
        content += "".join([f"<p class='name-text'>{i+1}. {n}</p>" for i, n in enumerate(t["N"])])
        
        content += "</div>"
        if side_html == "left": left_html = content
        else: right_html = content

    st.markdown(f"""
        <div class='main-container'>
            {left_html}
            {right_html}
        </div>
        """, unsafe_allow_html=True)
else:
    st.warning(f"{current_date.year}년 {current_date.month}월 근무표 데이터가 없습니다.")
