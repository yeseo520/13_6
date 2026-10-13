import streamlit as st

st.set_page_config(
    page_title="쉬운 키오스크 사용 안내",
    page_icon="🍽️",
    layout="centered"
)

st.markdown("""
<style>
html, body, [class*="css"] {
    font-size: 22px !important;
}
h1 {
    font-size: 38px !important;
    text-align: center;
}
h2 {
    font-size: 30px !important;
}
p, label {
    font-size: 23px !important;
}
.stButton > button {
    width: 100%;
    min-height: 65px;
    font-size: 24px;
    font-weight: bold;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

st.title("🍽️ 쉬운 키오스크 사용 안내")
st.subheader("천천히 따라 해 보세요!")

st.info("💡 큰 버튼을 누르며 한 단계씩 따라오세요.")

menus = {
    "☕ 아메리카노": 3000,
    "🥤 카페라떼": 4000,
    "🍵 녹차": 3500,
    "🧃 오렌지주스": 4000
}

if "step" not in st.session_state:
    st.session_state.step = 0
if "menu" not in st.session_state:
    st.session_state.menu = ""
if "size" not in st.session_state:
    st.session_state.size = "보통"
if "quantity" not in st.session_state:
    st.session_state.quantity = 1
if "payment" not in st.session_state:
    st.session_state.payment = ""

steps = [
    "1. 메뉴 선택",
    "2. 옵션 선택",
    "3. 주문 확인",
    "4. 결제",
    "5. 주문 완료"
]

st.progress((st.session_state.step + 1) / 5)
st.header(steps[st.session_state.step])

# 1단계: 메뉴 선택
if st.session_state.step == 0:
    st.write("👆 드시고 싶은 메뉴를 선택하세요.")

    for name, price in menus.items():
        if st.button(f"{name}  |  {price:,}원", key=name):
            st.session_state.menu = name
            st.session_state.step = 1
            st.rerun()

# 2단계: 옵션 선택
elif st.session_state.step == 1:
    st.success(f"선택한 메뉴: {st.session_state.menu}")
    st.write("👆 음료 크기와 수량을 선택하세요.")

    st.session_state.size = st.radio(
        "음료 크기",
        ["작게", "보통", "크게"],
        index=["작게", "보통", "크게"].index(
            st.session_state.size
        )
    )

    st.session_state.quantity = st.selectbox(
        "주문 수량",
        [1, 2, 3, 4, 5],
        index=st.session_state.quantity - 1
    )

    if st.button("다음: 주문 확인"):
        st.session_state.step = 2
        st.rerun()

# 금액 계산
extra = 500 if st.session_state.size == "크게" else 0
total = (
    menus.get(st.session_state.menu, 0) + extra
) * st.session_state.quantity

# 3단계: 주문 확인
elif st.session_state.step == 2:
    st.write("👀 주문 내역을 확인하세요.")

    st.markdown(f"""
    ### 🧾 주문 내역
    - 메뉴: {st.session_state.menu}
    - 크기: {st.session_state.size}
    - 수량: {st.session_state.quantity}개
    - 총 금액: **{total:,}원**
    """)

    if st.button("주문 확인하고 결제하기"):
        st.session_state.step = 3
        st.rerun()

# 4단계: 결제
elif st.session_state.step == 3:
    st.write(f"💰 결제할 금액: {total:,}원")
    st.write("결제 방법을 선택하세요.")

    st.session_state.payment = st.radio(
        "결제 방법",
        ["신용카드", "체크카드", "현금"]
    )

    st.warning("교육용 프로그램이며 실제 결제는 진행되지 않습니다.")

    if st.button("결제 연습 완료"):
        st.session_state.step = 4
        st.rerun()

# 5단계: 주문 완료
elif st.session_state.step == 4:
    st.success("🎉 주문이 완료되었습니다!")
    st.header("주문 완료")

    st.write(f"메뉴: {st.session_state.menu}")
    st.write(f"크기: {st.session_state.size}")
    st.write(f"수량: {st.session_state.quantity}개")
    st.write(f"결제 방법: {st.session_state.payment}")
    st.write(f"총 금액: {total:,}원")

    st.info("실제 매장에서는 주문 번호나 영수증을 확인하세요.")
    st.balloons()

    if st.button("처음부터 다시 연습하기"):
        for key in [
            "step", "menu", "size", "quantity", "payment"
        ]:
            del st.session_state[key]
        st.rerun()

# 이전 단계로 이동
if 0 < st.session_state.step < 4:
    if st.button("⬅️ 이전 단계로 돌아가기"):
        st.session_state.step -= 1
        st.rerun()
```
