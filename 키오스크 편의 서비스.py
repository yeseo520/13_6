
import streamlit as st

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="키오스크 편의 서비스",
    page_icon="♿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 기존에 만든 페이지의 파일 경로
# GitHub의 pages 폴더 안에 파일이 있어야 합니다.
PAGE_PATHS = {
    "글자 크기 조절": "pages/글자크기조절.py",
    "음성 지원": "pages/음성지원.py",
    "직원 호출": "pages/직원호출.py",
    "사용 방법 안내": "pages/사용방법안내.py",
}

# -----------------------------
# 화면 디자인
# -----------------------------
st.markdown("""
<style>
    .stApp {
        background-color: #FFFFFF;
    }

    .main .block-container {
        max-width: 1050px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3, p, label {
        color: #243247;
    }

    .intro {
        background: #F3F7FC;
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0 24px 0;
        border: 1px solid #E2EAF5;
    }

    .intro-title {
        font-size: 25px;
        font-weight: 700;
        margin-bottom: 8px;
        color: #234A7D;
    }

    .intro-text {
        font-size: 18px;
        line-height: 1.7;
        margin: 0;
    }

    .menu-card {
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 22px;
        min-height: 175px;
        background: #FFFFFF;
        margin-bottom: 12px;
    }

    .menu-icon {
        font-size: 32px;
        margin-bottom: 8px;
    }

    .menu-title {
        font-size: 23px;
        font-weight: 700;
        margin-bottom: 8px;
        color: #243247;
    }

    .menu-desc {
        font-size: 17px;
        line-height: 1.6;
        color: #526176;
    }

    div.stButton > button {
        width: 100%;
        min-height: 48px;
        border-radius: 10px;
        border: 1px solid #B8CCE5;
        background: #F3F7FC;
        color: #234A7D;
        font-size: 17px;
        font-weight: 600;
    }

    div.stButton > button:hover {
        background: #E3EEFC;
        border-color: #7199CC;
        color: #183D6B;
    }

    .footer {
        color: #64748B;
        text-align: center;
        font-size: 15px;
        padding-top: 24px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 글자 크기 조절
# -----------------------------
if "font_size" not in st.session_state:
    st.session_state.font_size = 18

with st.sidebar:
    st.header("화면 설정")
    st.caption("읽기 편하게 화면을 조절하세요.")

    st.session_state.font_size = st.slider(
        "안내 글자 크기",
        min_value=16,
        max_value=28,
        value=st.session_state.font_size,
        step=2
    )

    if st.button("글자 크기 기본값"):
        st.session_state.font_size = 18
        st.rerun()

st.markdown(
    f"<style>.intro-text, .menu-desc "
    f"{{font-size: {st.session_state.font_size}px !important;}}</style>",
    unsafe_allow_html=True
)

# -----------------------------
# 메인 화면
# -----------------------------
st.title("키오스크 편의 서비스")
st.caption("누구나 쉽고 편리하게 이용하는 키오스크")

st.markdown("""
<div class="intro">
    <div class="intro-title">무엇을 도와드릴까요?</div>
    <p class="intro-text">
        필요한 기능을 선택해 주세요.<br>
        각 메뉴의 설명을 읽고 버튼을 누르면 해당 안내 페이지로 이동합니다.
    </p>
</div>
""", unsafe_allow_html=True)

# 메뉴 정보
menus = [
    {
        "icon": "🔎",
        "title": "글자 크기 조절",
        "desc": "글씨가 작아서 읽기 불편할 때 글자를 크게 조절하는 기능입니다."
    },
    {
        "icon": "🔊",
        "title": "음성 지원",
        "desc": "음성 안내 기능을 이용해 화면의 내용을 듣는 데 도움을 줍니다."
    },
    {
        "icon": "🙋",
        "title": "직원 호출",
        "desc": "키오스크 사용이 어렵다면 직원에게 도움을 요청하는 방법을 확인합니다."
    },
    {
        "icon": "📖",
        "title": "사용 방법 안내",
        "desc": "화면 선택부터 주문 완료까지 키오스크 사용 순서를 배울 수 있습니다."
    },
]

# 두 열로 메뉴 배치
for start in range(0, len(menus), 2):
    left, right = st.columns(2, gap="large")

    for column, menu in zip(
        [left, right],
        menus[start:start + 2]
    ):
        with column:
            st.markdown(
                f"""
                <div class="menu-card">
                    <div class="menu-icon">{menu["icon"]}</div>
                    <div class="menu-title">{menu["title"]}</div>
                    <div class="menu-desc">{menu["desc"]}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button(
                f'{menu["title"]} 페이지로 이동 →',
                key=f'go_{menu["title"]}',
                use_container_width=True
            ):
                try:
                    st.switch_page(PAGE_PATHS[menu["title"]])
                except Exception:
                    st.error(
                        "페이지를 열 수 없습니다. "
                        "pages 폴더와 파일 이름을 확인해 주세요."
                    )
                    st.code(PAGE_PATHS[menu["title"]])

st.divider()

st.markdown("""
<div class="footer">
    도움이 필요하면 직원에게 편하게 요청하세요.<br>
    누구나 편리하게 이용할 수 있는 키오스크를 만들어 갑니다.
</div>
""", unsafe_allow_html=True)
