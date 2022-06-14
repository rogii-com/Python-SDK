from os import environ

import numpy as np
from calculations.enums import EMeasureUnits
from calculations.interpretation import get_segments
from calculations.trajectory import calculate_trajectory
from pandas import DataFrame

from python_sdk.client import PyRogii
from python_sdk.utils.objects import pd_to_dict

PROJECT_NAME = 'nsapegin (ft)'
WELL_NAME = 'Lateral1'
INTERPRETATION_NAME = 'Interpretation1'
MEASURE_UNIT = EMeasureUnits.METER_FOOT


def calc_interpretation_dip():
    pr = PyRogii(
        client_id=environ.get('CLIENT_ID'),
        client_secret=environ.get('CLIENT_SECRET'),
        solo_username=environ.get('SOLO_USERNAME'),
        solo_password=environ.get('SOLO_PASSWORD'),
        papi_domain_name=environ.get('PAPI_DOMAIN_NAME')
    )

    pr.set_project(project_name=PROJECT_NAME)

    pd_well = pr.get_well(well_name=WELL_NAME)

    if pd_well is None:
        print(f'Well "{WELL_NAME}" not found.')
        return

    well = pd_to_dict(pd_well)

    pd_well_trajectory: DataFrame = pr.get_well_trajectory(well_name=WELL_NAME)
    well_trajectory = [raw.to_dict() for _, raw in pd_well_trajectory.iterrows()]

    calculated_trajectory = calculate_trajectory(well_trajectory, well, measure_unit=MEASURE_UNIT)

    interpretation = pr.get_well_starred_interpretation(well_name=WELL_NAME)

    if not interpretation:
        interpretation = pr.get_well_interpretation(
            well_name=WELL_NAME, interpretation_name=INTERPRETATION_NAME
        )

    if not interpretation:
        print(f'Interpretation "{INTERPRETATION_NAME}" in the well "{WELL_NAME}" not found.')
        return

    segments = get_segments(
        well,
        assembled_segments=interpretation['segments'],
        assembled_horizons=interpretation['horizons'],
        calculated_trajectory=calculated_trajectory,
        measure_unit=MEASURE_UNIT
    )

    calculated_dips = DataFrame(segments, columns=['md', 'dip'])
    np_calculated_dips = calculated_dips.to_numpy()
    interpolated_md = sorted(
        np.unique(
            np.append(
                np.arange(np_calculated_dips[0, 0], np_calculated_dips[-1, 0], 50.0),
                np_calculated_dips[:, 0]
            )
        )
    )
    np_interpolated_dips = np.interp(interpolated_md, np_calculated_dips[:, 0], np_calculated_dips[:, 1])
    interpolated_dips = DataFrame((interpolated_md, np_interpolated_dips), index=['md', 'dip']).transpose()

    return calculated_dips, interpolated_dips


if __name__ == '__main__':
    dips, interpolated_dips = calc_interpretation_dip()
    print(dips)
    print(interpolated_dips)
