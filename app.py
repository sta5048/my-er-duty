import streamlit as st
import datetime
import os

st.set_page_config(page_title="ER 근무 조회", page_icon="📅")

def load_duty(selected_date):
    filename = f"data/duty_{selected_date.year}_{selected_date.month:02d}.csv"
    data = []
    if not os.path.exists(filename):
        st.error(f"⚠️ {selected_date.month}월 데이터 파일이 없습니다! ({filename})")
        return None
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                data.append([item.strip() for item in line.split(",")])
        return data
    except Exception as e:
        st.error(f"파일 오류: {e}")
        return None

st.title("📅 ER 근무 조회")
selected_date = st.date_input("조회할 날짜를 선택하세요", datetime.date.today())
day = selected_date.day

duty_list = load_duty(selected_date)

if duty_list:
    d, e, n, s_worker = [], [], [], []
    hmj_special = None  # 홍민정 선생님 특수 근무 저장용

    for row in duty_list[1:]:
        if len(row) > day:
            name, work = row[0], row[day]
            
            # 1. 기본 근무 분류
            if work == 'D': d.append(name)
            elif work == 'E': e.append(name)
            elif work == 'N': n.append(name)
            elif work == 'S': s_worker.append(name)
            
            # 2. 홍민정 선생님 특수 근무 체크 (D, E, N, S가 아닌 경우)
            if name == '홍민정' and work not in ['D', 'E', 'N', 'S', 'OF']:
                hmj_special = work

    st.subheader(f"🔍 {selected_date.month}월 {day}일 명단")
    cols = st.columns(3)
    
    for col, title, names, color in zip(cols, ["☀️ Day", "⛅ Eve", "🌙 Night"], [d, e, n], ["green", "orange", "red"]):
        with col:
            st.markdown(f"### :{color}[{title}]")
            
            # Day 컬럼인 경우 상단에 S근무자 및 홍민정 특수근무 표시
            if title == "☀️ Day":
                if s_worker:
                    for name in s_worker:
                        st.write(f"🚩 **S근무자: {name}**")
                
                if hmj_special:
                    st.write(f"✨ **홍민정: {hmj_special}**")
                
                if s_worker or hmj_special:
                    st.write("---") # 구분선

            # 일반 명단 출력
            if names:
                for i, name in enumerate(names, 1):
                    st.write(f"{i}. {name}")
            else:
                st.write("-")
