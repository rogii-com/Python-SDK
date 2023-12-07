from uuid import uuid4

METER_PROJECT_NAME = 'Global project'
METER_PROJECT_ID = uuid4()

FOOT_PROJECT_NAME = 'Global project (ft)'
FOOT_PROJECT_ID = uuid4()

FOOT_METER_PROJECT_NAME = 'Global project (ft-m)'
FOOT_METER_PROJECT_ID = uuid4()

WELL_NAME = 'Well'
WELL_XSRF = 33.8328
WELL_YSRF = 67.6656
WELL_XSRF_REAL = 111.0
WELL_YSRF_REAL = 222.0
WELL_KB = 10.058399999999999
WELL_AZIMUTH = 5.672320068981945
WELL_CONVERGENCE = 0.17453292519944444
WELL_TIE_IN_TVD = 169.164
WELL_TIE_IN_NS = 304.79999999999995
WELL_TIE_IN_EW = -609.5999999999999

EI_LAST_SEGMENT_EXTENDED_NAME = 'EI Last Segment Extended'
EI_LAST_SEGMENT_EXTENDED_ID = uuid4()

EI_LAST_SEGMENT_OUT_NAME = 'EI Last Segment Out Of Trajectory'
EI_LAST_SEGMENT_OUT_ID = uuid4()

EI_ABSENT_HORIZONS_LAST_SEGMENT_OUT_NAME = 'EI Absent Horizons Last Segment Out Of Trajectory'
EI_ABSENT_HORIZONS_LAST_SEGMENT_OUT_ID = uuid4()

EI_ALL_SEGMENTS_OUT_NAME = 'EI All Segments Out Of Trajectory'
EI_ALL_SEGMENTS_OUT_ID = uuid4()

TIME_TRACE_NAME = 'Bit depth'
CALC_TRACE_NAME = 'Rig Activity'

INTERPRETATION_NAME = 'Interpretation'

STARRED_INTERPRETATION_NAME = 'Starred Interpretation'
STARRED_INTERPRETATION_ID = uuid4()

INTERPRETATION_LAST_SEGMENT_ONE_POINT_NAME = 'Interpretation with last segment of one point'
INTERPRETATION_LAST_SEGMENT_ONE_POINT_ID = uuid4()

INTERPRETATION_LAST_SEGMENT_ONE_POINT_ABSENT_HORIZONS_NAME = (
    'Interpretation with last segment of one point without horizons'
)
INTERPRETATION_LAST_SEGMENT_ONE_POINT_ABSENT_HORIZONS_ID = uuid4()

HORIZON_NAME = 'Horizon'
HORIZON_ID = uuid4()

HORIZON_2_NAME = 'Horizon 2'
HORIZON_2_ID = '586a5e44-2a1c-402d-88bf-e82304e8fa2e'

HORIZON_3_NAME = 'Horizon 3'
HORIZON_3_ID = '86831e2a-3a0b-4085-9e63-90500a8b47ac'

STARRED_HORIZON_TOP_NAME = HORIZON_2_NAME
STARRED_HORIZON_CENTER_NAME = HORIZON_NAME
STARRED_HORIZON_BOTTOM_NAME = HORIZON_3_NAME

TARGET_LINE_NAME = 'Target Line'
STARRED_TARGET_LINE_ID = uuid4()
STARRED_TARGET_LINE_NAME = 'Starred Target Line'

NESTED_WELL_NAME = 'Nested Well'
STARRED_NESTED_WELL_NAME = 'Starred Nested Well'
STARRED_NESTED_WELL_ID = uuid4()

LOG_NAME = 'GR'

TYPEWELL_ID = uuid4()
TYPEWELL_NAME = 'Typewell'
TYPEWELL_XSRF = 33.8328
TYPEWELL_YSRF = 67.6656
TYPEWELL_XSRF_REAL = 111.0
TYPEWELL_YSRF_REAL = 222.0
TYPEWELL_KB = 10.058399999999999
TYPEWELL_CONVERGENCE = 0.6108652381980555
TYPEWELL_TIE_IN_TVD = 169.164
TYPEWELL_TIE_IN_NS = 304.79999999999995
TYPEWELL_TIE_IN_EW = -609.5999999999999


STARRED_TOPSET_NAME = 'Starred Topset'
STARRED_TOPSET_ID = uuid4()

STARRED_TOP_TOP_NAME = 'Top'
STARRED_TOP_CENTER_NAME = 'Top 2'
STARRED_TOP_BOTTOM_NAME = 'Top 3'

MUDLOG_NAME = 'Mudlog'

EARTH_MODEL_NAME = 'EarthModel1'

PROJECTS_DATA_RESPONSE = {
    'content': [
        {
            'uuid': METER_PROJECT_ID,
            'name': METER_PROJECT_NAME,
            'measure_unit': 'METER',
            'role': 'MANAGER',
            'accessed_on': '2022-06-30T08:26:30Z',
            'modified_on': '2022-06-24T13:30:32Z',
        },
        {
            'uuid': FOOT_PROJECT_ID,
            'name': FOOT_PROJECT_NAME,
            'measure_unit': 'FOOT',
            'role': 'MANAGER',
            'accessed_on': '2022-05-20T19:56:52Z',
            'modified_on': '2022-05-20T18:17:35Z',
        },
        {
            'uuid': FOOT_METER_PROJECT_ID,
            'name': FOOT_METER_PROJECT_NAME,
            'measure_unit': 'METER_FOOT',
            'role': 'MANAGER',
            'accessed_on': '2022-05-20T19:56:52Z',
            'modified_on': '2022-05-20T18:17:35Z',
        },
    ],
    'offset': 0,
    'limit': 100,
    'total': 3,
    'first': True,
    'last': True,
}

VIRTUAL_PROJECTS_DATA_RESPONSE = {
    'content': [
        {
            'uuid': '4e684dbc-37ed-4827-b677-dc0e3febc432',
            'name': 'Virtual project',
            'measure_unit': 'FOOT',
            'role': 'MANAGER',
            'geo_crs': {
                'code': 2194,
                'authority': 'EPSG',
                'name': 'American Samoa 1962 / American Samoa Lambert',
                'measure_unit': 'FOOT_US',
            },
            'parent_uuid': METER_PROJECT_ID,
            'parent_name': METER_PROJECT_NAME,
            'virtual': True,
            'modified_on': '2022-06-24T13:30:32Z',
        },
        {
            'uuid': 'b721009f-f71a-4c35-b6ad-084ca1cd624f',
            'name': 'Virtual project 2',
            'measure_unit': 'METER',
            'role': 'MANAGER',
            'geo_crs': {
                'code': 2194,
                'authority': 'EPSG',
                'name': 'American Samoa 1962 / American Samoa Lambert',
                'measure_unit': 'FOOT_US',
            },
            'parent_uuid': METER_PROJECT_ID,
            'parent_name': METER_PROJECT_NAME,
            'virtual': True,
            'modified_on': '2022-05-20T18:17:35Z',
        },
    ],
    'offset': 0,
    'limit': 100,
    'total': 2,
    'first': True,
    'last': True,
}

WELLS_DATA_RESPONSE = {
    'content': [
        {
            'uuid': '85fa6e44-3507-40b6-a7e2-ee07be241ac7',
            'name': WELL_NAME,
            'api': 'Lateral API',
            'operator': 'Lateral Operator',
            'xsrf': {'val': WELL_XSRF},
            'ysrf': {'val': WELL_YSRF},
            'xsrf_real': {'val': WELL_XSRF_REAL},
            'ysrf_real': {'val': WELL_YSRF_REAL},
            'kb': {'val': WELL_KB},
            'convergence': {'val': WELL_CONVERGENCE},
            'tie_in_tvd': {'val': WELL_TIE_IN_TVD},
            'tie_in_ns': {'val': WELL_TIE_IN_NS},
            'tie_in_ew': {'val': WELL_TIE_IN_EW},
            'azimuth': {'val': WELL_AZIMUTH},
            'starred': {
                'target_line': STARRED_TARGET_LINE_ID,
                'nested_well': STARRED_NESTED_WELL_ID,
                'interpretation': STARRED_INTERPRETATION_ID,
                'topset': STARRED_TOPSET_ID,
            },
        },
        {
            'uuid': '95fa6e44-3507-40b6-a7e2-ee07be241ac7',
            'name': 'Lateral 2',
            'api': 'Lateral 2 API',
            'operator': 'Lateral 2 Operator',
            'xsrf': {'val': WELL_XSRF},
            'ysrf': {'val': WELL_YSRF},
            'xsrf_real': {'val': WELL_XSRF_REAL},
            'ysrf_real': {'val': WELL_YSRF_REAL},
            'kb': {'val': WELL_KB},
            'convergence': {'val': WELL_CONVERGENCE},
            'tie_in_tvd': {'val': WELL_TIE_IN_TVD},
            'tie_in_ns': {'val': WELL_TIE_IN_NS},
            'tie_in_ew': {'val': WELL_TIE_IN_EW},
            'azimuth': {'val': WELL_AZIMUTH},
            'starred': {
                'target_line': STARRED_TARGET_LINE_ID,
                'nested_well': STARRED_NESTED_WELL_ID,
                'interpretation': STARRED_INTERPRETATION_ID,
            },
        },
    ],
    'offset': 0,
    'limit': 100,
    'total': 3,
    'first': True,
    'last': True,
}


