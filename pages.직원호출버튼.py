
import streamlit as st
from datetime import datetime
import uuid

st.set_page_config(
    page_title="직원 호출 센터",
    page_icon="🔔",
    layout="wide",
)

# 세션 데이터 초기화
if "calls" not in st.session_state:
    st.session_state.calls = []

if "table_count" not in st.session_state:
    st.session_state.table_count = 12

CALL_REASONS = [
    "직원 요청",
    "주문 / 추가 주문",
    "결제 요청",
    "물 / 식기 요청",
    "기타",
]

STATUSES = ["대기 중", "처리 중", "완료"]


def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def refresh():
    st.rerun()


st.title("🔔 직원 호출 센터")
st.caption("고객 호출과 직원 업무를 간편하게 관리하세요.")

page = st.sidebar.radio(
    "메뉴",
    ["고객 호출", "직원 현황판", "설정"],
)


# -------------------------
# 설정 화면
# -------------------------
if page == "설정":
    st.header("⚙️ 매장 설정")

    count = st.number_input(
        "테이블 수",
        min_value=1,
        max_value=100,
        value=int(st.session_state.table_count),
        step=1,
    )

    if st.button("설정 저장", type="primary"):
        st.session_state.table_count = int(count)
        st.success("테이블 설정을 저장했습니다.")

    st.divider()

    st.warning(
        "현재 버전은 세션 기반입니다. "
        "앱을 재시작하면 기록이 사라질 수 있습니다."
    )

    if st.button("모든 호출 기록 초기화"):
        st.session_state.calls = []
        st.success("호출 기록을 초기화했습니다.")
        refresh()


# -------------------------
# 고객 호출 화면
# -------------------------
elif page == "고객 호출":
    st.header("🙋 직원 호출하기")
    st.write("테이블 번호와 요청 사유를 선택하세요.")

    with st.form("call_form"):
        table = st.selectbox(
            "테이블 번호",
            list(range(1, int(st.session_state.table_count) + 1)),
            format_func=lambda n: f"{n}번 테이블",
        )

        reason = st.selectbox(
            "호출 사유",
            CALL_REASONS,
        )

        note = st.text_input(
            "추가 요청 사항 (선택)",
            max_chars=120,
            placeholder="예: 물 두 잔 부탁드립니다",
        )

        submitted = st.form_submit_button(
            "🔔 직원 호출하기",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        call = {
            "id": uuid.uuid4().hex[:8],
            "table": int(table),
            "reason": reason,
            "note": note.strip(),
            "status": "대기 중",
            "created": current_time(),
            "updated": current_time(),
        }

        st.session_state.calls.insert(0, call)
        st.success(f"{table}번 테이블 호출이 접수되었습니다.")

    st.divider()
    st.subheader("📌 해당 테이블 호출 상태")

    active_calls = [
        c for c in st.session_state.calls
        if c["table"] == table and c["status"] != "완료"
    ]

    if active_calls:
        for call in active_calls:
            st.info(
                f"**{call['status']}** · {call['reason']} · "
                f"{call['created']}"
            )
            if call["note"]:
                st.caption(f"요청 내용: {call['note']}")
    else:
        st.success("처리 대기 중인 호출이 없습니다.")


# -------------------------
# 직원 현황판
# -------------------------
else:
    st.header("🧑‍🍳 직원 현황판")

    calls = st.session_state.calls

    waiting = sum(
        c["status"] == "대기 중" for c in calls
    )
    working = sum(
        c["status"] == "처리 중" for c in calls
    )
    done = sum(
        c["status"] == "완료" for c in calls
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("🟠 대기 중", waiting)
    col2.metric("🔵 처리 중", working)
    col3.metric("🟢 완료", done)

    status_filter = st.selectbox(
        "상태 필터",
        ["전체"] + STATUSES,
    )

    table_filter = st.selectbox(
        "테이블 필터",
        ["전체"] + [
            f"{i}번 테이블"
            for i in range(1, int(st.session_state.table_count) + 1)
        ],
    )

    filtered = calls

    if status_filter != "전체":
        filtered = [
            c for c in filtered
            if c["status"] == status_filter
        ]

    if table_filter != "전체":
        table_number = int(table_filter.split("번")[0])
        filtered = [
            c for c in filtered
            if c["table"] == table_number
        ]

    if not filtered:
        st.info("표시할 호출이 없습니다.")

    for call in filtered:
        with st.container(border=True):
            st.subheader(
                f"{call['table']}번 테이블 · {call['reason']}"
            )

            st.caption(
                f"호출 시간: {call['created']} · "
                f"번호: {call['id']}"
            )

            if call["note"]:
                st.write(f"요청 사항: {call['note']}")

            new_status = st.selectbox(
                "처리 상태",
                STATUSES,
                index=STATUSES.index(call["status"]),
                key=f"status_{call['id']}",
            )

            if st.button(
                "상태 저장",
                key=f"save_{call['id']}",
            ):
                call["status"] = new_status
                call["updated"] = current_time()
                st.success("상태가 변경되었습니다.")
                refresh()

    st.divider()

    if st.button("완료된 호출 기록 삭제"):
        st.session_state.calls = [
            c for c in st.session_state.calls
            if c["status"] != "완료"
        ]
        st.success("완료된 호출 기록을 삭제했습니다.")
        refresh()
