import streamlit as st
import datetime
import os

st.set_page_config(page_title="을지 응급실 근무", layout="wide")

# CSS: 버튼과 근무 카드를 모두 5:5로 정렬
st.markdown("""
    <style>
    .main-container { display: flex; gap: 10px; width: 100%; }
    .team-box { flex: 1; min-width: 0; border: 1px solid #ddd; padding: 10px; border-radius: 5px; }
    .duty-title { font-size: 1.1rem; font-weight: bold; margin-bottom: 5px; }
    .name-text { font-size: 0.9rem; margin-bottom: 2px; }
    .D { color: #28a745; } .E { color: #fd7e14; } .N { color: #dc3545; }
    
    /* 버튼 스타일: 가로로 꽉 차게 */
    div.stButton > button {
        width: 100%;
        height: 3em;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

def load_duty(selected_date):
    filename = f"data/duty_{selected_date.year}_{selected_date.month:02d}.csv"
    if not os.path.exists(filename): return None
    with open(filename, "r", encoding="utf-8") as f:
        return [line.strip().split(",") for line in f if line.strip()]

st.title("📅 ER 근무 조회")

# --- 날짜 제어 로직 ---
if 'target_date' not in st.session_state:
    st.session_state.target_date = datetime.date.today()

# [어제]와 [내일] 버튼을 외상/비외상처럼 5:5로 배치
btn_col1, btn_col2, btn_col3 = st.columns(3)
with btn_col1:
    if st.button("⬅️ 어제"):
        st.session_state.target_date -= datetime.timedelta(days=1)
        st.rerun() # 즉시 반영을 위해 리런
with btn_col2: 
    if st.button("오늘 📍"):
        st.session_state.target_date = datetime.date.today()
with btn_col3:
    if st.button("내일 ➡️"):
        st.session_state.target_date += datetime.timedelta(days=1)
        st.rerun()

# 날짜 선택기 (버튼과 연동)
selected_date = st.date_input("날짜 선택", st.session_state.target_date)
st.session_state.target_date = selected_date

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
            if not work or work in ['OF', 'OFF', '']: continue
            
            team_key = "외상" if "*" in raw_name else "비외상"
            clean_name = raw_name.replace("*", "")
            target = teams[team_key]
            
            if work == 'D': target["D"].append(clean_name)
            elif work == 'E': target["E"].append(clean_name)
            elif work == 'N': target["N"].append(clean_name)
            elif work == 'S': target["S"].append(clean_name)
            elif "홍민정" in clean_name: target["hmj"] = work

    # HTML 렌더링 파트
    left_html = ""
    right_html = ""

    for team_label in ["비외상", "외상"]:
        t = teams[team_label]
        content = f"<div class='team-box'><h4>🏥 {team_label}</h4>"
        
        for shift, label in [("D", "Day"), ("E", "Eve"), ("N", "Night")]:
            content += f"<p class='duty-title {shift}'>{label}</p>"
            if shift == "D":
                if t["S"]: content += "".join([f"<p class='name-text'>🚩<b>S:{s}</b></p>" for s in t["S"]])
                if t["hmj"]: content += f"<p class='name-text'>✨<b>홍민정:{t['hmj']}</b></p>"
            
            names = t[shift]
            content += "".join([f"<p class='name-text'>{i+1}. {n}</p>" for i, n in enumerate(names)])
        
        content += "</div>"
        if team_label == "비외상": left_html = content
        else: right_html = content

    # 최종 결과 출력 (버튼 하단에 5:5 배치)
    st.markdown(f"""
        <div class='main-container'>
            {left_html}
            {right_html}
        </div>
        """, unsafe_allow_html=True)
else:
    st.error(f"⚠️ {selected_date.year}년 {selected_date.month}월 데이터 파일이 없습니다.")
