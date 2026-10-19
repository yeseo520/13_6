
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

# GitHub에서 확인한 실제 세부 페이지 파일 이름
PAGE_PATHS = {
    "사용 방법 안내": "pages/키오스크 사용방법 안내.py",
    "글자 크기 조절": "pages/키오스크 글자 크기 조절 버튼.py",
    "음성 지원": "pages/키오스크 음성지원 버튼.py",
}

# =====================================
# 2. 화면 디자인
# =====================================
st.markdown("""
<style>
.stApp {
    background-color: #F5F8FC;
}

.main .block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.hero {
    background: linear-gradient(120deg, #E2EDFF, #E0F5EE);
    border: 1px solid #D5E5F4;
    border-radius: 22px;
    padding: 30px;
    margin: 10px 0 26px 0;
}

.hero-label {
    color: #315C8A;
    font-size: 17px;
    font-weight: 700;
}

.hero-title {
    color: #193D68;
    font-size: 34px;
    font-weight: 800;
    line-height: 1.5;
    margin: 10px 0;
}

.hero-text {
    color: #405570;
    font-size: 19px;
    line-height: 1.8;
}

.section-title {
    color: #20334D;
    font-size: 26px;
    font-weight: 800;
    margin-top: 22px;
}

.section-desc {
    color: #5B6D82;
    font-size: 17px;
    margin: 8px 0 20px 0;
}

.menu-card {
    background: #FFFFFF;
    border: 1px solid #DCE6F1;
    border-radius: 18px;
    padding: 22px;
    min-height: 185px;
    margin-bottom: 10px;
}

.menu-icon {
    font-size: 36px;
    margin-bottom: 10px;
}

.menu-title {
    color: #20334D;
    font-size: 24px;
    font-weight: 800;
    margin-bottom: 10px;
}

.menu-desc {
    color: #52657C;
    font-size: 18px;
    line-height: 1.7;
}

div.stButton > button {
    width: 100%;
    min-height: 54px;
    background: #E8F1FF;
    color: #204E83;
    border: 1px solid #B8CFEA;
    border-radius: 12px;
    font-size: 18px;
    font-weight: 700;
}

div.stButton > button:hover {
    background: #D8E8FF;
    border-color: #7EA7D6;
    color: #183B67;
}

.help-box {
    background: #FFFFFF;
    border: 1px solid #DDE8F0;
    border-left: 6px solid #68BFA8;
    border-radius: 14px;
    padding: 20px;
    margin-top: 25px;
    color: #405570;
    font-size: 18px;
    line-height: 1.9;
}

.footer {
    text-align: center;
    color: #64748B;
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
""", unsafe_allow_html=True)

# =====================================
# 3. 글자 크기 조절
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
st.markdown("""
<div class="hero">
    <div class="hero-label">KIOSK EASY GUIDE</div>
    <div class="hero-title">
        안녕하세요!<br>
        무엇을 도와드릴까요?
    </div>
    <div class="hero-text">
        원하시는 메뉴를 선택해 주세요.<br>
        큰 글씨와 쉬운 설명으로 편리한 키오스크 이용을 도와드립니다.
    </div>
</div>
""", unsafe_allow_html=True)

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

# 요청한 순서대로 메뉴 배치
menus = [
    {
        "title": "사용 방법 안내",
        "icon": "📘",
        "desc": "키오스크를 처음 사용하시나요? 화면 선택부터 주문 완료까지 기본 사용 순서를 알려드립니다.",
        "button": "사용 방법 안내 바로가기 →",
    },
    {
        "title": "글자 크기 조절",
        "icon": "🔎",
        "desc": "글씨가 작아서 읽기 불편할 때 글자 크기 조절 기능을 이용해 보세요.",
        "button": "글자 크기 조절 바로가기 →",
    },
    {
        "title": "음성 지원",
        "icon": "🔊",
        "desc": "화면 내용을 듣고 싶을 때 음성 지원 페이지에서 안내 기능을 이용하세요.",
        "button": "음성 지원 바로가기 →",
    },
    {
        "title": "직원 호출",
        "icon": "🙋",
        "desc": "키오스크 사용 중 도움이 필요하다면 직원에게 도움을 요청하세요.",
        "button": "직원 호출 안내 보기 →",
    },
]

# 두 열로 메뉴 표시
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
                page_path = PAGE_PATHS.get(menu["title"])

                if page_path is None:
                    st.warning(
                        "직원 호출 페이지는 아직 연결되지 않았습니다. "
                        "해당 페이지 파일을 먼저 만들어 주세요."
                    )
                else:
                    try:
                        st.switch_page(page_path)
                    except Exception as e:
                        st.error(
                            f'{menu["title"]} 페이지로 이동하지 못했습니다.'
                        )
                        st.write("확인할 파일 경로:", page_path)
                        st.code(str(e))

# =====================================
# 5. 이용 안내
# =====================================
st.markdown("""
<div class="help-box">
    <strong>💡 이용 안내</strong><br>
    ① 필요한 서비스의 설명을 읽어 보세요.<br>
    ② 파란색 바로가기 버튼을 눌러 주세요.<br>
    ③ 이용이 어렵다면 직원에게 도움을 요청하셔도 됩니다.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    누구나 쉽고 편리하게 이용하는 키오스크 편의 서비스
</div>
""", unsafe_allow_html=True)
