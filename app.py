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
    </style>
    """, unsafe_allow_html=True)

def load_duty(selected_date):
    filename = f"data/duty_{selected_date.year}_{selected_date.month:02d}.csv"
    if not os.path.exists(filename): return None
    with open(filename, "r", encoding="utf-8") as f:
        return [line.strip().split(",") for line in f]

st.title("📅 ER 근무 조회")
# 1. 모바일 가로 유지 및 간격 최적화 CSS
st.markdown("""
    <style>
    /* 버튼들이 들어가는 한 줄(Row)의 간격을 아주 좁게 설정 */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 5px !important; /* 여기 숫자를 줄이면 더 붙습니다 (기존은 보통 16px) */
    }
    
    /* 각 컬럼의 불필요한 여백 제거 */
    [data-testid="column"] {
        flex: 1 !important;
        min-width: 0px !important;
        padding: 0px !important;
    }

    /* 버튼 디자인: 테두리를 없애고 배경색을 살짝 진하게 */
    div.stButton > button {
        width: 100%;
        padding: 8px 0px;
        font-size: 14px !important;
        background-color: #f8f9fa;
        border: 1px solid #eee;
        border-radius: 6px;
        margin: 0px !important;
    }
    
    /* 날짜 입력창 위쪽 여백 줄이기 */
    .stDateInput {
        margin-top: -15px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 날짜 세션 상태 (새로고침 시 오늘로 리셋)
if 'temp_date' not in st.session_state:
    st.session_state.temp_date = datetime.date.today()

# 3. 버튼 배치 (st.button 사용으로 매끄러운 전환)
cols = st.columns(3)
with cols[0]:
    if st.button("⬅️ 전날"):
        st.session_state.temp_date -= datetime.timedelta(days=1)
        st.rerun()
with cols[1]:
    if st.button("오늘"):
        st.session_state.temp_date = datetime.date.today()
        st.rerun()
with cols[2]:
    if st.button("담날 ➡️"):
        st.session_state.temp_date += datetime.timedelta(days=1)
        st.rerun()

# 4. 날짜 입력창 연동
selected_date = st.date_input("날짜 선택", st.session_state.temp_date)
st.session_state.temp_date = selected_date

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
