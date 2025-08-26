# app.py 파일
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
        
        # streamlit 내장 차트 기능 사용
        if st.button('차트로 보기'):
            for nutrient in nutrients:
                st.subheader(f'{nutrient} 함량')
                st.bar_chart(recommended.set_index('음식')[nutrient])
    except Exception as e:
        st.error(f"오류 발생: {e}")
else:
    st.write("영양소를 선택하면 음식 추천이 나옵니다.")
