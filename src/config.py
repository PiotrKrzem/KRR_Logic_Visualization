# https://visjs.github.io/vis-network/docs/network/nodes.html#
# https://visjs.github.io/vis-network/docs/network/edges.html


BIG_EDGE_LABELS = False
START_COLOR = '#dfe83c'
INBETWEEN_COLOR = '	#d4bb17'
END_COLOR = '#c28906'
INACTIVE_COLOR = '#6e5b30'

START_COLOR = '#ed9961'
INBETWEEN_COLOR = '	#eb8d75'
END_COLOR = '#e36259'
INACTIVE_COLOR = '#e0df7e'


node_config = {
    'shape': 'circle', 
    'scaling': {
        'label': True
    },
    'color': INACTIVE_COLOR,
    'font': {
        'color': '#1f1f1b',
        'size': 20
    }
}

after_edge_config = {
    'length': 300, 
    'width': 2,
    'arrowStrikethrough': False,
    'color': '#dba656',
    'smooth': {
        'enabled': True,
        'type': 'curvedCCW',
        'roundness': 0.2
    },
    'font': {
        'color': '#d68711',
        'size': 16,
        'align': 'center',
        'strokeWidth': 0,
        'vadjust': -10,
    }
}

causes_edge_config = {
    'length': 300, 
    'width': 2,
    'arrowStrikethrough': False,
    'color': '#edeb79',
    'smooth': {
        'enabled': True,
        'type': 'curvedCW',
        'roundness': 0.2
    },
    'font': {
        'color': '#d9d514',
        'size': 16,
        'align': 'center',
        'strokeWidth': 0,
        'vadjust': -10,
    }
}