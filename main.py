from dataclasses import dataclass, field
import streamlit as st
from typing import List

st.set_page_config(page_title='KRR Application', page_icon=':bar_chart:', layout='wide')
st.title('KRR Visualization')

with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

if 'initialize' not in st.session_state:
    st.session_state.initialize = True

    st.session_state.fluents = []
    st.session_state.actions = []
    st.session_state.statements = []

    st.session_state.fluent_input = ""
    st.session_state.action_input = ""

@dataclass
class Statement:
    type: str = ""
    markdown: str = ""

@dataclass
class InitiallyStatement(Statement):
    type: str = 'initially'
    fluent: str = ""

@dataclass
class CausesStatement(Statement):
    type: str = 'causes'
    action: str = ""
    fluents: List[str] = field(default_factory=list)
    if_fluent: str = ""
    cost: int  = 0

@dataclass
class AfterStatement(Statement):
    type: str = 'after'
    fluent: str = ""
    actions: List[str] = field(default_factory=list)

def input_fluent():
    fluent = st.session_state.fluent_input
    st.session_state.fluents.append(fluent)
    st.session_state.fluent_input = ""

def input_action():
    action = st.session_state.action_input
    st.session_state.actions.append(action)
    st.session_state.action_input = ""

def input_statement():
    statement_type = st.session_state.statement_select
    statement: Statement
    if statement_type == 'initially':
        statement = InitiallyStatement()
        statement.fluent = st.session_state.initially_fluent_select
        statement.markdown = f"**INITIALLY** {statement.fluent}"
    elif statement_type == 'causes':
        statement = CausesStatement()
        statement.action = st.session_state.causes_action_select
        statement.markdown = f"{statement.action} **CAUSES** "
        print(st.session_state.causes_fluent_select)
        for idx, fluent in enumerate(st.session_state.causes_fluent_select):
            statement.fluents.append(fluent)
            statement.markdown += f"{fluent}"
            statement.markdown += ", " if idx < len(st.session_state.causes_fluent_select) - 1 else " "
        if st.session_state.causes_if_fluent_select is not None:
            statement.if_fluent = st.session_state.causes_if_fluent_select
            statement.markdown += f"**IF** {statement.if_fluent} "
        statement.cost = int(st.session_state.causes_cost)
        statement.markdown += f"**COST** {statement.cost}"
    elif statement_type == 'after':
        statement = AfterStatement()
        statement.fluent = st.session_state.after_fluent_select
        statement.markdown = f"{statement.fluent} **AFTER** "
        for idx, action in enumerate(st.session_state.after_action_select):
            statement.actions.append(action)
            statement.markdown += f"{action}"
            statement.markdown += ", " if idx < len(st.session_state.after_action_select) - 1 else ""

    st.session_state.statements.append(statement)



def positive_and_negative_fluents() -> List[str]:
    fluents = []
    for fluent in st.session_state.fluents:
        fluents.append(fluent)
        fluents.append(f"~ {fluent}") 
    return fluents

top_col1, top_col2, top_col3 = st.columns([1, 1, 1])
with top_col1:
    st.subheader("ADD FLUENT")
    st.text_input("Enter fluent name", key="fluent_input")
    st.button("ADD FLUENT", on_click=input_fluent)

    st.divider()

    st.subheader("ADD ACTION")
    st.text_input("Enter fluent name", key="action_input")
    st.button("ADD ACTION", on_click=input_action)

with top_col2:
    subcol1, subol2 = st.columns([1, 2])
    with subcol1:
        st.subheader("FLUENTS")
    with subol2:
        file = st.file_uploader("IMPORT", type = "txt", key = "fluent_upload")
        if file is not None:
            pass
    for idx, item in enumerate(st.session_state.fluents):
        fluent_col1, fluent_col2 = st.columns([5, 1])
        
        with fluent_col1:
            st.markdown(f"**{item}**")
        with fluent_col2:
            if st.button(":x:", key = f"fluent_button_{idx}"):
                st.session_state.fluents.pop(idx)

