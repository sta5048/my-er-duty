import streamlit as st
import datetime
import os

st.set_page_config(page_title="ER 근무 조회", layout="wide")

# CSS를 사용하여 화면이 좁아져도 강제로 가로 배치를 유지하게 만듭니다.
st.markdown("""
    <style>
    [data-testid="column"] {
        min-width: 150px !important;
    }
    </style>
    """, unsafe_allow_html=True)

def load_duty(selected_date):
    filename = f"data/duty_{selected_date.year}_{selected_date.month:02d}.csv"
    if not os.path.exists(filename): return None
    with open(filename, "r", encoding="utf-8") as f:
        return [line.strip().split(",") for line in f]

st.title("📅 ER 근무 조회")
selected_date = st.date_input("날짜 선택", datetime.date.today())
day = selected_date.day
duty_list = load_duty(selected_date)

if duty_list:
    teams = {
        "비외상": {"D": [], "E": [], "N": [], "S": [], "hmj": None},
        "외상": {"D": [], "E": [], "N": [], "S": [], "hmj": None}
    }

    for row in duty_list[1:]:
        if len(row) > day:
            raw_name, work = row[0], row[day]
            team_key = "외상" if "*" in raw_name else "비외상"
            clean_name = raw_name.replace("*", "")
            target = teams[team_key]
            
            if work == 'D': target["D"].append(clean_name)
            elif work == 'E': target["E"].append(clean_name)
            elif work == 'N': target["N"].append(clean_name)
            elif work == 'S': target["S"].append(clean_name)
            elif "홍민정" in clean_name and work != 'OF': target["hmj"] = work

    # 메인 화면을 비외상/외상으로 크게 나눕니다.
    # gap="small"을 주어 공간 낭비를 줄입니다.
    main_cols = st.columns(2, gap="medium")

    for i, team_label in enumerate(["비외상", "외상"]):
        with main_cols[i]:
            st.subheader(f"🏥 {team_label}")
            t_data = teams[team_label]
            
            # D, E, N 열을 더 촘촘하게 배치
            d_col, e_col, n_col = st.columns(3)
            
            with d_col:
                st.markdown("### :green[D]")
                if t_data["S"]:
                    for s in t_data["S"]: st.write(f"🚩**S:{s}**")
                if t_data["hmj"]: st.write(f"✨**홍민정:{t_data['hmj']}**")
                for j, n in enumerate(t_data["D"], 1): st.write(f"{j}.{n}")
                
            with e_col:
                st.markdown("### :orange[E]")
                for j, n in enumerate(t_data["E"], 1): st.write(f"{j}.{n}")
                
            with n_col:
                st.markdown("### :red[N]")
                for j, n in enumerate(t_data["N"], 1): st.write(f"{j}.{n}")
            st.divider()
