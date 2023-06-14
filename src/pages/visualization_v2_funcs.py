import streamlit as st
from streamlit_agraph import *
from typing import List, Any, Tuple

from src.logic.statements import *
from src.config import *

SEQUENTIAL_AFTER = True

def state_label(state: State, add_cost = False):
    label = ""
    if state.fluents:
        for fluent in state.fluents:
            label += f"{fluent}\n"
    if add_cost:
        label += f"  Total cost: {state.cost}  "
    return label

def new_node(id: int, state: State, color = None):
    label = state_label(state)
    if color is None:
        return Node(id=f"{id}", title=label, label=label, **node_config)
    else:
        return Node(id=f"{id}", title=label, label=label, color=color, **node_config)

def add_node(nodes:List[Node], id:int, state:State, color = None):
    nodes.append(new_node(id, state, color))

def is_positive_fluent(fluent: str):
    return not fluent.count('~ ')

def is_negative_fluent(fluent: str):
    return fluent.count('~ ')

def positive_fluent(fluent: str):
    if is_negative_fluent(fluent):
        return fluent[2:]
    return fluent

def negative_fluent(fluent):
    if is_positive_fluent(fluent):
        return f"~ {fluent}"
    return fluent

def all_possible_states(only_positive_fluents):
    all_states = [[]]
    for fluent in only_positive_fluents:
        new_all_states = []
        for state in all_states:
            new_positive_state = state.copy()
            new_negative_state = state.copy()
            new_positive_state.append(fluent)
            new_negative_state.append(f"~ {fluent}")
            new_all_states.append(new_positive_state)
            new_all_states.append(new_negative_state)
        all_states = new_all_states
    return list(map(lambda list_of_fluents: State(list_of_fluents, 0), all_states))

def add_all_states_as_nodes(states):
    state_node_list = []
    nodes = []
    for i, state in enumerate(states):
        node = new_node(i, state)
        state_node_list.append((state, node))
        nodes.append(node)
    return nodes, state_node_list

def get_state_node_id(current_state: State, state_node_list:List[Tuple[State, Node]]):
    for state, node in state_node_list:
        if current_state == state:
            return node.id
    raise Exception(f"State missing: {state}\n{list(map(lambda x:x[0], state_node_list))}")

def after_statement_satisfied(statement: AfterStatement, performed_actions: List[str], sequential = True):
    if not sequential:
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

def causes_statement_satisfied(statement: CausesStatement, state: State):
    for fluent in statement.if_fluents:
        if fluent not in state.fluents:
            return False
    return True  

def update_state(state: State, fluent_updates: List[str], cost: int = 0):
    for fluent_update in fluent_updates:
        if fluent_update in state.fluents:
            pass
        elif negative_fluent(fluent_update) in state.fluents:
            state.fluents[state.fluents.index(negative_fluent(fluent_update))] = fluent_update
        elif positive_fluent(fluent_update) in state.fluents:
            state.fluents[state.fluents.index(positive_fluent(fluent_update))] = fluent_update
        else:
            state.fluents.append(fluent_update)
    state.cost += cost
    return state

def edge_present(edges:List[Edge], src_id, dst_id):
    for edge in edges:
        if edge.source == src_id and edge.to == dst_id:
            return True
    return False

def _new_after_edge(src_id, dst_id, label, mini_label):
    if BIG_EDGE_LABELS:
        return Edge(source=f"{src_id}", target=f"{dst_id}", title=label, label=label, **after_edge_config)
    else:
        return Edge(source=f"{src_id}", target=f"{dst_id}", title=label, label=mini_label, **after_edge_config)

def _new_causes_edge(src_id, dst_id, label, mini_label):
    if BIG_EDGE_LABELS:
        return Edge(source=f"{src_id}", target=f"{dst_id}", title=label, label=label, **causes_edge_config)
    else:
        return Edge(source=f"{src_id}", target=f"{dst_id}", title=label, label=mini_label, **causes_edge_config)

def new_after_edge(src_id, target_id, statement: AfterStatement):
    label = f"{statement.fluent}\nAFTER\n{', '.join(statement.actions)}"
    mini_label = f"{statement.fluent}"
    return _new_after_edge(src_id, target_id, label, mini_label)

def new_causes_edge(src_id, target_id, statement:CausesStatement):
    label = f"{', '.join(statement.fluents)}\nCAUSED BY\n{statement.action}"
    if len(statement.if_fluents):
        label += f"\nPROVIDED THAT\n{', '.join(statement.if_fluents)}"
    if statement.cost != 0:
        label += f"\nCOST: {statement.cost}"
    mini_label = f"{statement.action} ({', '.join(statement.fluents)})"
    return _new_causes_edge(src_id, target_id, label, mini_label)
