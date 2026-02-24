import streamlit as st
import datetime
import os

# 1. 페이지 설정 (넓게 보기)
st.set_page_config(page_title="ER 근무 조회", layout="wide")

def load_duty(selected_date):
    filename = f"data/duty_{selected_date.year}_{selected_date.month:02d}.csv"
    if not os.path.exists(filename):
        st.error(f"⚠️ {selected_date.month}월 파일이 없습니다!")
        return None
    with open(filename, "r", encoding="utf-8") as f:
        return [line.strip().split(",") for line in f]

# 2. 날짜 선택 및 데이터 로드
st.title("📅 ER 근무 조회")
selected_date = st.date_input("날짜를 선택하세요", datetime.date.today())
day = selected_date.day
duty_list = load_duty(selected_date)

if duty_list:
    # 비외상(Non-Trauma), 외상(Trauma) 분류용 딕셔너리
    teams = {
        "비외상": {"D": [], "E": [], "N": [], "S": [], "hmj": None},
        "외상": {"D": [], "E": [], "N": [], "S": [], "hmj": None}
    }

    for row in duty_list[1:]:
        if len(row) > day:
            raw_name, work = row[0], row[day]
            
            # '*' 유무로 팀 분류 후 화면 표시용 이름 정리
            team_key = "외상" if "*" in raw_name else "비외상"
            clean_name = raw_name.replace("*", "")

            target = teams[team_key]
            
            if work == 'D': target["D"].append(clean_name)
            elif work == 'E': target["E"].append(clean_name)
            elif work == 'N': target["N"].append(clean_name)
            elif work == 'S': target["S"].append(clean_name)
            # 홍민정 선생님만 특이사항 따로 저장
            elif clean_name == "홍민정" and work != 'OF':
                target["hmj"] = work

    # 3. 화면 출력 (좌: 비외상, 우: 외상)
    st.subheader(f"🔍 {selected_date.month}월 {day}일 근무 명단")
    left_col, right_col = st.columns(2)

    for side, team_label in zip([left_col, right_col], ["비외상", "외상"]):
        with side:
            st.markdown(f"### 🏥 {team_label}")
            t_data = teams[team_label]
            
            # 내부를 다시 D, E, N 3칸으로 분할
            sub_cols = st.columns(3)
            for col, title, names, color in zip(sub_cols, ["Day", "Eve", "Night"], [t_data["D"], t_data["E"], t_data["N"]], ["green", "orange", "red"]):
                with col:
                    st.markdown(f"#### :{color}[{title}]")
                    
                    # D열 상단에 S근무자 및 홍민정 특이사항 노출
                    if title == "Day":
                        if t_data["S"]:
                            for s in t_data["S"]: st.write(f"🚩 **S: {s}**")
                        if t_data["hmj"]:
                            st.write(f"✨ **홍민정: {t_data['hmj']}**")

                    if names:
                        for i, name in enumerate(names, 1):
                            st.write(f"{i}. {name}")
                    elif title != "Day" or (not t_data["S"] and not t_data["hmj"]):
                        st.write("-")
            st.divider()
