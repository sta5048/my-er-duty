import streamlit as st
import pandas as pd
import io

# 데이터 정리 (연->OF 변경 완료)
csv_data = """성명,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28
홍민정,OF,D,D,D,출연,D,OF,D,D,D,D,D,D,OF,OF,H,H,H,D,D,OF,OF,D,D,D,D,D,OF
허유미,D,D,D,D,OF,D,E,E,E,OF,OF,D,D,OF,OF,OF,D,D,D,OF,OF,E,E,E,OF,E,E,E
김지영,E,E,OF,OF,D,OF,OF,OF,D,D,D,D,OF,E,E,E,E,OF,E,E,E,OF,OF,D,D,OF,OF,OF
이초이,D,D,OF,E,E,N,N,OF,OF,E,E,E,E,OF,N,N,OF,OF,D,D,OF,OF,E,E,N,N,OF,OF
김은비,N,N,OF,OF,D,D,D,D,OF,E,N,N,N,OF,OF,D,E,E,OF,D,D,D,OF,OF,OF,E,E,N
주은지,OF,OF,E,E,OF,E,E,E,E,OF,E,E,OF,D,D,OF,OF,OF,E,E,OF,OF,D,E,E,OF,D,D
김선형,OF,OF,D,E,OF,D,D,N,N,N,OF,OF,D,E,E,OF,E,N,N,N,OF,OF,D,D,D,D,OF,OF
강도희,E,E,E,N,N,OF,OF,D,D,OF,OF,OF,OF,E,N,N,OF,E,E,OF,D,D,N,N,N,OF,OF,D
고민지,E,E,OF,D,OF,OF,OF,E,E,OF,D,N,N,N,OF,OF,D,D,D,OF,N,N,OF,OF,E,E,N,N
이가영,OF,E,N,N,N,OF,OF,D,D,D,D,OF,OF,D,E,E,N,N,OF,E,E,E,D,D,D,N,N,OF
이애진,OF,D,D,OF,E,N,N,N,OF,OF,E,E,E,E,OF,N,N,OF,OF,OF,OF,E,N,N,OF,D,D,D
이현진,OF,N,N,OF,E,E,E,E,OF,N,N,N,OF,OF,OF,D,D,OF,E,N,N,OF,D,D,D,D,D,E
김예진,OF,E,E,OF,D,D,D,OF,OF,E,E,OF,D,D,OF,OF,OF,OF,D,D,D,OF,E,E,E,OF,OF,E
최대인,N,N,N,OF,OF,OF,OF,E,E,OF,D,D,N,N,OF,E,E,E,OF,N,N,OF,D,D,D,D,D,D
박수현,D,OF,D,D,D,N,N,OF,OF,E,E,E,E,OF,N,N,OF,OF,D,D,E,E,D,D,N,N,OF,OF
임수진,N,OF,OF,E,E,E,E,OF,N,N,N,OF,OF,OF,D,D,D,D,OF,D,N,N,N,OF,교,OF,E,E
김태인,E,E,OF,N,N,OF,OF,OF,D,D,N,N,OF,OF,E,E,E,E,OF,OF,D,D,E,OF,교,N,N,N
박혜민,D,D,OF,D,N,N,OF,OF,D,D,OF,E,E,OF,D,D,N,N,OF,OF,OF,E,E,N,N,OF,OF,D
김소민,OF,OF,E,E,OF,N,N,N,OF,OF,D,D,D,D,OF,D,D,D,OF,N,N,OF,OF,E,E,N,N,OF
김민우,OF,N,N,OF,D,D,D,OF,OF,OF,OF,OF,N,N,N,OF,OF,OF,D,E,E,N,N,OF,OF,E,E,E
김현하,N,OF,E,E,E,E,OF,N,N,N,OF,OF,OF,OF,E,E,OF,N,N,N,OF,D,D,D,D,D,D,N
주혜진,OF,D,D,N,N,OF,OF,OF,OF,E,N,N,OF,E,E,OF,D,D,N,N,OF,OF,D,D,D,OF,D,OF
서현수,N,OF,OF,D,D,E,E,OF,N,N,OF,D,D,D,D,OF,D,E,E,OF,OF,N,N,N,OF,OF,F,E
이상희,D,D,D,OF,OF,D,D,D,E,OF,E,N,N,N,OF,OF,D,E,OF,N,N,N,OF,OF,E,E,E,OF
김민진,E,OF,OF,D,E,OF,OF,E,E,N,N,N,OF,OF,OF,D,D,D,D,D,D,D,D,OF,E,E,N,N
홍연경,D,OF,OF,E,E,N,N,OF,OF,D,D,D,D,D,N,N,OF,OF,D,D,E,E,OF,OF,N,N,OF,OF
이유진,OF,D,D,OF,D,D,N,N,OF,E,E,OF,E,E,OF,OF,N,N,OF,OF,D,D,N,N,OF,OF,E,E
이해민,N,N,OF,OF,OF,E,E,N,N,OF,OF,D,D,D,OF,OF,S,N,N,OF,OF,E,E,OF,OF,D,D,D
강채연,E,N,N,OF,OF,D,D,E,E,OF,OF,E,N,N,OF,E,E,E,E,OF,N,N,OF,OF,D,D,OF,OF
박에스더,OF,OF,E,N,N,OF,OF,D,D,D,D,OF,OF,OF,OF,E,N,N,OF,E,E,OF,D,D,E,N,N,N"""

df = pd.read_csv(io.StringIO(csv_data))

st.set_page_config(page_title="ER 근무 조회", layout="wide")
st.title("🏥 2월 비외상 근무 조회 시스템")

# 사용자 입력
my_duty_input = st.text_input("나의 2월 듀티를 순서대로 입력하세요 (예: DDEEOOFF...)", "")

if my_duty_input:
    my_duties = list(my_duty_input.upper().replace(" ", ""))
    st.divider()
    
    for i, duty in enumerate(my_duties):
        day_num = i + 1
        if day_num > 28: break
        day_col = str(day_num)
        
        # 교육 인원
        edu_workers = df[df[day_col] == '교']['성명'].tolist()
        
        # 동료 찾기
        search_duty = "OF" if duty in ["O", "OF"] else duty
        coworkers = df[df[day_col] == search_duty]['성명'].tolist()
        
        with st.expander(f"📅 2월 {day_num}일 ({duty})"):
            c1, c2 = st.columns(2)
            with c1:
                st.write("**👨‍⚕️ 같은 듀티 동료**")
                st.success(", ".join(coworkers)) if coworkers else st.write("없음")
            with c2:
                st.write("**📝 비고 (교육)**")
                st.info(f"교육: {', '.join(edu_workers)}") if edu_workers else st.write("-")
