import streamlit as st
from typing import List

def positive_and_negative_fluents() -> List[str]:
    fluents = []
    for fluent in st.session_state.fluents:
        fluents.append(fluent)
        fluents.append(f"~ {fluent}") 
    return fluents

@st.cache_data
def apply_style():
    with open('style.css')as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

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