INTERPRETATIONS_DATA_RESPONSE = {
    'content': [
        {
            'uuid': STARRED_INTERPRETATION_ID,
            'name': STARRED_INTERPRETATION_NAME,
            'properties': {
                'cutoff': {'val': 0},
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
                'interpretationExtend': {'val': 0},
                'boundaryPointsVisible': True,
                'display_hidden_segment': True,
            },
            'owner': 3,
            'mode': 'PUBLIC',
            'format': None,
        },
        {
            'uuid': 'a4811211-cf40-4b2a-9536-aa7f41b56b08',
            'name': INTERPRETATION_NAME,
            'properties': {
                'cutoff': {'val': 0},
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
                'interpretationExtend': {'val': 0},
                'boundaryPointsVisible': True,
                'display_hidden_segment': True,
            },
            'owner': 1,
            'mode': 'PUBLIC',
            'format': None,
        },
        {
            'uuid': '1e78d781-4804-42b6-974f-6f53830d9fb7',
            'name': 'Interpretation 2',
            'properties': {
                'cutoff': {'val': 0},
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
                'interpretationExtend': {'val': 0},
                'boundaryPointsVisible': True,
                'display_hidden_segment': True,
            },
            'owner': 2,
            'mode': 'PUBLIC',
            'format': None,
        },
        {
            'uuid': EI_LAST_SEGMENT_EXTENDED_ID,
            'name': EI_LAST_SEGMENT_EXTENDED_NAME,
            'properties': {
                'cutoff': {'val': 0},
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
                'interpretationExtend': {'val': 0},
                'boundaryPointsVisible': True,
                'display_hidden_segment': True,
            },
            'owner': 4,
            'mode': 'PUBLIC',
            'format': 'v2',
        },
        {
            'uuid': EI_ABSENT_HORIZONS_LAST_SEGMENT_OUT_ID,
            'name': EI_ABSENT_HORIZONS_LAST_SEGMENT_OUT_NAME,
            'properties': {
                'cutoff': {'val': 0},
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
                'interpretationExtend': {'val': 0},
                'boundaryPointsVisible': True,
                'display_hidden_segment': True,
            },
            'owner': 4,
            'mode': 'PUBLIC',
            'format': 'v2',
        },
        {
            'uuid': EI_LAST_SEGMENT_OUT_ID,
            'name': EI_LAST_SEGMENT_OUT_NAME,
            'properties': {
                'cutoff': {'val': 0},
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
                'interpretationExtend': {'val': 0},
                'boundaryPointsVisible': True,
                'display_hidden_segment': True,
            },
            'owner': 4,
            'mode': 'PUBLIC',
            'format': 'v2',
        },
        {
            'uuid': EI_ALL_SEGMENTS_OUT_ID,
            'name': EI_ALL_SEGMENTS_OUT_NAME,
            'properties': {
                'cutoff': {'val': 0},
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
                'interpretationExtend': {'val': 0},
                'boundaryPointsVisible': True,
                'display_hidden_segment': True,
            },
            'owner': 4,
            'mode': 'PUBLIC',
            'format': 'v2',
        },
        {
            'uuid': INTERPRETATION_LAST_SEGMENT_ONE_POINT_ID,
            'name': INTERPRETATION_LAST_SEGMENT_ONE_POINT_NAME,
            'properties': {
                'cutoff': {'val': 0},
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
                'interpretationExtend': {'val': 0},
                'boundaryPointsVisible': True,
                'display_hidden_segment': True,
            },
            'owner': 4,
            'mode': 'PUBLIC',
            'format': 'v2',
        },
        {
            'uuid': INTERPRETATION_LAST_SEGMENT_ONE_POINT_ABSENT_HORIZONS_ID,
            'name': INTERPRETATION_LAST_SEGMENT_ONE_POINT_ABSENT_HORIZONS_NAME,
            'properties': {
                'cutoff': {'val': 0},
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
                'interpretationExtend': {'val': 0},
                'boundaryPointsVisible': True,
                'display_hidden_segment': True,
            },
            'owner': 4,
            'mode': 'PUBLIC',
            'format': 'v2',
        },
    ],
    'offset': 0,
    'limit': 100,
    'total': 8,
    'first': True,
    'last': True,
}

HORIZONS_DATA_RESPONSE = {
    'content': [
        {'uuid': HORIZON_ID, 'name': HORIZON_NAME},
        {'uuid': '586a5e44-2a1c-402d-88bf-e82304e8fa2e', 'name': 'Horizon 2'},
        {'uuid': '86831e2a-3a0b-4085-9e63-90500a8b47ac', 'name': 'Horizon 3'},
    ],
    'offset': 0,
    'limit': 100,
    'total': 3,
    'first': True,
    'last': True,
}

ABSENT_HORIZONS_DATA_RESPONSE = {'content': [], 'offset': 0, 'limit': 100, 'total': 0, 'first': True, 'last': True}

TARGET_LINES_DATA_RESPONSE = {
    'content': [
        {
            'uuid': STARRED_TARGET_LINE_ID,
            'name': STARRED_TARGET_LINE_NAME,
            'azimuth': {'val': 324.9999999999999},
            'delta_tvd': {'val': 19.46959181839702},
            'delta_vs': {'val': 3377.727551431245},
            'inclination': {'val': 89.66974450459126},
            'length': {'val': 3377.783663395759},
            'origin_base_corridor_tvd': {'undefined': True},
            'origin_md': {'undefined': True},
            'origin_top_corridor_tvd': {'undefined': True},
            'origin_tvd': {'val': 11488.203352355784},
            'origin_vs': {'val': 6044.52554257121},
            'origin_x': {'val': 496536.37744074466},
            'origin_y': {'val': 604953.7485579867},
            'origin_z': {'val': -11094.203352355784},
            'target_base_corridor_tvd': {'undefined': True},
            'target_md': {'undefined': True},
            'target_top_corridor_tvd': {'undefined': True},
            'target_tvd': {'val': 11507.67294417418},
            'target_vs': {'val': 9422.253094002455},
            'target_x': {'val': 494598.99250883},
            'target_y': {'val': 607720.6209867928},
            'target_z': {'val': -11113.67294417418},
            'tvd_vs': {'val': 11453.362044625126},
        },
        {
            'uuid': 'ace335a9-bb9e-4f7a-b33d-a625b71e764e',
            'name': TARGET_LINE_NAME,
            'azimuth': {'val': 324.9999999999999},
            'delta_tvd': {'val': 19.46959181839702},
            'delta_vs': {'val': 3377.727551431245},
            'inclination': {'val': 89.66974450459126},
            'length': {'val': 3377.783663395759},
            'origin_base_corridor_tvd': {'undefined': True},
            'origin_md': {'undefined': True},
            'origin_top_corridor_tvd': {'undefined': True},
            'origin_tvd': {'val': 11488.203352355784},
            'origin_vs': {'val': 6044.52554257121},
            'origin_x': {'val': 496536.37744074466},
            'origin_y': {'val': 604953.7485579867},
            'origin_z': {'val': -11094.203352355784},
            'target_base_corridor_tvd': {'undefined': True},
            'target_md': {'undefined': True},
            'target_top_corridor_tvd': {'undefined': True},
            'target_tvd': {'val': 11507.67294417418},
            'target_vs': {'val': 9422.253094002455},
            'target_x': {'val': 494598.99250883},
            'target_y': {'val': 607720.6209867928},
            'target_z': {'val': -11113.67294417418},
            'tvd_vs': {'val': 11453.362044625126},
        },
        {
            'uuid': 'b8a72c7a-94c7-4f25-9f72-12f8013d06a5',
            'name': 'Target Line 2',
            'azimuth': {'val': 324.9999999999999},
            'delta_tvd': {'val': 19.46959181839702},
            'delta_vs': {'val': 3377.727551431245},
            'inclination': {'val': 89.66974450459126},
            'length': {'val': 3377.783663395759},
            'origin_base_corridor_tvd': {'undefined': True},
            'origin_md': {'undefined': True},
            'origin_top_corridor_tvd': {'undefined': True},
            'origin_tvd': {'val': 11488.203352355784},
            'origin_vs': {'val': 6044.52554257121},
            'origin_x': {'val': 496536.37744074466},
            'origin_y': {'val': 604953.7485579867},
            'origin_z': {'val': -11094.203352355784},
            'target_base_corridor_tvd': {'undefined': True},
            'target_md': {'undefined': True},
            'target_top_corridor_tvd': {'undefined': True},
            'target_tvd': {'val': 11507.67294417418},
            'target_vs': {'val': 9422.253094002455},
            'target_x': {'val': 494598.99250883},
            'target_y': {'val': 607720.6209867928},
            'target_z': {'val': -11113.67294417418},
            'tvd_vs': {'val': 11453.362044625126},
        },
    ],
    'offset': 0,
    'limit': 100,
    'total': 3,
    'first': True,
    'last': True,
}

NESTED_WELLS_DATA_RESPONSE = {
    'content': [
        {
            'uuid': STARRED_NESTED_WELL_ID,
            'name': STARRED_NESTED_WELL_NAME,
            'api': 'Starred Nested Well API',
            'operator': 'Operator',
            'xsrf': {'val': WELL_XSRF},
            'ysrf': {'val': WELL_YSRF},
            'xsrf_real': {'val': WELL_XSRF_REAL},
            'ysrf_real': {'val': WELL_YSRF_REAL},
            'kb': {'val': WELL_KB},
            'convergence': {'val': WELL_CONVERGENCE},
            'tie_in_tvd': {'val': WELL_TIE_IN_TVD},
            'tie_in_ns': {'val': WELL_TIE_IN_NS},
            'tie_in_ew': {'val': WELL_TIE_IN_EW},
            'azimuth': {'val': WELL_AZIMUTH},
        },
        {
            'uuid': 'afbbe18b-511d-4ef2-b65c-b70eddc49731',
            'name': NESTED_WELL_NAME,
            'api': 'Nested Well API',
            'operator': 'Nested Well Operator',
            'xsrf': {'val': WELL_XSRF},
            'ysrf': {'val': WELL_YSRF},
            'xsrf_real': {'val': WELL_XSRF_REAL},
            'ysrf_real': {'val': WELL_YSRF_REAL},
            'kb': {'undefined': True},
            'convergence': {'val': WELL_CONVERGENCE},
            'tie_in_tvd': {'val': WELL_TIE_IN_TVD},
            'tie_in_ns': {'val': WELL_TIE_IN_NS},
            'tie_in_ew': {'val': WELL_TIE_IN_EW},
            'azimuth': {'val': WELL_AZIMUTH},
        },
        {
            'uuid': 'bfbbe18b-511d-4ef2-b65c-b70eddc49731',
            'name': 'Nested Well 2',
            'api': 'Nested Well 2 API',
            'operator': 'Nested Well 2 Operator',
            'xsrf': {'val': WELL_XSRF},
            'ysrf': {'val': WELL_YSRF},
            'xsrf_real': {'val': WELL_XSRF_REAL},
            'ysrf_real': {'val': WELL_YSRF_REAL},
            'kb': {'undefined': True},
            'convergence': {'val': WELL_CONVERGENCE},
            'tie_in_tvd': {'undefined': True},
            'tie_in_ns': {'undefined': True},
            'tie_in_ew': {'undefined': True},
            'azimuth': {'val': WELL_AZIMUTH},
        },
    ],
    'offset': 0,
    'limit': 100,
    'total': 3,
    'first': True,
    'last': True,
}

