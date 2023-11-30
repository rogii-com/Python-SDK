from tests.papi_data import (
    CALC_TRACE_DATA_RESPONSE,
    CALC_TRACE_NAME,
    TIME_TRACE_DATA_RESPONSE,
    TIME_TRACE_NAME,
    WELL_NAME,
)


def test_get_time_trace(project):
    start_datetime = '2020-08-31T12:00:00Z'
    end_datetime = '2022-06-10T12:17:43.000Z'

    well = project.wells.find_by_name(WELL_NAME)
    assert well is not None

    time_traces = well.time_traces
    assert time_traces is not None

    traces_data = time_traces.to_dict()
    traces_df = time_traces.to_df()
    assert traces_data
    assert not traces_df.empty

    time_trace = time_traces.find_by_name(TIME_TRACE_NAME)
    assert time_trace is not None

    trace_points = time_trace.points
    assert trace_points is not None

    trace_points_data = trace_points.to_dict()
    assert trace_points_data
    assert len(trace_points_data) == len(trace_points)

    trace_points_data = trace_points.to_dict(time_from=start_datetime, time_to=end_datetime)
    trace_points_df = trace_points.to_df(time_from=start_datetime, time_to=end_datetime)

    assert trace_points_data
    assert not trace_points_df.empty

    point_index = 2
    point = TIME_TRACE_DATA_RESPONSE['content'][point_index]

    assert trace_points_data[point_index]['value'] == point['value']
    assert trace_points_data[point_index]['index'] == point['index']

    assert trace_points_df.at[point_index, 'value'] == point['value']
    assert trace_points_df.at[point_index, 'index'] == point['index']


def test_get_calc_trace(project):
    well = project.wells.find_by_name(WELL_NAME)
    assert well is not None

    calc_traces = well.calc_traces
    assert calc_traces is not None

    traces_data = calc_traces.to_dict()
    traces_df = calc_traces.to_df()
    assert traces_data
    assert not traces_df.empty

    calc_trace = calc_traces.find_by_name(CALC_TRACE_NAME)
    assert calc_trace is not None

    rac_codes = calc_trace.rac_codes
    assert rac_codes

    rac_codes_data = rac_codes.to_dict()
    rac_codes_df = rac_codes.to_df()
    assert rac_codes_data
    assert not rac_codes_df.empty

    trace_points = calc_trace.points
    assert trace_points is not None

    trace_points_data = trace_points.to_dict()
    trace_points_df = trace_points.to_df()
    assert trace_points_data
    assert not trace_points_df.empty
    assert len(trace_points_data) == len(trace_points_df) == len(CALC_TRACE_DATA_RESPONSE['content'])


def test_calc_trace_before_interval(project):
    calc_trace = project.wells.find_by_name(WELL_NAME).calc_traces.find_by_name(CALC_TRACE_NAME)
    assert calc_trace is not None

    trace_points = calc_trace.points
    assert trace_points is not None

    time_from = '2020-08-01T10:00:00Z'
    time_to = '2020-09-01T10:00:00Z'
    trace_points_data = trace_points.to_dict(time_from=time_from, time_to=time_to)
    trace_points_df = trace_points.to_df(time_from=time_from, time_to=time_to)
    assert not trace_points_data
    assert trace_points_df.empty


def test_calc_trace_after_interval(project):
    calc_trace = project.wells.find_by_name(WELL_NAME).calc_traces.find_by_name(CALC_TRACE_NAME)
    assert calc_trace is not None

    trace_points = calc_trace.points
    assert trace_points is not None

    time_from = '2020-09-13T10:53:19Z'
    time_to = '2020-10-13T10:53:19Z'
    trace_points_data = trace_points.to_dict(time_from=time_from, time_to=time_to)
    trace_points_df = trace_points.to_df(time_from=time_from, time_to=time_to)
    assert not trace_points_data
    assert trace_points_df.empty


def test_calc_trace_interval_boundaries(project):
    calc_trace = project.wells.find_by_name(WELL_NAME).calc_traces.find_by_name(CALC_TRACE_NAME)
    assert calc_trace is not None

    trace_points = calc_trace.points
    assert trace_points is not None

    point_index = 0
    point = CALC_TRACE_DATA_RESPONSE['content'][point_index]
    time_from = point['start']
    time_to = point['end']
    trace_points_data = trace_points.to_dict(time_from=time_from, time_to=time_to)
    trace_points_df = trace_points.to_df(time_from=time_from, time_to=time_to)
    assert len(trace_points_data) == len(trace_points_df) == 1

    assert trace_points_data[point_index]['start'] == point['start']
    assert trace_points_data[point_index]['end'] == point['end']
    assert trace_points_data[point_index]['value'] == point['value']

    point_index = -1
    point = CALC_TRACE_DATA_RESPONSE['content'][point_index]
    time_from = point['start']
    time_to = point['end']
    trace_points_data = trace_points.to_dict(time_from=time_from, time_to=time_to)
    trace_points_df = trace_points.to_df(time_from=time_from, time_to=time_to)
    assert len(trace_points_data) == len(trace_points_df) == 1

    assert trace_points_data[point_index]['start'] == point['start']
    assert trace_points_data[point_index]['end'] == point['end']
    assert trace_points_data[point_index]['value'] == point['value']


