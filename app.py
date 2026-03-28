import streamlit as st
import datetime
import os

st.set_page_config(page_title="을지 응급실 근무", layout="wide")

# CSS: 버튼이 화면 밖으로 나가지 않도록 너비를 50%로 고정하고 여백을 축소
st.markdown("""
    <style>
    /* 1. 버튼 영역 가로 배치 강제 및 화면 뚫림 방지 */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        width: 100% !important;
        gap: 5px !important; /* 버튼 사이 간격을 좁게 */
    }
    [data-testid="column"] {
        flex: 1 !important;
        min-width: 0 !important; /* 중요: 내부 컨텐츠에 의해 늘어나지 않게 함 */
    }
    
    /* 2. 버튼 사이즈 및 폰트 최적화 */
    .stButton > button {
        width: 100% !important;
        padding: 5px 2px !important; /* 위아래 5px, 양옆 2px로 축소 */
        font-size: 13px !important; /* 폰트를 살짝 줄여서 한 줄 유지 */
        white-space: nowrap !important; /* 글자가 아래로 꺾이지 않게 */
        overflow: hidden;
    }

    /* 3. 결과 박스 (비외상/외상) 가로 배치 */
    .flex-container { display: flex; gap: 8px; width: 100%; }
    .flex-item { flex: 1; min-width: 0; }
    .team-box { border: 1px solid #ddd; padding: 10px; border-radius: 5px; }
    
    .duty-title { font-size: 1rem; font-weight: bold; margin-bottom: 5px; }
    .name-text { font-size: 0.85rem; margin-bottom: 2px; }
    .D { color: #28a745; } .E { color: #fd7e14; } .N { color: #dc3545; }
    </style>
""", unsafe_allow_html=True)

def load_duty(selected_date):
    filename = f"data/duty_{selected_date.year}_{selected_date.month:02d}.csv"
    if not os.path.exists(filename): return None
    with open(filename, "r", encoding="utf-8") as f:
        return [line.strip().split(",") for line in f]

st.title("📅 을지 ER 근무")

if 'target_date' not in st.session_state:
    st.session_state.target_date = datetime.date.today()

# --- 버튼 레이아웃 ---
col1, col2 = st.columns(2)
with col1:
    if st.button("⬅️ 전날", use_container_width=True):
        st.session_state.target_date -= datetime.timedelta(days=1)
        st.rerun()
with col2:
    if st.button("다음날 ➡️", use_container_width=True):
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

if duty_list:
    teams = {"비외상": {"D":[], "E":[], "N":[], "S":[], "hmj":None},
             "외상": {"D":[], "E":[], "N":[], "S":[], "hmj":None}}

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
            if "홍민정" in clean_name and work != 'OF': target["hmj"] = work

    # 결과 출력
    html_content = "<div class='flex-container'>"
    for team_label in ["비외상", "외상"]:
        t = teams[team_label]
        html_content += f"<div class='flex-item team-box'><h4>🏥 {team_label}</h4>"
        for code, label in [("D", "Day"), ("E", "Eve"), ("N", "Night")]:
            html_content += f"<p class='duty-title {code}'>{label}</p>"
            if code == "D":
                if t["S"]: html_content += "".join([f"<p class='name-text'>🚩<b>S:{s}</b></p>" for s in t["S"]])
                if t["hmj"]: html_content += f"<p class='name-text'>✨<b>홍민정:{t['hmj']}</b></p>"
            html_content += "".join([f"<p class='name-text'>{i+1}. {n}</p>" for i, n in enumerate(t[code])])
        html_content += "</div>"
    html_content += "</div>"
    st.markdown(html_content, unsafe_allow_html=True)
else:
    st.warning(f"{current_date.year}년 {current_date.month:02d}월 데이터 없음")
