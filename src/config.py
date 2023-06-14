# https://visjs.github.io/vis-network/docs/network/nodes.html#


BIG_EDGE_LABELS = False

node_config = {
    'shape': 'circle', 
    'scaling': {
        'label': True
    }
}

after_edge_config = {
    'length': 300, 
    'width': 4,
    'arrowStrikethrough': False,
    'color': 'green',
    'smooth': {
        'enabled': True,
        'type': 'curvedCCW',
        'roundness': 0.2
    }
}

causes_edge_config = {
    'length': 300, 
    'width': 4,
    'arrowStrikethrough': False,
    'color': 'red',
    'smooth': {
        'enabled': True,
        'type': 'curvedCW',
        'roundness': 0.2
    }
}