def test_calc_trace_interval_middle(project):
    calc_trace = project.wells.find_by_name(WELL_NAME).calc_traces.find_by_name(CALC_TRACE_NAME)
    assert calc_trace is not None

    trace_points = calc_trace.points
    assert trace_points is not None

    time_from = '2020-09-03T11:53:09Z'
    time_to = '2020-09-04T06:11:37Z'
    trace_points_data = trace_points.to_dict(time_from=time_from, time_to=time_to)
    trace_points_df = trace_points.to_df(time_from=time_from, time_to=time_to)
    assert len(trace_points_data) == len(trace_points_df) == 2

    for point_index in [1, 2]:
        point = CALC_TRACE_DATA_RESPONSE['content'][point_index]
        assert trace_points_data[point_index - 1]['start'] == point['start']
        assert trace_points_data[point_index - 1]['end'] == point['end']
        assert trace_points_data[point_index - 1]['value'] == point['value']


def test_calc_trace_after_interval_start(project):
    calc_trace = project.wells.find_by_name(WELL_NAME).calc_traces.find_by_name(CALC_TRACE_NAME)
    assert calc_trace is not None

    trace_points = calc_trace.points
    assert trace_points is not None

    time_from = '2020-09-01T10:00:00Z'
    time_to = '2020-09-01T10:00:01Z'
    trace_points_data = trace_points.to_dict(time_from=time_from, time_to=time_to)
    trace_points_df = trace_points.to_df(time_from=time_from, time_to=time_to)
    assert len(trace_points_data) == len(trace_points_df) == 1

    point_index = 0
    point = CALC_TRACE_DATA_RESPONSE['content'][point_index]
    assert trace_points_data[point_index]['start'] == point['start']
    assert trace_points_data[point_index]['end'] == point['end']
    assert trace_points_data[point_index]['value'] == point['value']


def test_calc_trace_after_interval_start_no_time_from(project):
    calc_trace = project.wells.find_by_name(WELL_NAME).calc_traces.find_by_name(CALC_TRACE_NAME)
    assert calc_trace is not None

    trace_points = calc_trace.points
    assert trace_points is not None

    time_from = None
    time_to = '2020-09-01T10:00:01Z'
    trace_points_data = trace_points.to_dict(time_from=time_from, time_to=time_to)
    trace_points_df = trace_points.to_df(time_from=time_from, time_to=time_to)
    assert len(trace_points_data) == len(trace_points_df) == 1

    point_index = 0
    point = CALC_TRACE_DATA_RESPONSE['content'][point_index]
    assert trace_points_data[point_index]['start'] == point['start']
    assert trace_points_data[point_index]['end'] == point['end']
    assert trace_points_data[point_index]['value'] == point['value']


def test_calc_trace_before_interval_end(project):
    calc_trace = project.wells.find_by_name(WELL_NAME).calc_traces.find_by_name(CALC_TRACE_NAME)
    assert calc_trace is not None

    trace_points = calc_trace.points
    assert trace_points is not None

    time_from = '2020-09-13T10:53:18Z'
    time_to = '2020-10-13T10:53:19Z'
    trace_points_data = trace_points.to_dict(time_from=time_from, time_to=time_to)
    trace_points_df = trace_points.to_df(time_from=time_from, time_to=time_to)
    assert len(trace_points_data) == len(trace_points_df) == 1

    point_index = -1
    point = CALC_TRACE_DATA_RESPONSE['content'][point_index]
    assert trace_points_data[point_index]['start'] == point['start']
    assert trace_points_data[point_index]['end'] == point['end']
    assert trace_points_data[point_index]['value'] == point['value']


def test_calc_trace_before_interval_end_no_time_to(project):
    calc_trace = project.wells.find_by_name(WELL_NAME).calc_traces.find_by_name(CALC_TRACE_NAME)
    assert calc_trace is not None

    trace_points = calc_trace.points
    assert trace_points is not None

    time_from = '2020-09-13T10:53:18Z'
    time_to = None
    trace_points_data = trace_points.to_dict(time_from=time_from, time_to=time_to)
    trace_points_df = trace_points.to_df(time_from=time_from, time_to=time_to)
    assert len(trace_points_data) == len(trace_points_df) == 1

    point_index = -1
    point = CALC_TRACE_DATA_RESPONSE['content'][point_index]
    assert trace_points_data[point_index]['start'] == point['start']
    assert trace_points_data[point_index]['end'] == point['end']
    assert trace_points_data[point_index]['value'] == point['value']
