import streamlit as st
import pandas as pd

# 예시 데이터
food_data = pd.DataFrame({
    '음식': ['계란', '시금치', '연어', '두부', '오렌지'],
    '단백질': [6, 2, 20, 8, 1],
    '비타민 C': [0, 28, 0, 0, 53],
    '철분': [1, 2, 1, 3, 0.1]
})

st.title("영양소 맞춤 메뉴 추천")

# 부족한 영양소 선택
nutrients = st.multiselect(
    "부족한 영양소를 선택하세요",
    ['단백질', '비타민 C', '철분']
)

if nutrients:
    # 선택한 영양소 기준으로 음식 추천
    try:
        recommended = food_data.sort_values(by=nutrients, ascending=False)
        st.write("추천 음식:")
        st.dataframe(recommended[['음식'] + nutrients])
    except Exception as e:
        st.error(f"추천 음식 불러오기 중 오류 발생: {e}")
else:
    st.write("영양소를 선택하면 음식 추천이 나옵니다.")