TRAJECTORY_DATA_RESPONSE = {
    'content': [
        {'azim': {'val': 0}, 'incl': {'val': 0}, 'md': {'val': 0}},
        {'azim': {'val': 5.585053606382222}, 'incl': {'val': 0}, 'md': {'val': 19.4}},
        {'azim': {'val': 5.7288687367465645}, 'incl': {'val': 0.008203047484373888}, 'md': {'val': 107.39999999999999}},
        {'azim': {'val': 5.984210406313352}, 'incl': {'val': 0.010122909661567777}, 'md': {'val': 207.4}},
        {'azim': {'val': 5.647536393603623}, 'incl': {'val': 0.007853981633975}, 'md': {'val': 307.40000000000003}},
        {'azim': {'val': 6.123836746472907}, 'incl': {'val': 0.006457718232379445}, 'md': {'val': 407.4}},
        {'azim': {'val': 0.2675589743307483}, 'incl': {'val': 0.008203047484373888}, 'md': {'val': 507.4}},
        {'azim': {'val': 6.165026516819976}, 'incl': {'val': 0.008552113334772776}, 'md': {'val': 607.4}},
        {'azim': {'val': 5.834286623567027}, 'incl': {'val': 0.004712388980385}, 'md': {'val': 707.4000000000001}},
        {'azim': {'val': 1.4156365562926936}, 'incl': {'val': 0.007853981633975}, 'md': {'val': 807.4}},
        {'azim': {'val': 0.4326671215694228}, 'incl': {'val': 0.0017453292519944445}, 'md': {'val': 907.4000000000001}},
        {'azim': {'val': 6.209532412745832}, 'incl': {'val': 0.0036651914291883332}, 'md': {'val': 1007.4}},
        {'azim': {'val': 1.1470303844107488}, 'incl': {'val': 0.00279252680319111}, 'md': {'val': 1107.4}},
        {'azim': {'val': 0.85765479443007}, 'incl': {'val': 0.0040142572795872225}, 'md': {'val': 1207.4}},
        {'azim': {'val': 4.805589562441503}, 'incl': {'val': 0.001396263401595555}, 'md': {'val': 1307.4000000000003}},
        {'azim': {'val': 1.8671532337836567}, 'incl': {'val': 0.0010471975511966666}, 'md': {'val': 1407.4}},
        {'azim': {'val': 1.6362461737447913}, 'incl': {'val': 0.0026179938779916667}, 'md': {'val': 1507.4}},
        {'azim': {'val': 0.5461135229490617}, 'incl': {'val': 0.003490658503988889}, 'md': {'val': 1607.4}},
        {'azim': {'val': 0.7534586380860017}, 'incl': {'val': 0.008901179185171667}, 'md': {'val': 1707.4000000000003}},
        {'azim': {'val': 0.7927285462558765}, 'incl': {'val': 0.010122909661567777}, 'md': {'val': 1807.4}},
        {'azim': {'val': 0.7326892199872675}, 'incl': {'val': 0.010646508437166111}, 'md': {'val': 1907.4}},
        {'azim': {'val': 0.33841934196172274}, 'incl': {'val': 0.00942477796077}, 'md': {'val': 2007.4}},
        {'azim': {'val': 0.5668829410477955}, 'incl': {'val': 0.008901179185171667}, 'md': {'val': 2107.4}},
        {
            'azim': {'val': 0.16528268016387387},
            'incl': {'val': 0.007504915783576111},
            'md': {'val': 2207.4000000000005},
        },
        {'azim': {'val': 5.988050130667739}, 'incl': {'val': 0.008377580409573333}, 'md': {'val': 2307.4}},
        {'azim': {'val': 5.642649471698037}, 'incl': {'val': 0.008203047484373888}, 'md': {'val': 2407.4}},
        {'azim': {'val': 4.872435672792892}, 'incl': {'val': 0.005235987755983333}, 'md': {'val': 2507.4}},
        {'azim': {'val': 4.465424891227786}, 'incl': {'val': 0.004363323129986111}, 'md': {'val': 2607.4}},
        {'azim': {'val': 4.2561599139136534}, 'incl': {'val': 0.005061454830783889}, 'md': {'val': 2707.4000000000005}},
        {'azim': {'val': 4.290891966028341}, 'incl': {'val': 0.006981317007977778}, 'md': {'val': 2807.4}},
        {'azim': {'val': 4.400498643053592}, 'incl': {'val': 0.011519173063163331}, 'md': {'val': 2907.4}},
        {'azim': {'val': 4.63978328350203}, 'incl': {'val': 0.010122909661567777}, 'md': {'val': 3007.4}},
        {'azim': {'val': 4.729667739979745}, 'incl': {'val': 0.01117010721276444}, 'md': {'val': 3047.4}},
        {'azim': {'val': 4.952371752534236}, 'incl': {'val': 0.0040142572795872225}, 'md': {'val': 3195.4000000000005}},
        {'azim': {'val': 0.7318165553612705}, 'incl': {'val': 0.003490658503988889}, 'md': {'val': 3225.4000000000005}},
        {'azim': {'val': 0.6764896180730466}, 'incl': {'val': 0.003490658503988889}, 'md': {'val': 3256.4}},
        {'azim': {'val': 0.17383479349864667}, 'incl': {'val': 0.02234021442552888}, 'md': {'val': 3286.4}},
        {'azim': {'val': 0.24905848425960714}, 'incl': {'val': 0.0314159265359}, 'md': {'val': 3316.4}},
        {'azim': {'val': 0.13997540600995442}, 'incl': {'val': 0.03822271061867833}, 'md': {'val': 3346.4}},
        {
            'azim': {'val': 0.17296212887264947},
            'incl': {'val': 0.036651914291883324},
            'md': {'val': 3376.4000000000005},
        },
        {'azim': {'val': 0.11815879036002383}, 'incl': {'val': 0.03595378259108554}, 'md': {'val': 3407.4}},
        {'azim': {'val': 5.9861302684905455}, 'incl': {'val': 0.04485496177625721}, 'md': {'val': 3437.4}},
        {'azim': {'val': 5.670923805580348}, 'incl': {'val': 0.061784655520603325}, 'md': {'val': 3467.4}},
        {'azim': {'val': 5.577897756449042}, 'incl': {'val': 0.06946410422937888}, 'md': {'val': 3497.4}},
        {'azim': {'val': 5.427101309076725}, 'incl': {'val': 0.08674286382412388}, 'md': {'val': 3527.4}},
        {'azim': {'val': 5.355542809744952}, 'incl': {'val': 0.10140362954087721}, 'md': {'val': 3558.4}},
        {'azim': {'val': 5.278573789731999}, 'incl': {'val': 0.10367255756847}, 'md': {'val': 3588.4}},
        {'azim': {'val': 5.155004478690791}, 'incl': {'val': 0.11362093430483833}, 'md': {'val': 3618.4}},
        {'azim': {'val': 5.02270852138961}, 'incl': {'val': 0.12199851471441167}, 'md': {'val': 3648.4}},
        {'azim': {'val': 4.952371752534236}, 'incl': {'val': 0.1218239817892122}, 'md': {'val': 3679.4000000000005}},
        {'azim': {'val': 4.7827257492403765}, 'incl': {'val': 0.12322024519080776}, 'md': {'val': 3709.4000000000005}},
        {'azim': {'val': 4.65584031262038}, 'incl': {'val': 0.12636183784439778}, 'md': {'val': 3739.4000000000005}},
        {'azim': {'val': 4.602782303359749}, 'incl': {'val': 0.12636183784439778}, 'md': {'val': 3770.4}},
        {'azim': {'val': 4.571017310973448}, 'incl': {'val': 0.14172073526194887}, 'md': {'val': 3800.4}},
        {'azim': {'val': 4.582361951111414}, 'incl': {'val': 0.15934856070709275}, 'md': {'val': 3831.4000000000005}},
        {'azim': {'val': 4.594230190024977}, 'incl': {'val': 0.16493361431347497}, 'md': {'val': 3861.4000000000005}},
        {'azim': {'val': 4.612730680096116}, 'incl': {'val': 0.180641577581425}, 'md': {'val': 3891.4000000000005}},
        {'azim': {'val': 4.623202655608083}, 'incl': {'val': 0.20420352248334994}, 'md': {'val': 3922.4}},
        {'azim': {'val': 4.633325565269652}, 'incl': {'val': 0.21083577364092881}, 'md': {'val': 3952.4}},
        {'azim': {'val': 4.6411795469036266}, 'incl': {'val': 0.22357667718048835}, 'md': {'val': 3982.4}},
        {'azim': {'val': 4.687779837931877}, 'incl': {'val': 0.24068090385003388}, 'md': {'val': 4013.4000000000005}},
        {'azim': {'val': 4.706803926778618}, 'incl': {'val': 0.24120450262563223}, 'md': {'val': 4043.4}},
        {'azim': {'val': 4.745201170322495}, 'incl': {'val': 0.25429447201559063}, 'md': {'val': 4073.4}},
        {'azim': {'val': 4.77190470787801}, 'incl': {'val': 0.27122416575993663}, 'md': {'val': 4104.4}},
        {'azim': {'val': 4.761956331141642}, 'incl': {'val': 0.29181905093347105}, 'md': {'val': 4134.4}},
        {'azim': {'val': 4.748342762976084}, 'incl': {'val': 0.31730085801259006}, 'md': {'val': 4164.4}},
        {'azim': {'val': 4.738743452090115}, 'incl': {'val': 0.3467969223712961}, 'md': {'val': 4194.4}},
        {'azim': {'val': 4.741885044743705}, 'incl': {'val': 0.36686820876923215}, 'md': {'val': 4225.4}},
        {'azim': {'val': 4.748866361751683}, 'incl': {'val': 0.382925237887581}, 'md': {'val': 4255.4}},
        {'azim': {'val': 4.773300971279607}, 'incl': {'val': 0.4075343803407028}, 'md': {'val': 4285.4}},
        {'azim': {'val': 4.77818789318519}, 'incl': {'val': 0.41137410469509056}, 'md': {'val': 4315.4}},
        {'azim': {'val': 4.780805887063181}, 'incl': {'val': 0.4223696789826556}, 'md': {'val': 4345.400000000001}},
        {'azim': {'val': 4.781154952913581}, 'incl': {'val': 0.43109632524262775}, 'md': {'val': 4376.4}},
        {'azim': {'val': 4.771555642027609}, 'incl': {'val': 0.4255112716362456}, 'md': {'val': 4406.4}},
        {'azim': {'val': 4.790579730874351}, 'incl': {'val': 0.43388885204581873}, 'md': {'val': 4436.4}},
        {'azim': {'val': 4.782900282165577}, 'incl': {'val': 0.44331363000658885}, 'md': {'val': 4466.4}},
        {'azim': {'val': 4.7685885822992224}, 'incl': {'val': 0.4471533543609767}, 'md': {'val': 4497.4}},
        {'azim': {'val': 4.763003528692838}, 'incl': {'val': 0.4577998627981428}, 'md': {'val': 4527.4}},
        {'azim': {'val': 4.754800481208464}, 'incl': {'val': 0.48101274184966886}, 'md': {'val': 4557.4}},
        {'azim': {'val': 4.752880619031271}, 'incl': {'val': 0.49026298688523945}, 'md': {'val': 4587.4}},
        {'azim': {'val': 4.7518334214800735}, 'incl': {'val': 0.5384340742402861}, 'md': {'val': 4679.4}},
        {'azim': {'val': 4.7434558410704994}, 'incl': {'val': 0.5499532473034494}, 'md': {'val': 4769.4}},
        {'azim': {'val': 4.732809332633334}, 'incl': {'val': 0.5520476424058426}, 'md': {'val': 4862.400000000001}},
        {'azim': {'val': 4.734554661885329}, 'incl': {'val': 0.5448917924726655}, 'md': {'val': 4952.4}},
        {'azim': {'val': 4.7397906496413125}, 'incl': {'val': 0.5150466622635607}, 'md': {'val': 5043.4}},
        {'azim': {'val': 4.745899302023293}, 'incl': {'val': 0.5037020221255967}, 'md': {'val': 5134.4}},
        {'azim': {'val': 4.746422900798891}, 'incl': {'val': 0.5030038904247989}, 'md': {'val': 5164.4}},
        {'azim': {'val': 4.739267050865712}, 'incl': {'val': 0.4782202150464776}, 'md': {'val': 5248}},
        {'azim': {'val': 4.733158398483733}, 'incl': {'val': 0.5106833391335744}, 'md': {'val': 5315}},
        {'azim': {'val': 4.711690848684202}, 'incl': {'val': 0.6037093882648784}, 'md': {'val': 5404}},
        {'azim': {'val': 4.728795075353748}, 'incl': {'val': 0.6183701539816316}, 'md': {'val': 5494}},
        {'azim': {'val': 4.717799501066183}, 'incl': {'val': 0.6173229564304347}, 'md': {'val': 5583}},
        {'azim': {'val': 4.705058597526623}, 'incl': {'val': 0.6173229564304347}, 'md': {'val': 5673}},
        {'azim': {'val': 4.704534998751025}, 'incl': {'val': 0.6187192198320306}, 'md': {'val': 5763}},
        {'azim': {'val': 4.7027896694990305}, 'incl': {'val': 0.6169738905800362}, 'md': {'val': 5852}},
        {'azim': {'val': 4.701218873172236}, 'incl': {'val': 0.6162757588792382}, 'md': {'val': 5942}},
        {'azim': {'val': 4.698775412219444}, 'incl': {'val': 0.6169738905800362}, 'md': {'val': 6031.000000000001}},
        {'azim': {'val': 4.693364891538261}, 'incl': {'val': 0.6171484235052357}, 'md': {'val': 6121.000000000001}},
        {'azim': {'val': 4.688827035483073}, 'incl': {'val': 0.6178465552060333}, 'md': {'val': 6210}},
        {'azim': {'val': 4.697204615892648}, 'incl': {'val': 0.6174974893556343}, 'md': {'val': 6300}},
        {'azim': {'val': 4.530351139401979}, 'incl': {'val': 0.6195918844580276}, 'md': {'val': 6390}},
        {'azim': {'val': 4.3060763305206935}, 'incl': {'val': 0.6468190207891411}, 'md': {'val': 6479}},
        {'azim': {'val': 4.151091092943586}, 'incl': {'val': 0.6927211801165948}, 'md': {'val': 6569}},
        {'azim': {'val': 3.982317754275722}, 'incl': {'val': 0.7752752537359322}, 'md': {'val': 6659}},
        {'azim': {'val': 3.8437386116673644}, 'incl': {'val': 0.8496262798708956}, 'md': {'val': 6748.000000000001}},
        {'azim': {'val': 3.7121407860669837}, 'incl': {'val': 0.9663888068293238}, 'md': {'val': 6838}},
        {'azim': {'val': 3.59659998958495}, 'incl': {'val': 1.0794861423585638}, 'md': {'val': 6927}},
        {'azim': {'val': 1.9224798994731556}, 'incl': {'val': 1.4779243883463222}, 'md': {'val': 8405.913767207876}},
        {'azim': {'val': 2.548180707911912}, 'incl': {'val': 1.5518093964885145}, 'md': {'val': 8980.891243929258}},
        {'azim': {'val': 2.548180707946217}, 'incl': {'val': 1.470621959565225}, 'md': {'val': 9553.16627586735}},
    ]
}

