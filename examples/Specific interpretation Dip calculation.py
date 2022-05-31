from os import environ

import numpy as np
from pandas import DataFrame
from tools.interpretation import get_segments
from tools.trajectory import calculate_trajectory
from tools.enums import EMeasureUnits
from python_sdk.client import PyRogii


PROJECT_NAME = 'nsapegin (ft)'
WELL_NAME = 'Lateral1'
INTERPRETATION_NAME = 'Interpretation1'
measure_unit = EMeasureUnits.METER_FOOT


pr = PyRogii(
    client_id=environ.get('CLIENT_ID'),
    client_secret=environ.get('CLIENT_SECRET'),
    project_name=PROJECT_NAME,
    solo_username=environ.get('SOLO_USERNAME'),
    solo_password=environ.get('SOLO_PASSWORD'),
    papi_domain_name=environ.get('PAPI_DOMAIN_NAME')
)


def interpretation_dip_calculation():
    papi_well = pr.get_well(well_name=WELL_NAME)

    if not papi_well:
        print(f'Well "{papi_well["name"]}" not found')
        return

    well_trajectory = pr.get_well_trajectory(well_name=WELL_NAME)

    calculated_trajectory = calculate_trajectory(well_trajectory, papi_well, measure_unit=measure_unit)

    interpretation = pr.get_well_starred_interpretation(well_name=WELL_NAME)

    if not interpretation:
        interpretation = pr.get_well_interpretation(
            well_name=WELL_NAME, interpretation_name=INTERPRETATION_NAME
        )

    if not interpretation:
        print(f'Interpretation "{INTERPRETATION_NAME}" in the well "{WELL_NAME}" not found')
        return

    segments = get_segments(
        papi_well,
        assembled_segments=interpretation['segments'],
        assembled_horizons=interpretation['horizons'],
        calculated_trajectory=calculated_trajectory,
        measure_unit=measure_unit
    )

    _df = DataFrame(segments, columns=['md', 'dip'])
    np_array = _df.to_numpy()
    axe = np.arange(np_array[0, 0], np_array[-1, 0], 50.0)
    axe = np.unique(np.append(axe, np_array[:, 0]))
    axe.sort()
    interpolated_dip = np.interp(axe, np_array[:, 0], np_array[:, 1])
    _result_df = DataFrame((axe, interpolated_dip), index=['md', 'dip']).transpose()
    return _df, _result_df


if __name__ == '__main__':
    dips, interpolated_dips = interpretation_dip_calculation()
    print(dips)
    print(interpolated_dips)
