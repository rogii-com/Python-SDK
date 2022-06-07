from os import environ

from pandas import DataFrame

from calculations.trajectory import calculate_trajectory
from calculations.enums import EMeasureUnits
from python_sdk.client import PyRogii
from python_sdk.utils.objects import pd_to_dict


PROJECT_NAME = 'nsapegin (ft)'
WELL_NAME = 'Lateral1'
INTERPRETATION_NAME = 'Interpretation1'
MEASURE_UNIT = EMeasureUnits.METER_FOOT

THRESHOLD = 0.5


def check_dls_excess():
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

    dls_list = [
        {
            'md': row['md'],
            'dls': row['dls'],
            'exceeds': row['dls'] > THRESHOLD
        }
        for row in calculated_trajectory
    ]

    for row in dls_list:
        if row['exceeds']:
            print(f'DLS exceeds threshold={THRESHOLD} at MD={row["md"]}')

    return DataFrame(dls_list)


if __name__ == '__main__':
    pd_dlses = check_dls_excess()
