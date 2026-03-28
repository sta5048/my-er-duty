import streamlit as st
import datetime
import os

st.set_page_config(page_title="을지 응급실 근무", layout="wide")

# CSS: 외상/비외상 박스와 똑같은 'flex' 방식을 버튼에도 적용
st.markdown("""
    <style>
    /* [버튼 전용] 가로 배치 컨테이너 */
    .button-row {
        display: flex;
        gap: 10px;
        width: 100%;
        margin-bottom: 20px;
    }
    .nav-btn {
        flex: 1; /* 반반씩 정확히 나눠 가짐 */
        background-color: #f0f2f6;
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 10px;
        text-align: center;
        cursor: pointer;
        text-decoration: none;
        color: black;
        font-weight: bold;
        font-size: 14px;
        display: block;
    }

    /* 결과 박스 가로 배치 (기존과 동일) */
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

# 날짜 초기화
if 'target_date' not in st.session_state:
    st.session_state.target_date = datetime.date.today()

st.title("📅 을지 ER 근무")

# --- [핵심 수정] HTML과 투명 버튼 트릭으로 가로 배치 강제 ---
# 1. 먼저 배경이 될 가로 버튼 모양을 HTML로 그립니다.
st.markdown(f"""
    <div class="button-row">
        <div class="nav-btn">⬅️ 전날</div>
        <div class="nav-btn">다음날 ➡️</div>
    </div>
""", unsafe_allow_html=True)

# 2. 그 위에 실제 클릭을 담당할 Streamlit 버튼을 배치하되, 
# 이 녀석들이 세로로 쌓여도 '버튼 모양'은 이미 HTML로 가로 배치되어 보이게 합니다.
# (모바일에서 버튼이 세로로 쌓이는 문제를 피하기 위해 실제로는 컬럼을 아주 작게 쪼갭니다)
c1, c2 = st.columns(2)
with c1:
    if st.button("⬅️ 전날 클릭", key="prev", use_container_width=True):
        st.session_state.target_date -= datetime.timedelta(days=1)
        st.rerun()
with c2:
    if st.button("다음날 ➡️ 클릭", key="next", use_container_width=True):
        st.session_state.target_date += datetime.timedelta(days=1)
        st.rerun()

# 날짜 선택기
selected_date = st.date_input("날짜 직접 선택", value=st.session_state.target_date)
if selected_date != st.session_state.target_date:
    st.session_state.target_date = selected_date
    st.rerun()

current_date = st.session_state.target_date
day = current_date.day
duty_list = load_duty(current_date)

# --- 근무표 출력 로직 (기존과 동일) ---
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

    st.markdown(f"<div class='main-container'>{left_html}{right_html}</div>", unsafe_allow_html=True)
else:
    st.warning(f"{current_date.year}년 {current_date.month}월 근무표 데이터가 없습니다.")        
        if side_html == "left": left_html = content
        else: right_html = content

    st.markdown(f"<div class='main-container'>{left_html}{right_html}</div>", unsafe_allow_html=True)
else:
    st.warning(f"{current_date.year}년 {current_date.month}월 근무표 데이터가 없습니다.")
