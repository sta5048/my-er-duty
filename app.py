import streamlit as st
import datetime
import os

st.set_page_config(page_title="을지 응급실 근무", layout="wide")

# CSS: 모바일에서도 가로 배치를 강제하고 폰트 크기를 살짝 조절함
st.markdown("""
    <style>
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

st.title("📅 ER 근무 조회")
# --- st.title("📅 ER 근무 조회") 바로 아래에 있던 기존 CSS 및 버튼 코드를 아래로 교체 ---

# 1. 날짜 조절 세션 상태 (기존 유지)
if 'temp_date' not in st.session_state:
    st.session_state.temp_date = datetime.date.today()

# 2. 강제 가로 배치를 위한 완전한 HTML 버튼 & CSS
st.markdown("""
    <style>
    /* 전체 버튼 컨테이너 설정: 무조건 가로로 나열 */
    .nav-btn-container {
        display: flex;
        width: 100%;
        gap: 8px; /* 버튼 사이 간격 */
        margin-bottom: 15px;
    }
    
    /* 각 버튼 스타일: 크기 동일, 가운데 정렬 */
    .nav-btn {
        flex: 1; /* 3등분 */
        text-align: center;
        padding: 12px 5px;
        background-color: #f0f2f6; /* 버튼 배경색 */
        border: 1px solid #dcdde1;
        border-radius: 10px;
        cursor: pointer;
        font-size: 15px;
        font-weight: bold;
        color: #31333F;
        text-decoration: none; /* 링크 밑줄 제거 */
        display: inline-block;
    }

    /* 버튼 호버/클릭 효과 */
    .nav-btn:hover {
        background-color: #e0e2e6;
    }
    .nav-btn:active {
        background-color: #d0d2d6;
        transform: translateY(1px); /* 클릭 느낌 */
    }
    </style>
    """, unsafe_allow_html=True)

# 3. HTML 버튼 링크 생성 (클릭 시 쿼리 파라미터를 통해 날짜 변경)
# 스트림릿에서 직접 HTML 클릭을 날짜 변경으로 연결하려면 쿼리 파라미터가 가장 확실합니다.
prev_date_str = (st.session_state.temp_date - datetime.timedelta(days=1)).isoformat()
today_date_str = datetime.date.today().isoformat()
next_date_str = (st.session_state.temp_date + datetime.timedelta(days=1)).isoformat()

# HTML 렌더링
st.markdown(f"""
    <div class="nav-btn-container">
        <a href="?date={prev_date_str}" class="nav-btn" target="_self">⬅️ 전날</a>
        <a href="?date={today_date_str}" class="nav-btn" target="_self">오늘</a>
        <a href="?date={next_date_str}" class="nav-btn" target="_self">담날 ➡️</a>
    </div>
    """, unsafe_allow_html=True)

# 4. URL 쿼리 파라미터에서 날짜 읽어오기
query_params = st.query_params
if "date" in query_params:
    try:
        new_date = datetime.date.fromisoformat(query_params["date"])
        # URL의 날짜와 세션의 날짜가 다를 때만 갱신 (무한 루프 방지)
        if new_date != st.session_state.temp_date:
            st.session_state.temp_date = new_date
            st.rerun()
    except ValueError:
        pass # 잘못된 날짜 형식은 무시

# 5. 날짜 입력창 및 변수 설정 (기존 코드 유지)
selected_date = st.date_input("날짜 선택", st.session_state.temp_date)
st.session_state.temp_date = selected_date

day = selected_date.day
duty_list = load_duty(selected_date)

# --- 이후 코드(if duty_list: ...)는 기존대로 유지 ---

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

    # HTML을 이용한 좌우 강제 배치
    left_html = ""
    right_html = ""

    for team_label, side_html in [("비외상", "left"), ("외상", "right")]:
        t = teams[team_label]
        content = f"<div class='team-box'><h4>🏥 {team_label}</h4>"
        
        # Day
        content += "<p class='duty-title D'>Day</p>"
        if t["S"]: content += "".join([f"<p class='name-text'>🚩<b>S:{s}</b></p>" for s in t["S"]])
        if t["hmj"]: content += f"<p class='name-text'>✨<b>홍민정:{t['hmj']}</b></p>"
        content += "".join([f"<p class='name-text'>{i+1}. {n}</p>" for i, n in enumerate(t["D"])])
        
        # Eve
        content += "<p class='duty-title E'>Eve</p>"
        content += "".join([f"<p class='name-text'>{i+1}. {n}</p>" for i, n in enumerate(t["E"])])
        
        # Night
        content += "<p class='duty-title N'>Night</p>"
        content += "".join([f"<p class='name-text'>{i+1}. {n}</p>" for i, n in enumerate(t["N"])])
        
        content += "</div>"
        if side_html == "left": left_html = content
        else: right_html = content

    # 최종 결과 출력
    st.markdown(f"""
        <div class='main-container'>
            {left_html}
            {right_html}
        </div>
        """, unsafe_allow_html=True)
