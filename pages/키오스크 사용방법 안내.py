

### `app.py`

python
```

import streamlit as st

st.set_page_config(
    page_title="쉬운 키오스크",
    page_icon="☕",
    layout="centered"
)

# 화면 설정
st.markdown("""
<style>
.stApp {
    background-color: #FFFDF5;
}
h1 {
    font-size: 36px !important;
    text-align: center;
    color: #333333;
}
h2 {
    font-size: 28px !important;
}
p, label, div {
    font-size: 20px;
}
.stButton > button {
    width: 100%;
    min-height: 60px;
    font-size: 22px;
    font-weight: bold;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

st.title("☕ 쉬운 키오스크")
st.subheader("어르신을 위한 키오스크 사용 연습")
st.info("천천히 읽고 큰 버튼을 눌러 보세요.")

MENUS = {
    "아메리카노": 3000,
    "카페라떼": 4000,
    "녹차": 3500,
    "오렌지주스": 4000,
}

# 초기 상태
if "step" not in st.session_state:
    st.session_state.step = 0

if "menu" not in st.session_state:
    st.session_state.menu = ""

if "size" not in st.session_state:
    st.session_state.size = "보통"

if "quantity" not in st.session_state:
    st.session_state.quantity = 1

if "payment" not in st.session_state:
    st.session_state.payment = "신용카드"

step = st.session_state.step

st.progress((step + 1) / 5)

# 1단계: 메뉴 선택
if step == 0:
    st.header("1단계. 메뉴 선택")
    st.write("드시고 싶은 음료를 선택하세요.")

    for menu, price in MENUS.items():
        if st.button(
            f"☕ {menu} - {price:,}원",
            key=f"menu_{menu}"
        ):
            st.session_state.menu = menu
            st.session_state.step = 1
            st.rerun()

# 2단계: 옵션 선택
elif step == 1:
    st.header("2단계. 옵션 선택")
    st.write(f"선택한 메뉴: {st.session_state.menu}")

    st.session_state.size = st.radio(
        "음료 크기를 선택하세요.",
        ["작게", "보통", "크게"],
        index=["작게", "보통", "크게"].index(
            st.session_state.size
        )
    )

    st.session_state.quantity = st.selectbox(
        "주문 수량을 선택하세요.",
        [1, 2, 3, 4, 5],
        index=st.session_state.quantity - 1
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("다음 단계"):
            st.session_state.step = 2
            st.rerun()

    with col2:
        if st.button("메뉴 다시 선택"):
            st.session_state.step = 0
            st.rerun()

# 가격 계산
base_price = MENUS.get(st.session_state.menu, 0)
extra_price = 500 if st.session_state.size == "크게" else 0
total = (
    base_price + extra_price
) * st.session_state.quantity

# 3단계: 주문 확인
elif step == 2:
    st.header("3단계. 주문 확인")

    st.write(f"메뉴: {st.session_state.menu}")
    st.write(f"크기: {st.session_state.size}")
    st.write(f"수량: {st.session_state.quantity}잔")
    st.write(f"총 금액: {total:,}원")

    st.info("주문 내용이 맞는지 확인하세요.")

    if st.button("주문 확인 후 결제"):
        st.session_state.step = 3
        st.rerun()

# 4단계: 결제 연습
elif step == 3:
    st.header("4단계. 결제")
    st.write(f"결제할 금액: {total:,}원")

    st.session_state.payment = st.radio(
        "결제 방법을 선택하세요.",
        ["신용카드", "체크카드", "현금"]
    )

    st.warning(
        "연습용 프로그램입니다. 실제 결제는 진행되지 않습니다."
    )

    if st.button("결제 연습 완료"):
        st.session_state.step = 4
        st.rerun()

# 5단계: 주문 완료
elif step == 4:
    st.header("5단계. 주문 완료")
    st.success("🎉 주문 연습이 완료되었습니다!")

    st.write(f"메뉴: {st.session_state.menu}")
    st.write(f"크기: {st.session_state.size}")
    st.write(f"수량: {st.session_state.quantity}잔")
    st.write(f"결제 방법: {st.session_state.payment}")
    st.write(f"총 금액: {total:,}원")

    st.info(
        "잘하셨습니다! 실제 매장에서는 주문 번호나 영수증을 확인하세요."
    )

    if st.button("처음부터 다시 연습하기"):
        for key in [
            "step",
            "menu",
            "size",
            "quantity",
            "payment"
        ]:
            if key in st.session_state:
                del st.session_state[key]

        st.rerun()

# 이전 단계 버튼
if 0 < step < 4:
    if st.button("⬅️ 이전 단계"):
        st.session_state.step -= 1
        st.rerun()
```
