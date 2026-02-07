import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="ER 근무 조회 시스템", page_icon="📅")

@st.cache_data
def load_data():
    try:
        # 데이터 로드 시 앞뒤 공백을 제거하는 str.strip() 적용
        df = pd.read_csv("duty_data.csv")
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].str.strip()
        return df
    except FileNotFoundError:
        st.error("데이터 파일(duty_data.csv)을 찾을 수 없습니다.")
        return None

df = load_data()

if df is not None:
    st.title("📅 ER 비외상 근무 조회")
    
    selected_date = st.date_input("조회할 날짜를 선택하세요", value=date.today())
    target_day = str(selected_date.day)

    if target_day in df.columns:
        # 1. Day 명단 추출: 'D'인 사람 + (홍민정이고 'H'인 사람)
        d_mask = (df[target_day] == 'D') | ((df['성명'] == '홍민정') & (df[target_day] == 'H'))
        d_list = df[d_mask]['성명'].tolist()
        
        # 2. Evening/Night/교육 명단 (공백에 강해짐)
        e_list = df[df[target_day] == 'E']['성명'].tolist()
        n_list = df[df[target_day] == 'N']['성명'].tolist()
        edu_list = df[df[target_day] == '교']['성명'].tolist()

        st.divider()
        st.subheader(f"🔍 {selected_date.month}월 {target_day}일 근무 현황")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("### ☀️ Day")
            if d_list:
                for i, name in enumerate(d_list, 1): st.write(f"{i}. {name}")
            else: st.write("-")

        with col2:
            st.markdown("### ⛅ Evening")
            if e_list:
                for i, name in enumerate(e_list, 1): st.write(f"{i}. {name}")
            else: st.write("-")

        with col3:
            st.markdown("### 🌙 Night")
            if n_list:
                for i, name in enumerate(n_list, 1): st.write(f"{i}. {name}")
            else: st.write("-")

        if edu_list:
            st.info(f"📝 **비고(교육):** {', '.join(edu_list)}")
            
    else:
        st.warning(f"해당 날짜({target_day}일)에 대한 데이터가 없습니다.")
