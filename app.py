import streamlit as st
import datetime
import os

st.set_page_config(page_title="을지 응급실 근무", layout="wide")

# CSS: 모바일 가로 고정 (절대 밑으로 안 내려가게 강제)
st.markdown("""
    <style>
    /* 1. 상단 버튼 및 하단 근무표 레이아웃 강제 고정 */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 5px !important;
    }
    [data-testid="column"] {
        flex: 1 !important;
        min-width: 0px !important;
    }

    /* 2. 버튼 텍스트 및 패딩 최적화 */
    div.stButton > button {
        width: 100%;
        padding: 5px 0px !important;
        font-size: 13px !important;
        white-space: nowrap;
    }

    /* 3. 근무표 박스 디자인 */
    .team-box { 
        border: 1px solid #ddd; 
        padding: 8px; 
        border-radius: 5px; 
        background-color: #ffffff;
    }
    .duty-title { font-size: 0.95rem; font-weight: bold; margin-top: 8px; margin-bottom: 2px; }
    .name-text { font-size: 0.85rem; margin-bottom: 1px; }
    .D { color: #28a745; } .E { color: #fd7e14; } .N { color: #dc3545; }
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

# 버튼 영역: CSS 덕분에 좁은 화면에서도 한 줄에 3개 유지
b1, b2, b3 = st.columns(3)
with b1:
    if st.button("⬅️ 어제"):
        st.session_state.target_date -= datetime.timedelta(days=1)
        st.rerun()
with b2:
    if st.button("오늘 📍"):
        st.session_state.target_date = datetime.date.today()
        st.rerun()
with b3:
    if st.button("내일 ➡️"):
        st.session_state.target_date += datetime.timedelta(days=1)
        st.rerun()

# 날짜 선택기
selected_date = st.date_input("날짜 선택", st.session_state.target_date)
st.session_state.target_date = selected_date

day = selected_date.day
duty_list = load_duty(selected_date)

# --- 핵심: 들여쓰기 주의 구간 ---
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

    # 근무표 영역: 가로 배치 고정
    c1, c2 = st.columns(2)
    for label, col in [("비외상", c1), ("외상", c2)]:
        with col:
            t = teams[label]
            st.markdown(f"<div class='team-box'><b>🏥 {label}</b>", unsafe_allow_html=True)
            for shift, s_name in [("D", "Day"), ("E", "Eve"), ("N", "Night")]:
                st.markdown(f"<p class='duty-title {shift}'>{s_name}</p>", unsafe_allow_html=True)
                if shift == "D":
                    if t["S"]:
                        for s in t["S"]: st.markdown(f"<p class='name-text'>🚩<b>S:{s}</b></p>", unsafe_allow_html=True)
                    if t["hmj"]: st.markdown(f"<p class='name-text'>✨<b>홍민정:{t['hmj']}</b></p>", unsafe_allow_html=True)
                for i, name in enumerate(t[shift]):
                    st.markdown(f"<p class='name-text'>{i+1}. {name}</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
else:
    # 이 else는 바로 위의 if duty_list와 세로 줄이 딱 맞아야 합니다.
    st.error(f"⚠️ {selected_date.year}년 {selected_date.month}월 데이터가 없습니다.")else:
    st.error(f"⚠️ {selected_date.year}년 {selected_date.month}월 데이터가 없습니다.")
    # 최종 결과: 근무표도 flex-container를 사용하여 배치
    st.markdown(f"""
        <div class="flex-container">
            <div class="flex-item">{left_html}</div>
            <div class="flex-item">{right_html}</div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.error(f"⚠️ {selected_date.year}년 {selected_date.month}월 데이터 파일이 없습니다.")
