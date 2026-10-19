
import streamlit as st

st.set_page_config(
    page_title="쉬운 키오스크",
    page_icon="🔎",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# 글자 크기별 설정
FONT_SIZES = {
    "보통": 18,
    "크게": 24,
    "아주 크게": 30,
}

# 메뉴 데이터
MENU = {
    "아메리카노": {"price": 2500, "emoji": "☕"},
    "카페라떼": {"price": 3500, "emoji": "🥛"},
    "녹차": {"price": 3000, "emoji": "🍵"},
    "핫초코": {"price": 3500, "emoji": "🍫"},
}

# 세션 초기화
if "font_size" not in st.session_state:
    st.session_state.font_size = "크게"
if "cart" not in st.session_state:
    st.session_state.cart = {}
if "message" not in st.session_state:
    st.session_state.message = ""

font_size = FONT_SIZES[st.session_state.font_size]

# 글자 크기와 대비를 적용하는 CSS
st.markdown(
    f"""
    <style>
    html, body, [class*="stApp"] {{
        font-size: {font_size}px !important;
    }}

    .stApp {{
        background-color: #F7F9FC;
        color: #172033;
    }}

    h1 {{
        font-size: {font_size * 1.7}px !important;
        color: #153B70 !important;
    }}

    h2, h3 {{
        font-size: {font_size * 1.3}px !important;
        color: #153B70 !important;
    }}

    p, label, .stMarkdown, [data-testid="stCaptionContainer"] {{
        font-size: {font_size}px !important;
    }}

    div.stButton > button {{
        min-height: 58px;
        width: 100%;
        border: 2px solid #2458A6;
        border-radius: 12px;
        background-color: #FFFFFF;
        color: #153B70;
        font-size: {font_size}px !important;
        font-weight: 700;
        white-space: normal;
    }}

    div.stButton > button[kind="primary"] {{
        background-color: #174A8B;
        color: #FFFFFF;
    }}

    [data-testid="stNumberInput"] input {{
        font-size: {font_size}px !important;
    }}

    [data-testid="stAlert"] {{
        font-size: {font_size}px !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

def add_to_cart(name):
    """메뉴를 장바구니에 추가합니다."""
    st.session_state.cart[name] = (
        st.session_state.cart.get(name, 0) + 1
    )
    st.session_state.message = f"{name} 메뉴를 담았습니다."

def remove_from_cart(name):
    """장바구니에서 메뉴 하나를 삭제합니다."""
    if name in st.session_state.cart:
        st.session_state.cart[name] -= 1
        if st.session_state.cart[name] <= 0:
            del st.session_state.cart[name]

def clear_cart():
    st.session_state.cart = {}
    st.session_state.message = "장바구니를 비웠습니다."

try:
    # 상단 제목
    st.title("☕ 쉬운 키오스크")
    st.write("천천히, 편하게 원하는 메뉴를 선택하세요.")

    # 글자 크기 조절 영역
    st.subheader("🔎 글자 크기 조절")
    st.write("읽기 편한 글자 크기를 선택하세요.")

    size_columns = st.columns(3)
    for index, size_name in enumerate(FONT_SIZES):
        with size_columns[index]:
            if st.button(
                size_name,
                key=f"size_{size_name}",
                type=(
                    "primary"
                    if st.session_state.font_size == size_name
                    else "secondary"
                ),
                use_container_width=True,
            ):
                st.session_state.font_size = size_name
                st.rerun()

    st.info(f"현재 글자 크기: {st.session_state.font_size}")

    st.divider()

    # 메뉴 선택
    st.header("1. 메뉴를 선택하세요")
    st.write("원하는 메뉴 아래의 버튼을 누르세요.")

    menu_columns = st.columns(2)

    for index, (name, item) in enumerate(MENU.items()):
        with menu_columns[index % 2]:
            st.subheader(f"{item['emoji']} {name}")
            st.write(f"{item['price']:,}원")

            if st.button(
                f"{name} 담기",
                key=f"menu_{name}",
                use_container_width=True,
            ):
                add_to_cart(name)
                st.rerun()

    if st.session_state.message:
        st.success(st.session_state.message)

    st.divider()

    # 장바구니
    st.header("2. 주문을 확인하세요")

    if not st.session_state.cart:
        st.info("아직 선택한 메뉴가 없습니다.")
    else:
        total = 0

        for name, quantity in list(st.session_state.cart.items()):
            price = MENU[name]["price"]
            subtotal = price * quantity
            total += subtotal

            left, middle, right = st.columns([3, 1, 2])

            with left:
                st.write(f"**{name}**")
                st.write(f"{price:,}원 × {quantity}")

            with middle:
                st.write(f"{quantity}개")

            with right:
                if st.button(
                    "1개 삭제",
                    key=f"remove_{name}",
                    use_container_width=True,
                ):
                    remove_from_cart(name)
                    st.rerun()

        st.subheader(f"총 결제 금액: {total:,}원")

        col1, col2 = st.columns(2)

        with col1:
            if st.button(
                "장바구니 비우기",
                use_container_width=True,
            ):
                clear_cart()
                st.rerun()

        with col2:
            if st.button(
                "주문 확인하기",
                type="primary",
                use_container_width=True,
            ):
                st.session_state.message = (
                    f"주문 확인 완료! 총 {total:,}원입니다. "
                    "실제 결제는 진행되지 않았습니다."
                )
                st.rerun()

    st.divider()
    st.caption(
        "이 앱은 키오스크 사용 연습용입니다. "
        "실제 결제나 주문 전송 기능은 포함하지 않습니다."
    )

except Exception:
    st.error(
        "화면을 표시하는 중 문제가 발생했습니다. "
        "페이지를 새로고침한 뒤 다시 이용해 주세요."
    )
