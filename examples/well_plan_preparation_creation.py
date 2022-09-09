import random
from os import environ

from rogii_solo import SoloClient

PROJECT_NAME = 'Global project'
WELL_NAME = 'Lateral'


def prepare_well_plan():
    solo_client = SoloClient(
        client_id=environ.get('ROGII_SOLO_CLIENT_ID'),
        client_secret=environ.get('ROGII_SOLO_CLIENT_SECRET'),
        papi_domain_name=environ.get('ROGII_SOLO_PAPI_DOMAIN_NAME')
    )

    solo_client.set_project_by_name(PROJECT_NAME)
    project = solo_client.project
    wells = project.wells

    wells_df = wells.to_df()
    print('Wells in the project (all information in the pandas format):\n', wells_df)
    print('\nWells in the project (selected info):\n', wells_df[['name', 'api']])

    well = wells.find_by_name(WELL_NAME)

    if well is None:
        print(f'Well "{WELL_NAME}" not found.')
        return

    print('\nWell (in the python dictionary format):\n', well.to_dict())

    well_trajectory = well.trajectory.to_df()
    print('\nWell trajectory (in the pandas format):\n', well_trajectory)

    starred_interpretation = well.starred_interpretation.to_df()
    print('\nStarred interpretation (python dictionary of three items (one python dict and two pandas dataframes)):\n',
          starred_interpretation)

    starred_target_line = well.starred_target_line.to_dict()
    print('\nStarred target line (in the python dictionary format)):\n', starred_target_line)

    nested_well_name = 'Nested Well ' + str(random.randint(0, 10000))
    well.create_nested_well(
        nested_well_name=nested_well_name,
        operator='Operator',
        api=nested_well_name,
        xsrf=100000.0,
        ysrf=100000.0,
        kb=0.0,
        tie_in_tvd=0.0,
        tie_in_ns=0.0,
        tie_in_ew=0.0
    )
    print(f'\nCreated nested well "{nested_well_name}"')
    print(well.nested_wells.find_by_name(nested_well_name).to_dict())


if __name__ == '__main__':
    prepare_well_plan()
