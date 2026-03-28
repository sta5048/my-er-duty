import streamlit as st
import datetime
import os

st.set_page_config(page_title="을지 응급실 근무", layout="wide")

# CSS
st.markdown("""
    <style>
    .main-container { display: flex; gap: 10px; width: 100%; }
    .team-box { flex: 1; min-width: 0; border: 1px solid #ddd; padding: 10px; border-radius: 5px; }
    
    .duty-title { font-size: 1.1rem; font-weight: bold; margin-bottom: 5px; }
    .name-text { font-size: 0.9rem; margin-bottom: 2px; }
    .D { color: #28a745; } .E { color: #fd7e14; } .N { color: #dc3545; }

    /* ✅ 상단 고정 */
    .fixed-nav {
        position: fixed;
        top: 70px;
        left: 0;
        right: 0;
        display: flex;
        justify-content: center;
        gap: 10px;
        z-index: 9999;
    }

    /* 버튼 크기 */
    .stButton > button {
        padding: 6px 14px;
        font-size: 14px;
        border-radius: 8px;
        width: auto;
    }

    /* 본문 안 가려지게 */
    .block-container {
        padding-top: 120px;
    }
    </style>
    """, unsafe_allow_html=True)

def load_duty(selected_date):
    filename = f"data/duty_{selected_date.year}_{selected_date.month:02d}.csv"
    if not os.path.exists(filename): return None
    with open(filename, "r", encoding="utf-8") as f:
        return [line.strip().split(",") for line in f]

st.title("📅 을지 ER 근무")

# --- 날짜 조절 ---
if 'target_date' not in st.session_state:
    st.session_state.target_date = datetime.date.today()

# ✅ 상단 고정 버튼 (진짜 동작함)
st.markdown('<div class="fixed-nav">', unsafe_allow_html=True)

col1, col2 = st.columns([1,1])

with col1:
    if st.button("⬅️ 전날"):
        st.session_state.target_date -= datetime.timedelta(days=1)
        st.rerun()

with col2:
    if st.button("다음날 ➡️"):
        st.session_state.target_date += datetime.timedelta(days=1)
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# 날짜 선택
selected_date = st.date_input("날짜 직접 선택", value=st.session_state.target_date)
if selected_date != st.session_state.target_date:
    st.session_state.target_date = selected_date
    st.rerun()

current_date = st.session_state.target_date
day = current_date.day
duty_list = load_duty(current_date)

# --- 근무표 ---
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

    left_html = ""
    right_html = ""

    for team_label, side_html in [("비외상", "left"), ("외상", "right")]:
        t = teams[team_label]
        content = f"<div class='team-box'><h4>🏥 {team_label}</h4>"
        content += "<p class='duty-title D'>Day</p>"
        if t["S"]: content += "".join([f"<p class='name-text'>🚩<b>S:{s}</b></p>" for s in t["S"]])
        if t["hmjfor team_label, side_html in [("비외상", "left"), ("외상", "right")]:
    t = teams[team_label]
    content = f"<div class='team-box'><h4>🏥 {team_label}</h4>"

    content += "<p class='duty-title D'>Day</p>"
    if t["S"]:
        content += "".join([f"<p class='name-text'>🚩<b>S:{s}</b></p>" for s in t["S"]])
    if t["hmj"]:
        content += f"<p class='name-text'>✨<b>홍민정:{t['hmj']}</b></p>"
    content += "".join([f"<p class='name-text'>{i+1}. {n}</p>" for i, n in enumerate(t["D"])])

    content += "<p class='duty-title E'>Eve</p>"
    content += "".join([f"<p class='name-text'>{i+1}. {n}</p>" for i, n in enumerate(t["E"])])

    content += "<p class='duty-title N'>Night</p>"
    content += "".join([f"<p class='name-text'>{i+1}. {n}</p>" for i, n in enumerate(t["N"])])

    content += "</div>"

    if side_html == "left":
        left_html = content
    else:
        right_html = content

    st.markdown(f"""
        <div class='main-container'>
            {left_html}
            {right_html}
        </div>
        """, unsafe_allow_html=True)
else:
    st.warning(f"{current_date.year}년 {current_date.month}월 근무표 데이터가 없습니다.")        
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
    st.warning(f"{current_date.year}년 {current_date.month}월 근무표 데이터가 없습니다.")
