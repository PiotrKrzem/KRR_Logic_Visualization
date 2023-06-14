import streamlit as st
import random
from typing import List

from src.logic.statements import *


@st.cache_data
def apply_style():
    with open('style.css')as f:
        style = f.read()
        st.markdown(f"<style>{style}</style>", unsafe_allow_html = True)

def positive_and_negative_fluents() -> List[str]:
    fluents = []
    for fluent in st.session_state.fluents:
        fluents.append(fluent)
        fluents.append(f"~ {fluent}") 
    return fluents

def add_title():
    
    # [data-testid="stSidebarNav"] {
    #     background-image: url(http://placekitten.com/200/200);
    #     background-repeat: no-repeat;
    #     padding-top: 120px;
    #     background-position: 20px 20px;
    # }
    st.markdown(
        """
        <style>

            [data-testid="stSidebarNav"]::before {
                content: "KRR Visualization";
                margin-left: 20px;
                margin-top: 40px;
                font-size: 50px;
                font-weight: bold;
                position: centered;
                top: 100px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

def mock_example():
    statements = [
        InitiallyStatement(fluent="hi"),
        InitiallyStatement(fluent="there"),
        InitiallyStatement(fluent="~ hello"),
        CausesStatement(action="greet", fluents=["~ hi", "~ there", "hello"], if_fluents=[ "hi", "there", '~ hello'], cost=4),
        CausesStatement(action="bang", fluents=["~ hello", "there"], if_fluents=['~ hi', "~ there"], cost=2),
        AfterStatement(fluent='hello', actions=['greet', 'bang'])
    ]
    fluents = ['hi', 'there', 'hello']
    return statements, fluents

def increase_self_reference(inc = 0):
    return {
        'size': 30 + inc * 25
    }