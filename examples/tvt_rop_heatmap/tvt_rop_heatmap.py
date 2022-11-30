import math
from bisect import bisect_left
from os import environ
from typing import Any, Dict, List, Tuple

import numpy as np
import plotly
import plotly.graph_objs as go
from scipy import stats

import rogii_solo.well
from rogii_solo import SoloClient
from rogii_solo.calculations.base import get_nearest_values
from rogii_solo.calculations.interpretation import interpolate_trajectory_point
from rogii_solo.calculations.trajectory import calculate_trajectory
from rogii_solo.interpretation import Interpretation


def get_interpolated_trajectory(solo_client: SoloClient, well: 'rogii_solo.well.Well') -> List[Dict[str, float]]:
    well_data = well.to_dict()
    calculated_trajectory = calculate_trajectory(
        raw_trajectory=well.trajectory.to_dict(),
        well=well_data,
        measure_units=solo_client.project.measure_unit
    )
    # get md range for interpolation
    md_range = range(int(calculated_trajectory[0]['md']), int(calculated_trajectory[-1]['md']) + 1)
    mds, mds_map = [], {}
    interpolated_trajectory = []

    for i, point in enumerate(calculated_trajectory):
        mds.append(point['md'])
        mds_map[point['md']] = i

    for md in md_range:
        nearest_mds = get_nearest_values(value=md, input_list=mds)

        if len(nearest_mds) < 2:
            interpolated_point = calculated_trajectory[0]
        else:
            left_point_md, right_point_md = nearest_mds

            left_point = calculated_trajectory[mds_map[left_point_md]]
            right_point = calculated_trajectory[mds_map[right_point_md]]

            interpolated_point = interpolate_trajectory_point(
                left_point=left_point,
                right_point=right_point,
                md=md,
                well=well_data,
                measure_units=solo_client.project.measure_unit,
            )

        interpolated_trajectory.append(interpolated_point)

    return interpolated_trajectory


def get_horizons(interpretation: Interpretation, md_step: int) -> List[Dict[str, Any]]:
    horizons = interpretation.get_tvt_data(md_step)

    if not horizons:
        raise Exception('Horizons\' data not found.')

    return horizons


def get_horizon_tvts(interpretation: Interpretation) -> List[Dict[str, Any]]:
    horizon_tvts = []
    horizons_data = interpretation.assembled_segments['horizons'].values()

    for horizon in horizons_data:
        horizon_tvts.append(
            {
                'name': horizon['name'],
                'uuid': horizon['uuid'],
                'tvt': horizon['tvd'],
            }
        )

    return horizon_tvts


def get_horizons_data_by_md(horizons: List[Dict[str, Any]], md: float) -> Dict[str, Any]:
    mds = [horizon_data['md'] for horizon_data in horizons]
    idx = bisect_left(mds, md)
    idx = idx if idx < len(mds) else -1

    return horizons[idx]


def add_tvt_to_trajectory(trajectory: List[Dict[str, float]],
                          horizons: List[Dict[str, Any]]
                          ) -> List[Dict[str, float]]:
    start_md = horizons[0]['md']
    end_md = horizons[-1]['md']

    for point in trajectory:
        md = point['md']

        if md < start_md or md > end_md:
            point['tvt'] = math.nan
            continue

        horizons_data = get_horizons_data_by_md(horizons=horizons, md=md)
        point['tvt'] = horizons_data['tvt']

    return trajectory


def get_trajectory_tvt_by_md(trajectory: List[Dict[str, float]], md: float) -> float:
    mds = [point['md'] for point in trajectory]
    idx = bisect_left(mds, md)

    return trajectory[idx]['tvt'] if idx < len(mds) else trajectory[-1]['tvt']


def filter_log(log: List[Dict[str, Any]], filter_window: int, idx: int) -> float:
    filtered_value = log[idx]['data']

    for j in range(-1 * filter_window, filter_window):
        filtered_value = filtered_value + log[idx + j]['data']

    return filtered_value / (filter_window * 2 + 1)


def get_heatmap_data(trajectory: List[Dict[str, float]],
                     filter_window: int,
                     x_log: List[Dict[str, Any]],
                     tvt_min: int,
                     tvt_max: int,
                     bins: int
                     ) -> Tuple[Any, Any, Any, float, float]:
    x, y = [], []

    for i in range(filter_window, len(x_log) - 1 - filter_window):
        md = x_log[i]['md']
        tvt = get_trajectory_tvt_by_md(trajectory=trajectory, md=md)
        value = filter_log(log=x_log, filter_window=filter_window, idx=i)

        if md < trajectory[-1]['md'] and tvt_min < tvt < tvt_max and not math.isnan(value):
            x.append(value)
            y.append(tvt)

    if not x or not y:
        raise Exception(
            'Warning! Data arrays are empty. '
            'Try to extend the TVT range (tvt_min, tvt_max) or check logs for values and MD ranges.'
        )

    histogram2d, xedges2, yedges2, _ = stats.binned_statistic_2d(
        x=x,
        y=y,
        values=y,
        statistic='count',
        bins=bins
    )
    histogram2d = histogram2d.T

    for i in range(bins):
        max_val = max(histogram2d[i])

        if max_val > 0:
            for j in range(bins):
                histogram2d[i][j] = histogram2d[i][j] / max_val

    return histogram2d, xedges2, yedges2, x[-1], y[-1]


