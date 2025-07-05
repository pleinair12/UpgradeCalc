import streamlit as st
import random

st.set_page_config(page_title="로스트사가 강화 시뮬레이터", layout="centered")

st.title("로스트사가 강화 시뮬레이터")
st.markdown("시작 강화 수치부터 목표 수치까지의 평균 **페소** 및 **차원조각** 소비량을 시뮬레이션합니다.")

# 강화 데이터
enhance_data = {
    0: (50.0, 100.0), 1: (50.0, 100.0), 2: (50.0, 100.0), 3: (50.0, 100.0), 4: (50.0, 100.0),
    5: (20.0, 80.0), 6: (20.0, 80.0), 7: (20.0, 80.0), 8: (20.0, 80.0), 9: (20.0, 80.0),
    10: (10.0, 60.0), 11: (10.0, 60.0), 12: (10.0, 60.0), 13: (10.0, 60.0), 14: (10.0, 60.0),
    15: (5.0, 40.0),
    16: (2.5, 20.0),
    17: (1.67, 13.33),
    18: (1.25, 10.0),
    19: (1.0, 8.0),
    20: (0.67, 6.67),
    21: (0.5, 5.0),
    22: (0.33, 3.33),
    23: (0.25, 2.5),
    24: (0.17, 1.67),
    25: (29.94, 0.0), 26: (29.94, 0.0), 27: (29.94, 0.0), 28: (29.94, 0.0), 29: (29.94, 0.0)
}

def get_peso_cost(level):
    if 0 <= level <= 4:
        return 4500
    elif 5 <= level <= 9:
        return 5000
    elif 10 <= level <= 14:
        return 5500
    elif 15 <= level <= 19:
        return 6000
    elif 20 <= level <= 24:
        return 6500
    elif 25 <= level <= 29:
        return 4000
    else:
        return 0

def simulate_enhance(start_level, end_level):
    peso_total = 0
    crystal_total = 0

    for level in range(start_level, end_level):
        success_rate, fail_exp = enhance_data[level]
        current_rate = success_rate

        while True:
            peso_total += get_peso_cost(level)
            if level >= 25:
                crystal_total += 250

            if random.random() * 100 < current_rate:
                break
            else:
                if fail_exp > 0:
                    current_rate = min(current_rate + fail_exp, 100.0)

    return peso_total, crystal_total

# Streamlit UI
st.sidebar.header("시뮬레이션 설정")
start_level = st.sidebar.number_input("시작 강화 수치", min_value=0, max_value=29, value=10)

# end_level의 기본값은 start_level+1 이상이어야 하므로 동적으로 설정
default_end = max(start_level + 1, 20)
end_level = st.sidebar.number_input("목표 강화 수치", min_value=start_level + 1, max_value=30, value=default_end)
simulations = st.sidebar.number_input("시뮬레이션 반복 횟수", min_value=1, max_value=10000, value=1000)

if st.sidebar.button("강화 시뮬레이션 시작"):
    with st.spinner("시뮬레이션 중..."):
        total_peso = 0
        total_crystal = 0

        for _ in range(simulations):
            peso, crystal = simulate_enhance(start_level, end_level)
            total_peso += peso
            total_crystal += crystal

        avg_peso = total_peso / simulations
        avg_crystal = total_crystal / simulations

        st.success(f" {start_level}강 → {end_level}강 시뮬레이션 결과 (평균값)")
        st.metric("평균 페소 소모량", f"{avg_peso:,.0f} 페소")
        st.metric("평균 차원조각 소모량", f"{avg_crystal:,.2f} 개")

        st.caption(f"{simulations:,}회의 시뮬레이션을 기준으로 한 평균값입니다.")

