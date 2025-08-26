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

# 슬라이더로 최소 영양소 기준 설정
if nutrients:
    st.subheader("영양소 최소 기준 설정")
    min_values = {}
    
    for nutrient in nutrients:
        min_val = st.slider(
            f"{nutrient} 최소 기준",
            min_value=0,
            max_value=int(food_data[nutrient].max()),
            value=0
        )
        min_values[nutrient] = min_val
    
    # 필터링된 음식 추천
    filtered_foods = food_data.copy()
    for nutrient, min_val in min_values.items():
        filtered_foods = filtered_foods[filtered_foods[nutrient] >= min_val]
    
    # 선택한 영양소 기준으로 정렬
    if not filtered_foods.empty:
        recommended = filtered_foods.sort_values(by=nutrients, ascending=False)
        st.success(f"총 {len(recommended)}개의 음식이 추천되었습니다!")
        st.dataframe(recommended[['음식'] + nutrients])
        
        # 시각화 추가
        st.subheader("영양소 비교 차트")
        chart_data = recommended.set_index('음식')[nutrients]
        st.bar_chart(chart_data)
    else:
        st.warning("설정한 기준에 맞는 음식이 없습니다. 기준을 낮춰보세요.")
else:
    st.info("영양소를 선택하면 음식 추천이 나옵니다.")
    
# 새 음식 추가 기능
st.sidebar.header("새로운 음식 추가")
new_food = st.sidebar.text_input("음식 이름")
new_protein = st.sidebar.number_input("단백질 (g)", min_value=0.0, step=0.1)
new_vitamin_c = st.sidebar.number_input("비타민 C (mg)", min_value=0.0, step=0.1)
new_iron = st.sidebar.number_input("철분 (mg)", min_value=0.0, step=0.1)

if st.sidebar.button("음식 추가"):
    if new_food:
        # 실제로는 데이터를 저장하는 로직이 필요합니다
        st.sidebar.success(f"{new_food}이(가) 추가되었습니다!")
    else:
        st.sidebar.error("음식 이름을 입력해주세요.")
