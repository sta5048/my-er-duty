import streamlit as st
import pandas as pd
import io
from datetime import date

# 1. 데이터 준비 (이미지 기반 추출 데이터)
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

# 2. 페이지 설정
st.set_page_config(page_title="ER 2월 근무 조회", page_icon="📅")

st.title("📅 2월 비외상 듀티 조회")
st.markdown("조회하고 싶은 날짜를 선택하면 **D, E, N 근무자**가 표시됩니다.")

# 3. 달력 위젯 (2025년 2월 기준)
# 2월 1일부터 28일 사이만 선택 가능하게 제한
selected_date = st.date_input(
    "날짜를 선택하세요",
    value=date(2025, 2, 1),
    min_value=date(2025, 2, 1),
    max_value=date(2025, 2, 28)
)

# 4. 데이터 조회 및 분류
target_day = str(selected_date.day)

# 듀티별 명단 추출 (OF, 교, 연 등 제외)
d_list = df[df[target_day] == 'D']['성명'].tolist()
e_list = df[df[target_day] == 'E']['성명'].tolist()
n_list = df[df[target_day] == 'N']['성명'].tolist()

st.divider()
st.subheader(f"🔍 2월 {target_day}일 근무 현황")

# 5. 결과 레이아웃 (3단 컬럼)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### ☀️ Day")
    if d_list:
        for i, name in enumerate(d_list, 1):
            st.write(f"{i}. {name}")
    else:
        st.write("근무자 없음")

with col2:
    st.markdown("### ⛅ Evening")
    if e_list:
        for i, name in enumerate(e_list, 1):
            st.write(f"{i}. {name}")
    else:
        st.write("근무자 없음")

with col3:
    st.markdown("### 🌙 Night")
    if n_list:
        for i, name in enumerate(n_list, 1):
            st.write(f"{i}. {name}")
    else:
        st.write("근무자 없음")

# (선택 사항) 비고란 - 교육 인원만 따로 표시
edu_list = df[df[target_day] == '교']['성명'].tolist()
if edu_list:
    st.info(f"📝 **비고(교육):** {', '.join(edu_list)}")
