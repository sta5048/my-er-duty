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
    div.stButton > button {
    padding: 12px 0;
    font-weight: bold;
    border-radius: 6px;
    border: 1px solid #ddd;
    background-color: #f0f2f6;
}
div.stButton > button:hover {
    background-color: #e6e9ef;
}
    </style>
    """, unsafe_allow_html=True)


def load_duty(selected_date):
    filename = f"data/duty_{selected_date.year}_{selected_date.month:02d}.csv"
    if not os.path.exists(filename): return None
    with open(filename, "r", encoding="utf-8") as f:
        return [line.strip().split(",") for line in f]

st.title("📅 ER 근무 조회")
# --- st.title 바로 아래부터 데이터 로드 전까지 교체 ---

# 1. 날짜 세션 상태 초기화
if 'temp_date' not in st.session_state:
    st.session_state.temp_date = datetime.date.today()

# 2. 실제 동작용 버튼 (화면에서 완전히 숨김)
# container를 사용해 감싸고 CSS로 해당 영역을 아예 보이지 않게(display:none) 처리
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("⬅️ 전날", use_container_width=True):
        st.session_state.temp_date -= datetime.timedelta(days=1)
        st.rerun()

with col2:
    if st.button("오늘", use_container_width=True):
        st.session_state.temp_date = datetime.date.today()
        st.rerun()

with col3:
    if st.button("담날 ➡️", use_container_width=True):
        st.session_state.temp_date += datetime.timedelta(days=1)
        st.rerun()

# 5. 날짜 선택창
selected_date = st.date_input("날짜 선택", st.session_state.temp_date, label_visibility="collapsed")
st.session_state.temp_date = selected_date

day = selected_date.day
duty_list = load_duty(selected_date)
# --- 이후 코드(if duty_list: ...)는 동일 ---

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

    # HTML을 이용한 좌우 강제 배치
    left_html = ""
    right_html = ""

    for team_label, side_html in [("비외상", "left"), ("외상", "right")]:
        t = teams[team_label]
        content = f"<div class='team-box'><h4>🏥 {team_label}</h4>"
        
        # Day
        content += "<p class='duty-title D'>Day</p>"
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

    # 최종 결과 출력
    st.markdown(f"""
        <div class='main-container'>
            {left_html}
            {right_html}
        </div>
        """, unsafe_allow_html=True)
