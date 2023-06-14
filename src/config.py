# https://visjs.github.io/vis-network/docs/network/nodes.html#
# https://visjs.github.io/vis-network/docs/network/edges.html


BIG_EDGE_LABELS = False
START_COLOR = '#dfe83c'
INBETWEEN_COLOR = '	#d4bb17'
END_COLOR = '#c28906'
INACTIVE_COLOR = '#6e5b30'


node_config = {
    'shape': 'circle', 
    'scaling': {
        'label': True
    },
    'color': INACTIVE_COLOR,
    'font': {
        'color': 'white',
        'size': 20
    }
}

after_edge_config = {
    'length': 300, 
    'width': 2,
    'arrowStrikethrough': False,
    'color': '#d68711',
    'smooth': {
        'enabled': True,
        'type': 'curvedCCW',
        'roundness': 0.2
    },
    'font': {
        'color': 'white',
        'size': 16,
        'align': 'center',
        'strokeWidth': 0,

    }
}

causes_edge_config = {
    'length': 300, 
    'width': 2,
    'arrowStrikethrough': False,
    'color': '#d9d514',
    'smooth': {
        'enabled': True,
        'type': 'curvedCW',
        'roundness': 0.2
    },
    'font': {
        'color': 'white',
        'size': 16,
        'align': 'center',
        'strokeWidth': 0,
    }
}