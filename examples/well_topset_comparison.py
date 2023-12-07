from copy import deepcopy
from os import environ
from typing import Any, Dict, List, Tuple

import pandas as pd

from rogii_solo import SoloClient
from rogii_solo.calculations.base import get_nearest_values
from rogii_solo.calculations.enums import EMeasureUnits
from rogii_solo.calculations.trajectory import (
    calculate_trajectory,
    interpolate_trajectory_point,
)
from rogii_solo.calculations.types import Trajectory
from rogii_solo.topset import Topset
from rogii_solo.well import NestedWell, Well

PROJECT_NAME = ''
WELL_NAME = ''


def get_input_data() -> Tuple[Well, Topset, NestedWell, Topset, EMeasureUnits]:
    solo_client = SoloClient(
        client_id=environ.get('ROGII_SOLO_CLIENT_ID'),
        client_secret=environ.get('ROGII_SOLO_CLIENT_SECRET'),
        papi_domain_name=environ.get('ROGII_SOLO_PAPI_DOMAIN_NAME'),
    )

    solo_client.set_project_by_name(PROJECT_NAME)
    project = solo_client.project
    wells = project.wells

    well = wells.find_by_name(WELL_NAME)

    if well is None:
        raise Exception(f'Well "{WELL_NAME}" not found.')

    starred_well_topset = well.starred_topset
    if starred_well_topset is None:
        raise Exception(f'Starred topset in the well "{WELL_NAME}" not found.')

    starred_nested_well = well.starred_nested_well
    if starred_nested_well is None:
        raise Exception(f'Starred wellplan in the well "{WELL_NAME}" not found.')

    starred_nested_well_topset = starred_nested_well.starred_topset
    if starred_nested_well_topset is None:
        raise Exception(f'Starred topset in the wellplan "{starred_nested_well.name}" not found.')

    return (
        well,
        starred_well_topset,
        starred_nested_well,
        starred_nested_well_topset,
        solo_client.project.measure_unit,
    )


def calc_top_tvd(
    well_data: Dict[str, Any], calculated_trajectory: Trajectory, md: float, measure_unit: EMeasureUnits
) -> Tuple[float, float]:
    mds, mds_map = [], {}

    for i, point in enumerate(calculated_trajectory):
        mds.append(point['md'])
        mds_map[point['md']] = i

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
            measure_units=measure_unit,
        )

    return interpolated_point['tvd'], interpolated_point['tvdss']


def add_tvd_in_tops(
    well_data: Dict[str, Any],
    tops_data: List[Dict[str, Any]],
    calculated_trajectory: Trajectory,
    measure_unit: EMeasureUnits,
):
    for top in tops_data:
        top['tvd'], top['tvdss'] = calc_top_tvd(
            well_data=well_data, calculated_trajectory=calculated_trajectory, md=top['md'], measure_unit=measure_unit
        )


def compare_topsets():
    well, starred_well_topset, nested_well, nested_well_topset, measure_units = get_input_data()

    well_data = well.to_dict()
    calculated_trajectory = calculate_trajectory(
        raw_trajectory=well.trajectory.to_dict(), well=well_data, measure_units=measure_units
    )
    nested_well_data = nested_well.to_dict()
    calculated_nested_trajectory = calculate_trajectory(
        raw_trajectory=nested_well.trajectory.to_dict(), well=nested_well_data, measure_units=measure_units
    )

    well_tops_data = starred_well_topset.tops.to_dict()
    add_tvd_in_tops(
        well_data=well_data,
        tops_data=well_tops_data,
        calculated_trajectory=calculated_trajectory,
        measure_unit=measure_units,
    )
    well_tops_data.sort(key=lambda x: x['md'])

    nested_well_tops_data = nested_well_topset.tops.to_dict()
    add_tvd_in_tops(
        well_data=well_data,
        tops_data=nested_well_tops_data,
        calculated_trajectory=calculated_nested_trajectory,
        measure_unit=measure_units,
    )
    nested_well_tops_data.sort(key=lambda x: x['md'])

    unique_top_names = set()
    result_tops_data = deepcopy(nested_well_tops_data)

    for top_data in result_tops_data:
        if top_data['name'] in unique_top_names:
            continue

        unique_top_names.add(top_data['name'])
        first_eponymous_well_top_data = next((top for top in well_tops_data if top['name'] == top_data['name']), None)

        if first_eponymous_well_top_data is None:
            continue

        top_data['actual_md'] = first_eponymous_well_top_data['md']
        top_data['actual_tvd'] = first_eponymous_well_top_data['tvd']
        top_data['actual_tvdss'] = first_eponymous_well_top_data['tvdss']
        top_data['delta_md'] = top_data['actual_md'] - top_data['md']
        top_data['delta_tvd'] = top_data['actual_tvd'] - top_data['tvd']
        top_data['delta_tvdss'] = top_data['actual_tvdss'] - top_data['tvdss']

    # Set pandas output without truncated columns ("...")
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)

    df = pd.DataFrame(result_tops_data)
    print(df)


if __name__ == '__main__':
    compare_topsets()