LOGS_DATA_RESPONSE = {
    'content': [
        {'name': LOG_NAME, 'uuid': '1b6424cf-1af1-4bdc-a371-561063689b94'},
        {'name': 'Gamma Ray', 'uuid': '1070fbaf-25e2-4ede-807a-98a1c2e0f763'},
    ],
    'offset': 0,
    'limit': 10,
    'total': 2,
    'first': True,
    'last': True,
}

LOG_POINTS_DATA_RESPONSE = {
    'log_points': [
        {'data': {'val': -3688.6927}, 'md': {'val': 744.6263999999999}},
        {'data': {'val': 16.581}, 'md': {'val': 744.7787999999999}},
        {'data': {'val': -11.85}, 'md': {'val': 744.9311999999999}},
        {'data': {'val': 15.187}, 'md': {'val': 745.0835999999999}},
        {'data': {'val': -4.363}, 'md': {'val': 745.2359999999999}},
        {'data': {'val': -40.475}, 'md': {'val': 745.3883999999999}},
        {'data': {'val': 61.463}, 'md': {'val': 745.5407999999999}},
        {'data': {'val': 82.305}, 'md': {'val': 745.6931999999999}},
        {'data': {'val': 114.139}, 'md': {'val': 745.8455999999999}},
        {'data': {'val': 144.503}, 'md': {'val': 745.9979999999999}},
    ]
}


HORIZONS_TVT_DATA_RESPONSE = {
    'content': [
        {
            'azimuth': {'val': 71.543},
            'horizons': [
                {'name': HORIZON_NAME, 'tvdss': {'val': 22.965879265091868}, 'uuid': HORIZON_ID},
                {
                    'name': 'Horizon 2',
                    'tvdss': {'val': -3257.8740157480324},
                    'uuid': '586a5e44-2a1c-402d-88bf-e82304e8fa2e',
                },
            ],
            'inclination': {'val': 0},
            'kb': {'val': 22.965879265091868},
            'md': {'val': 0},
            'tvt': {'val': 0},
            'vs_azim': {'azimuth': {'val': 0}, 'vs': {'val': 3.280839895013124}},
            'well_name': WELL_NAME,
            'x': {'val': 19.68503937007874},
            'y': {'val': 36.08923884514436},
            'z': {'val': 22.965879265091868},
        },
        {
            'azimuth': {'val': 149.253},
            'horizons': [
                {'name': HORIZON_NAME, 'tvdss': {'val': 22.965879265091868}, 'uuid': HORIZON_ID},
                {
                    'name': 'Horizon 2',
                    'tvdss': {'val': -3257.8740157480324},
                    'uuid': '586a5e44-2a1c-402d-88bf-e82304e8fa2e',
                },
            ],
            'inclination': {'val': 1.33},
            'kb': {'val': 22.965879265091868},
            'md': {'val': 3280.839895013124},
            'tvt': {'val': 3280.0196063852154},
            'vs_azim': {'azimuth': {'val': 0}, 'vs': {'val': -60.07861128428071}},
            'well_name': WELL_NAME,
            'x': {'val': 53.715600823725445},
            'y': {'val': -27.270212334149477},
            'z': {'val': -3257.0537271201238},
        },
    ]
}


TYPEWELLS_DATA_RESPONSE = {
    'content': [
        {
            'uuid': TYPEWELL_ID,
            'name': TYPEWELL_NAME,
            'api': 'Typewell API',
            'xsrf': {'val': TYPEWELL_XSRF},
            'ysrf': {'val': TYPEWELL_YSRF},
            'xsrf_real': {'val': TYPEWELL_XSRF_REAL},
            'ysrf_real': {'val': TYPEWELL_YSRF_REAL},
            'kb': {'val': TYPEWELL_KB},
            'convergence': {'val': TYPEWELL_CONVERGENCE},
            'tie_in_tvd': {'val': TYPEWELL_TIE_IN_TVD},
            'tie_in_ns': {'val': TYPEWELL_TIE_IN_NS},
            'tie_in_ew': {'val': TYPEWELL_TIE_IN_EW},
        },
        {
            'name': 'Typewell 2',
            'uuid': '66a1dd35-6bc2-4d01-a550-c5054d956146',
            'api': 'Typewell 2 API',
            'xsrf': {'val': TYPEWELL_XSRF},
            'ysrf': {'val': TYPEWELL_YSRF},
            'xsrf_real': {'val': TYPEWELL_XSRF_REAL},
            'ysrf_real': {'val': TYPEWELL_YSRF_REAL},
            'kb': {'val': TYPEWELL_KB},
            'convergence': {'val': TYPEWELL_CONVERGENCE},
            'tie_in_tvd': {'val': TYPEWELL_TIE_IN_TVD},
            'tie_in_ns': {'val': TYPEWELL_TIE_IN_NS},
            'tie_in_ew': {'val': TYPEWELL_TIE_IN_EW},
        },
    ],
    'offset': 0,
    'limit': 100,
    'total': 2,
    'first': True,
    'last': True,
}

TOPSETS_DATA_RESPONSE = {
    'content': [
        {'name': STARRED_TOPSET_NAME, 'uuid': STARRED_TOPSET_ID},
        {'name': 'Topset 2', 'uuid': 'fb20162a-0c47-4eea-8bc5-a56b1bd856dc'},
        {'name': 'Topset 3', 'uuid': '7e86bd40-124d-466a-9592-24811963fa12'},
        {'name': 'Topset 4', 'uuid': '95c15955-af34-4b41-ba6a-c1abb979ea68'},
    ],
    'offset': 0,
    'limit': 10,
    'total': 4,
    'first': True,
    'last': True,
}

TOPS_DATA_RESPONSE = {
    'content': [
        {
            'md': {'val': 9.842519685039372},
            'name': STARRED_TOP_TOP_NAME,
            'topset_name': 'Topset',
            'uuid': 'c0332dab-9468-4b27-b1f6-3d4d7c875ecf',
        },
        {
            'md': {'val': 13.123359580052496},
            'name': STARRED_TOP_CENTER_NAME,
            'topset_name': 'Topset',
            'uuid': '3e5f09a8-0a0a-4722-ab1a-c52c769fc72b',
        },
        {
            'md': {'val': 15.443359580052496},
            'name': STARRED_TOP_BOTTOM_NAME,
            'topset_name': 'Topset',
            'uuid': '77b3db2b-83f0-4122-8068-647ce432d221',
        },
    ],
    'offset': 0,
    'limit': 20,
    'total': 3,
    'first': True,
    'last': True,
}

STARRED_HORIZONS_DATA_RESPONSE = {
    'top': '586a5e44-2a1c-402d-88bf-e82304e8fa2e',
    'center': HORIZON_ID,
    'bottom': '86831e2a-3a0b-4085-9e63-90500a8b47ac',
}

