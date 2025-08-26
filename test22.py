import streamlit as st
import pandas as pd

# 예시 데이터
food_data = pd.DataFrame({
    '음식': ['계란', '시금치', '연어', '두부', '오렌지', '아몬드'],
    '단백질': [6, 2, 20, 8, 1, 6],
    '비타민 C': [0, 28, 0, 0, 53, 0],
    '칼슘': [50, 99, 12, 350, 40, 269],
    '철분': [1.2, 2.7, 0.8, 2.0, 0.1, 3.7],
    '설명': [
        '단백질이 풍부한 기본 식품',
        '비타민과 철분이 많은 녹색 채소',
        '단백질과 오메가3가 풍부한 생선',
        '단백질과 칼슘이 풍부한 두부',
        '비타민 C가 많은 과일',
        '단백질과 건강한 지방이 풍부한 견과류'
    ]
})

st.title("🍽 영양소 기반 메뉴 추천")

# 부족한 영양소 선택
nutrient = st.selectbox("어떤 영양소가 부족한가요?", ['단백질', '비타민 C', '칼슘', '철분'])

# 선택한 영양소 기준으로 상위 5개 음식 추천
top_foods = food_data.sort_values(by=nutrient, ascending=False).head(5)

st.subheader(f"{nutrient}가 풍부한 추천 메뉴")
for _, row in top_foods.iterrows():
    st.markdown(f"### {row['음식']}")
    st.write(f"**{nutrient}:** {row[nutrient]}")
    st.write(f"{row['설명']}")
    st.markdown("---")
