import streamlit as st
from streamlit_agraph import *
from typing import List, Any

from src.logic.statements import *
from src.pages.visualization_v2_funcs import *
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
                    collapsible=True
    )

    # statements: List[Statement] = st.session_state.statements
    # fluents: List[str] = st.session_state.fluents

    statements, fluents = mock_example()

    initially_statements: List[InitiallyStatement] = list(filter(lambda statement:statement.type == INITIALLY, statements))
    causes_statements: List[CausesStatement] = list(filter(lambda statement:statement.type == CAUSES, statements))
    after_statements: List[AfterStatement] = list(filter(lambda statement:statement.type == AFTER, statements))
    program_state = State(list(map(lambda statement:statement.fluent, initially_statements)), 0)

    states = all_possible_states(fluents)
    nodes, state_node_list = add_all_states_as_nodes(states)
    causes_edges, after_edges = [], []

    print("Graph in construction...")
    for state in states:
        current_state = State(state.fluents.copy(), state.cost)

        loop = 0
        performed_actions = []
        state_causes_statements = causes_statements.copy()
        state_after_statements = after_statements.copy()
        program_update_was_performed = True
        while program_update_was_performed and loop < MAX_LOOPS:
            program_update_was_performed = False

            for statement in state_after_statements:
                if after_statement_satisfied(statement, performed_actions):
                    src_id = get_state_node_id(current_state, state_node_list)
                    current_state = update_state(current_state, [statement.fluent], 0)
                    dst_id = get_state_node_id(current_state, state_node_list)
                    if not edge_present(after_edges, src_id, dst_id):
                        after_edges.append(new_after_edge(src_id, dst_id, statement))
                        loop = 0
                    else:
                        loop += 1
                    state_after_statements.remove(statement)
                    program_update_was_performed = True
                    break

            for statement in state_causes_statements:
                if causes_statement_satisfied(statement, current_state):
                    src_id = get_state_node_id(current_state, state_node_list)
                    current_state = update_state(current_state, statement.fluents, 0)
                    dst_id = get_state_node_id(current_state, state_node_list)

                    if not edge_present(causes_edges, src_id, dst_id):
                        causes_edges.append(new_causes_edge(src_id, dst_id, statement))
                        loop = 0
                    else:
                        loop += 1
                    performed_actions.append(statement.action)
                    program_update_was_performed = True
                    break

    print("Finished!")
                    
    edges = [*causes_edges, *after_edges]
    agraph(nodes, edges, config)

    # current_state = [0]
    # current_state.extend(list(map(lambda statement:statement.fluent, initially_statements)))
    # current_state_id = 1
    # add_node(nodes, current_state_id, current_state, 'yellow')
    # # while ...
    # color_node_with_current_id(nodes, current_state_id, current_state)

    construct_summary_panel(current_state)
    

def construct():
    apply_style()
    add_title()
    construct_graph()

construct()