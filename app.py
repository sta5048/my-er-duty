import streamlit as st
import datetime

st.set_page_config(page_title="ER 근무 조회", page_icon="📅")

# 1. 데이터 읽기
def get_data():
    data = []
    try:
        with open("duty_data.csv", "r", encoding="utf-8") as f:
            for line in f:
                # 쉼표로 나누고 앞뒤 공백 제거
                data.append([item.strip() for item in line.split(",")])
    except:
        st.error("duty_data.csv 파일을 확인해주세요.")
    return data

duty_list = get_data()

# 2. 화면 구성
st.title("📅 ER 근무 조회")
selected_date = st.date_input("날짜 선택", datetime.date.today())
day = selected_date.day

if duty_list:
    # 근무자 담을 리스트
    d, e, n, edu = [], [], [], []

    # 3. 데이터 분류 (첫 줄 헤더 제외)
    for row in duty_list[1:]:
        if len(row) <= day: continue
        
        name = row[0]   # 이름
        work = row[day] # 해당 날짜 근무
        
        if work == 'D' or (name == '홍민정' and work == 'H'): d.append(name)
        elif work == 'E': e.append(name)
        elif work == 'N': n.append(name)
        elif work == '교': edu.append(name)

    # 4. 결과 출력
    st.subheader(f"🔍 {selected_date.month}월 {day}일 명단")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.success("☀️ Day")
        for i, val in enumerate(d, 1): st.write(f"{i}. {val}")
    with c2:
        st.warning("⛅ Evening")
        for i, val in enumerate(e, 1): st.write(f"{i}. {val}")
    with c3:
        st.error("🌙 Night")
        for i, val in enumerate(n, 1): st.write(f"{i}. {val}")

    if edu:
        st.info(f"📝 교육: {', '.join(edu)}")
