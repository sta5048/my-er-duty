import streamlit as st
import datetime
import os

st.set_page_config(page_title="을지 응급실 근무", layout="wide")

# CSS: 기존 레이아웃 유지 + 버튼 스타일 살짝 추가
st.markdown("""
    <style>
    .main-container { display: flex; gap: 10px; width: 100%; }
    .team-box { flex: 1; min-width: 0; border: 1px solid #ddd; padding: 10px; border-radius: 5px; }
    .duty-title { font-size: 1.1rem; font-weight: bold; margin-bottom: 5px; }
    .name-text { font-size: 0.9rem; margin-bottom: 2px; }
    .D { color: #28a745; } .E { color: #fd7e14; } .N { color: #dc3545; }
    /* 버튼 정렬을 위한 컨테이너 */
    .stButton>button { width: 100%; }
    </style>
    """, unsafe_allow_html=True)

def load_duty(selected_date):
    filename = f"data/duty_{selected_date.year}_{selected_date.month:02d}.csv"
    if not os.path.exists(filename): return None
    with open(filename, "r", encoding="utf-8") as f:
        # 빈 줄 제외하고 로드
        return [line.strip().split(",") for line in f if line.strip()]

st.title("📅 ER 근무 조회")

# --- 날짜 조절 로직 추가 ---
if 'target_date' not in st.session_state:
    st.session_state.target_date = datetime.date.today()

# 버튼을 가로로 배치 (화면 분할 방식과 동일하게 2컬럼 사용)
btn_col1, btn_col2 = st.columns(2)
with btn_col1:
    if st.button("⬅️ 어제"):
        st.session_state.target_date -= datetime.timedelta(days=1)
with btn_col2:
    if st.button("오늘 📍"):
        st.session_state.target_date = datetime.date.today()

# 날짜 선택기 (버튼 클릭 시 연동됨)
selected_date = st.date_input("날짜 선택", st.session_state.target_date, key="date_picker")
# 선택기에서 직접 날짜를 바꿨을 때를 위해 세션 상태 동기화
st.session_state.target_date = selected_date

day = selected_date.day
duty_list = load_duty(selected_date)

if duty_list:
    # (데이터 처리 로직은 기존과 동일)
    teams = {
        "비외상": {"D": [], "E": [], "N": [], "S": [], "hmj": None},
        "외상": {"D": [], "E": [], "N": [], "S": [], "hmj": None}
    }

    # 헤더 제외 데이터 파싱
    header = duty_list[0]
    for row in duty_list[1:]:
        if len(row) > day:
            raw_name, work = row[0], row[day]
            if not work or work == 'OFF': continue # 쉬는 날 제외
            
            team_key = "외상" if "*" in raw_name else "비외상"
            clean_name = raw_name.replace("*", "")
            target = teams[team_key]
            
            if work == 'D': target["D"].append(clean_name)
            elif work == 'E': target["E"].append(clean_name)
            elif work == 'N': target["N"].append(clean_name)
            elif work == 'S': target["S"].append(clean_name)
            elif "홍민정" in clean_name: target["hmj"] = work

    # HTML 생성 및 렌더링 (기존 방식 유지)
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
            content += "".join([f<p class='name-text'>{i+1}. {n}</p>" for i, n in enumerate(names)])
        
        content += "</div>"
        if team_label == "비외상": left_html = content
        else: right_html = content

    st.markdown(f"<div class='main-container'>{left_html}{right_html}</div>", unsafe_allow_html=True)
else:
    st.warning(f"{selected_date.month}월 근무표 파일이 존재하지 않습니다.")
