import streamlit as st
st.title('키오스크')
st.write('키오스크 글자 크기 조절 버튼')

import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="어르신을 위한 쉬운 키오스크",
    page_icon="🖥️",
    layout="centered"
)

# 글자 크기 설정
if "font_size" not in st.session_state:
    st.session_state.font_size = "보통"

font_sizes = {
    "보통": 20,
    "크게": 28,
    "아주 크게": 36
}

size = font_sizes[st.session_state.font_size]

# 화면 디자인
st.markdown(f"""
<style>
    .stApp {{
        background-color: #F7F9FC;
    }}

    h1, h2, h3, p, label, div {{
        line-height: 1.6;
    }}

    .main-title {{
        font-size: {size + 12}px;
        font-weight: bold;
        color: #12345A;
        text-align: center;
    }}

    .description {{
        font-size: {size}px;
        color: #222222;
        text-align: center;
    }}

    .menu-title {{
        font-size: {size + 4}px;
        font-weight: bold;
        color: #12345A;
    }}

    .price {{
        font-size: {size}px;
        font-weight: bold;
        color: #222222;
    }}

    div.stButton > button {{
        font-size: {size}px;
        min-height: 65px;
        border: 2px solid #174A7E;
        border-radius: 12px;
        font-weight: bold;
    }}

    div.stButton > button[kind="primary"] {{
        background-color: #174A7E;
        color: white;
    }}

    .size-label {{
        font-size: {size}px;
        font-weight: bold;
        color: #12345A;
    }}
</style>
""", unsafe_allow_html=True)

# 키오스크 제목
st.markdown(
    f'<div class="main-title">🍽️ 쉬운 주문 키오스크</div>',
    unsafe_allow_html=True
)

st.markdown(
    f'<div class="description">원하는 메뉴를 선택해 주세요.</div>',
    unsafe_allow_html=True
)

st.divider()

# 글자 크기 조절 영역
st.markdown(
    f'<div class="size-label">🔎 글자 크기 조절</div>',
    unsafe_allow_html=True
)

st.caption("잘 보이는 크기를 선택하세요.")

col1, col2, col3 = st.columns(3)

if col1.button(
    "보통",
    use_container_width=True,
    type="primary" if st.session_state.font_size == "보통" else "secondary"
):
    st.session_state.font_size = "보통"
    st.rerun()

if col2.button(
    "크게",
    use_container_width=True,
    type="primary" if st.session_state.font_size == "크게" else "secondary"
):
    st.session_state.font_size = "크게"
    st.rerun()

if col3.button(
    "아주 크게",
    use_container_width=True,
    type="primary" if st.session_state.font_size == "아주 크게" else "secondary"
):
    st.session_state.font_size = "아주 크게"
    st.rerun()

st.info(f"현재 글자 크기: {st.session_state.font_size}")

st.divider()

# 메뉴 안내
st.markdown(
    f'<div class="menu-title">📋 메뉴 선택</div>',
    unsafe_allow_html=True
)

menu_data = [
    ("☕ 아메리카노", 2500),
    ("🥤 딸기 주스", 4000),
    ("🍵 녹차", 3000)
]

if "selected_menu" not in st.session_state:
    st.session_state.selected_menu = None

for menu, price in menu_data:
    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown(
            f'<p style="font-size:{size}px;">{menu}</p>',
            unsafe_allow_html=True
        )

    with col2:
        if st.button(
            f"{price:,}원",
            key=menu,
            use_container_width=True
        ):
            st.session_state.selected_menu = menu
            st.rerun()

st.divider()

# 선택한 메뉴 확인
st.markdown(
    f'<div class="menu-title">🛒 주문 확인</div>',
    unsafe_allow_html=True
)

if st.session_state.selected_menu:
    selected = st.session_state.selected_menu
    selected_price = dict(menu_data)[selected]

    st.success(f"선택한 메뉴: {selected}")
    st.markdown(
        f'<p style="font-size:{size}px; font-weight:bold;">'
        f'가격: {selected_price:,}원</p>',
        unsafe_allow_html=True
    )

    if st.button("주문 완료", type="primary",
                 use_container_width=True):
        st.success("주문이 확인되었습니다!")
else:
    st.markdown(
        f'<p style="font-size:{size}px;">아직 선택한 메뉴가 없습니다.</p>',
        unsafe_allow_html=True
    )