def get_horizon_scatters(xedges2: Any,
                         yedges2: Any,
                         horizons: List[Dict[str, Any]],
                         zero_horizon_uuid: str
                         ) -> List[go.Scatter]:
    tvt_margin = 0.1
    y_min, y_max = np.nanmin(yedges2), np.nanmax(yedges2)
    x_min, x_max = np.nanmin(xedges2), np.nanmax(xedges2)
    data = []
    zero_tvt = 0

    for horizon in horizons:
        if horizon['uuid'] == zero_horizon_uuid:
            zero_tvt = horizon['tvt']
            break

    for horizon in horizons:
        tvt = horizon['tvt'] - zero_tvt

        if y_min - tvt_margin <= tvt <= y_max + tvt_margin:
            data.append(
                go.Scatter(
                    x=[x_min, x_max],
                    y=[tvt, tvt],
                    name=horizon['name'],
                    line={'dash': 'dot'},
                    mode='lines+text',
                    text=['', horizon['name']],
                    textposition='top left',
                    showlegend=False,
                    textfont={'size': 14, 'color': 'rgb(0, 175, 0)'}
                )
            )

    return data


def get_last_rop_point_scatter(last_x: float, last_y: float) -> go.Scatter:
    return go.Scatter(
        x=[last_x, ],
        y=[last_y, ],
        mode='markers',
        marker={
            'color': 'White',
            'size': 20,
            'line': {'width': 2, 'color': 'Red'},
        },
        showlegend=False
    )


def refine_log_points(log_points: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [point for point in log_points if point['data'] is not None]


def build_tvt_rop_heatmap(script_settings: Dict[str, Any]):
    project_name, well_name = script_settings['project_name'], script_settings['well_name']
    x_log_name, filter_window = script_settings['x_log'], script_settings['filter_window']
    tvt_min, tvt_max = script_settings['tvt_min'], script_settings['tvt_max']
    bins = script_settings['bins']

    solo_client = SoloClient(
        client_id=environ.get('ROGII_SOLO_CLIENT_ID'),
        client_secret=environ.get('ROGII_SOLO_CLIENT_SECRET'),
        papi_domain_name=environ.get('ROGII_SOLO_PAPI_DOMAIN_NAME')
    )
    solo_client.set_project_by_name(project_name)

    well = solo_client.project.wells.find_by_name(well_name)

    if well is None:
        raise Exception(f'Well "{well_name}" not found.')

    interpretation = well.starred_interpretation

    if not interpretation:
        raise Exception('Starred interpretation not found.')

    interpretation_data = interpretation.to_dict()

    # get trajectory and change its representation for convenience of calculations
    trajectory = get_interpolated_trajectory(solo_client=solo_client, well=well)

    # get horizons data with provided step by md
    horizons = get_horizons(interpretation=interpretation, md_step=1)

    # add tvts from horizon data
    trajectory = add_tvt_to_trajectory(trajectory=trajectory, horizons=horizons)

    x_log = well.logs.find_by_name(x_log_name)

    if not x_log:
        raise Exception(f'Log "{x_log_name}" not found.')

    # start plotting
    data = []
    histogram2d, xedges2, yedges2, last_x, last_y = get_heatmap_data(
        trajectory=trajectory,
        filter_window=filter_window,
        x_log=refine_log_points(x_log.to_dict()['points']),
        tvt_min=tvt_min,
        tvt_max=tvt_max,
        bins=bins
    )
    data.append(go.Heatmap(x=xedges2, y=yedges2, z=histogram2d, showscale=False))

    horizon_tvts = get_horizon_tvts(interpretation)
    horizon_scatters = get_horizon_scatters(
        xedges2=xedges2,
        yedges2=yedges2,
        horizons=horizon_tvts,
        zero_horizon_uuid=interpretation_data['meta']['properties']['zero_horizon_uuid']
    )
    data.extend(horizon_scatters)

    last_rop_point_scatter = get_last_rop_point_scatter(last_x, last_y)
    data.append(last_rop_point_scatter)

    layout = go.Layout(
        font={'size': 16},
        yaxis={
            'zeroline': False,
            'title': 'TVT',
            'range': [yedges2[-1], yedges2[0]],
            # set yaxes tick value format to xxxxx, not to xx.xxk
            'tickformatstops': [{'dtickrange': [-1000000, 1000000], 'value': ':d'}, ],
            'showticklabels': True,
            'tickcolor': 'rgb(127, 127, 127)',
            'ticks': 'outside'
        },
        xaxis={
            'zeroline': False,
            'title': x_log_name,
            'dtick': 25,
            'showticklabels': True,
            'tickcolor': 'rgb(127, 127, 127)',
            'ticks': 'outside',
            'range': [xedges2[0], xedges2[-1]]
        }
    )
    figure = go.Figure(data=data, layout=layout)
    config = {'showLink': True, 'linkText': "Edit Plot", 'scrollZoom': True}
    plotly.offline.plot(figure, filename='./tmpplot.html', config=config)


if __name__ == '__main__':
    script_settings = {
        'project_name': '',
        'well_name': '',
        'x_log': '',
        'tvt_min': -1,
        'tvt_max': 1,
        'filter_window': 5,
        'bins': 60
    }

    build_tvt_rop_heatmap(script_settings)
