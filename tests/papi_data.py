PROJECT_NAME = 'Global project'
WELL_NAME = 'Lateral'
INTERPRETATION_NAME = 'Interpretation'

STARRED_INTERPRETATION_NAME = 'Starred Interpretation'
STARRED_INTERPRETATION_ID = 'ddb9700c-fdf9-46c9-a12a-1939cb6890a1'

HORIZON_NAME = 'Horizon'

TARGET_LINE_NAME = 'Target Line'
STARRED_TARGET_LINE_ID = '5623ac16-ca3f-4e77-8416-4365c274bf5d'
STARRED_TARGET_LINE_NAME = 'Starred Target Line'

NESTED_WELL_NAME = 'Nested Well'
STARRED_NESTED_WELL_NAME = 'Starred Nested Well'
STARRED_NESTED_WELL_ID = '3408e926-0ccf-4698-b453-509dd793db94'

PROJECTS_DATA_RESPONSE = {
    'content': [
        {
            'uuid': '3e684dbc-37ed-4827-b677-dc0e3febc432',
            'name': PROJECT_NAME,
            'measure_unit': 'FOOT',
            'role': 'MANAGER',
            'accessed_on': '2022-06-30T08:26:30Z',
            'modified_on': '2022-06-24T13:30:32Z'
        },
        {
            'uuid': 'a721009f-f71a-4c35-b6ad-084ca1cd624f',
            'name': 'Global project 2',
            'measure_unit': 'METER',
            'role': 'MANAGER',
            'accessed_on': '2022-05-20T19:56:52Z',
            'modified_on': '2022-05-20T18:17:35Z'
        }
    ],
    'offset': 0,
    'limit': 100,
    'total': 2,
    'first': True,
    'last': True
}

VIRTUAL_PROJECTS_DATA_RESPONSE = {
    'content': [
        {
            'uuid': '4e684dbc-37ed-4827-b677-dc0e3febc432',
            'name': 'Virtual project',
            'measure_unit': 'FOOT',
            'role': 'MANAGER',
            'accessed_on': '2022-06-30T08:26:30Z',
            'modified_on': '2022-06-24T13:30:32Z'
        },
        {
            'uuid': 'b721009f-f71a-4c35-b6ad-084ca1cd624f',
            'name': 'Virtual project 2',
            'measure_unit': 'METER',
            'role': 'MANAGER',
            'accessed_on': '2022-05-20T19:56:52Z',
            'modified_on': '2022-05-20T18:17:35Z'
        }
    ],
    'offset': 0,
    'limit': 100,
    'total': 2,
    'first': True,
    'last': True
}

WELLS_DATA_RESPONSE = {
    'content': [
        {
            'uuid': '85fa6e44-3507-40b6-a7e2-ee07be241ac7',
            'name': WELL_NAME,
            'api': 'Lateral API',
            'operator': 'Lateral Operator',
            'xsrf_real': {
                'val': 500000.0
            },
            'ysrf_real': {
                'val': 600000.0
            },
            'kb': {
                'val': 394.0
            },
            'convergence': {
                'val': 0.017453292519944444
            },
            'tie_in_tvd': {
                'val': 0.0
            },
            'tie_in_ns': {
                'val': 0.0
            },
            'tie_in_ew': {
                'val': 0.0
            },
            'azimuth': {
                'val': 5.672320068981945
            },
            'starred': {
                'target_line': STARRED_TARGET_LINE_ID,
                'nested_well': STARRED_NESTED_WELL_ID,
                'interpretation': STARRED_INTERPRETATION_ID
            }
        },
        {
            'uuid': '95fa6e44-3507-40b6-a7e2-ee07be241ac7',
            'name': 'Lateral 2',
            'api': 'Lateral 2 API',
            'operator': 'Lateral 2 Operator',
            'xsrf_real': {
                'val': 600000.0
            },
            'ysrf_real': {
                'val': 700000.0
            },
            'kb': {
                'val': 494.0
            },
            'convergence': {
                'val': 0.027453292519944444
            },
            'tie_in_tvd': {
                'val': 0.0
            },
            'tie_in_ns': {
                'val': 0.0
            },
            'tie_in_ew': {
                'val': 0.0
            },
            'azimuth': {
                'val': 5.372320068981945
            },
            'starred': {
                'target_line': STARRED_TARGET_LINE_ID,
                'nested_well': STARRED_NESTED_WELL_ID,
                'interpretation': STARRED_INTERPRETATION_ID
            }
        }
    ],
    'offset': 0,
    'limit': 100,
    'total': 2,
    'first': True,
    'last': True
}

