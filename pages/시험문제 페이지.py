import streamlit as st
from db import saveScore


di = {
    "q1": {
        "title": "1번문제",
        "1번": False,
        "2번": False,
        "3번": False,
        "4번": True,
    },
    "q2": {
        "title": "2번문제",
        "1번": False,
        "2번": True,
        "3번": False,
        "4번": False,
    },
    "q3": {
        "title": "3번문제",
        "1번": True,
        "2번": False,
        "3번": False,
        "4번": False,
    },
    "q4": {
        "title": "4번문제",
        "1번": False,
        "2번": False,
        "3번": True,
        "4번": False,
    },
    "q5": {
        "title": "5번문제",
        "1번": False,
        "2번": False,
        "3번": False,
        "4번": True,
    },
}

if 'selectValueList' not in st.session_state:
    st.session_state['selectValueList'] = [None] * len(di)  # Initialize with None

def selectValue():
    for q, details in di.items():
        select_val = st.session_state.get(q)
        if select_val:
            st.session_state['selectValueList'][int(q[1]) - 1] = details.get(select_val)
    # st.write(f"답: {st.session_state['selectValueList']}")

for q in di:
    st.radio(
        f"{di[q]['title']} 문제",
        ["1번", "2번", "3번", "4번"],
        key=q,
        on_change=selectValue
    )

if len(st.session_state.selectValueList) != 0:
    true_count = sum(1 for value in st.session_state['selectValueList'] if value)
    total_count = len(st.session_state['selectValueList'])
    st.write(f"정답: {true_count}/{total_count}")

submitted=st.button("제출", type="primary")
if submitted:
    id=st.session_state.id
    saveScore(id=id,value=true_count)