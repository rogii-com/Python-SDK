import random
from os import environ

from python_sdk.client import PyRogii

PROJECT_NAME = 'nsapegin (ft)'
WELL_NAME = 'Lateral1'

pr = PyRogii(
    client_id=environ.get('CLIENT_ID'),
    client_secret=environ.get('CLIENT_SECRET'),
    solo_username=environ.get('SOLO_USERNAME'),
    solo_password=environ.get('SOLO_PASSWORD'),
    papi_domain_name=environ.get('PAPI_DOMAIN_NAME')
)

pr.set_project(project_name=PROJECT_NAME)

wells = pr.get_project_wells()
print('Wells in the project (all information in the pandas format):\n', wells)
print('\nWells in the project (selected info):\n', wells[['name', 'api']])

well = pr.get_well(well_name=WELL_NAME)
print('\nWell (in the python dictionary format):\n', well)

well_trajectory = pr.get_well_trajectory(well_name=WELL_NAME)
print('\nWell trajectory (in the pandas format):\n', well_trajectory)

starred_interpretation = pr.get_well_starred_interpretation(well_name=WELL_NAME)
print('\nStarred interpretation (python dictionary of three items (one python dict and two pandas dataframes)):\n',
      starred_interpretation)

starred_target_line = pr.get_well_starred_target_line(well_name=WELL_NAME)
print('\nStarred target line (in the python dictionary format)):\n', starred_target_line)

nested_well_name = 'Nested Well ' + str(random.randint(0, 10000))
result = pr.create_nested_well(
    well_name=WELL_NAME,
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
print(pr.get_well_nested_well(well_name=WELL_NAME, nested_well_name=nested_well_name))
