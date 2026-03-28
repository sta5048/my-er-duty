import streamlit as st
import datetime
import os

st.set_page_config(page_title="을지 응급실 근무", layout="wide")

# CSS: 모바일에서도 가로 배치를 절대적으로 유지하도록 설정
st.markdown("""
    <style>
    /* 1. 결과 박스 가로 배치 */
    .main-container { display: flex; gap: 10px; width: 100%; }
    .team-box { flex: 1; min-width: 0; border: 1px solid #ddd; padding: 10px; border-radius: 5px; }
    
    /* 2. [중요] 전날/다음날 버튼 가로 배치 강제 */
    /* Streamlit의 내부 컬럼 구조가 모바일에서 수직으로 변하는 것을 방지 */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 10px !important;
    }
    [data-testid="column"] {
        flex: 1 !important;
        width: 50% !important;
        min-width: 0 !important;
    }

    .duty-title { font-size: 1.1rem; font-weight: bold; margin-bottom: 5px; }
    .name-text { font-size: 0.9rem; margin-bottom: 2px; }
    .D { color: #28a745; } .E { color: #fd7e14; } .N { color: #dc3545; }
    
    /* 버튼 텍스트가 잘리지 않도록 함 */
    .stButton > button {
        width: 100%;
        white-space: nowrap;
    }
    </style>
""", unsafe_allow_html=True)

def load_duty(selected_date):
    filename = f"data/duty_{selected_date.year}_{selected_date.month:02d}.csv"
    if not os.path.exists(filename):
        return None
    with open(filename, "r", encoding="utf-8") as f:
        return [line.strip().split(",") for line in f]

st.title("📅 을지 ER 근무")

# 날짜 초기화 로직
if 'target_date' not in st.session_state:
    st.session_state.target_date = datetime.date.today()

# 전날/다음날 버튼 영역 (CSS가 가로 배치를 강제함)
col1, col2 = st.columns(2)

with col1:
    if st.button("⬅️ 전날", use_container_width=True):
        st.session_state.target_date -= datetime.timedelta(days=1)
        st.rerun()

with col2:
    if st.button("다음날 ➡️", use_container_width=True):
        st.session_state.target_date += datetime.timedelta(days=1)
        st.rerun()

# 날짜 직접 선택
selected_date = st.date_input("날짜 직접 선택", value=st.session_state.target_date)
if selected_date != st.session_state.target_date:
    st.session_state.target_date = selected_date
    st.rerun()

current_date = st.session_state.target_date
day = current_date.day
duty_list = load_duty(current_date)

# 근무표 출력 부분
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
            
            if "홍민정" in clean_name and work != 'OF':
                target["hmj"] = work

    left_html = ""
    right_html = ""

    for team_label, side_html in [("비외상", "left"), ("외상", "right")]:
        t = teams[team_label]
        content = f"<div class='team-box'><h4>🏥 {team_label}</h4>"
        
        content += "<p class='duty-title D'>Day</p>"
        if t["S"]: content += "".join([f"<p class='name-text'>🚩<b>S:{s}</b></p>" for s in t["S"]])
        if t["hmj"]: content += f"<p class='name-text'>✨<b>홍민정:{t['hmj']}</b></p>"
        content += "".join([f"<p class='name-text'>{i+1}. {n}</p>" for i, n in enumerate(t["D"])])
        
        content += "<p class='duty-title E'>Eve</p>"
        content += "".join([f"<p class='name-text'>{i+1}. {n}</p>" for i, n in enumerate(t["E"])])
        
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
    st.warning(f"{current_date.year}년 {current_date.month}월 근무표 데이터가 없습니다.")        content += "".join([f"<p class='name-text'>{i+1}. {n}</p>" for i, n in enumerate(t["D"])])

        # Eve
        content += "<p class='duty-title E'>Eve</p>"
        content += "".join([f"<p class='name-text'>{i+1}. {n}</p>" for i, n in enumerate(t["E"])])

        # Night
        content += "<p class='duty-title N'>Night</p>"
        content += "".join([f"<p class='name-text'>{i+1}. {n}</p>" for i, n in enumerate(t["N"])])

        content += "</div>"

        if side_html == "left":
            left_html = content
        else:
            right_html = content

    # 결과 출력
    st.markdown(f"""
        <div class='main-container'>
            {left_html}
            {right_html}
        </div>
    """, unsafe_allow_html=True)

else:
    st.warning(f"{current_date.year}년 {current_date.month}월 근무표 데이터가 없습니다.")
