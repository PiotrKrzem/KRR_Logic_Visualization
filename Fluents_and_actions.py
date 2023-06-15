import streamlit as st
from typing import List

from src.pages.fluents_actions_funcs import *
from src.utils import apply_style, add_title

def main_config():
    st.set_page_config(page_title='KRR Application', page_icon=':bar_chart:', layout='wide')

def initialize_session():
    if 'initialize' not in st.session_state:
        st.session_state.initialize = True

        st.session_state.fluents = []
        st.session_state.actions = []
        st.session_state.statements = []
        st.session_state.query_statements = []
        st.session_state.queries = []
        st.session_state.queries_outcomes = []

        st.session_state.fluent_input = ""
        st.session_state.action_input = ""

def construct_add_fluent_add_action_panel():
    st.subheader("ADD FLUENT")
    st.divider()
    value = st.text_input("Enter fluent name", key="fluent_input")
    if value:
        input_fluent(False)
        
    st.button("ADD FLUENT", on_click=input_fluent)

    st.divider()

    st.subheader("ADD ACTION")
    value = st.text_input("Enter action name", key="action_input")
    if value:
        input_action(False)
    st.button("ADD ACTION", on_click=input_action)

def construct_fluents_view():
    subcol1, subol2 = st.columns([1, 2])
    with subcol1:
        st.subheader("FLUENTS")
    st.divider()
    # with subol2:
    #     file = st.file_uploader("IMPORT", type = "txt", key = "fluent_upload")
    #     if file is not None:
    #         pass
    for idx, item in enumerate(st.session_state.fluents):
        fluent_col1, fluent_col2 = st.columns([5, 1])
        
        with fluent_col1:
            st.markdown(f"**{item}**")
        with fluent_col2:
            if st.button(":x:", key = f"fluent_button_{idx}"):
                delete_fluent(idx)
                st.experimental_rerun() 

def construct_actions_view():
    subcol1, subol2 = st.columns([1, 2])
    with subcol1:
        st.subheader("ACTIONS")
    st.divider()

    # with subol2:
    #     file = st.file_uploader("IMPORT", type = "txt", key = "action_upload")
    #     if file is not None:
    #         pass
    for idx, item in enumerate(st.session_state.actions):
        action_col1, action_col2 = st.columns([5, 1])
        
        with action_col1:
            st.markdown(f"**{item}**")
        with action_col2:
            if st.button(":x:", key = f"action_button_{idx}"):
                delete_action(idx)
                st.experimental_rerun()

def construct():
    main_config()
    apply_style()
    initialize_session()

    add_title()
    top_col1, top_col2, top_col3 = st.columns([1, 1, 1])
    with top_col1:
        construct_add_fluent_add_action_panel()
    with top_col2:
        construct_fluents_view()
    with top_col3:
        construct_actions_view()

construct()