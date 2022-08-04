from os import environ

from pandas import DataFrame

from rogii_solo import SoloClient
from rogii_solo.calculations.enums import EMeasureUnits
from rogii_solo.calculations.trajectory import calculate_trajectory

PROJECT_NAME = 'Global project'
WELL_NAME = 'Lateral'
MEASURE_UNIT = EMeasureUnits.METER_FOOT
DLS_THRESHOLD = 0.5


def get_trajectory_dls():
    client = SoloClient(
        client_id=environ.get('ROGII_SOLO_CLIENT_ID'),
        client_secret=environ.get('ROGII_SOLO_CLIENT_SECRET'),
        papi_domain_name=environ.get('ROGII_SOLO_PAPI_DOMAIN_NAME')
    )
    client.set_project_by_name(project_name=PROJECT_NAME)

    well = client.project.wells.find_by_name(WELL_NAME)

    if well is None:
        print(f'Well "{WELL_NAME}" not found.')
        return

    well_data = well.to_dict()
    calculated_trajectory = calculate_trajectory(well.trajectory_data, well_data, measure_unit=MEASURE_UNIT)

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
