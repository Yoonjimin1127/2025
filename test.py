import streamlit as st
import pandas as pd

# -------------------------------
# 1. 식단 균형 분석기
# -------------------------------
food_data = {
    "김밥": {"칼로리": 300, "탄수화물": 45, "단백질": 8, "지방": 9},
    "치킨": {"칼로리": 500, "탄수화물": 20, "단백질": 25, "지방": 30},
    "샐러드": {"칼로리": 150, "탄수화물": 10, "단백질": 5, "지방": 7},
    "라면": {"칼로리": 450, "탄수화물": 65, "단백질": 10, "지방": 15},
    "떡볶이": {"칼로리": 400, "탄수화물": 70, "단백질": 7, "지방": 10}
}

def diet_balance():
    st.header("🍽️ 식단 균형 분석기")

    menu = st.text_input("먹은 음식을 입력하세요 (예: 김밥, 치킨, 샐러드, 라면, 떡볶이)")

    if menu in food_data:
        nutrients = food_data[menu]

        st.subheader(f"'{menu}'의 영양 성분")
        st.write(nutrients)

        # ✅ matplotlib 대신 Streamlit 내장 차트 사용
        chart_data = pd.DataFrame({
            "영양소": ["탄수화물", "단백질", "지방"],
            "값": [nutrients["탄수화물"], nutrients["단백질"], nutrients["지방"]]
        })
        st.bar_chart(chart_data.set_index("영양소"))

        # 개선 제안
        carb, protein, fat = nutrients["탄수화물"], nutrients["단백질"], nutrients["지방"]
        suggestion = ""

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

    elif menu != "":
        st.warning("데이터에 없는 음식이에요. (예: 김밥, 치킨, 샐러드, 라면, 떡볶이)")
