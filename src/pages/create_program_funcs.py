import streamlit as st
from typing import List

from src.logic.statements import *

def input_statement():
    statement_type = st.session_state.statement_select
    statement: Statement
    if statement_type == INITIALLY:
        statement = InitiallyStatement()
        statement.fluent = st.session_state.initially_fluent_select
        statement.markdown = f"**INITIALLY** {statement.fluent}"
        for addedStatement in filter(lambda x:isinstance(x, InitiallyStatement), st.session_state.statements):
            if addedStatement.fluent.replace("~ ","") == statement.fluent.replace("~ ",""):
                statement.markdown = "error"
    elif statement_type == CAUSES:
        statement = CausesStatement()
        statement.action = st.session_state.causes_action_select
        statement.markdown = f"{statement.action} **CAUSES** "
        for idx, fluent in enumerate(st.session_state.causes_fluent_select):
            statement.fluents.append(fluent)
            statement.markdown += f"{fluent}"
            statement.markdown += ", " if idx < len(st.session_state.causes_fluent_select) - 1 else " "
            if "~" in fluent:
                if fluent.replace("~ ","") in statement.fluents:
                    statement.markdown = "error"
            else:
                if f"~ {fluent}" in statement.fluents:
                    statement.markdown = "error"
        if len(st.session_state.causes_if_fluents_select) and statement.markdown != "error":
            statement.markdown += f"**IF** "
            for idx, fluent in enumerate(st.session_state.causes_if_fluents_select):
                statement.if_fluents.append(fluent)
                statement.markdown += f"{fluent} "
                statement.markdown += ", " if idx < len(st.session_state.causes_if_fluents_select) - 1 else " "
                if "~" in fluent:
                    if fluent.replace("~ ","") in statement.if_fluents:
                        statement.markdown = "error"
                else:
                    if f"~ {fluent}" in statement.if_fluents:
                        statement.markdown = "error"
        for addedStatement in filter(lambda x:isinstance(x, CausesStatement), st.session_state.statements):
            if statement.markdown in addedStatement.markdown:
                statement.markdown = "error"
        if statement.markdown != "error":
            statement.cost = int(st.session_state.causes_cost)
            statement.markdown += f"**COST** {statement.cost}"
        for fluent in st.session_state.causes_fluent_select:
            if fluent in statement.if_fluents:
                statement.markdown = "error"
    elif statement_type == AFTER:
        statement = AfterStatement()
        statement.fluent = st.session_state.after_fluent_select
        statement.markdown = f"{statement.fluent} **AFTER** "
        for idx, action in enumerate(st.session_state.after_action_select):
            statement.actions.append(action)
            statement.markdown += f"{action}"
            statement.markdown += ", " if idx < len(st.session_state.after_action_select) - 1 else ""
        for addedStatement in filter(lambda x:isinstance(x, AfterStatement), st.session_state.statements):
            for action in statement.actions:
                if action in addedStatement.actions and statement.fluent == addedStatement.fluent:
                    statement.markdown = "error"
    if statement.markdown != "error":
        st.session_state.statements.append(statement)