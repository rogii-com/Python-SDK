from os import environ

import numpy as np
from pandas import DataFrame
from calculations.interpretation import get_segments
from calculations.trajectory import calculate_trajectory
from calculations.enums import EMeasureUnits
from python_sdk.client import PyRogii


PROJECT_NAME = 'nsapegin (ft)'
WELL_NAME = 'Lateral1'
INTERPRETATION_NAME = 'Interpretation1'
MEASURE_UNIT = EMeasureUnits.METER_FOOT


def pd_to_dict(dataframe):
    if isinstance(dataframe, DataFrame):
        if not dataframe.empty:
            return dataframe.loc[0].to_dict()

    return None


def interpretation_dip_calculation():
    pr = PyRogii(
        client_id=environ.get('CLIENT_ID'),
        client_secret=environ.get('CLIENT_SECRET'),
        solo_username=environ.get('SOLO_USERNAME'),
        solo_password=environ.get('SOLO_PASSWORD'),
        papi_domain_name=environ.get('PAPI_DOMAIN_NAME')
    )

    pr.set_project(project_name=PROJECT_NAME)

    pd_papi_well = pr.get_well(well_name=WELL_NAME)

    if pd_papi_well is None:
        print(f'Well "{WELL_NAME}" not found.')
        return

    papi_well = pd_to_dict(pd_papi_well)
    well_trajectory = pr.get_well_trajectory(well_name=WELL_NAME)

    calculated_trajectory = calculate_trajectory(well_trajectory, papi_well, measure_unit=MEASURE_UNIT)

    interpretation = pr.get_well_starred_interpretation(well_name=WELL_NAME)

    if not interpretation:
        interpretation = pr.get_well_interpretation(
            well_name=WELL_NAME, interpretation_name=INTERPRETATION_NAME
        )

    if not interpretation:
        print(f'Interpretation "{INTERPRETATION_NAME}" in the well "{WELL_NAME}" not found.')
        return

    segments = get_segments(
        papi_well,
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
    dips, interpolated_dips = interpretation_dip_calculation()
    print(dips)
    print(interpolated_dips)
