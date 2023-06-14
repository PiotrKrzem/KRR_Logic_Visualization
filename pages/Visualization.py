import streamlit as st
from streamlit_agraph import *
from typing import List, Any

from src.logic.statements import *
from src.pages.visualization_funcs import *
from src.utils import apply_style, add_title, mock_example

# from statements import *

SEQUENTIAL_AFTER = True
MAX_LOOPS = 20

def after_statement_satisfied(statement: AfterStatement, performed_actions: List[str]):
    if not SEQUENTIAL_AFTER:
        for action in statement.actions:
            if action not in performed_actions:
                return False
        return True
    else:
        idx = 0
        for action in performed_actions:
            if len(statement.actions) and statement.actions[idx] == action:
                idx += 1
        return len(statement.actions) == idx

def causes_statement_satisfied(statement: CausesStatement, state: List[Any]):
    for fluent in statement.if_fluents:
        if fluent not in state:
            return False
    return True  

def update_state(state: List[Any], updates: List[str], cost: int):
    for update in updates:
        if update in state:
            continue
        elif (update.count('~ ') == 1 and update[2:] in state):
            state[state.index(update[2:])] = update
        elif (update.count('~ ') == 0 and f"~ {update}" in state):
            state[state.index(f"~ {update}")] = update
        else:
            state.append(update)
    state[0] += cost

def add_node(nodes:List[Node], id:int, state:List[Any], color=None):
    text = ""
    if len(state) >= 2:
        for fluent in state[1:]:
            text += f"{fluent}\n"
    text += f"  Total cost: {state[0]}  "
    if color is None:
        nodes.append(Node(id=f"{id}", title=text, label=text, shape='circle', scaling={'label':True}))
    else:
        nodes.append(Node(id=f"{id}", title=text, label=text, shape='circle', scaling={'label':True}, color=color))
    return text

def add_edge(edges:List[Edge], src_id, target_id, label):
    edges.append(Edge(source=f"{src_id}", target=f"{target_id}", type="CURVE_SMOOTH", title=label, label=label, length=300, width=4))

def add_edge_after(edges:List[Edge], src_id, target_id, statement:AfterStatement):
    label = f"{statement.fluent}\nAFTER\n{', '.join(statement.actions)}"
    add_edge(edges, src_id, target_id, label)

def add_edge_causes(edges:List[Edge], src_id, target_id, statement:CausesStatement):
    label = f"{', '.join(statement.fluents)}\nCAUSED BY\n{statement.action}"
    if len(statement.if_fluents):
        label += f"\nPROVIDED THAT\n{', '.join(statement.if_fluents)}"
    if statement.cost != 0:
        label += f"\nCOST: {statement.cost}"
    add_edge(edges, src_id, target_id, label)

def add_node_if_missing(current_state, current_state_id, state_map, nodes):
    keys = list(map(lambda x:x[0], state_map))
    src_id = current_state_id
    add_new_node = current_state not in keys
    if add_new_node:
        new_id = len(state_map) + 1
        state_map.append((current_state.copy(), new_id)) 
        add_node(nodes, new_id, current_state)
    else:
        src_id = current_state_id
        new_id = state_map[keys.index(current_state)][1]
    return src_id, new_id, add_new_node

def color_node_with_current_id(nodes: List[Node], current_state_id, current_state):
    for node in nodes:
        # Cheesy way to compute label coz Im tired
        if add_node([], current_state_id, current_state) == node.title:
            node.color = 'red'

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
    statements, _ = mock_example()

    initially_statements: List[InitiallyStatement] = list(filter(lambda statement:statement.type == INITIALLY, statements))
    causes_statements: List[CausesStatement] = list(filter(lambda statement:statement.type == CAUSES, statements))
    after_statements: List[AfterStatement] = list(filter(lambda statement:statement.type == AFTER, statements))

    current_state = [0]
    current_state.extend(list(map(lambda statement:statement.fluent, initially_statements)))
    current_state_id = 1
    add_node(nodes, current_state_id, current_state, 'yellow')

    performed_actions = []
    state_map = [(current_state.copy(), current_state_id)]
    program_update_was_performed = True
    loop = 0
    while program_update_was_performed and loop < MAX_LOOPS:
        program_update_was_performed = False

        after_update = False
        for statement in after_statements:
            if after_statement_satisfied(statement, performed_actions):
                update_state(current_state, [statement.fluent], 0)
                src_id, current_state_id, add_new_node = add_node_if_missing(current_state, current_state_id, state_map, nodes)
                add_edge_after(edges, src_id, current_state_id, statement)
                after_statements.remove(statement)
                after_update = True
                if add_new_node:
                    loop = 0
                break

        causes_update = False
        if not after_update:
            for statement in causes_statements:
                if causes_statement_satisfied(statement, current_state):
                    update_state(current_state, statement.fluents, statement.cost)
                    src_id, current_state_id, add_new_node = add_node_if_missing(current_state, current_state_id, state_map, nodes)
                    add_edge_causes(edges, src_id, current_state_id, statement)
                    performed_actions.append(statement.action)
                    causes_statements.remove(statement)
                    causes_update = True
                    if add_new_node:
                        loop = 0
                    break

        if causes_update or after_update:
            program_update_was_performed = True
            loop += 1

    color_node_with_current_id(nodes, current_state_id, current_state)
    agraph(nodes, edges, config)
    final_cost = current_state[0]
    final_fluents = current_state[1:]

    bottom_subcol1, bottom_subol2 = st.columns([1, 4])
    with bottom_subcol1:
        st.caption("FINAL STATE")
        st.caption("OVERALL COST")
    with bottom_subol2:
        st.text_input("_", value = f"{', '.join(final_fluents)}", key="output_state", label_visibility='collapsed', disabled=True)
        st.text_input("_", value = f"{final_cost}",key = "overall_cost", label_visibility='collapsed', disabled=True)

def construct():
    apply_style()
    add_title()
    construct_graph()

construct()