STARRED_TOPS_DATA_RESPONSE = {
    'top': 'c0332dab-9468-4b27-b1f6-3d4d7c875ecf',
    'center': '3e5f09a8-0a0a-4722-ab1a-c52c769fc72b',
    'bottom': '77b3db2b-83f0-4122-8068-647ce432d221',
}

MUDLOGS_DATA_RESPONSE = {
    'content': [{'name': MUDLOG_NAME, 'uuid': 'fc927f99-aae2-4ac5-b16e-676c4d70d8b7'}],
    'offset': 0,
    'limit': 10,
    'total': 1,
    'first': True,
    'last': True,
}

MUDLOG_DATA_RESPONSE = {
    'logs': [
        {
            'uuid': '0a157968-8265-44c7-99a4-a18d17baa71a',
            'name': 'GRMA',
            'log_points': [
                {'md': {'val': 9465.499999999998}, 'data': {'val': 16.917995}},
                {'md': {'val': 9465.999999999998}, 'data': {'val': 17.194681}},
                {'md': {'val': 9466.499999999998}, 'data': {'val': 18.103792}},
            ],
        },
        {
            'uuid': 'f2f36585-2036-4d90-a291-1da771c2b04d',
            'name': 'RHOB',
            'log_points': [
                {'md': {'val': 9465.499999999998}, 'data': {'val': 2.241943}},
                {'md': {'val': 9465.999999999998}, 'data': {'val': 2.269067}},
                {'md': {'val': 9466.499999999998}, 'data': {'val': 2.287254}},
            ],
        },
    ]
}


TRACES_DATA_RESPONSE = {
    'content': [
        {'uuid': '793b06f6-d494-45e0-9ed8-b5e8e916a2a8', 'name': 'Bit depth'},
        {'uuid': '11b379f9-184b-465a-beb8-7307c7b4b1d9', 'name': 'Hole Depth'},
        {'uuid': '491c2160-c65b-4ca0-afa9-7514fc6f7c56', 'name': 'Block position'},
        {'uuid': '8752123d-d270-4eb6-b132-ba0f3e0d83b8', 'name': 'Hookload'},
        {'uuid': 'c908bc68-0e9b-4368-a2be-97b48cbd5440', 'name': 'Surface RPM'},
        {'uuid': 'a07b5bc6-a36f-4b8c-a3bb-4ce426eac7c0', 'name': 'Surface Torque'},
        {'uuid': '2b2ad244-f208-4bb9-9b7c-6bbde9483635', 'name': 'Standpipe Pressure'},
        {'uuid': '77c1bd4d-0fc1-470f-a24c-e28a5dd4c5fc', 'name': 'Mud Weight IN'},
        {'uuid': '0a745541-0a23-45be-870d-9fdd8a1849c6', 'name': 'Downhole WOB'},
        {'uuid': '9f7ed05c-66cd-441c-855d-a4aec51b33e2', 'name': 'SPM1'},
        {'uuid': 'e0a2398e-21ad-4410-9cdd-e212c516061a', 'name': 'SPM2'},
        {'uuid': '98bce1cd-fda0-41dd-8d04-e6020dd6e3e1', 'name': 'SPM3'},
        {'uuid': '14b6654f-ba57-4bc5-8374-e219fc491e75', 'name': 'Surface Torque Max'},
        {'uuid': '24624b80-b34c-4062-98c8-d42dea5fa125', 'name': 'Block Velocity'},
        {'uuid': '6f83f7e7-40ac-448c-a2ce-e3c72d828735', 'name': 'Gas'},
        {'uuid': '66d264d4-d935-49c8-bf17-c15c88d1f082', 'name': 'Total Tank Volume'},
        {'uuid': 'b72b91cd-9482-47a7-8914-fe4c17b7aa02', 'name': 'Trip Tank Volume'},
        {'uuid': 'accde91d-d6a3-4bc1-9986-f117a59f17e9', 'name': 'Mud Weight Out'},
        {'uuid': '2c32a691-8787-49a6-83a1-c54d859a43ff', 'name': 'Survey MD'},
        {'uuid': '16968239-944d-480e-ba34-195d4ba12927', 'name': 'Inclination'},
        {'uuid': 'fa3a2cfb-c858-4c4f-8776-4130c475e594', 'name': 'Cont Inclination'},
        {'uuid': '01da81cf-b8c7-4a3b-b561-3fdaf2f61dd4', 'name': 'Azimuth'},
        {'uuid': 'ea9f7ad6-0880-4a5a-bddc-79e7c79d26bc', 'name': 'Cont Azimuth'},
        {'uuid': '4022fb41-6279-4a5a-bec0-e8e0563119cc', 'name': 'Gamma Ray'},
        {'uuid': '02f37da6-ced8-4b57-8a7d-0a583615a196', 'name': 'Resistivity'},
        {'uuid': '865ba522-5800-40df-9271-5b8d8efece5c', 'name': 'Density'},
        {'uuid': 'e58a09e4-9036-4bf4-b645-b1ef1984b867', 'name': 'Caliper'},
        {'uuid': '83a18db4-e419-4671-8191-2d67149ac67e', 'name': 'ECD'},
        {'uuid': '7572a7e5-8d99-444f-9be6-3de328354274', 'name': 'StickSlip'},
        {'uuid': '061a437d-74de-41d0-b21d-c5858293d3e5', 'name': 'Shock Levels'},
        {'uuid': '88d7ccaf-dafe-495f-934f-ad56e2e16c42', 'name': 'On bottom hours'},
        {'uuid': 'd30498b6-6e8a-41b0-a6a4-9be5be5319e5', 'name': 'Circulation hours'},
        {'uuid': '9fc059d1-85c6-429a-b03e-d92fb466b168', 'name': 'User Defined 1'},
        {'uuid': '9e26b22f-b4ef-4284-80a9-f2716aac718c', 'name': 'User Defined 2'},
        {'uuid': 'dbcf25d9-f808-4877-b3ca-90accf3d784b', 'name': 'User Defined 3'},
        {'uuid': '908905a3-0269-4711-8007-1b7755471528', 'name': 'User Defined 4'},
        {'uuid': '4be6e7f7-1eae-4f4e-ac6a-350327e59a39', 'name': 'User Defined 5'},
        {'uuid': '54cd355d-8acf-4442-b62f-a50c78c189f8', 'name': 'User Defined 6'},
        {'uuid': '6f304e26-802b-4118-a9ec-189b0d08d58f', 'name': 'User Defined 7'},
        {'uuid': 'aaddd315-5693-4aac-ba31-4b5fd592923c', 'name': 'User Defined 8'},
        {'uuid': '45369f92-7074-431f-8e9a-c47a0c64afff', 'name': 'User Defined 9'},
        {'uuid': '435990bc-ead8-4268-8821-a8aea9e93944', 'name': 'User Defined 10'},
        {'uuid': '074cb1e6-2bec-4b61-9e76-f48ebecf5ddd', 'name': 'Mud Flow In'},
        {'uuid': 'ff172791-85e2-43cc-95f9-1fbb719abc6c', 'name': 'SMP Total'},
        {'uuid': '227f118f-7845-49b2-9896-55dc5222519d', 'name': 'WOB'},
        {'uuid': '9cb51894-17ff-4928-b8b4-4919f492c5c9', 'name': 'In Slips'},
        {'uuid': '1b2beeff-a4a1-4e13-a25a-feabdc593da7', 'name': 'GTF'},
        {'uuid': '0abaf4b2-6a97-4b0b-8609-f7ac37136a3b', 'name': 'MTF'},
        {'uuid': '30146cef-6942-4247-bc75-521d76b85127', 'name': 'ROP'},
        {'uuid': '7e01b567-d5f6-4912-bfe0-2ba189db6b2f', 'name': 'Downhole TQ'},
        {'uuid': '9f0cb268-e4b7-425e-a191-596489da81d2', 'name': 'Temperature In'},
        {'uuid': '009f1d02-b17a-41cf-9166-d02c37bcd834', 'name': 'Temperature Out'},
        {'uuid': '36c53c74-8836-4a91-b95b-d5c3785c1f27', 'name': 'Bit Depth Vertical'},
        {'uuid': '81a04429-a30f-4f13-ba33-138ab0981183', 'name': 'Total RPM'},
        {'uuid': '7b021e39-f422-462c-87ac-d7e1105ac188', 'name': 'WOB Max'},
        {'uuid': 'a8bfeb47-37f3-4bf8-b256-2f773307ee5b', 'name': 'Mud Flow Out'},
        {'uuid': '82db3825-d6eb-4925-a73d-f5af1d1d6743', 'name': 'Pump Stroke Count'},
        {'uuid': 'fe637ea0-4ae2-48d3-8c1d-2a4a84f8e06f', 'name': 'Hole Depth Vertical'},
        {'uuid': '6eecd916-a7d2-47de-a72c-8afe5dd36373', 'name': 'Flow'},
        {'uuid': '8eb6a4af-9453-44e7-ade3-aace18e0024a', 'name': 'Casing Pressure'},
        {'uuid': 'c3b19920-8f01-47cb-acd9-0da8843e3ce7', 'name': 'KPI: Slip to slip'},
        {'uuid': 'a0448fd5-d2d5-435f-9f57-dc23bafec82d', 'name': 'Rig Activity'},
        {'uuid': '3fe5ea4a-e7d4-4679-aa10-0eba283a1e7d', 'name': 'KPI: Trip In: Connection'},
        {'uuid': 'c0e7707d-24df-44c8-bd71-24aee1a5abe6', 'name': 'KPI: Trip Out: Running'},
        {'uuid': 'a6f3ad7b-5363-427c-98ec-8bfee338cdd8', 'name': 'KPI: Trip In: Running'},
        {'uuid': '6455f4ed-2ee7-4b1a-8535-d8df017e4b83', 'name': 'KPI: Weight to Weight'},
        {'uuid': 'b35c6e45-45b1-46ea-8463-21237bf53353', 'name': 'KPI: Trip Out: Connection'},
    ]
}


MAPPED_TIME_TRACES_DATA_RESPONSE = {
    'content': [
        {
            'uuid': '793b06f6-d494-45e0-9ed8-b5e8e916a2a8',
            'name': 'Bit depth',
            'hash': 'bd9863171705c3a0bf3e334cdcfcb85d',
            'unit': '',
            'start_date_time_index': '2020-09-01T10:00:00Z',
            'last_date_time_index': '2020-09-13T10:53:19Z',
        },
        {
            'uuid': '11b379f9-184b-465a-beb8-7307c7b4b1d9',
            'name': 'Hole Depth',
            'hash': 'bdf8d4fbfc4a9238a0a77077fc8c7e89',
            'unit': 'm',
            'start_date_time_index': '2020-09-01T10:00:00Z',
            'last_date_time_index': '2020-09-13T10:53:19Z',
        },
        {
            'uuid': '491c2160-c65b-4ca0-afa9-7514fc6f7c56',
            'name': 'Block position',
            'hash': '1afd16706047b52fae650a4c90c5e212',
            'unit': 'm',
            'start_date_time_index': '2020-09-01T10:00:00Z',
            'last_date_time_index': '2020-09-13T10:53:19Z',
        },
        {
            'uuid': '8752123d-d270-4eb6-b132-ba0f3e0d83b8',
            'name': 'Hookload',
            'hash': '68e05d9c28dc1440d606cd2ea421e822',
            'unit': '',
            'start_date_time_index': '2020-09-01T10:00:00Z',
            'last_date_time_index': '2020-09-13T10:53:19Z',
        },
    ]
}

