import streamlit as st
from typing import List

from src.logic.statements import *
from src.pages.create_program_funcs import *
from src.utils import positive_and_negative_fluents
from src.utils import apply_style, add_title


def construct_add_statement_panel():
    st.subheader("ADD STATEMENT")
    option = st.selectbox("Select statement type", (INITIALLY, CAUSES, AFTER), key="statement_select")
    if option == INITIALLY:
        initially_col1, initially_col2 = st.columns([1, 1])
        with initially_col1:
            st.caption("INITIALLY")
        with initially_col2:
            initially_fluent_option = st.selectbox("_", positive_and_negative_fluents(), key="initially_fluent_select", label_visibility='collapsed')
    elif option == CAUSES:
        causes_col1, causes_col2 = st.columns([1, 1])
        with causes_col1:
            causes_action_option = st.selectbox("_", st.session_state.actions, key="causes_action_select", label_visibility='collapsed')
            causes_fluent_options = st.multiselect("_", positive_and_negative_fluents(), key="causes_fluent_select", label_visibility='collapsed')
            causes_if_fluents_option = st.multiselect("_", positive_and_negative_fluents(), key="causes_if_fluents_select", label_visibility='collapsed')
            causes_cost = st.number_input("_", 0, 9999, key="causes_cost", label_visibility='collapsed')
        with causes_col2:
            st.caption("CAUSES")
            st.caption("IF")
            st.caption("COST")
    elif option == AFTER:
        after_col1, after_col2 = st.columns([1, 1])
        with after_col1:
            after_fluent_option = st.selectbox("_", positive_and_negative_fluents(), key="after_fluent_select", label_visibility='collapsed')
            after_action_option = st.multiselect("_", st.session_state.actions, key="after_action_select", label_visibility='collapsed')
        with after_col2:
            st.caption("AFTER")
    st.button("ADD STATEMENT", on_click=input_statement)

def construct_program_view_panel():
    subcol1, subol2 = st.columns([2, 1])
    with subcol1:
        st.subheader("PROGRAM")
    with subol2:
        file = st.file_uploader("IMPORT", type = "txt", key = "program_upload")
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


def construct():
    apply_style()
    add_title()
    bottom_col1, bottom_col2 = st.columns([1, 2])
    with bottom_col1:
        construct_add_statement_panel()
    with bottom_col2:
        construct_program_view_panel()

construct()
