import streamlit as st
import datetime

st.set_page_config(page_title="ER 근무 조회", page_icon="📅")

# 1. 데이터 읽기
def load_duty():
    data = []
    try:
        with open("duty_data.csv", "r", encoding="utf-8") as f:
            for line in f:
                data.append([item.strip() for item in line.split(",")])
        return data
    except:
        return None

duty_list = load_duty()

# 2. 화면 구성
st.title("📅 ER 근무 조회")
selected_date = st.date_input("날짜 선택", datetime.date.today())
day = selected_date.day

if duty_list:
    # 근무자 리스트 (Day, Evening, Night)
    d, e, n = [], [], []

    # 3. 데이터 매칭 (첫 줄 제외)
    for row in duty_list[1:]:
        if len(row) > day:
            name, work = row[0], row[day]
            if work == 'D': d.append(name)
            elif work == 'E': e.append(name)
            elif work == 'N': n.append(name)

    # 4. 결과 출력
    st.subheader(f"🔍 {selected_date.month}월 {day}일 명단")
    cols = st.columns(3)
    
    for col, title, names, color in zip(cols, ["☀️ Day", "⛅ Eve", "🌙 Night"], [d, e, n], ["green", "orange", "red"]):
        with col:
            st.markdown(f"### :{color}[{title}]")
            if names:
                for i, name in enumerate(names, 1):
                    st.write(f"{i}. {name}")
            else:
                st.write("-")
