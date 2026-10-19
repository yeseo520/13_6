
import streamlit as st

# =====================================
# 1. 기본 설정
# =====================================
st.set_page_config(
    page_title="키오스크 편의 서비스",
    page_icon="🧑‍🦳",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 실제 GitHub에 올린 페이지 파일 경로와 일치시켜 주세요.
PAGE_PATHS = {
    "사용 방법 안내": "pages/사용방법안내.py",
    "글자 크기 조절": "pages/글자크기조절.py",
    "음성 지원": "pages/음성지원.py",
    "직원 호출": "pages/직원호출.py",
}

# =====================================
# 2. 디자인 설정
# =====================================
st.markdown(
    """
    <style>
    .stApp {
        background-color: #F7FAFE;
    }

    .main .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3, p, label {
        color: #20334D;
    }

    .hero {
        background: linear-gradient(120deg, #E3EEFF, #E5F7F1);
        border: 1px solid #D6E6F4;
        border-radius: 22px;
        padding: 30px 28px;
        margin: 12px 0 22px 0;
    }

    .hero-label {
        color: #315C8A;
        font-size: 17px;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .hero-title {
        color: #183B65;
        font-size: 32px;
        font-weight: 800;
        line-height: 1.45;
        margin-bottom: 10px;
    }

    .hero-text {
        color: #405570;
        font-size: 19px;
        line-height: 1.7;
    }

    .section-title {
        font-size: 25px;
        font-weight: 800;
        color: #20334D;
        margin: 24px 0 5px 0;
    }

    .section-desc {
        font-size: 17px;
        color: #5B6D82;
        margin-bottom: 18px;
    }

    .menu-card {
        background: #FFFFFF;
        border: 1px solid #DDE7F1;
        border-radius: 18px;
        padding: 22px;
        min-height: 180px;
        margin-bottom: 10px;
    }

    .menu-icon {
        font-size: 35px;
        margin-bottom: 8px;
    }

    .menu-title {
        color: #20334D;
        font-size: 23px;
        font-weight: 800;
        margin-bottom: 9px;
    }

    .menu-desc {
        color: #53657B;
        font-size: 17px;
        line-height: 1.7;
    }

    div.stButton > button {
        width: 100%;
        min-height: 52px;
        border-radius: 12px;
        border: 1px solid #B9CEE6;
        background: #EAF2FF;
        color: #204E83;
        font-size: 18px;
        font-weight: 700;
    }

    div.stButton > button:hover {
        background: #D9E9FF;
        border-color: #7FA8D8;
        color: #163B67;
    }

    .help-box {
        background: #FFFFFF;
        border: 1px solid #DDE7F1;
        border-left: 6px solid #65BFA7;
        border-radius: 13px;
        padding: 18px 20px;
        color: #405570;
        font-size: 17px;
        line-height: 1.8;
        margin-top: 20px;
    }

    .footer {
        text-align: center;
        color: #697B90;
        font-size: 15px;
        padding-top: 25px;
    }

    @media (max-width: 600px) {
        .hero-title {
            font-size: 27px;
        }
        .hero-text {
            font-size: 18px;
        }
        .menu-card {
            padding: 18px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =====================================
# 3. 글자 크기 설정
# =====================================
if "font_size" not in st.session_state:
    st.session_state["font_size"] = 18

def reset_font_size():
    st.session_state["font_size"] = 18

with st.sidebar:
    st.subheader("화면 설정")
    st.caption("안내 글자를 편하게 조절하세요.")

    st.slider(
        "글자 크기",
        min_value=16,
        max_value=28,
        step=2,
        key="font_size",
    )

    st.button(
        "글자 크기 기본값",
        on_click=reset_font_size,
        use_container_width=True,
    )

st.markdown(
    f"""
    <style>
    .hero-text, .menu-desc, .help-box {{
        font-size: {st.session_state["font_size"]}px !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# =====================================
# 4. 메인 화면
# =====================================
st.markdown(
    """
    <div class="hero">
        <div class="hero-label">KIOSK EASY GUIDE</div>
        <div class="hero-title">
            안녕하세요!<br>
            무엇을 도와드릴까요?
        </div>
        <div class="hero-text">
            원하시는 메뉴를 선택해 주세요.<br>
            큰 글씨와 쉬운 안내로 편리한 키오스크 이용을 도와드립니다.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-title">필요한 서비스를 선택하세요</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-desc">'
    '아래 버튼을 누르면 해당 서비스 페이지로 이동합니다.'
    '</div>',
    unsafe_allow_html=True,
)

# 요청한 순서대로 메뉴 구성
menus = [
    {
        "title": "사용 방법 안내",
        "icon": "📘",
        "desc": "키오스크를 처음 사용하시나요? 화면 선택부터 주문까지 기본 사용 순서를 알려드립니다.",
        "button": "사용 방법 안내 바로가기 →",
    },
    {
        "title": "글자 크기 조절",
        "icon": "🔎",
        "desc": "글씨가 작아 읽기 힘들 때 글자 크기 조절 기능을 이용해 더 편하게 확인하세요.",
        "button": "글자 크기 조절 바로가기 →",
    },
    {
        "title": "음성 지원",
        "icon": "🔊",
        "desc": "화면 내용을 듣고 싶을 때 음성 지원 페이지에서 음성 안내 기능을 이용하세요.",
        "button": "음성 지원 바로가기 →",
    },
    {
        "title": "직원 호출",
        "icon": "🙋",
        "desc": "사용 중 도움이 필요하다면 직원에게 도움을 요청하는 방법을 확인하세요.",
        "button": "직원 호출 바로가기 →",
    },
]

# 두 열로 배치하며 목록 순서를 유지
for start in range(0, len(menus), 2):
    col1, col2 = st.columns(2, gap="large")

    for col, menu in zip(
        [col1, col2],
        menus[start:start + 2],
    ):
        with col:
            st.markdown(
                f"""
                <div class="menu-card">
                    <div class="menu-icon">{menu["icon"]}</div>
                    <div class="menu-title">{menu["title"]}</div>
                    <div class="menu-desc">{menu["desc"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if st.button(
                menu["button"],
                key=f'page_{menu["title"]}',
                use_container_width=True,
            ):
                page_path = PAGE_PATHS[menu["title"]]

                try:
                    st.switch_page(page_path)
                except Exception:
                    st.error(
                        f'"{menu["title"]}" 페이지를 열지 못했습니다. '
                        "pages 폴더와 파일 이름을 확인해 주세요."
                    )
                    st.code(page_path)

# =====================================
# 5. 이용 도움말
# =====================================
st.markdown(
    """
    <div class="help-box">
        <strong>💡 이용 안내</strong><br>
        1. 필요한 서비스의 설명을 읽어 보세요.<br>
        2. 파란색 바로가기 버튼을 눌러 주세요.<br>
        3. 이용이 어렵다면 직원에게 도움을 요청하셔도 됩니다.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="footer">
        누구나 쉽고 편리하게 이용하는 키오스크 편의 서비스
    </div>
    """,
    unsafe_allow_html=True,
)
