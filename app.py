import streamlit as st
import datetime
import os

st.set_page_config(page_title="을지 응급실 근무", layout="wide")

# CSS: 모바일에서도 가로 배치를 강제하고 폰트 크기를 살짝 조절함


def load_duty(selected_date):
    filename = f"data/duty_{selected_date.year}_{selected_date.month:02d}.csv"
    if not os.path.exists(filename): return None
    with open(filename, "r", encoding="utf-8") as f:
        return [line.strip().split(",") for line in f]

st.title("📅 ER 근무 조회")
# --- st.title 바로 아래부터 데이터 로드 전까지 교체 ---
hidden = st.container()
with hidden:
    btn_prev = st.button("prev")
    btn_today = st.button("today")
    btn_next = st.button("next")

st.markdown("""
<div style="display: flex; width: 100%; gap: 2px; margin-bottom: 5px;">
    <div style="flex: 1; padding: 12px 0; text-align: center; background-color: #f0f2f6; border: 1px solid #ddd; border-radius: 6px; font-weight: bold; cursor: pointer;"
         onclick="window.parent.document.querySelectorAll('button[kind=secondary]')[0].click()">⬅️ 전날</div>

    <div style="flex: 1; padding: 12px 0; text-align: center; background-color: #f0f2f6; border: 1px solid #ddd; border-radius: 6px; font-weight: bold; cursor: pointer;"
         onclick="window.parent.document.querySelectorAll('button[kind=secondary]')[1].click()">오늘</div>

    <div style="flex: 1; padding: 12px 0; text-align: center; background-color: #f0f2f6; border: 1px solid #ddd; border-radius: 6px; font-weight: bold; cursor: pointer;"
         onclick="window.parent.document.querySelectorAll('button[kind=secondary]')[2].click()">담날 ➡️</div>
</div>
""", unsafe_allow_html=True)

# 1. 날짜 세션 상태 초기화
if 'temp_date' not in st.session_state:
    st.session_state.temp_date = datetime.date.today()

# 2. 실제 동작용 버튼 (화면에서 완전히 숨김)
# container를 사용해 감싸고 CSS로 해당 영역을 아예 보이지 않게(display:none) 처리
st.markdown("""
<div style="display: flex; gap: 4px; margin-bottom: 8px;">
    <form action="" method="post" style="flex:1;">
        <button name="action" value="prev" style="width:100%; padding:12px; border-radius:6px; border:1px solid #ddd; background:#f0f2f6; font-weight:bold;">⬅️ 전날</button>
    </form>
    <form action="" method="post" style="flex:1;">
        <button name="action" value="today" style="width:100%; padding:12px; border-radius:6px; border:1px solid #ddd; background:#f0f2f6; font-weight:bold;">오늘</button>
    </form>
    <form action="" method="post" style="flex:1;">
        <button name="action" value="next" style="width:100%; padding:12px; border-radius:6px; border:1px solid #ddd; background:#f0f2f6; font-weight:bold;">담날 ➡️</button>
    </form>
</div>
""", unsafe_allow_html=True)
# 5. 날짜 선택창
selected_date = st.date_input("날짜 선택", st.session_state.temp_date, label_visibility="collapsed")
st.session_state.temp_date = selected_date

day = selected_date.day
duty_list = load_duty(selected_date)
# --- 이후 코드(if duty_list: ...)는 동일 ---

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
