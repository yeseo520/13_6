# 키오스크 사용방법 안내 앱 만들기

초보자도 쉽게 사용할 수 있도록 단계별 키오스크 체험 학습 앱을 설계하겠습니다. 음식점에서 음식을 주문하는 상황을 중심으로, 화면의 안내를 따라 직접 선택하고 주문을 완료하는 방식입니다.

실제 키오스크를 사용하기 전에 연습할 수 있도록 만들며, 스마트폰과 PC 모두에서 사용할 수 있는 Streamlit 앱으로 구현합니다. 별도의 AI API 없이 동작하도록 구성해 API 키 설정이나 추가 비용 없이 배포할 수 있습니다.

## 1. 앱 기획 설명

セルフレジとは？飲食店に導入するメリット、種類や導入のポイントを徹底解説｜お役立ち情報

### ① 키오스크 사용법 배우기

학습 안내

키오스크의 기본 사용 순서와 주의 사항을 그림과 설명으로 배웁니다.

#hospitalidad #franquicias #restaurantes #midmarket #omnicanalidad #leadin #transformacióndigital #customerexperience #crecimiento | Leadin IT Services

### ② 주문 단계별 체험

직접 조작하는 실습

메뉴 선택 → 수량 확인 → 장바구니 확인 → 결제 방법 선택 순서로 연습합니다.

Nova self Ordering Kiosk

### ③ 결제 및 주문 완료

마무리 학습

카드·간편결제·현금 등 결제 방법을 확인하고, 주문번호와 영수증 확인 방법을 배웁니다.

### 주요 기능

- 단계별 안내: 현재 해야 할 일을 한 단계씩 보여줍니다.
- 가상 주문 체험: 메뉴와 수량을 직접 선택하고 합계를 확인합니다.
- 결제 방법 학습: 실제 결제 없이 결제 절차만 연습합니다.
- 진행률 표시: 전체 과정 중 어디까지 완료했는지 보여줍니다.
- 학습 퀴즈: 마지막에 간단한 문제를 풀어 이해도를 확인합니다.
- 초기화 기능: 언제든 처음부터 다시 연습할 수 있습니다.

## 2. `app.py` — 전체 실행 코드

아래 코드를 `app.py` 파일에 그대로 복사하세요. 메뉴 선택, 장바구니, 결제 절차, 진행률, 퀴즈와 초기화 기능까지 포함한 완성 코드입니다.