TRAJECTORY_DATA_RESPONSE = {
    'content': [
        {'azim': {'val': 0}, 'incl': {'val': 0}, 'md': {'val': 0}},
        {'azim': {'val': 0}, 'incl': {'val': 0}, 'md': {'val': 0.9143999999999999}},
        {'azim': {'val': 0}, 'incl': {'val': 0}, 'md': {'val': 1.8287999999999998}},
        {'azim': {'val': 0}, 'incl': {'val': 0}, 'md': {'val': 2.7432000000000003}},
        {'azim': {'val': 0}, 'incl': {'val': 0.5235987755983332}, 'md': {'val': 3.6575999999999995}},
        {'azim': {'val': 0}, 'incl': {'val': 0.8726646259972222}, 'md': {'val': 6.095999999999999}},
        {'azim': {'val': 0}, 'incl': {'val': 1.0471975511966665}, 'md': {'val': 9.143999999999998}},
        {'azim': {'val': 0}, 'incl': {'val': 1.0471975511966665}, 'md': {'val': 10.668}},
        {'azim': {'val': 0}, 'incl': {'val': 1.2217304763961108}, 'md': {'val': 11.277599999999998}},
        {'azim': {'val': 0}, 'incl': {'val': 1.3962634015955555}, 'md': {'val': 15.239999999999998}},
        {'azim': {'val': 0}, 'incl': {'val': 1.4835298641952777}, 'md': {'val': 24.383999999999997}},
        {'azim': {'val': 0}, 'incl': {'val': 1.570796326795}, 'md': {'val': 30.479999999999997}},
        {'azim': {'val': 0}, 'incl': {'val': 1.570796326795}, 'md': {'val': 31.3944}},
        {'azim': {'val': 0}, 'incl': {'val': 1.570796326795}, 'md': {'val': 33.2232}},
        {'azim': {'val': 0}, 'incl': {'val': 1.605702911834889}, 'md': {'val': 36.57599999999999}},
        {'azim': {'val': 0}, 'incl': {'val': 1.5882496193149445}, 'md': {'val': 39.623999999999995}},
        {'azim': {'val': 0}, 'incl': {'val': 1.570796326795}, 'md': {'val': 54.86399999999999}},
        {'azim': {'val': 0}, 'incl': {'val': 1.570796326795}, 'md': {'val': 76.19999999999999}},
        {'azim': {'val': 0}, 'incl': {'val': 1.605702911834889}, 'md': {'val': 79.24799999999999}},
        {'azim': {'val': 0}, 'incl': {'val': 1.6580627893947222}, 'md': {'val': 82.29599999999999}}
    ]
}

