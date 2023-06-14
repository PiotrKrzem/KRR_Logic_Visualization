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
    'selfReference': {
        'size': 40
    },
    'color': 'green',
    'smooth': {
        'enabled': True,
        'type': 'curvedCCW',
        'roundness': 0.5
    }
}

causes_edge_config = {
    'length': 300, 
    'width': 4,
    'arrowStrikethrough': False,
    'selfReference': {
        'size': 40
    },
    'color': 'red',
    'smooth': {
        'enabled': True,
        'type': 'curvedCW',
        'roundness': 0.5
    }
}