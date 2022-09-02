from os import environ

from pandas import DataFrame

from rogii_solo import SoloClient
from rogii_solo.calculations.enums import EMeasureUnits
from rogii_solo.calculations.trajectory import calculate_trajectory

PROJECT_NAME = 'Global project'
WELL_NAME = 'Lateral'
MEASURE_UNITS = EMeasureUnits.METER_FOOT
DLS_THRESHOLD = 0.5


def get_trajectory_dls():
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

    calculated_trajectory = calculate_trajectory(
        raw_trajectory=well.trajectory.to_dict(get_converted=False),
        well=well.to_dict(get_converted=False),
        measure_units=MEASURE_UNITS
    )

    return [
        {
            'md': trajectory_point['md'],
            'dls': trajectory_point['dls'],
            'exceeds': trajectory_point['dls'] > DLS_THRESHOLD
        }
        for trajectory_point in calculated_trajectory
    ]


if __name__ == '__main__':
    dls_list = get_trajectory_dls()

    for row in dls_list:
        if row['exceeds']:
            print(f'DLS exceeds threshold={DLS_THRESHOLD} at MD={row["md"]}')

    print(DataFrame(dls_list))