INTERPRETATIONS_DATA_RESPONSE = {
    'content': [
        {
            'uuid': STARRED_INTERPRETATION_ID,
            'name': STARRED_INTERPRETATION_NAME,
            'properties': {
                'cutoff': {
                    'val': 0
                },
                'palette': 10,
                'lightness': 0,
                'transparency': 0,
                'typelogFillUuid': '39980ce2-2961-4a35-8baf-8941e9b0169a',
                'extensionGridUuid': '00000000-0000-0000-0000-000000000000',
                'faultLabelVisible': True,
                'reverse_extension': False,
                'zero_horizon_uuid': '00000000-0000-0000-0000-000000000000',
                'coloredLogsVisible': True,
                'boundaryPointsColor': '#ffa5a5a5',
                'interpretationExtend': {
                    'val': 0
                },
                'boundaryPointsVisible': True,
                'display_hidden_segment': True
            },
            'owner': 3,
            'mode': 'PUBLIC'
        },
        {
            'uuid': 'a4811211-cf40-4b2a-9536-aa7f41b56b08',
            'name': INTERPRETATION_NAME,
            'properties': {
                'cutoff': {
                    'val': 0
                },
                'palette': 10,
                'lightness': 0,
                'transparency': 0,
                'typelogFillUuid': '39980ce2-2961-4a35-8baf-8941e9b0169a',
                'extensionGridUuid': '00000000-0000-0000-0000-000000000000',
                'faultLabelVisible': True,
                'reverse_extension': False,
                'zero_horizon_uuid': '00000000-0000-0000-0000-000000000000',
                'coloredLogsVisible': True,
                'boundaryPointsColor': '#ffa5a5a5',
                'interpretationExtend': {
                    'val': 0
                },
                'boundaryPointsVisible': True,
                'display_hidden_segment': True
            },
            'owner': 1,
            'mode': 'PUBLIC'
        },
        {
            'uuid': '1e78d781-4804-42b6-974f-6f53830d9fb7',
            'name': 'Interpretation 2',
            'properties': {
                'cutoff': {
                    'val': 0
                },
                'palette': 10,
                'lightness': 0,
                'transparency': 0,
                'typelogFillUuid': '39980ce2-2961-4a35-8baf-8941e9b0169a',
                'extensionGridUuid': '00000000-0000-0000-0000-000000000000',
                'faultLabelVisible': True,
                'reverse_extension': False,
                'zero_horizon_uuid': '00000000-0000-0000-0000-000000000000',
                'coloredLogsVisible': True,
                'boundaryPointsColor': '#ffa5a5a5',
                'interpretationExtend': {
                    'val': 0
                },
                'boundaryPointsVisible': True,
                'display_hidden_segment': True
            },
            'owner': 2,
            'mode': 'PUBLIC'
        }
    ],
    'offset': 0,
    'limit': 100,
    'total': 3,
    'first': True,
    'last': True
}

HORIZONS_DATA_RESPONSE = {
    'content': [
        {
            'uuid': '55e53b91-8dee-4e42-94c0-77f476fbd52f',
            'name': 'Horizon'
        },
        {
            'uuid': '586a5e44-2a1c-402d-88bf-e82304e8fa2e',
            'name': 'Horizon 2'
        }
    ],
    'offset': 0,
    'limit': 100,
    'total': 2,
    'first': True,
    'last': True
}

ASSEMBLED_SEGMENTS_DATA_RESPONSE = {
    'assembled_segments': {
        'horizons': {
            '55e53b91-8dee-4e42-94c0-77f476fbd52f': {
                'tvd': {'val': 3321.1804093826713},
                'uuid': '55e53b91-8dee-4e42-94c0-77f476fbd52f'
            },
            '586a5e44-2a1c-402d-88bf-e82304e8fa2e': {
                'tvd': {'val': 4237.059795448965},
                'uuid': '586a5e44-2a1c-402d-88bf-e82304e8fa2e'
            }
        },
        'segments': [
            {
                'uuid': 'fd682038-ca80-42a8-8f83-cf1877d7d655',
                'boundary_type': 1,
                'end': {'val': 0},
                'horizon_shifts': {
                    '55e53b91-8dee-4e42-94c0-77f476fbd52f': {
                        'end': {'val': -1296.4421136765654},
                        'start': {'val': -1311.3665351848522},
                        'uuid': '55e53b91-8dee-4e42-94c0-77f476fbd52f'
                    },
                    '586a5e44-2a1c-402d-88bf-e82304e8fa2e': {
                        'end': {'val': -1296.4421136765654},
                        'start': {'val': -1311.3665351848522},
                        'uuid': '586a5e44-2a1c-402d-88bf-e82304e8fa2e'
                    }
                },
                'md': {'val': 9.143999999999998},
                'start': {'val': 0}
            },
            {
                'uuid': '671876d6-35f5-4046-9b80-b6b7e66dfc08',
                'boundary_type': 1,
                'end': {'val': 0},
                'horizon_shifts': {
                    '55e53b91-8dee-4e42-94c0-77f476fbd52f': {
                        'end': {'val': -1301.7226984967617},
                        'start': {'val': -1296.4421136765654},
                        'uuid': '55e53b91-8dee-4e42-94c0-77f476fbd52f'
                    },
                    '586a5e44-2a1c-402d-88bf-e82304e8fa2e': {
                        'end': {'val': -1301.7226984967617},
                        'start': {'val': -1296.4421136765654},
                        'uuid': '586a5e44-2a1c-402d-88bf-e82304e8fa2e'
                    }
                },
                'md': {'val': 3170.0580252785107},
                'start': {'val': 0}
            }
        ]
    }
}

