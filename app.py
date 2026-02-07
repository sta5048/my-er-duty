import streamlit as st
import pandas as pd
from datetime import date

# 페이지 설정
st.set_page_config(page_title="ER 근무 조회 시스템", page_icon="📅")

# 외부 CSV 파일 불러오기
@st.cache_data
def load_data():
    try:
        # 같은 폴더에 있는 duty_data.csv를 읽어옵니다.
        return pd.read_csv("duty_data.csv")
    except FileNotFoundError:
        st.error("데이터 파일(duty_data.csv)을 찾을 수 없습니다.")
        return None

df = load_data()

if df is not None:
    st.title("📅 ER 비외상 근무 조회")
    st.markdown("날짜를 선택하면 해당 날짜의 **D, E, N 근무자**를 확인할 수 있습니다.")

    # 날짜 선택 위젯
    selected_date = st.date_input(
        "조회할 날짜를 선택하세요",
        value=date.today(),
    )

    # 선택한 날짜의 '일' 추출
    target_day = str(selected_date.day)

    if target_day in df.columns:
        # 듀티별 명단 추출 (OF, 교, 연 등은 자동 제외됨)
        d_list = df[df[target_day] == 'D']['성명'].tolist()
        e_list = df[df[target_day] == 'E']['성명'].tolist()
        n_list = df[df[target_day] == 'N']['성명'].tolist()
        edu_list = df[df[target_day] == '교']['성명'].tolist()

        st.divider()
        st.subheader(f"🔍 {selected_date.month}월 {target_day}일 근무 현황")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("### ☀️ Day")
            if d_list:
                for i, name in enumerate(d_list, 1):
                    st.write(f"{i}. {name}")
            else:
                st.write("-")

        with col2:
            st.markdown("### ⛅ Evening")
            if e_list:
                for i, name in enumerate(e_list, 1):
                    st.write(f"{i}. {name}")
            else:
                st.write("-")

        with col3:
            st.markdown("### 🌙 Night")
            if n_list:
                for i, name in enumerate(n_list, 1):
                    st.write(f"{i}. {name}")
            else:
                st.write("-")

        if edu_list:
            st.info(f"📝 **비고(교육):** {', '.join(edu_list)}")
    else:
        st.warning(f"해당 날짜({target_day}일)에 대한 데이터가 엑셀 파일에 없습니다.")
