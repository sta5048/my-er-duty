import streamlit as st
import datetime
import os

st.set_page_config(page_title="을지 응급실 근무", layout="wide")

# CSS: 글자 크기를 확 줄여서 한 화면에 쑤셔넣기
st.markdown("""
    <style>
    /* 전체 배경 및 폰트 설정 */
    html, body, [data-testid="stAppViewContainer"] {
        font-size: 12px !important;
    }
    
    /* 가로 배치 강제 */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 2px !important;
    }
    [data-testid="column"] {
        flex: 1 !important;
        min-width: 0px !important;
    }

    /* 버튼: 글자 크기 최소화 */
    div.stButton > button {
        width: 100%;
        padding: 2px 0px !important;
        font-size: 11px !important;
        height: 35px !important;
        white-space: nowrap;
    }

    /* 근무표 박스: 여백 최소화 */
    .team-box { 
        border: 1px solid #ddd; 
        padding: 4px; 
        border-radius: 4px; 
        background-color: #ffffff;
    }
    .team-title { font-size: 12px; font-weight: bold; margin-bottom: 4px; display: block;}
    .duty-title { font-size: 11px; font-weight: bold; margin-top: 4px; margin-bottom: 0px; }
    .name-text { font-size: 10.5px; margin-bottom: 0px; line-height: 1.2; }
    .D { color: #28a745; } .E { color: #fd7e14; } .N { color: #dc3545; }
    
    /* 날짜 선택기 크기 조절 */
    div[data-testid="stDateInput"] { width: 100% !important; }
    </style>
    """, unsafe_allow_html=True)

def load_duty(selected_date):
    filename = f"data/duty_{selected_date.year}_{selected_date.month:02d}.csv"
    if not os.path.exists(filename): return None
    with open(filename, "r", encoding="utf-8") as f:
        return [line.strip().split(",") for line in f if line.strip()]

st.title("📅 ER 근무")

if 'target_date' not in st.session_state:
    st.session_state.target_date = datetime.date.today()

# 버튼 3개
b1, b2, b3 = st.columns(3)
with b1:
    if st.button("⬅️어제"):
        st.session_state.target_date -= datetime.timedelta(days=1)
        st.rerun()
with b2:
    if st.button("오늘📍"):
        st.session_state.target_date = datetime.date.today()
        st.rerun()
with b3:
    if st.button("내일➡️"):
        st.session_state.target_date += datetime.timedelta(days=1)
        st.rerun()

selected_date = st.date_input("날짜", st.session_state.target_date)
st.session_state.target_date = selected_date

day = selected_date.day
duty_list = load_duty(selected_date)

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

    c1, c2 = st.columns(2)
    for label, col in [("비외상", c1), ("외상", c2)]:
        with col:
            t = teams[label]
            st.markdown(f"<div class='team-box'><span class='team-title'>🏥{label}</span>", unsafe_allow_html=True)
            for shift, s_name in [("D", "Day"), ("E", "Eve"), ("N", "Night")]:
                st.markdown(f"<p class='duty-title {shift}'>{s_name}</p>", unsafe_allow_html=True)
                if shift == "D":
                    if t["S"]:
                        for s in t["S"]: st.markdown(f"<p class='name-text'>🚩<b>S:{s}</b></p>", unsafe_allow_html=True)
                    if t["hmj"]: st.markdown(f"<p class='name-text'>✨<b>홍:{t['hmj']}</b></p>", unsafe_allow_html=True)
                for i, name in enumerate(t[shift]):
                    st.markdown(f"<p class='name-text'>{i+1}.{name}</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
else:
    st.error("데이터 없음")
