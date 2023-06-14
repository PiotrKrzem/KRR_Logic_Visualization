import streamlit as st
from typing import List
import re

from src.logic.statements import *

# On-click actions
def input_fluent():
    fluent = st.session_state.fluent_input
    if fluent not in st.session_state.fluents and not re.search("^.*~.*$", fluent):
        st.session_state.fluents.append(fluent)
        st.session_state.fluent_input = ""

def input_action():
    action = st.session_state.action_input
    if action not in st.session_state.actions:
        st.session_state.actions.append(action)
        st.session_state.action_input = ""

def delete_fluent(idx: int):
    st.session_state.fluents.pop(idx)

def delete_action(idx: int):
    st.session_state.actions.pop(idx)
