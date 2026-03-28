import streamlit as st
import datetime
import os

st.set_page_config(page_title="을지 응급실 근무", layout="wide")

# CSS: 외상/비외상 박스와 완전히 동일한 로직 적용
st.markdown("""
    <style>
    /* 1. 공통 가로 배치 컨테이너 (버튼 & 결과박스 공용) */
    .half-split-container {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        width: 100% !important;
        gap: 10px !important;
        margin-bottom: 15px;
    }
    .half-item {
        flex: 1 !important;
        min-width: 0 !important; /* 박스가 화면 밖으로 절대 안 나감 */
    }

    /* 2. 버튼 디자인 (외상/비외상 박스처럼 깔끔하게) */
    .custom-btn {
        display: block;
        width: 100%;
        padding: 12px 0;
        text-align: center;
        background-color: #f0f2f6;
        border: 1px solid #ddd;
        border-radius: 8px;
        color: #31333F;
        font-weight: 600;
        font-size: 14px;
        cursor: pointer;
        text-decoration: none;
    }
    
    /* 3. 실제 클릭을 처리할 Streamlit 버튼 숨기기 트릭 */
    .stButton button {
        width: 100%;
        height: 45px;
    }

    /* 4. 결과 박스 스타일 */
    .team-box { border: 1px solid #ddd; padding: 10px; border-radius: 5px; height: 100%; }
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

if 'target_date' not in st.session_state:
    st.session_state.target_date = datetime.date.today()

st.title("📅 을지 ER 근무")

# --- [해결책] 버튼 가로 배치 (외상/비외상과 똑같은 flex 구조) ---
# st.columns 대신 직접 div로 묶어 모바일 강제 줄바꿈을 원천 차단합니다.
st.markdown('<div class="half-split-container">', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    if st.button("⬅️ 전날", use_container_width=True):
        st.session_state.target_date -= datetime.timedelta(days=1)
        st.rerun()
with col2:
    if st.button("다음날 ➡️", use_container_width=True):
        st.session_state.target_date += datetime.timedelta(days=1)
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

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

    # 결과 박스 출력 (성공했던 flex-container 방식 유지)
    html_content = "<div class='half-split-container'>"
    for team_label in ["비외상", "외상"]:
        t = teams[team_label]
        html_content += f"<div class='half-item team-box'><h4>🏥 {team_label}</h4>"
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
