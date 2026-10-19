
import streamlit as st

st.set_page_config(
    page_title="어르신을 위한 쉬운 키오스크",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -------------------------------
# 1. 기본 설정
# -------------------------------
FONT_SIZES = {
    "보통": 18,
    "크게": 24,
    "아주 크게": 30,
}

CATEGORIES = [
    ("🍚", "식사류"),
    ("🥤", "음료"),
    ("🍔", "분식"),
    ("🍰", "디저트"),
]

if "font_size_name" not in st.session_state:
    st.session_state.font_size_name = "보통"

if "show_font_options" not in st.session_state:
    st.session_state.show_font_options = False

if "selected_category" not in st.session_state:
    st.session_state.selected_category = ""

if "language" not in st.session_state:
    st.session_state.language = "한국어"

font_px = FONT_SIZES[st.session_state.font_size_name]

# -------------------------------
# 2. 화면 디자인
# -------------------------------
st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: #F3F7FC;
        color: #152C48;
    }}

    [data-testid="stHeader"] {{
        background-color: #F3F7FC;
    }}

    .block-container {{
        max-width: 1100px;
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }}

    h1 {{
        font-size: {font_px * 1.7}px !important;
        color: #163B68 !important;
        font-weight: 800 !important;
    }}

    h2 {{
        font-size: {font_px * 1.4}px !important;
        color: #163B68 !important;
    }}

    h3 {{
        font-size: {font_px * 1.2}px !important;
        color: #163B68 !important;
    }}

    p, label, .stMarkdown, [data-testid="stCaptionContainer"] {{
        font-size: {font_px}px !important;
        color: #152C48;
    }}

    div.stButton > button {{
        min-height: 64px;
        width: 100%;
        border: 2px solid #C4D5E8;
        border-radius: 14px;
        background-color: #FFFFFF;
        color: #15385F;
        font-size: {font_px}px !important;
        font-weight: 700;
        white-space: normal;
        overflow-wrap: anywhere;
    }}

    div.stButton > button[kind="primary"] {{
        background-color: #2673D9;
        border-color: #2673D9;
        color: #FFFFFF;
    }}

    [data-testid="stAlert"] {{
        border-radius: 12px;
    }}

    .welcome-box {{
        background-color: #FFFFFF;
        border: 2px solid #D7E3F1;
        border-radius: 18px;
        padding: 22px;
        margin-bottom: 16px;
    }}

    .bottom-label {{
        text-align: center;
        color: #FFFFFF;
        font-weight: bold;
    }}

    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------
# 3. 상단 환영 화면
# -------------------------------
st.title("🏪 무인 주문 키오스크에 오신 것을 환영합니다!")
st.write("아래에서 원하시는 메뉴를 선택해주세요.")

st.markdown(
    f"""
    <div class="welcome-box">
        <strong style="font-size:{font_px * 1.15}px;">
            편안하게 이용하세요
        </strong>
        <p style="margin-bottom:0;">
            글자가 작아서 읽기 어려우면 아래의
            'Aa 글자 크기' 버튼을 눌러주세요.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# -------------------------------
# 4. 메뉴 선택 화면
# -------------------------------
st.header("메뉴 선택")

menu_columns = st.columns(2)

for index, (emoji, category) in enumerate(CATEGORIES):
    with menu_columns[index % 2]:
        if st.button(
            f"{emoji}   {category}",
            key=f"category_{category}",
            use_container_width=True,
        ):
            st.session_state.selected_category = category

if st.session_state.selected_category:
    st.success(
        f"'{st.session_state.selected_category}' 메뉴를 선택했습니다."
    )
    st.write("이 화면은 키오스크 사용 시연용입니다.")

# -------------------------------
# 5. 하단 고정형 기능 영역
# -------------------------------
st.divider()

home_col, size_col, language_col = st.columns([1, 1.5, 1])

with home_col:
    if st.button("⌂ 처음으로", use_container_width=True):
        st.session_state.selected_category = ""
        st.session_state.show_font_options = False
        st.rerun()

with size_col:
    if st.button(
        "Aa  글자 크기",
        type="primary",
        use_container_width=True,
    ):
        st.session_state.show_font_options = (
            not st.session_state.show_font_options
        )
        st.rerun()

with language_col:
    if st.button("◎ 다른 언어", use_container_width=True):
        st.session_state.language = (
            "English"
            if st.session_state.language == "한국어"
            else "한국어"
        )
        st.rerun()

# -------------------------------
# 6. 글자 크기 선택 영역
# -------------------------------
if st.session_state.show_font_options:
    st.subheader("🔎 글자 크기를 선택하세요")
    st.write("원하는 크기를 누르면 화면의 글자가 바뀝니다.")

    size_columns = st.columns(3)

    for index, size_name in enumerate(FONT_SIZES):
        with size_columns[index]:
            if st.button(
                f"{size_name} ({FONT_SIZES[size_name]}px)",
                key=f"choose_size_{size_name}",
                type=(
                    "primary"
                    if st.session_state.font_size_name == size_name
                    else "secondary"
                ),
                use_container_width=True,
            ):
                st.session_state.font_size_name = size_name
                st.session_state.show_font_options = True
                st.rerun()

    st.info(
        f"현재 설정: {st.session_state.font_size_name}"
    )

st.caption(
    "어르신을 위한 글자 크기 조절 키오스크 · 시연용 앱"
)
