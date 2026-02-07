import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="ER 근무 조회 시스템", page_icon="📅")

@st.cache_data
def load_data():
    try:
        # CSV 로드 및 데이터 정제
        df = pd.read_csv("duty_data.csv")
        df.columns = df.columns.str.strip()
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        return df
    except Exception as e:
        st.error(f"파일 오류: {e}")
        return None

df = load_data()

if df is not None:
    st.title("📅 ER 비외상 근무 조회")
    
    selected_date = st.date_input("날짜 선택", value=date.today())
    target_day = str(selected_date.day)

    if target_day in df.columns:
        # 각 리스트 초기화
        d_list, e_list, n_list, edu_list = [], [], [], []

        # 한 줄씩 읽으면서 이름과 해당 날짜 근무를 매칭
        for _, row in df.iterrows():
            name = row['성명']  # 정확히 '성명' 컬럼에서 이름을 가져옴
            duty = str(row[target_day])

            if duty == 'D' or (name == '홍민정' and duty == 'H'):
                d_list.append(name)
            elif duty == 'E':
                e_list.append(name)
            elif duty == 'N':
                n_list.append(name)
            elif duty == '교':
                edu_list.append(name)

        st.divider()
        st.subheader(f"🔍 {selected_date.month}월 {target_day}일 근무 현황")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.success("☀️ Day")
            if d_list:
                for i, n in enumerate(d_list, 1): st.write(f"{i}. {n}")
            else: st.write("-")

        with col2:
            st.warning("⛅ Evening")
            if e_list:
                for i, n in enumerate(e_list, 1): st.write(f"{i}. {n}")
            else: st.write("-")

        with col3:
            st.error("🌙 Night")
            if n_list:
                for i, n in enumerate(n_list, 1): st.write(f"{i}. {n}")
            else: st.write("-")

        if edu_list:
            st.info(f"📝 **교육:** {', '.join(edu_list)}")