TIME_TRACE_DATA_RESPONSE = {
    'content': [
        {'index': '2020-09-01T10:00:00.000Z', 'value': '1.0'},
        {'index': '2020-09-03T11:00:00.000Z', 'value': '2.0'},
        {'index': '2020-09-05T12:00:00.000Z', 'value': '3.0'},
        {'index': '2020-09-08T13:00:00.000Z', 'value': '4.0'},
        {'index': '2020-09-13T10:53:19.000Z', 'value': '5.0'},
    ]
}

MAPPED_CALC_TRACES_DATA_RESPONSE = {
    'content': [
        {
            'uuid': 'e3c996b6-9cdb-4876-ac99-0aab694b801a',
            'name': 'Rig Activity',
            'hash': '2e4ae0788e59ca3508cb29088c36e95c',
            'start_date_time_index': '2020-09-01T10:00:00Z',
            'last_date_time_index': '2020-09-13T10:53:19Z',
        },
        {
            'uuid': 'fed6681e-1f21-466c-bf91-55fed528a07d',
            'name': 'KPI: Trip In: Running',
            'hash': '137b912122af693d25cca00e5569d055',
            'start_date_time_index': '2022-06-10T12:17:41Z',
            'last_date_time_index': '2022-06-21T23:21:31Z',
        },
        {
            'uuid': '5fe2a454-86ad-4fdc-abbf-686e4f67a4fa',
            'name': 'KPI: Trip Out: Connection',
            'hash': '13f2ddf5eca16303369a3eb3629223f3',
            'start_date_time_index': '2022-06-10T12:17:41Z',
            'last_date_time_index': '2022-06-21T23:21:33Z',
        },
    ]
}

CALC_TRACE_DATA_RESPONSE = {
    'content': [
        {'start': '2020-09-01T10:00:00Z', 'end': '2020-09-02T11:53:09Z', 'value': '54'},
        {'start': '2020-09-02T11:53:09Z', 'end': '2020-09-04T06:11:36Z', 'value': '98'},
        {'start': '2020-09-04T06:11:36Z', 'end': '2020-09-04T06:11:37Z', 'value': '22'},
        {'start': '2020-09-04T06:11:37Z', 'end': '2020-09-04T06:14:26Z', 'value': '21'},
        {'start': '2020-09-13T10:53:01Z', 'end': '2020-09-13T10:53:11Z', 'value': '32'},
        {'start': '2020-09-13T10:53:11Z', 'end': '2020-09-13T10:53:12Z', 'value': '51'},
        {'start': '2020-09-13T10:53:12Z', 'end': '2020-09-13T10:53:19Z', 'value': '31'},
    ]
}


ASSEMBLED_SEGMENTS_DATA_RESPONSE = {
    'assembled_segments': {
        'horizons': {
            HORIZON_ID: {'tvd': {'val': 4875.37313679709}, 'uuid': HORIZON_ID},
            HORIZON_2_ID: {'tvd': {'val': 4329.045990215498}, 'uuid': HORIZON_2_ID},
            HORIZON_3_ID: {'tvd': {'val': 4029.045990215498}, 'uuid': HORIZON_3_ID},
        },
        'interp_end_md': {'val': 9553.16627586735},
        'interp_end_x': {'val': 1506.8463116346054},
        'interp_end_y': {'val': -1064.5840083926553},
        'linked_to_trj_end': True,
        'segments': [
            {
                'boundary_type': 1,
                'end': {'val': 0},
                'horizon_shifts': {
                    HORIZON_ID: {
                        'end': {'val': 1685.1139500714344},
                        'start': {'val': 1632.956791751696},
                        'uuid': HORIZON_ID,
                    },
                    HORIZON_2_ID: {
                        'end': {'val': 1685.1139500714344},
                        'start': {'val': 1632.956791751696},
                        'uuid': HORIZON_2_ID,
                    },
                    HORIZON_3_ID: {
                        'end': {'val': 1685.1139500714344},
                        'start': {'val': 1632.956791751696},
                        'uuid': HORIZON_3_ID,
                    },
                },
                'md': {'val': 7627.5},
                'start': {'val': 0},
                'uuid': '651fe01d-30a4-4c85-b2af-a2dceb4f0385',
                'x': {'val': 0},
                'y': {'val': 0},
            },
            {
                'boundary_type': 1,
                'end': {'val': 0},
                'horizon_shifts': {
                    HORIZON_ID: {
                        'end': {'val': 1654.0526934167056},
                        'start': {'val': 1685.1139500714344},
                        'uuid': HORIZON_ID,
                    },
                    HORIZON_2_ID: {
                        'end': {'val': 1654.0526934167056},
                        'start': {'val': 1685.1139500714344},
                        'uuid': HORIZON_2_ID,
                    },
                    HORIZON_3_ID: {
                        'end': {'val': 1654.0526934167056},
                        'start': {'val': 1685.1139500714344},
                        'uuid': HORIZON_3_ID,
                    },
                },
                'md': {'val': 8756.1},
                'start': {'val': 0},
                'uuid': 'de40551b-d869-47ab-b414-d41fc49aeff9',
                'x': {'val': 936.0090093403047},
                'y': {'val': -512.7027100919538},
            },
        ],
    }
}

ASSEMBLED_SEGMENTS_LAST_SEGMENT_ONE_POINT_DATA_RESPONSE = {
    'assembled_segments': {
        'horizons': {
            HORIZON_ID: {'tvd': {'val': 4875.37313679709}, 'uuid': HORIZON_ID},
            HORIZON_2_ID: {'tvd': {'val': 4329.045990215498}, 'uuid': HORIZON_2_ID},
            HORIZON_3_ID: {'tvd': {'val': 4029.045990215498}, 'uuid': HORIZON_3_ID},
        },
        'interp_end_md': {'val': 10741.239115452869},
        'interp_end_x': {'val': 2328.0135891272166},
        'interp_end_y': {'val': -1914.927616987544},
        'linked_to_trj_end': False,
        'segments': [
            {
                'boundary_type': 1,
                'end': {'val': 0},
                'horizon_shifts': {
                    HORIZON_ID: {
                        'end': {'val': 1685.1139500714344},
                        'start': {'val': 1632.956791751696},
                        'uuid': HORIZON_ID,
                    },
                    HORIZON_2_ID: {
                        'end': {'val': 1685.1139500714344},
                        'start': {'val': 1632.956791751696},
                        'uuid': HORIZON_2_ID,
                    },
                    HORIZON_3_ID: {
                        'end': {'val': 1685.1139500714344},
                        'start': {'val': 1632.956791751696},
                        'uuid': HORIZON_3_ID,
                    },
                },
                'md': {'val': 7627.5},
                'start': {'val': 0},
                'uuid': 'a0cbc76d-b524-4061-ad69-2751353209d0',
                'x': {'val': 0},
                'y': {'val': 0},
            },
            {
                'boundary_type': 1,
                'end': {'val': 0},
                'horizon_shifts': {
                    HORIZON_ID: {
                        'end': {'val': 1654.0526934167056},
                        'start': {'val': 1685.1139500714344},
                        'uuid': HORIZON_ID,
                    },
                    HORIZON_2_ID: {
                        'end': {'val': 1654.0526934167056},
                        'start': {'val': 1685.1139500714344},
                        'uuid': HORIZON_2_ID,
                    },
                    HORIZON_3_ID: {
                        'end': {'val': 1654.0526934167056},
                        'start': {'val': 1685.1139500714344},
                        'uuid': HORIZON_3_ID,
                    },
                },
                'md': {'val': 8756.1},
                'start': {'val': 0},
                'uuid': '5841ccb7-5f38-4209-87d1-3830b98ab86f',
                'x': {'val': 936.0090093403047},
                'y': {'val': -512.7027100919538},
            },
            {
                'boundary_type': 1,
                'end': {'val': 0},
                'horizon_shifts': {
                    HORIZON_ID: {
                        'end': {'val': 1607.4987997150938},
                        'start': {'val': 1654.0526934167056},
                        'uuid': HORIZON_ID,
                    },
                    HORIZON_2_ID: {
                        'end': {'val': 1607.4987997150938},
                        'start': {'val': 1654.0526934167056},
                        'uuid': HORIZON_2_ID,
                    },
                    HORIZON_3_ID: {
                        'end': {'val': 1607.4987997150938},
                        'start': {'val': 1654.0526934167056},
                        'uuid': HORIZON_3_ID,
                    },
                },
                'md': {'val': 9553.16627586735},
                'start': {'val': 0},
                'uuid': '84848ad6-c533-4399-a180-2c96928e1fc3',
                'x': {'val': 1506.8463116346054},
                'y': {'val': -1064.5840083926553},
            },
        ],
    }
}

ASSEMBLED_SEGMENTS_LAST_SEGMENT_ONE_POINT_ABSENT_HORIZONS_DATA_RESPONSE = {
    'assembled_segments': {
        'horizons': {},
        'interp_end_md': {'val': 10741.239115452869},
        'interp_end_x': {'val': 2328.0135891272166},
        'interp_end_y': {'val': -1914.927616987544},
        'linked_to_trj_end': False,
        'segments': [
            {
                'boundary_type': 1,
                'end': {'val': 0},
                'horizon_shifts': {},
                'md': {'val': 7627.5},
                'start': {'val': 0},
                'uuid': '975a8cee-ac1c-4ce1-9aa6-b7c51131a49a',
                'x': {'val': 0},
                'y': {'val': 0},
            },
            {
                'boundary_type': 1,
                'end': {'val': 0},
                'horizon_shifts': {},
                'md': {'val': 8756.1},
                'start': {'val': 0},
                'uuid': 'b7089fc1-6973-46a5-b1f5-559b219eadd7',
                'x': {'val': 936.0090093403047},
                'y': {'val': -512.7027100919538},
            },
            {
                'boundary_type': 1,
                'end': {'val': 0},
                'horizon_shifts': {},
                'md': {'val': 9553.16627586735},
                'start': {'val': 0},
                'uuid': '9a29ef17-5c48-4d7c-a610-974730472e2f',
                'x': {'val': 1506.8463116346054},
                'y': {'val': -1064.5840083926553},
            },
        ],
    }
}

