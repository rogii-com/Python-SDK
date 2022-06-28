from os import environ

import numpy as np
from calculations.enums import EMeasureUnits
from calculations.interpretation import get_segments
from calculations.trajectory import calculate_trajectory
from pandas import DataFrame

from python_sdk.client import RogiiSolo

PROJECT_NAME = 'Global project'
WELL_NAME = 'Lateral'
INTERPRETATION_NAME = 'Interpretation'
MEASURE_UNIT = EMeasureUnits.METER_FOOT


def calc_interpretation_dip():
    client = RogiiSolo(
        client_id=environ.get('CLIENT_ID'),
        client_secret=environ.get('CLIENT_SECRET'),
        solo_username=environ.get('SOLO_USERNAME'),
        solo_password=environ.get('SOLO_PASSWORD'),
        papi_domain_name=environ.get('PAPI_DOMAIN_NAME')
    )
    client.set_project_by_name(project_name=PROJECT_NAME)

    well = client.project.wells.find_by_name(WELL_NAME)

    if well is None:
        print(f'Well "{WELL_NAME}" not found.')
        return

    well_data = well.to_dict()
    calculated_trajectory = calculate_trajectory(well.trajectory_data, well_data, measure_unit=MEASURE_UNIT)
    interpretation = well.starred_interpretation or well.interpretations.find_by_name(INTERPRETATION_NAME)

    if not interpretation:
        print(f'Interpretation "{INTERPRETATION_NAME}" in the well "{WELL_NAME}" not found.')
        return

    interpretation_df = interpretation.to_df()
    segments = get_segments(
        well_data,
        assembled_segments=interpretation_df['segments'],
        assembled_horizons=interpretation_df['horizons'],
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
