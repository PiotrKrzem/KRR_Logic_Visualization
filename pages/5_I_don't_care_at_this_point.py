import streamlit as st
from streamlit_agraph import *
from typing import List, Any

from src.logic.statements import *
from src.pages.idc_funcs import *
from src.utils import apply_style, add_title, mock_example

# from statements import *

MAX_LOOPS = 20

def construct_summary_panel(current_state: State):
    final_cost = current_state.cost
    final_fluents = current_state.fluents

    bottom_subcol1, bottom_subol2 = st.columns([1, 4])
    with bottom_subcol1:
        st.caption("OVERALL COST")
        st.caption("FINAL STATE")
    with bottom_subol2:
        st.text_input("_", value = f"{final_cost}",key = "overall_cost", label_visibility='collapsed', disabled=True)
        st.text_input("_", value = f"{', '.join(final_fluents)}", key="output_state", label_visibility='collapsed', disabled=True)

def construct_graph():
    nodes = []
    edges = []
    config = Config(height=900,
		            width=1600, 
                    nodeHighlightBehavior=False,
                    highlightColor="#F7A7A6", 
                    directed=True, 
                    collapsible=True,
                    physics=False
    )

    statements: List[Statement] = st.session_state.statements
    fluents: List[str] = st.session_state.fluents

    # statements, fluents = mock_example()

    initially_statements: List[InitiallyStatement] = list(filter(lambda statement:statement.type == INITIALLY, statements))
    causes_statements: List[CausesStatement] = list(filter(lambda statement:statement.type == CAUSES, statements))
    after_statements: List[AfterStatement] = list(filter(lambda statement:statement.type == AFTER, statements))
    program_state = State(list(map(lambda statement:statement.fluent, initially_statements)), 0)

    states = all_possible_states(fluents)
    nodes, state_node_list = add_all_states_as_nodes(states)
    causes_edges, after_edges = [], []

    for state in states:
        current_state = State(state.fluents.copy(), state.cost)
        pretty_paint = state == program_state
        if pretty_paint:
            start_node_id = get_state_node_id(current_state, state_node_list)
            color_node(start_node_id, nodes, START_COLOR)

        performed_actions = []
        state_causes_statements = causes_statements.copy()
        state_after_statements = after_statements.copy()

        causes_statement_was_satisfied = False
        for causes_statement in state_causes_statements:
            src_id = get_state_node_id(current_state, state_node_list)
            if causes_statement_satisfied(causes_statement, current_state):
                causes_statement_was_satisfied = True
                current_state = update_state(current_state, causes_statement.fluents, 0)
            
            dst_id = get_state_node_id(current_state, state_node_list)
            performed_actions.append(causes_statement.action)

            after_statement_was_satisfied = False
            for after_statement in state_after_statements:
                if after_statement_satisfied(after_statement, performed_actions):
                    after_statement_was_satisfied = True
                    current_state = update_state(current_state, [after_statement.fluent], 0)
                    dst_id = get_state_node_id(current_state, state_node_list)
                    _, mini_label = new_after_edge_labels(causes_statement, after_statement, causes_statement_was_satisfied)
                    if not edge_present(after_edges, src_id, dst_id, mini_label):
                        self_references = count_self_references(causes_edges, after_edges, src_id, dst_id)
                        after_edges.append(new_after_edge(src_id, dst_id, causes_statement, after_statement, causes_statement_was_satisfied, self_references))
                    state_after_statements.remove(after_statement)
                    break

            if not after_statement_was_satisfied:
                _, mini_label = new_causes_edge_labels(causes_statement, causes_statement_was_satisfied)
                if not edge_present(causes_edges, src_id, dst_id, mini_label):
                    self_references = count_self_references(causes_edges, after_edges, src_id, dst_id)
                    causes_edges.append(new_causes_edge(src_id, dst_id, causes_statement, causes_statement_was_satisfied, self_references))
            if pretty_paint and src_id != dst_id:
                node_id = get_state_node_id(current_state, state_node_list)
                color_node(node_id, nodes, INBETWEEN_COLOR)

        if pretty_paint:
            end_node_id = get_state_node_id(current_state, state_node_list)
            color_node(end_node_id, nodes, END_COLOR)

    edges = [*causes_edges, *after_edges]
    agraph(nodes, edges, config)

def construct():
    apply_style()
    add_title()
    construct_graph()

construct()