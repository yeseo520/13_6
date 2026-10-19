
import streamlit as st

st.set_page_config(
    page_title="쉬운 키오스크",
    page_icon="☕",
    layout="centered",
)

FONT_SIZES = {
    "보통": 18,
    "크게": 24,
    "아주 크게": 30,
}

MENU = {
    "아메리카노": 2500,
    "카페라떼": 3500,
    "녹차": 3000,
    "핫초코": 3500,
}

# 세션 상태 초기화
if "font_choice" not in st.session_state:
    st.session_state.font_choice = "크게"

if "cart" not in st.session_state:
    st.session_state.cart = {}

if "notice" not in st.session_state:
    st.session_state.notice = ""

# 현재 글자 크기 적용
font_size = FONT_SIZES[st.session_state.font_choice]

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: #F5F8FC;
        color: #172033;
    }}

    html, body, [class*="st-"] {{
        font-size: {font_size}px;
    }}

    h1 {{
        font-size: {font_size * 1.6}px !important;
        color: #174A8B !important;
    }}

    h2, h3 {{
        color: #174A8B !important;
    }}

    div.stButton > button {{
        min-height: 56px;
        border: 2px solid #174A8B;
        border-radius: 12px;
        font-size: {font_size}px;
        font-weight: bold;
        white-space: normal;
    }}

    div[data-testid="stMarkdownContainer"] p {{
        font-size: {font_size}px;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("☕ 쉬운 키오스크")
st.write("원하는 글자 크기를 선택하고 편하게 주문하세요.")

# 글자 크기 조절
st.subheader("🔎 글자 크기 조절")
size_columns = st.columns(3)

for i, size_name in enumerate(FONT_SIZES):
    with size_columns[i]:
        if st.button(
            size_name,
            key="font_" + size_name,
            type=(
                "primary"
                if st.session_state.font_choice == size_name
                else "secondary"
            ),
            use_container_width=True,
        ):
            st.session_state.font_choice = size_name
            st.rerun()

st.info("현재 글자 크기: " + st.session_state.font_choice)

st.divider()

# 메뉴 선택
st.header("1. 메뉴 선택")
menu_columns = st.columns(2)

for i, (name, price) in enumerate(MENU.items()):
    with menu_columns[i % 2]:
        st.subheader(name)
        st.write(f"{price:,}원")

        if st.button(
            name + " 담기",
            key="add_" + name,
            use_container_width=True,
        ):
            st.session_state.cart[name] = (
                st.session_state.cart.get(name, 0) + 1
            )
            st.session_state.notice = name + " 메뉴를 담았습니다."
            st.rerun()

if st.session_state.notice:
    st.success(st.session_state.notice)

st.divider()

# 장바구니
st.header("2. 주문 확인")

if not st.session_state.cart:
    st.info("선택한 메뉴가 없습니다.")
else:
    total = 0

    for name in list(st.session_state.cart.keys()):
        quantity = st.session_state.cart[name]
        subtotal = MENU[name] * quantity
        total += subtotal

        left, right = st.columns([3, 1])

        with left:
            st.write(
                f"**{name}** — {quantity}개 "
                f"({subtotal:,}원)"
            )

        with right:
            if st.button("1개 삭제", key="del_" + name):
                st.session_state.cart[name] -= 1

                if st.session_state.cart[name] <= 0:
                    del st.session_state.cart[name]

                st.rerun()

    st.subheader(f"총 결제 금액: {total:,}원")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("장바구니 비우기", use_container_width=True):
            st.session_state.cart = {}
            st.session_state.notice = "장바구니를 비웠습니다."
            st.rerun()

    with col2:
        if st.button(
            "주문 확인하기",
            type="primary",
            use_container_width=True,
        ):
            st.success(
                f"주문 확인 완료! 총 {total:,}원입니다. "
                "실제 결제는 진행되지 않았습니다."
            )

st.divider()
st.caption("키오스크 연습용 앱 · 실제 결제 기능 없음")
