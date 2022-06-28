from os import environ

from calculations.enums import EMeasureUnits
from calculations.trajectory import calculate_trajectory
from pandas import DataFrame

from python_sdk.client import RogiiSolo

PROJECT_NAME = 'nsapegin (ft)'
WELL_NAME = 'Lateral1'
INTERPRETATION_NAME = 'Interpretation1'
MEASURE_UNIT = EMeasureUnits.METER_FOOT

DLS_THRESHOLD = 0.5


def check_dls_excess():
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

    dls_list = [
        {
            'md': row['md'],
            'dls': row['dls'],
            'exceeds': row['dls'] > DLS_THRESHOLD
        }
        for row in calculated_trajectory
    ]

    for row in dls_list:
        if row['exceeds']:
            print(f'DLS exceeds threshold={DLS_THRESHOLD} at MD={row["md"]}')

    return DataFrame(dls_list)


if __name__ == '__main__':
    pd_dlses = check_dls_excess()
