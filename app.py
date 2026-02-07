import streamlit as st
import pandas as pd
from datetime import date

# 1. 페이지 기본 설정
st.set_page_config(page_title="ER 근무 조회 시스템", page_icon="📅", layout="wide")

@st.cache_data
def load_and_clean_data():
    try:
        # 데이터 로드
        df = pd.read_csv("duty_data.csv")
        
        # [방어 로직 1] 컬럼명 앞뒤 공백 제거 (날짜 ' 8' 등 오타 방지)
        df.columns = [str(col).strip() for col in df.columns]
        
        # [방어 로직 2] 데이터 내용 앞뒤 공백 제거 (' D' 등 오타 방지)
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        
        return df
    except Exception as e:
        st.error(f"데이터 파일을 읽는 중 오류가 발생했습니다: {e}")
        return None

df = load_and_clean_data()

# 제목 섹션
st.title("📅 ER 비외상 근무 현황")
st.info("CSV 파일의 '성명' 열과 '날짜(1~28)' 열을 대조하여 근무자를 표시합니다.")

if df is not None:
    # 2. 날짜 선택
    selected_date = st.date_input("조회할 날짜를 선택하세요", value=date(today=True))
    target_day = str(selected_date.day) # 선택한 '일'을 문자열로 변환

    if target_day in df.columns:
        # 3. 근무자 분류 리스트
        day_workers = []
        evening_workers = []
        night_workers = []
        edu_workers = []

        # 4. 데이터 분석 (한 줄씩 검사)
        for i, row in df.iterrows():
            name = str(row['성명'])   # '성명' 컬럼에서 이름 추출
            duty = str(row[target_day]) # 선택한 날짜 컬럼에서 근무 기호 추출

            # [핵심 로직] 근무 기호에 따른 분류
            # 홍민정 선생님의 'H'는 Day(D)로 간주하는 예외 처리 포함
            if duty == 'D' or (name == '홍민정' and duty == 'H'):
                day_workers.append(name)
            elif duty == 'E':
                evening_workers.append(name)
            elif duty == 'N':
                night_workers.append(name)
            elif duty == '교':
                edu_workers.append(name)

        # 5. 화면 출력
        st.subheader(f"🔍 {selected_date.month}월 {target_day}일 근무 명단")
        
        col1, col2, col3 = st.columns(3)

        with col1:
            st.success("☀️ **DAY**")
            if day_workers:
                for idx, name in enumerate(day_workers, 1):
                    st.write(f"**{idx}. {name}**") # 이름이 굵게 표시됨
            else:
                st.write("근무자 없음")

        with col2:
            st.warning("⛅ **EVENING**")
            if evening_workers:
                for idx, name in enumerate(evening_workers, 1):
                    st.write(f"**{idx}. {name}**")
            else:
                st.write("근무자 없음")

        with col3:
            st.error("🌙 **NIGHT**")
            if night_workers:
                for idx, name in enumerate(night_workers, 1):
                    st.write(f"**{idx}. {name}**")
            else:
                st.write("근무자 없음")

        # 교육 인원 별도 표시
        if edu_workers:
            st.divider()
            st.write(f"📝 **교육(교):** {', '.join(edu_workers)}")
            
    else:
        st.error(f"데이터 파일에 '{target_day}'일 컬럼이 없습니다. CSV 헤더를 확인해주세요.")

# 하단 도움말
st.caption("※ 홍민정 선생님의 'H' 근무는 Day 명단에 포함되어 표시됩니다.")