with top_col3:
    subcol1, subol2 = st.columns([1, 2])
    with subcol1:
        st.subheader("ACTIONS")
    with subol2:
        file = st.file_uploader("IMPORT", type = "txt", key = "action_uploader")
        if file is not None:
            pass
    for idx, item in enumerate(st.session_state.actions):
        action_col1, action_col2 = st.columns([5, 1])
        
        with action_col1:
            st.markdown(f"**{item}**")
        with action_col2:
            if st.button(":x:", key = f"action_button_{idx}"):
                st.session_state.fluents.pop(idx)

st.divider()

bottom_col1, bottom_col2 = st.columns([1, 2])
with bottom_col1:
    st.subheader("ADD STATEMENT")
    option = st.selectbox("Select statement type", ("initially", "causes", "after"), key="statement_select")
    if option == "initially":
        initially_col1, initially_col2 = st.columns([1, 1])
        with initially_col1:
            st.caption("INITIALLY")
        with initially_col2:
            initially_fluent_option = st.selectbox("_", positive_and_negative_fluents(), key="initially_fluent_select", label_visibility='collapsed')
    elif option == "causes":
        causes_col1, causes_col2 = st.columns([1, 1])
        with causes_col1:
            causes_action_option = st.selectbox("_", st.session_state.actions, key="causes_action_select", label_visibility='collapsed')
            causes_fluent_options = st.multiselect("_", positive_and_negative_fluents(), key="causes_fluent_select", label_visibility='collapsed')
            causes_if_fluent_option = st.selectbox("_", positive_and_negative_fluents(), key="causes_if_fluent_select", label_visibility='collapsed')
            causes_cost = st.number_input("_", 0, 9999, key="causes_cost", label_visibility='collapsed')
        with causes_col2:
            st.caption("CAUSES")
            st.caption("IF")
            st.caption("COST")
    elif option == "after":
        after_col1, after_col2 = st.columns([1, 1])
        with after_col1:
            after_fluent_option = st.selectbox("_", positive_and_negative_fluents(), key="after_fluent_select", label_visibility='collapsed')
            after_action_option = st.multiselect("_", st.session_state.actions, key="after_action_select", label_visibility='collapsed')
        with after_col2:
            st.caption("AFTER")
    st.button("ADD STATEMENT", on_click=input_statement)

with bottom_col2:
    subcol1, subol2 = st.columns([2, 1])
    with subcol1:
        st.subheader("PROGRAM")
    with subol2:
        file = st.file_uploader("IMPORT", type = "txt", key = "program_uploader")

    for idx, item in enumerate(st.session_state.statements):
        statement_col1, statement_col2, statement_col3, statement_col4 = st.columns([20, 1, 1, 1])
        
        with statement_col1:
            st.markdown(item.markdown)
        with statement_col2:
            if st.button(":x:", key = f"statement_button_{idx}"):
                st.session_state.statements.pop(idx)
        with statement_col3:
            if st.button(":arrow_up_small:", key = f"statement_up_button_{idx}"):
                if idx != 0:
                    st.session_state.statements[idx], st.session_state.statements[idx - 1] = st.session_state.statements[idx - 1], st.session_state.statements[idx]
        with statement_col4:
            if st.button(":arrow_down_small:", key = f"statement_down_button_{idx}"):
                if idx < len(st.session_state.statements) - 1:
                    st.session_state.statements[idx], st.session_state.statements[idx + 1] = st.session_state.statements[idx + 1], st.session_state.statements[idx]

    if st.button("EXECUTE PROGRAM"):
        pass
    bottom_subcol1, bottom_subol2 = st.columns([1, 4])
    with bottom_subcol1:
        st.caption("FINAL STATE")
        st.caption("OVERALL COST")
    with bottom_subol2:
        st.text_input("_", key="output_state", label_visibility='collapsed')
        st.text_input("_", key="overall_cost", label_visibility='collapsed')