EI_LAST_SEGMENT_EXTENDED_ASSEMBLED_SEGMENTS_DATA_RESPONSE = {
    'assembled_segments': {
        'horizons': {
            HORIZON_ID: {'tvd': {'val': 4875.37313679709}, 'uuid': HORIZON_ID},
            HORIZON_2_ID: {'tvd': {'val': 4329.045990215498}, 'uuid': HORIZON_2_ID},
            HORIZON_3_ID: {'tvd': {'val': 4029.045990215498}, 'uuid': HORIZON_3_ID},
        },
        'interp_end_md': {'val': 10752.111566697264},
        'interp_end_x': {'val': 2335.5283650656565},
        'interp_end_y': {'val': -1922.709395273677},
        'linked_to_trj_end': False,
        'segments': [
            {
                'boundary_type': 1,
                'end': {'val': 0},
                'horizon_shifts': {
                    HORIZON_ID: {
                        'end': {'val': 1685.1139500714344},
                        'start': {'val': 1632.956791751696},
                        'uuid': HORIZON_ID,
                    },
                    HORIZON_2_ID: {
                        'end': {'val': 1685.1139500714344},
                        'start': {'val': 1632.956791751696},
                        'uuid': HORIZON_2_ID,
                    },
                    HORIZON_3_ID: {
                        'end': {'val': 1685.1139500714344},
                        'start': {'val': 1632.956791751696},
                        'uuid': HORIZON_3_ID,
                    },
                },
                'md': {'val': 7627.5},
                'start': {'val': 0},
                'uuid': '651fe01d-30a4-4c85-b2af-a2dceb4f0385',
                'x': {'val': 0},
                'y': {'val': 0},
            },
            {
                'boundary_type': 1,
                'end': {'val': 0},
                'horizon_shifts': {
                    HORIZON_ID: {
                        'end': {'val': 1607.072769489806},
                        'start': {'val': 1685.1139500714344},
                        'uuid': HORIZON_ID,
                    },
                    HORIZON_2_ID: {
                        'end': {'val': 1607.072769489806},
                        'start': {'val': 1685.1139500714344},
                        'uuid': HORIZON_2_ID,
                    },
                    HORIZON_3_ID: {
                        'end': {'val': 1607.072769489806},
                        'start': {'val': 1685.1139500714344},
                        'uuid': HORIZON_3_ID,
                    },
                },
                'md': {'val': 8756.1},
                'start': {'val': 0},
                'uuid': 'de40551b-d869-47ab-b414-d41fc49aeff9',
                'x': {'val': 936.0090093403047},
                'y': {'val': -512.7027100919538},
            },
            {
                'boundary_type': 1,
                'end': {'val': 0},
                'fake': True,
                'horizon_shifts': {
                    HORIZON_ID: {
                        'end': {'val': 1607.072769489806},
                        'start': {'val': 1607.072769489806},
                        'uuid': HORIZON_ID,
                    },
                    HORIZON_2_ID: {
                        'end': {'val': 1607.072769489806},
                        'start': {'val': 1607.072769489806},
                        'uuid': HORIZON_2_ID,
                    },
                    HORIZON_3_ID: {
                        'end': {'val': 1607.072769489806},
                        'start': {'val': 1607.072769489806},
                        'uuid': HORIZON_3_ID,
                    },
                },
                'md': {'val': 10752.111566697264},
                'start': {'val': 0},
                'uuid': '1914d408-51ce-4117-b91f-e20dcfece20a',
                'x': {'val': 2335.5283650656565},
                'y': {'val': -1922.709395273677},
            },
        ],
    }
}

EI_LAST_SEGMENT_OUT_ASSEMBLED_SEGMENTS_DATA_RESPONSE = {
    'assembled_segments': {
        'horizons': {
            HORIZON_ID: {'tvd': {'val': 4875.37313679709}, 'uuid': HORIZON_ID},
            HORIZON_2_ID: {'tvd': {'val': 4329.045990215498}, 'uuid': HORIZON_2_ID},
            HORIZON_3_ID: {'tvd': {'val': 4029.045990215498}, 'uuid': HORIZON_3_ID},
        },
        'interp_end_md': {'val': 10741.239115452869},
        'interp_end_x': {'val': 2328.0135891272166},
        'interp_end_y': {'val': -1914.927616987544},
        'linked_to_trj_end': False,
        'segments': [
            {
                'boundary_type': 1,
                'end': {'val': 0},
                'horizon_shifts': {
                    HORIZON_ID: {
                        'end': {'val': 1685.1139500714344},
                        'start': {'val': 1632.956791751696},
                        'uuid': HORIZON_ID,
                    },
                    HORIZON_2_ID: {
                        'end': {'val': 1685.1139500714344},
                        'start': {'val': 1632.956791751696},
                        'uuid': HORIZON_2_ID,
                    },
                    HORIZON_3_ID: {
                        'end': {'val': 1685.1139500714344},
                        'start': {'val': 1632.956791751696},
                        'uuid': HORIZON_3_ID,
                    },
                },
                'md': {'val': 7627.5},
                'start': {'val': 0},
                'uuid': 'a0cbc76d-b524-4061-ad69-2751353209d0',
                'x': {'val': 0},
                'y': {'val': 0},
            },
            {
                'boundary_type': 1,
                'end': {'val': 0},
                'horizon_shifts': {
                    HORIZON_ID: {
                        'end': {'val': 1654.0526934167056},
                        'start': {'val': 1685.1139500714344},
                        'uuid': HORIZON_ID,
                    },
                    HORIZON_2_ID: {
                        'end': {'val': 1654.0526934167056},
                        'start': {'val': 1685.1139500714344},
                        'uuid': HORIZON_2_ID,
                    },
                    HORIZON_3_ID: {
                        'end': {'val': 1654.0526934167056},
                        'start': {'val': 1685.1139500714344},
                        'uuid': HORIZON_3_ID,
                    },
                },
                'md': {'val': 8756.1},
                'start': {'val': 0},
                'uuid': '5841ccb7-5f38-4209-87d1-3830b98ab86f',
                'x': {'val': 936.0090093403047},
                'y': {'val': -512.7027100919538},
            },
            {
                'boundary_type': 1,
                'end': {'val': 0},
                'horizon_shifts': {
                    HORIZON_ID: {
                        'end': {'val': 1607.4987997150938},
                        'start': {'val': 1654.0526934167056},
                        'uuid': HORIZON_ID,
                    },
                    HORIZON_2_ID: {
                        'end': {'val': 1607.4987997150938},
                        'start': {'val': 1654.0526934167056},
                        'uuid': HORIZON_2_ID,
                    },
                    HORIZON_3_ID: {
                        'end': {'val': 1607.4987997150938},
                        'start': {'val': 1654.0526934167056},
                        'uuid': HORIZON_3_ID,
                    },
                },
                'md': {'val': 9553.16627586735},
                'start': {'val': 0},
                'uuid': '84848ad6-c533-4399-a180-2c96928e1fc3',
                'x': {'val': 1506.8463116346054},
                'y': {'val': -1064.5840083926553},
            },
            {
                'boundary_type': 1,
                'end': {'val': 0},
                'fake': True,
                'horizon_shifts': {
                    HORIZON_ID: {
                        'end': {'val': 1607.4987997150938},
                        'start': {'val': 1607.4987997150938},
                        'uuid': HORIZON_ID,
                    },
                    HORIZON_2_ID: {
                        'end': {'val': 1607.4987997150938},
                        'start': {'val': 1607.4987997150938},
                        'uuid': HORIZON_2_ID,
                    },
                    HORIZON_3_ID: {
                        'end': {'val': 1607.4987997150938},
                        'start': {'val': 1607.4987997150938},
                        'uuid': HORIZON_3_ID,
                    },
                },
                'md': {'val': 10741.239115452869},
                'start': {'val': 0},
                'uuid': 'ff150e23-d57b-4604-85b0-7a37752d1868',
                'x': {'val': 2328.0135891272166},
                'y': {'val': -1914.927616987544},
            },
        ],
    }
}

EI_ABSENT_HORIZONS_LAST_SEGMENT_OUT_ASSEMBLED_SEGMENTS_DATA_RESPONSE = {
    'assembled_segments': {
        'horizons': {},
        'interp_end_md': {'val': 10741.239115452869},
        'interp_end_x': {'val': 2328.0135891272166},
        'interp_end_y': {'val': -1914.927616987544},
        'linked_to_trj_end': False,
        'segments': [
            {
                'boundary_type': 1,
                'end': {'val': 0},
                'horizon_shifts': {},
                'md': {'val': 7627.5},
                'start': {'val': 0},
                'uuid': '975a8cee-ac1c-4ce1-9aa6-b7c51131a49a',
                'x': {'val': 0},
                'y': {'val': 0},
            },
            {
                'boundary_type': 1,
                'end': {'val': 0},
                'horizon_shifts': {},
                'md': {'val': 8756.1},
                'start': {'val': 0},
                'uuid': 'b7089fc1-6973-46a5-b1f5-559b219eadd7',
                'x': {'val': 936.0090093403047},
                'y': {'val': -512.7027100919538},
            },
            {
                'boundary_type': 1,
                'end': {'val': 0},
                'horizon_shifts': {},
                'md': {'val': 9553.16627586735},
                'start': {'val': 0},
                'uuid': '9a29ef17-5c48-4d7c-a610-974730472e2f',
                'x': {'val': 1506.8463116346054},
                'y': {'val': -1064.5840083926553},
            },
            {
                'boundary_type': 1,
                'end': {'val': 0},
                'fake': True,
                'horizon_shifts': {},
                'md': {'val': 10741.239115452869},
                'start': {'val': 0},
                'uuid': '3e890133-2b73-465b-880a-ec74971c11a2',
                'x': {'val': 2328.0135891272166},
                'y': {'val': -1914.927616987544},
            },
        ],
    }
}

