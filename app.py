import streamlit as st
import datetime
import os

st.set_page_config(page_title="을지 응급실 근무", layout="wide")

# CSS: 핵심은 flex-wrap을 nowrap으로 강제하고, column의 너비를 강제로 고정하는 것
st.markdown("""
    <style>
    /* 1. 버튼과 레이아웃이 포함된 모든 컬럼 컨테이너를 한 줄로 강제 */
    [data-testid="column"] {
        flex: 1 1 0% !important;
        min-width: 0px !important;
    }

    /* 2. 상위 컨테이너의 줄바꿈 방지 */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: flex-start !important;
    }

    /* 3. 버튼 텍스트 크기 조절 (좁은 화면 대비) */
    div.stButton > button {
        width: 100%;
        padding: 5px 2px !important;
        font-size: 14px !important; /* 글자가 깨지면 12px로 줄이세요 */
        white-space: nowrap; /* 버튼 글자 줄바꿈 방지 */
    }

    /* 4. 근무표 박스 스타일 */
    .team-box { 
        border: 1px solid #ddd; 
        padding: 10px; 
        border-radius: 5px; 
        background-color: white;
    }
    .duty-title { font-size: 1rem; font-weight: bold; margin-bottom: 5px; }
    .name-text { font-size: 0.85rem; margin-bottom: 2px; }
    .D { color: #28a745; } .E { color: #fd7e14; } .N { color: #dc3545; }
    </style>
    """, unsafe_allow_html=True)

def load_duty(selected_date):
    filename = f"data/duty_{selected_date.year}_{selected_date.month:02d}.csv"
    if not os.path.exists(filename): return None
    with open(filename, "r", encoding="utf-8") as f:
        return [line.strip().split(",") for line in f if line.strip()]

st.title("📅 ER 근무 조회")

# --- 날짜 제어 (버튼 영역) ---
if 'target_date' not in st.session_state:
    st.session_state.target_date = datetime.date.today()

# 버튼 3개를 강제로 한 줄 배치 (CSS가 적용됨)
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

# 날짜 선택기
selected_date = st.date_input("날짜 선택", st.session_state.target_date)
st.session_state.target_date = selected_date

day = selected_date.day
duty_list = load_duty(selected_date)

if duty_list:
    # (데이터 처리 로직은 기존과 동일)
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

    # 근무표 영역 (st.columns를 사용하여 CSS 효과 적용)
    col_left, col_right = st.columns(2)
    
    for team_label, col in [("비외상", col_left), ("외상", col_right)]:
        with col:
            t = teams[team_label]
            st.markdown(f"<div class='team-box'><h4>🏥 {team_label}</h4>", unsafe_allow_html=True)
            for shift, label in [("D", "Day"), ("E", "Eve"), ("N", "Night")]:
                st.markdown(f"<p class='duty-title {shift}'>{label}</p>", unsafe_allow_html=True)
                if shift == "D":
                    if t["S"]: 
                        for s in t["S"]: st.markdown(f"<p class='name-text'>🚩<b>S:{s}</b></p>", unsafe_allow_html=True)
                    if t["hmj"]: st.markdown(f"<p class='name-text'>✨<b>홍민정:{t['hmj']}</b></p>", unsafe_allow_html=True)
                for i, n in enumerate(t[shift]):
                    st.markdown(f"<p class='name-text'>{i+1}. {n}</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
else:
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