TARGET_LINES_DATA_RESPONSE = {
    'content': [
        {
            'uuid': STARRED_TARGET_LINE_ID,
            'name': STARRED_TARGET_LINE_NAME,
            'azimuth': {
                'val': 324.9999999999999
            },
            'delta_tvd': {
                'val': 19.46959181839702
            },
            'delta_vs': {
                'val': 3377.727551431245
            },
            'inclination': {
                'val': 89.66974450459126
            },
            'length': {
                'val': 3377.783663395759
            },
            'origin_base_corridor_tvd': {
                'undefined': True
            },
            'origin_md': {
                'undefined': True
            },
            'origin_top_corridor_tvd': {
                'undefined': True
            },
            'origin_tvd': {
                'val': 11488.203352355784
            },
            'origin_vs': {
                'val': 6044.52554257121
            },
            'origin_x': {
                'val': 496536.37744074466
            },
            'origin_y': {
                'val': 604953.7485579867
            },
            'origin_z': {
                'val': -11094.203352355784
            },
            'target_base_corridor_tvd': {
                'undefined': True
            },
            'target_md': {
                'undefined': True
            },
            'target_top_corridor_tvd': {
                'undefined': True
            },
            'target_tvd': {
                'val': 11507.67294417418
            },
            'target_vs': {
                'val': 9422.253094002455
            },
            'target_x': {
                'val': 494598.99250883
            },
            'target_y': {
                'val': 607720.6209867928
            },
            'target_z': {
                'val': -11113.67294417418
            },
            'tvd_vs': {
                'val': 11453.362044625126
            }
        },
        {
            'uuid': 'ace335a9-bb9e-4f7a-b33d-a625b71e764e',
            'name': TARGET_LINE_NAME,
            'azimuth': {
                'val': 324.9999999999999
            },
            'delta_tvd': {
                'val': 19.46959181839702
            },
            'delta_vs': {
                'val': 3377.727551431245
            },
            'inclination': {
                'val': 89.66974450459126
            },
            'length': {
                'val': 3377.783663395759
            },
            'origin_base_corridor_tvd': {
                'undefined': True
            },
            'origin_md': {
                'undefined': True
            },
            'origin_top_corridor_tvd': {
                'undefined': True
            },
            'origin_tvd': {
                'val': 11488.203352355784
            },
            'origin_vs': {
                'val': 6044.52554257121
            },
            'origin_x': {
                'val': 496536.37744074466
            },
            'origin_y': {
                'val': 604953.7485579867
            },
            'origin_z': {
                'val': -11094.203352355784
            },
            'target_base_corridor_tvd': {
                'undefined': True
            },
            'target_md': {
                'undefined': True
            },
            'target_top_corridor_tvd': {
                'undefined': True
            },
            'target_tvd': {
                'val': 11507.67294417418
            },
            'target_vs': {
                'val': 9422.253094002455
            },
            'target_x': {
                'val': 494598.99250883
            },
            'target_y': {
                'val': 607720.6209867928
            },
            'target_z': {
                'val': -11113.67294417418
            },
            'tvd_vs': {
                'val': 11453.362044625126
            }
        },
        {
            'uuid': 'b8a72c7a-94c7-4f25-9f72-12f8013d06a5',
            'name': 'Target Line 2',
            'azimuth': {
                'val': 324.9999999999999
            },
            'delta_tvd': {
                'val': 19.46959181839702
            },
            'delta_vs': {
                'val': 3377.727551431245
            },
            'inclination': {
                'val': 89.66974450459126
            },
            'length': {
                'val': 3377.783663395759
            },
            'origin_base_corridor_tvd': {
                'undefined': True
            },
            'origin_md': {
                'undefined': True
            },
            'origin_top_corridor_tvd': {
                'undefined': True
            },
            'origin_tvd': {
                'val': 11488.203352355784
            },
            'origin_vs': {
                'val': 6044.52554257121
            },
            'origin_x': {
                'val': 496536.37744074466
            },
            'origin_y': {
                'val': 604953.7485579867
            },
            'origin_z': {
                'val': -11094.203352355784
            },
            'target_base_corridor_tvd': {
                'undefined': True
            },
            'target_md': {
                'undefined': True
            },
            'target_top_corridor_tvd': {
                'undefined': True
            },
            'target_tvd': {
                'val': 11507.67294417418
            },
            'target_vs': {
                'val': 9422.253094002455
            },
            'target_x': {
                'val': 494598.99250883
            },
            'target_y': {
                'val': 607720.6209867928
            },
            'target_z': {
                'val': -11113.67294417418
            },
            'tvd_vs': {
                'val': 11453.362044625126
            }
        }
    ],
    'offset': 0,
    'limit': 100,
    'total': 3,
    'first': True,
    'last': True
}