EI_ALL_SEGMENTS_OUT_ASSEMBLED_SEGMENTS_DATA_RESPONSE = {
    'assembled_segments': {
        'horizons': {
            '0a4ef2ef-5174-4c25-b29b-a2f7c85fbbcc': {
                'tvd': {'val': 4329.045990215498},
                'uuid': '0a4ef2ef-5174-4c25-b29b-a2f7c85fbbcc',
            },
            '4f3e2434-cfe5-435e-92d1-70fbd79068a1': {
                'tvd': {'val': 4875.37313679709},
                'uuid': '4f3e2434-cfe5-435e-92d1-70fbd79068a1',
            },
        },
        'interp_end_md': {'val': 10815.482734181383},
        'interp_end_x': {'val': 552.3509149701249},
        'interp_end_y': {'val': -571.9761163408157},
        'linked_to_trj_end': False,
        'segments': [
            {
                'boundary_type': 1,
                'end': {'val': 0},
                'horizon_shifts': {
                    '0a4ef2ef-5174-4c25-b29b-a2f7c85fbbcc': {
                        'end': {'val': 1604.589609790748},
                        'start': {'val': 1635.9036751295716},
                        'uuid': '0a4ef2ef-5174-4c25-b29b-a2f7c85fbbcc',
                    },
                    '4f3e2434-cfe5-435e-92d1-70fbd79068a1': {
                        'end': {'val': 1604.589609790748},
                        'start': {'val': 1635.9036751295716},
                        'uuid': '4f3e2434-cfe5-435e-92d1-70fbd79068a1',
                    },
                },
                'md': {'val': 10016.336034132659},
                'start': {'val': 0},
                'uuid': 'dbaf3052-b33e-4d1c-81e1-18b6badc473d',
                'x': {'val': 0},
                'y': {'val': 0},
            },
            {
                'boundary_type': 1,
                'end': {'val': 0},
                'fake': True,
                'horizon_shifts': {
                    '0a4ef2ef-5174-4c25-b29b-a2f7c85fbbcc': {
                        'end': {'val': 1604.589609790748},
                        'start': {'val': 1604.589609790748},
                        'uuid': '0a4ef2ef-5174-4c25-b29b-a2f7c85fbbcc',
                    },
                    '4f3e2434-cfe5-435e-92d1-70fbd79068a1': {
                        'end': {'val': 1604.589609790748},
                        'start': {'val': 1604.589609790748},
                        'uuid': '4f3e2434-cfe5-435e-92d1-70fbd79068a1',
                    },
                },
                'md': {'val': 10815.482734181383},
                'start': {'val': 0},
                'uuid': '40127000-d2a4-4209-9935-b71ec99ecee1',
                'x': {'val': 552.3509149701249},
                'y': {'val': -571.9761163408157},
            },
        ],
    }
}

WELL_LINKED_TYPEWELLS_DATA_RESPONSE = {
    'content': [{'shift': {'val': 100.0}, 'typewell_id': TYPEWELL_ID}],
    'offset': 0,
    'limit': 100,
    'total': 1,
    'first': True,
    'last': True,
}


COMMENTS_DATA_RESPONSE = {
    'content': [
        {
            'comment_id': '34664bbc-e560-4e82-8925-7f8268f579be',
            'name': 'Comment 1',
            'comment_boxes': [
                {
                    'commentbox_id': '3e277460-4156-496d-850c-48e64ab8b273',
                    'text': 'Comment Text 1',
                    'anchor_md': {'val': 9999.999999998},
                },
                {
                    'commentbox_id': '7a31617e-393e-4cda-9fd5-bdeec1a08222',
                    'text': 'Comment Text 2',
                    'anchor_md': {'val': 9999.999999998},
                },
            ],
        },
        {'comment_id': '400a0f63-5064-4939-a2c7-05e7b5ddb920', 'name': 'Comment 2', 'comment_boxes': []},
    ],
    'offset': 0,
    'limit': 10,
    'total': 2,
    'first': True,
    'last': True,
}

WELL_ATTRIBUTES_DATA_RESPONSE = {
    'Name': {'value': WELL_NAME, 'attribute_id': 1},
    'API': {'value': 'api', 'attribute_id': 2},
    'Well Type': {'value': 'Deviated', 'attribute_id': 3},
    'Operator': {'value': 'operator', 'attribute_id': 4},
    'KB': {'value': {'val': WELL_KB}, 'attribute_id': 7},
    'Azimuth VS': {'value': {'val': WELL_AZIMUTH}, 'attribute_id': 8},
    'Convergence': {'value': {'val': WELL_CONVERGENCE}, 'attribute_id': 9},
    'X-srf': {'value': {'val': WELL_XSRF_REAL}, 'attribute_id': 12},
    'Y-srf': {'value': {'val': WELL_YSRF_REAL}, 'attribute_id': 13},
    'Spud date': {'value': '2022-11-17T13:15:31.000+00:00', 'attribute_id': 17},
    '# of Stages': {'value': 43, 'attribute_id': 43},
    'Final TVD': {'value': {'val': 0.49}, 'attribute_id': 49},
    'Final TVDSS': {'value': {'val': -0.5}, 'attribute_id': 50},
    'Formation': {'value': 'test51', 'attribute_id': 51},
    'Net pay': {'value': {'val': 52.0}, 'attribute_id': 52},
}

EARTH_MODELS_DATA_RESPONSE = {
    'content': [{'name': 'EarthModel1', 'uuid': 'fb8b686b-7be4-428b-a420-1d131667680f'}],
    'offset': 0,
    'limit': 100,
    'total': 1,
    'first': True,
    'last': True,
}

EARTH_MODEL_SECTIONS_DATA_RESPONSE = {
    '39691ce4-14fd-46b8-9fbb-e142ff61949f': {
        'dip': {'val': 1.570796326795},
        'layers': [
            {
                'resistivity_horizontal': {'val': 10},
                'resistivity_vertical': {'val': 10},
                'tvd': {'val': -100000},
                'uuid': 'd410849e-6868-4322-beec-381fed103bdb',
            },
            {
                'resistivity_horizontal': {'val': 119.282},
                'resistivity_vertical': {'val': 119.282},
                'tvd': {'val': 1905.66},
                'uuid': 'e5941785-139a-4f67-afbc-44a7a5eafb92',
            },
            {
                'resistivity_horizontal': {'val': 119.253},
                'resistivity_vertical': {'val': 119.253},
                'tvd': {'val': 1905.7},
                'uuid': 'da6b9ec8-2f87-4bdc-ba9d-e4bb3c291dda',
            },
            {
                'resistivity_horizontal': {'val': 130.576},
                'resistivity_vertical': {'val': 130.576},
                'tvd': {'val': 1905.76},
                'uuid': '99621e3e-2d31-4a78-8dd5-e19830cd9997',
            },
            {
                'resistivity_horizontal': {'val': 137.125},
                'resistivity_vertical': {'val': 137.125},
                'tvd': {'val': 1905.78},
                'uuid': '0c3bba7b-0b00-4686-bc80-bd52cc0e5f91',
            },
            {
                'resistivity_horizontal': {'val': 137.129},
                'resistivity_vertical': {'val': 137.129},
                'tvd': {'val': 1905.8},
                'uuid': '3f8a26f7-c20c-441e-9f1b-270362172ed5',
            },
            {
                'resistivity_horizontal': {'val': 137.114},
                'resistivity_vertical': {'val': 137.114},
                'tvd': {'val': 1905.88},
                'uuid': '0216eec3-3638-42c9-a747-81aef5c26ae0',
            },
        ],
        'md': {'val': 2126},
        'uuid': '3a5771d3-1770-4685-87d3-16075f6da92f',
    },
    '3fd0a985-a77a-411e-a108-1fbac6238913': {
        'dip': {'val': 1.570796326795},
        'layers': [
            {
                'resistivity_horizontal': {'val': 10},
                'resistivity_vertical': {'val': 10},
                'tvd': {'val': -100000},
                'uuid': '3315f216-bcd3-46dc-8361-233e4ae6476b',
            },
            {
                'resistivity_horizontal': {'val': 215.009},
                'resistivity_vertical': {'val': 215.009},
                'tvd': {'val': 1903.13},
                'uuid': 'efec41ad-5f2a-4a5b-aa23-495b757feedb',
            },
            {
                'resistivity_horizontal': {'val': 214.994},
                'resistivity_vertical': {'val': 214.994},
                'tvd': {'val': 1903.32},
                'uuid': '587131a6-4759-4fc4-857b-2a776c375e89',
            },
            {
                'resistivity_horizontal': {'val': 198.325},
                'resistivity_vertical': {'val': 198.325},
                'tvd': {'val': 1903.39},
                'uuid': '77f9f980-9ece-463b-9e84-6ff38b9b7bf2',
            },
            {
                'resistivity_horizontal': {'val': 198.336},
                'resistivity_vertical': {'val': 198.336},
                'tvd': {'val': 1903.6000000000001},
                'uuid': '5213f83e-ae15-448b-9002-83962e1c5a83',
            },
            {
                'resistivity_horizontal': {'val': 198.234},
                'resistivity_vertical': {'val': 198.234},
                'tvd': {'val': 1903.79},
                'uuid': '2b55c8ed-85f2-4392-a3fd-a651f2922b7d',
            },
            {
                'resistivity_horizontal': {'val': 197.855},
                'resistivity_vertical': {'val': 197.855},
                'tvd': {'val': 1904.16},
                'uuid': 'edefa44b-c2be-4abe-9c77-ca314ae33171',
            },
        ],
        'md': {'val': 7630.1},
        'uuid': '3fd0a985-a77a-411e-a108-1fbac6238913',
    },
    '461ac4d4-3e2a-433b-8708-961ce9806375': {
        'dip': {'val': 1.570796326795},
        'layers': [
            {
                'resistivity_horizontal': {'val': 10},
                'resistivity_vertical': {'val': 10},
                'tvd': {'val': -100000},
                'uuid': 'ada80dc2-f62f-4bb2-a281-99ab2ec8d7e0',
            },
            {
                'resistivity_horizontal': {'val': 23.7215},
                'resistivity_vertical': {'val': 23.7215},
                'tvd': {'val': 1905.38},
                'uuid': 'f172dd02-f6de-49ba-9587-a6965b6f46e5',
            },
            {
                'resistivity_horizontal': {'val': 24.1746},
                'resistivity_vertical': {'val': 24.1746},
                'tvd': {'val': 1905.4},
                'uuid': '402173b7-c21d-498e-80a7-2a33588962c9',
            },
            {
                'resistivity_horizontal': {'val': 24.2001},
                'resistivity_vertical': {'val': 24.2001},
                'tvd': {'val': 1905.44},
                'uuid': 'c5d9950c-39bb-44b3-b554-5868596b5b79',
            },
            {
                'resistivity_horizontal': {'val': 25.0165},
                'resistivity_vertical': {'val': 25.0165},
                'tvd': {'val': 1905.45},
                'uuid': '348d8bf2-ea5b-45f2-8aad-c7bb06fe2f2b',
            },
            {
                'resistivity_horizontal': {'val': 25.5327},
                'resistivity_vertical': {'val': 25.5327},
                'tvd': {'val': 1905.47},
                'uuid': '4e077ad4-efae-4821-a37f-595c7081b752',
            },
            {
                'resistivity_horizontal': {'val': 27.0291},
                'resistivity_vertical': {'val': 27.0291},
                'tvd': {'val': 1905.49},
                'uuid': '91c24db1-c2d8-4565-bada-7f2e9e060bff',
            },
        ],
        'md': {'val': 8780.1},
        'uuid': '461ac4d4-3e2a-433b-8708-961ce9806375',
    },
}
