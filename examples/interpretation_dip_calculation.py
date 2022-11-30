from os import environ

import numpy as np
from pandas import DataFrame

from rogii_solo import SoloClient
from rogii_solo.calculations.enums import EMeasureUnits
from rogii_solo.calculations.interpretation import get_segments, get_segments_with_dip
from rogii_solo.calculations.trajectory import calculate_trajectory

PROJECT_NAME = 'Global project'
WELL_NAME = 'Lateral'
INTERPRETATION_NAME = 'Interpretation'
MEASURE_UNITS = EMeasureUnits.METER_FOOT


def calc_interpretation_dip():
    solo_client = SoloClient(
        client_id=environ.get('ROGII_SOLO_CLIENT_ID'),
        client_secret=environ.get('ROGII_SOLO_CLIENT_SECRET'),
        papi_domain_name=environ.get('ROGII_SOLO_PAPI_DOMAIN_NAME')
    )
    solo_client.set_project_by_name(PROJECT_NAME)

    well = solo_client.project.wells.find_by_name(WELL_NAME)

    if well is None:
        print(f'Well "{WELL_NAME}" not found.')
        return

    well_data = well.to_dict(get_converted=False)
    calculated_trajectory = calculate_trajectory(
        raw_trajectory=well.trajectory.to_dict(get_converted=False),
        well=well_data,
        measure_units=MEASURE_UNITS
    )
    interpretation = well.starred_interpretation or well.interpretations.find_by_name(INTERPRETATION_NAME)

    if not interpretation:
        print(f'Interpretation "{INTERPRETATION_NAME}" in the well "{WELL_NAME}" not found.')
        return

    segments = get_segments(
        well=well_data,
        assembled_segments=interpretation.assembled_segments['segments'],
        calculated_trajectory=calculated_trajectory,
        measure_units=MEASURE_UNITS
    )
    segments_with_dip = get_segments_with_dip(
        segments=segments,
        assembled_horizons=interpretation.assembled_segments['horizons']
    )

    calculated_dips = DataFrame(segments_with_dip, columns=['md', 'dip'])
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
    calculated, interpolated = calc_interpretation_dip()
    print(calculated)
    print(interpolated)
