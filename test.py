import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
# -------------------------------
# 샘플 음식 데이터
# -------------------------------
food_data = {
    "김밥": {"탄수화물": 45, "단백질": 8, "지방": 9},
    "치킨": {"탄수화물": 20, "단백질": 25, "지방": 30},
    "샐러드": {"탄수화물": 10, "단백질": 5, "지방": 7},
    "라면": {"탄수화물": 65, "단백질": 10, "지방": 15},
    "떡볶이": {"탄수화물": 70, "단백질": 7, "지방": 10}
}

# 건강식 추천 데이터 (간단)
healthy_foods = {
    "탄수화물": ["샐러드", "두부", "현미밥"],
    "단백질": ["닭가슴살", "달걀", "두부"],
    "지방": ["아몬드", "연어", "아보카도"]
}

# -------------------------------
# Streamlit 앱
# -------------------------------
st.title("🥗 식단 균형 분석기")

menu = st.text_input("먹은 음식을 입력하세요 (예: 김밥, 치킨, 샐러드, 라면, 떡볶이)")

if menu:
    if menu in food_data:
        nutrients = food_data[menu]
        st.subheader(f"'{menu}'의 영양 성분")
        st.write(nutrients)

        # 차트
        chart_data = pd.DataFrame({
            "영양소": ["탄수화물", "단백질", "지방"],
            "값": [nutrients["탄수화물"], nutrients["단백질"], nutrients["지방"]]
        })
        st.bar_chart(chart_data.set_index("영양소"))

        # 개선점
        suggestion = ""
        carb, protein, fat = nutrients["탄수화물"], nutrients["단백질"], nutrients["지방"]

        # 기준: 탄:단:지 = 50:30:20
        if carb > 60:
            suggestion += "- 탄수화물이 많아요. 채소나 단백질을 더 추가해보세요.\n"
        if protein < 15:
            suggestion += "- 단백질이 부족해요. 달걀, 두부, 닭가슴살을 곁들여 보세요.\n"
        if fat > 25:
            suggestion += "- 지방이 많아요. 기름진 음식은 조금 줄이는 게 좋아요.\n"
        if suggestion == "":
            suggestion = "균형 잡힌 식단이에요! 👍"

        st.subheader("개선할 점")
        st.write(suggestion)

        # 비슷한 건강식 추천
        st.subheader("비슷한 건강식 추천")
        for key, foods in healthy_foods.items():
            st.write(f"{key} 보충 추천: {', '.join(foods)}")

    else:
        st.warning("데이터에 없는 음식이에요. (예: 김밥, 치킨, 샐러드, 라면, 떡볶이)")