python
```

import streamlit as st

st.set_page_config(
    page_title="키오스크 사용 연습",
    page_icon="🖥️",
    layout="centered",
    initial_sidebar_state="expanded",
)

MENU = {
    "🍔 불고기버거": 5500,
    "🍟 감자튀김": 2500,
    "🥤 콜라": 2000,
    "🍗 치킨너겟": 3500,
    "🍦 아이스크림": 1800,
}

STEPS = [
    "메뉴 선택",
    "주문 확인",
    "결제 방법",
    "주문 완료",
]

def initialize():
    st.session_state.stage = 0
    st.session_state.cart = {}
    st.session_state.payment = None
    st.session_state.quiz_answers = {}
    st.session_state.quiz_submitted = False

if "stage" not in st.session_state:
    initialize()

if "cart" not in st.session_state:
    initialize()

if "payment" not in st.session_state:
    st.session_state.payment = None

if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}

if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False

def money(amount):
    return f"{amount:,}원"

def cart_total():
    return sum(
        MENU[item] * quantity
        for item, quantity in st.session_state.cart.items()
    )

def go_to(stage):
    st.session_state.stage = stage

st.title("🖥️ 키오스크 사용 연습")
st.caption("천천히 따라 해 보세요. 실제 결제는 진행되지 않습니다.")

with st.sidebar:
    st.header("📚 학습 메뉴")
    page = st.radio(
        "원하는 학습을 선택하세요.",
        ["사용법 배우기", "주문 체험하기", "확인 퀴즈"],
        label_visibility="collapsed",
    )
    st.divider()
    st.subheader("내 학습 진행률")
    completed_steps = st.session_state.stage
    st.progress(completed_steps / len(STEPS))
    st.caption(f"{completed_steps}/{len(STEPS)}단계 완료")

    if st.button("🔄 처음부터 다시 하기", use_container_width=True):
        initialize()
        st.rerun()

if page == "사용법 배우기":
    st.header("키오스크는 이렇게 사용해요")
    st.write(
        "키오스크는 화면을 직접 눌러 상품을 선택하고 "
        "주문하는 무인 주문 기기입니다."
    )

    lessons = [
        (
            "1. 주문 시작하기",
            "화면에서 '주문하기' 또는 원하는 매장 이용 방식을 선택합니다.",
            "💡",
        ),
        (
            "2. 메뉴 선택하기",
            "먹고 싶은 메뉴를 누르고 수량과 옵션을 확인합니다.",
            "🍔",
        ),
        (
            "3. 주문 내역 확인하기",
            "메뉴 이름, 수량, 가격과 최종 합계가 맞는지 확인합니다.",
            "🧾",
        ),
        (
            "4. 결제 방법 선택하기",
            "카드, 간편결제 등 기기에서 지원하는 결제 방법을 선택합니다.",
            "💳",
        ),
        (
            "5. 주문 완료 확인하기",
            "주문번호와 영수증을 확인하고 안내에 따라 음식을 받습니다.",
            "✅",
        ),
    ]

    for title, description, emoji in lessons:
        with st.container(border=True):
            st.subheader(f"{emoji} {title}")
            st.write(description)

    st.info(
        "어려우면 주변 직원에게 도움을 요청해도 괜찮아요. "
        "결제 전에는 반드시 주문 내역과 금액을 확인하세요."
    )

    if st.button("실제처럼 주문 연습하기 ➜", type="primary"):
        go_to(0)
        st.rerun()

elif page == "주문 체험하기":
    stage = st.session_state.stage
    st.header("🍽️ 가상 음식점 주문")
    st.write("화면의 안내에 따라 한 단계씩 진행해 보세요.")

    st.progress((stage + 1) / len(STEPS))
    st.caption(f"현재 단계: {stage + 1} / {len(STEPS)} · {STEPS[stage]}")

    if stage == 0:
        st.subheader("1단계. 먹고 싶은 메뉴를 선택하세요")
        st.write("메뉴 아래에서 수량을 선택하면 주문에 추가됩니다.")

        for item, price in MENU.items():
            with st.container(border=True):
                left, right = st.columns([3, 2])
                with left:
                    st.markdown(f"**{item}**")
                    st.write(money(price))
                with right:
                    quantity = st.number_input(
                        f"{item} 수량",
                        min_value=0,
                        max_value=10,
                        value=st.session_state.cart.get(item, 0),
                        step=1,
                        key=f"qty_{item}",
                    )
                    st.session_state.cart[item] = quantity

        st.session_state.cart = {
            item: quantity
            for item, quantity in st.session_state.cart.items()
            if quantity > 0
        }

        st.metric("현재 주문 금액", money(cart_total()))

        if st.button("주문 내역 확인하기 ➜", type="primary"):
            if not st.session_state.cart:
                st.warning("메뉴를 한 개 이상 선택해 주세요.")
            else:
                go_to(1)
                st.rerun()

    elif stage == 1:
        st.subheader("2단계. 주문 내역을 확인하세요")
        st.write("선택한 메뉴와 수량이 맞는지 확인합니다.")

        for item, quantity in st.session_state.cart.items():
            subtotal = MENU[item] * quantity
            st.write(
                f"- {item} × {quantity}개 — {money(subtotal)}"
            )

        st.divider()
        st.metric("총 주문 금액", money(cart_total()))
        st.warning("실제 주문에서는 결제하기 전에 금액을 꼭 확인하세요.")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("← 메뉴 수정하기"):
                go_to(0)
                st.rerun()
        with col2:
            if st.button("결제 방법 선택 ➜", type="primary"):
                go_to(2)
                st.rerun()

    elif stage == 2:
        st.subheader("3단계. 결제 방법을 선택하세요")
        st.write(f"결제할 금액: **{money(cart_total())}**")
        st.info("이 화면은 학습용입니다. 실제 결제는 발생하지 않습니다.")

        payment = st.radio(
            "어떤 방법으로 결제할까요?",
            ["💳 카드 결제", "📱 간편결제", "💵 현금 결제"],
            index=(
                ["💳 카드 결제", "📱 간편결제", "💵 현금 결제"].index(
                    st.session_state.payment
                )
                if st.session_state.payment in [
                    "💳 카드 결제", "📱 간편결제", "💵 현금 결제"
                ]
                else 0
            ),
        )

        with st.container(border=True):
            if payment == "💳 카드 결제":
                st.write("1. 카드 투입구 또는 카드 태그 위치를 확인합니다.")
                st.write("2. 기기의 안내에 따라 카드를 사용합니다.")
                st.write("3. 결제 완료 메시지를 확인합니다.")
            elif payment == "📱 간편결제":
                st.write("1. 기기가 간편결제를 지원하는지 확인합니다.")
                st.write("2. 화면 안내에 따라 휴대전화를 사용합니다.")
                st.write("3. 결제 완료 메시지를 확인합니다.")
            else:
                st.write("1. 현금 결제를 지원하는 기기인지 확인합니다.")
                st.write("2. 안내된 투입구에 현금을 넣습니다.")
                st.write("3. 거스름돈이 있다면 꼭 확인합니다.")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("← 주문 내역으로"):
                go_to(1)
                st.rerun()
        with col2:
            if st.button("가상 결제 완료하기 ➜", type="primary"):
                st.session_state.payment = payment
                go_to(3)
                st.rerun()

    else:
        st.success("🎉 주문 체험을 완료했습니다!")
        st.balloons()
        st.subheader("주문 완료 내역")
        st.write("가상 주문번호: **K2026-001**")
        st.write(f"결제 방법: {st.session_state.payment}")
        st.write(f"총 주문 금액: **{money(cart_total())}**")
        st.write("주문번호와 영수증을 확인한 뒤 음식을 받으면 됩니다.")
        st.caption("이 주문번호는 연습용이며 실제 주문이 아닙니다.")

        if st.button("주문 한 번 더 연습하기", type="primary"):
            initialize()
            st.rerun()

elif page == "확인 퀴즈":
    st.header("📝 키오스크 사용 확인 퀴즈")
    st.write("문제를 읽고 가장 알맞은 답을 선택해 보세요.")

    questions = [
        (
            "1. 결제하기 전에 가장 먼저 확인할 것은?",
            [
                "화면 색상",
                "메뉴와 최종 결제 금액",
                "옆 사람의 주문",
            ],
            1,
            "메뉴, 수량, 최종 금액이 맞는지 확인해야 합니다.",
        ),
        (
            "2. 키오스크 사용법을 잘 모르겠다면?",
            [
                "아무 버튼이나 누른다",
                "바로 결제한다",
                "직원에게 도움을 요청한다",
            ],
            2,
            "직원에게 도움을 요청하면 안전하게 이용할 수 있습니다.",
        ),
        (
            "3. 주문을 마친 다음 해야 할 일은?",
            [
                "주문번호와 영수증을 확인한다",
                "화면을 다시 누른다",
                "주문 내역을 확인하지 않는다",
            ],
            0,
            "주문번호와 영수증을 확인하고 수령 안내를 따르면 됩니다.",
        ),
        (
            "4. 이 연습 앱에서 결제를 완료하면 실제 돈이 나갈까요?",
            [
                "네, 항상 결제된다",
                "아니요, 가상 체험이다",
                "카드가 있어야만 결제된다",
            ],
            1,
            "이 앱은 학습용 시뮬레이션이며 실제 결제 기능이 없습니다.",
        ),
    ]

    with st.form("quiz_form"):
        answers = {}
        for index, (question, options, correct, explanation) in enumerate(
            questions
        ):
            answers[index] = st.radio(
                question,
                options,
                index=None,
                key=f"quiz_{index}",
            )

        submitted = st.form_submit_button(
            "정답 확인하기",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        st.session_state.quiz_answers = answers
        st.session_state.quiz_submitted = True

    if st.session_state.quiz_submitted:
        answers = st.session_state.quiz_answers
        unanswered = [
            index for index in range(len(questions))
            if answers.get(index) is None
        ]

        if unanswered:
            st.warning("아직 답하지 않은 문제가 있습니다. 답을 선택해 주세요.")
            st.session_state.quiz_submitted = False
        else:
            score = 0
            for index, (question, options, correct, explanation) in enumerate(
                questions
            ):
                if options.index(answers[index]) == correct:
                    score += 1

            st.subheader(f"결과: {score} / {len(questions)}점")
            st.progress(score / len(questions))

            if score == len(questions):
                st.success("완벽해요! 키오스크 사용법을 잘 이해했습니다.")
            elif score >= 2:
                st.info("잘했어요! 해설을 확인하고 한 번 더 연습해 보세요.")
            else:
                st.info("괜찮아요. 사용법 배우기 메뉴를 다시 살펴보세요.")

            for index, (question, options, correct, explanation) in enumerate(
                questions
            ):
                is_correct = options.index(answers[index]) == correct
                with st.container(border=True):
                    st.write(
                        f"{'✅ 정답' if is_correct else '❌ 다시 확인'} — "
                        f"{question}"
                    )
                    st.write(f"정답: {options[correct]}")
                    st.caption(explanation)

            if st.button("퀴즈 다시 풀기"):
                st.session_state.quiz_answers = {}
                st.session_state.quiz_submitted = False
                st.rerun()

st.divider()
st.caption(
    "키오스크 사용 연습 | 교육용 가상 체험 · 실제 주문 및 결제 없음"
)
```