NESTED_WELLS_DATA_RESPONSE = {
    'content': [
        {
            'uuid': STARRED_NESTED_WELL_ID,
            'name': STARRED_NESTED_WELL_NAME,
            'api': 'Starred Nested Well API',
            'operator': 'Operator',
            'xsrf_real': {
                'val': 100000.0
            },
            'ysrf_real': {
                'val': 100000.0
            },
            'kb': {
                'undefined': True
            },
            'convergence': {
                'val': 0.017453292519944444
            },
            'tie_in_tvd': {
                'undefined': True
            },
            'tie_in_ns': {
                'undefined': True
            },
            'tie_in_ew': {
                'undefined': True
            },
            'azimuth': {
                'val': 5.672320068981945
            }
        },
        {
            'uuid': 'afbbe18b-511d-4ef2-b65c-b70eddc49731',
            'name': NESTED_WELL_NAME,
            'api': 'Nested Well API',
            'operator': 'Nested Well Operator',
            'xsrf_real': {
                'val': 100000.0
            },
            'ysrf_real': {
                'val': 100000.0
            },
            'kb': {
                'undefined': True
            },
            'convergence': {
                'val': 0.017453292519944444
            },
            'tie_in_tvd': {
                'undefined': True
            },
            'tie_in_ns': {
                'undefined': True
            },
            'tie_in_ew': {
                'undefined': True
            },
            'azimuth': {
                'val': 5.672320068981945
            }
        },
        {
            'uuid': 'bfbbe18b-511d-4ef2-b65c-b70eddc49731',
            'name': 'Nested Well 2',
            'api': 'Nested Well 2 API',
            'operator': 'Nested Well 2 Operator',
            'xsrf_real': {
                'val': 200000.0
            },
            'ysrf_real': {
                'val': 200000.0
            },
            'kb': {
                'undefined': True
            },
            'convergence': {
                'val': 0.027453292519944444
            },
            'tie_in_tvd': {
                'undefined': True
            },
            'tie_in_ns': {
                'undefined': True
            },
            'tie_in_ew': {
                'undefined': True
            },
            'azimuth': {
                'val': 4.672320068981945
            }
        }
    ],
    'offset': 0,
    'limit': 100,
    'total': 3,
    'first': True,
    'last': True
}
