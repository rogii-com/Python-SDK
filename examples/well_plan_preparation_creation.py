import random
from os import environ

from python_sdk.client import RogiiSolo

PROJECT_NAME = 'nsapegin (ft)'
WELL_NAME = 'Lateral1'

client = RogiiSolo(
    client_id=environ.get('CLIENT_ID'),
    client_secret=environ.get('CLIENT_SECRET'),
    solo_username=environ.get('SOLO_USERNAME'),
    solo_password=environ.get('SOLO_PASSWORD'),
    papi_domain_name=environ.get('PAPI_DOMAIN_NAME')
)

client.set_project_by_name(PROJECT_NAME)
project = client.project
wells = project.wells

wells_df = wells.to_df()
print('Wells in the project (all information in the pandas format):\n', wells_df)
print('\nWells in the project (selected info):\n', wells_df[['name', 'api']])

well = wells.find_by_name(WELL_NAME)
print('\nWell (in the python dictionary format):\n', well.to_dict())

well_trajectory = well.trajectory.to_df()
print('\nWell trajectory (in the pandas format):\n', well_trajectory)

starred_interpretation = well.starred_interpretation.to_df()
print('\nStarred interpretation (python dictionary of three items (one python dict and two pandas dataframes)):\n',
      starred_interpretation)

starred_target_line = well.starred_target_line.to_dict()
print('\nStarred target line (in the python dictionary format)):\n', starred_target_line)

nested_well_name = 'Nested Well ' + str(random.randint(0, 10000))
result = well.create_nested_well(
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
