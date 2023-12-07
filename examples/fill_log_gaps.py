from os import environ

from rogii_solo import SoloClient

PROJECT_NAME = ''
WELL_NAME = ''
LOG_NAME = ''


def fill_gapped_logs():
    solo_client = SoloClient(
        client_id=environ.get('ROGII_SOLO_CLIENT_ID'),
        client_secret=environ.get('ROGII_SOLO_CLIENT_SECRET'),
        papi_domain_name=environ.get('ROGII_SOLO_PAPI_DOMAIN_NAME'),
    )

    solo_client.set_project_by_name(PROJECT_NAME)
    well = solo_client.project.wells.find_by_name(WELL_NAME)
    log = well.logs.find_by_name(LOG_NAME)
    filled_log_df = log.points.to_df().interpolate()
    well.create_log(log_name=f'{log.name}_gap_filled', log_points=filled_log_df.to_dict(orient='records'))


if __name__ == '__main__':
    fill_gapped_logs()
