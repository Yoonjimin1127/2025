import streamlit as st

# ----- 스타일 (CSS 추가) -----
page_bg = """
<style>
body {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    color: #FFFFFF;
}
h1, h2, h3, h4 {
    font-family: 'Orbitron', sans-serif;
    text-shadow: 0 0 10px #00f5ff, 0 0 20px #00f5ff;
}
.stButton>button {
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    color: white;
    border-radius: 12px;
    border: none;
    padding: 10px 20px;
    font-size: 18px;
    box-shadow: 0 0 10px #00f5ff;
}
.stSelectbox label {
    font-size: 18px;
    font-weight: bold;
    color: #00f5ff;
}
.result-card {
    background: rgba(255,255,255,0.1);
    border-radius: 15px;
    padding: 20px;
    margin-top: 20px;
    box-shadow: 0 0 15px rgba(0,245,255,0.6);
    font-size: 20px;
    text-align: center;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ----- 데이터 -----
mbti_food = {
    "INTJ": "🥩 스테이크 — 겉은 단단하지만 속은 깊고 진한 맛을 가진 유형!",
    "INTP": "🍜 라면 — 언제든지 편하고 자유롭게 즐길 수 있는 유연한 성격!",
    "ENTJ": "🌶 불닭볶음면 — 강렬하고 리더십이 넘치는 불같은 카리스마!",
    "ENTP": "🌮 타코 — 어디서든 어울리고 새로운 조합을 즐기는 타입!",
    "INFJ": "🍵 녹차 — 은은하면서도 오래 기억에 남는 따뜻한 기운!",
    "INFP": "🍬 마카롱 — 달콤하고 감성적인 예술가 같은 영혼!",
    "ENFJ": "🍲 떡볶이 — 따뜻하게 사람들을 모으는 친근한 매력!",
    "ENFP": "🍦 아이스크림 — 다채롭고 어디서나 즐거움을 주는 자유로운 성격!",
    "ISTJ": "🍚 백반정식 — 기본에 충실하고 안정적인 신뢰감을 주는 타입!",
    "ISFJ": "🥘 된장찌개 — 가족적이고 따뜻한 마음을 가진 헌신적인 존재!",
    "ESTJ": "🥓 삼겹살 — 확실하고 든든하게 모두를 책임지는 리더!",
    "ESFJ": "🍰 케이크 — 함께할 때 가장 빛나고 분위기를 밝히는 사람!",
    "ISTP": "🍫 초콜릿 — 간단하면서도 묘하게 중독적인 매력!",
    "ISFP": "🥗 샐러드 — 자연스럽고 자유롭게 자신을 표현하는 타입!",
    "ESTP": "🍗 치킨 — 언제 어디서나 인기 만점, 에너지 넘치는 성격!",
    "ESFP": "🍕 피자 — 파티의 중심, 어디서든 즐거움을 나누는 타입!"
}

# ----- UI -----
st.title("🌌 MBTI X FOOD EXPLORER")
st.write("당신의 MBTI를 선택하면, 음식으로 비유한 당신의 모습이 나타납니다 🚀")

# MBTI 선택
mbti = st.selectbox("당신의 MBTI를 선택하세요", list(mbti_food.keys()))

# 결과
if st.button("✨ 결과 보기 ✨"):
    st.markdown(f"""
    <div class="result-card">
        <h2>당신의 MBTI ({mbti})</h2>
        <p>{mbti_food[mbti]}</p>
    </div>
    """, unsafe_allow_html=True)

