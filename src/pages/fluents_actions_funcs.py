import streamlit as st
from typing import List

from src.logic.statements import *

# On-click actions
def input_fluent():
    fluent = st.session_state.fluent_input
    st.session_state.fluents.append(fluent)
    st.session_state.fluent_input = ""

def input_action():
    action = st.session_state.action_input
    st.session_state.actions.append(action)
    st.session_state.action_input = ""
