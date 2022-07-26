from rogii_solo.calculations.base import np_is_close

from tests.papi_data import (
    WELL_NAME,
    HORIZON_NAME
)


def test_get_converted_meter_well(project):
    well = project.wells.find_by_name(WELL_NAME)

    assert well is not None

    well_df = well.to_df()

    assert not well_df.empty

    assert np_is_close(well_df['xsrf_real'], 500000)
    assert np_is_close(well_df['ysrf_real'], 600000)
    assert np_is_close(well_df['kb'], 100)
    assert np_is_close(well_df['azimuth'], 325)
    assert np_is_close(well_df['convergence'], 10)


def test_get_not_converted_meter_well(project):
    well = project.wells.find_by_name(WELL_NAME)

    assert well is not None

    well_df = well.to_df(get_converted=False)

    assert not well_df.empty

    assert np_is_close(well_df['xsrf_real'], 500000)
    assert np_is_close(well_df['ysrf_real'], 600000)
    assert np_is_close(well_df['kb'], 100)
    assert np_is_close(well_df['azimuth'], 5.672320068981945)
    assert np_is_close(well_df['convergence'], 0.17453292519944444)


def test_get_converted_foot_well(ft_project):
    well = ft_project.wells.find_by_name(WELL_NAME)

    assert well is not None

    well_df = well.to_df()

    assert not well_df.empty

    assert np_is_close(well_df['xsrf_real'], 500000)
    assert np_is_close(well_df['ysrf_real'], 600000)
    assert np_is_close(well_df['kb'], 328.08399)
    assert np_is_close(well_df['azimuth'], 325)
    assert np_is_close(well_df['convergence'], 10)


def test_get_not_converted_foot_well(ft_project):
    well = ft_project.wells.find_by_name(WELL_NAME)

    assert well is not None

    well_df = well.to_df(get_converted=False)

    assert not well_df.empty

    assert np_is_close(well_df['xsrf_real'], 500000)
    assert np_is_close(well_df['ysrf_real'], 600000)
    assert np_is_close(well_df['kb'], 100)
    assert np_is_close(well_df['azimuth'], 5.672320068981945)
    assert np_is_close(well_df['convergence'], 0.17453292519944444)


def test_get_converted_ftm_well(ftm_project):
    well = ftm_project.wells.find_by_name(WELL_NAME)

    assert well is not None

    well_df = well.to_df()

    assert not well_df.empty

    assert np_is_close(well_df['xsrf_real'], 500000)
    assert np_is_close(well_df['ysrf_real'], 600000)
    assert np_is_close(well_df['kb'], 328.08399)
    assert np_is_close(well_df['azimuth'], 325)
    assert np_is_close(well_df['convergence'], 10)


def test_get_not_converted_ftm_well(ftm_project):
    well = ftm_project.wells.find_by_name(WELL_NAME)

    assert well is not None

    well_df = well.to_df(get_converted=False)

    assert not well_df.empty

    assert np_is_close(well_df['xsrf_real'], 500000)
    assert np_is_close(well_df['ysrf_real'], 600000)
    assert np_is_close(well_df['kb'], 100)
    assert np_is_close(well_df['azimuth'], 5.672320068981945)
    assert np_is_close(well_df['convergence'], 0.17453292519944444)


def test_get_converted_meter_trajectory(project):
    well = project.wells.find_by_name(WELL_NAME)

    assert well is not None

    trajectory_df = well.trajectory.to_df()

    assert not trajectory_df.empty

    assert not trajectory_df[
        np_is_close(trajectory_df['md'], 0) &
        np_is_close(trajectory_df['incl'], 0) &
        np_is_close(trajectory_df['azim'], 0)
        ].empty
    assert not trajectory_df[
        np_is_close(trajectory_df['md'], 447.99999999999994) &
        np_is_close(trajectory_df['incl'], 0.40000000000002633) &
        np_is_close(trajectory_df['azim'], 247.80000000001635)
        ].empty
    assert not trajectory_df[
        np_is_close(trajectory_df['md'], 7735.0) &
        np_is_close(trajectory_df['incl'], 1.5000000000000988) &
        np_is_close(trajectory_df['azim'], 157.50000000001032)
        ].empty
    assert not trajectory_df[
        np_is_close(trajectory_df['md'], 11383.0) &
        np_is_close(trajectory_df['incl'], 48.30000000000318) &
        np_is_close(trajectory_df['azim'], 326.00000000002143)
        ].empty
    assert not trajectory_df[
        np_is_close(trajectory_df['md'], 16854.0) &
        np_is_close(trajectory_df['incl'], 88.90000000000586) &
        np_is_close(trajectory_df['azim'], 322.0000000000212)
        ].empty


def test_get_not_converted_meter_trajectory(project):
    well = project.wells.find_by_name(WELL_NAME)

    assert well is not None

    trajectory_df = well.trajectory.to_df(get_converted=False)

    assert not trajectory_df.empty

    assert not trajectory_df[
        np_is_close(trajectory_df['md'], 0) &
        np_is_close(trajectory_df['incl'], 0) &
        np_is_close(trajectory_df['azim'], 0)
        ].empty
    assert not trajectory_df[
        np_is_close(trajectory_df['md'], 447.99999999999994) &
        np_is_close(trajectory_df['incl'], 0.006981317007977778) &
        np_is_close(trajectory_df['azim'], 4.324925886442234)
        ].empty
    assert not trajectory_df[
        np_is_close(trajectory_df['md'], 7735.0) &
        np_is_close(trajectory_df['incl'], 0.026179938779916666) &
        np_is_close(trajectory_df['azim'], 2.7488935718912493)
        ].empty
    assert not trajectory_df[
        np_is_close(trajectory_df['md'], 11383.0) &
        np_is_close(trajectory_df['incl'], 0.8429940287133166) &
        np_is_close(trajectory_df['azim'], 5.689773361501889)
        ].empty
    assert not trajectory_df[
        np_is_close(trajectory_df['md'], 16854.0) &
        np_is_close(trajectory_df['incl'], 1.5515977050230612) &
        np_is_close(trajectory_df['azim'], 5.619960191422111)
        ].empty


def test_get_converted_foot_trajectory(ft_project):
    well = ft_project.wells.find_by_name(WELL_NAME)

    assert well is not None

    trajectory_df = well.trajectory.to_df()

    assert not trajectory_df.empty

    assert not trajectory_df[
        np_is_close(trajectory_df['md'], 0) &
        np_is_close(trajectory_df['incl'], 0) &
        np_is_close(trajectory_df['azim'], 0)
        ].empty
    assert not trajectory_df[
        np_is_close(trajectory_df['md'], 1469.8162729658789) &
        np_is_close(trajectory_df['incl'], 0.40000000000002633) &
        np_is_close(trajectory_df['azim'], 247.80000000001635)
        ].empty
    assert not trajectory_df[
        np_is_close(trajectory_df['md'], 25377.296587926507) &
        np_is_close(trajectory_df['incl'], 1.5000000000000988) &
        np_is_close(trajectory_df['azim'], 157.50000000001032)
        ].empty
    assert not trajectory_df[
        np_is_close(trajectory_df['md'], 37345.80052493438) &
        np_is_close(trajectory_df['incl'], 48.30000000000318) &
        np_is_close(trajectory_df['azim'], 326.00000000002143)
        ].empty
    assert not trajectory_df[
        np_is_close(trajectory_df['md'], 55295.27559055117) &
        np_is_close(trajectory_df['incl'], 88.90000000000586) &
        np_is_close(trajectory_df['azim'], 322.0000000000212)
        ].empty


def test_get_not_converted_foot_trajectory(ft_project):
    well = ft_project.wells.find_by_name(WELL_NAME)

    assert well is not None

    trajectory_df = well.trajectory.to_df(get_converted=False)

    assert not trajectory_df.empty

    assert not trajectory_df[
        np_is_close(trajectory_df['md'], 0) &
        np_is_close(trajectory_df['incl'], 0) &
        np_is_close(trajectory_df['azim'], 0)
        ].empty
    assert not trajectory_df[
        np_is_close(trajectory_df['md'], 447.99999999999994) &
        np_is_close(trajectory_df['incl'], 0.006981317007977778) &
        np_is_close(trajectory_df['azim'], 4.324925886442234)
        ].empty
    assert not trajectory_df[
        np_is_close(trajectory_df['md'], 7735.0) &
        np_is_close(trajectory_df['incl'], 0.026179938779916666) &
        np_is_close(trajectory_df['azim'], 2.7488935718912493)
        ].empty
    assert not trajectory_df[
        np_is_close(trajectory_df['md'], 11383.0) &
        np_is_close(trajectory_df['incl'], 0.8429940287133166) &
        np_is_close(trajectory_df['azim'], 5.689773361501889)
        ].empty
    assert not trajectory_df[
        np_is_close(trajectory_df['md'], 16854.0) &
        np_is_close(trajectory_df['incl'], 1.5515977050230612) &
        np_is_close(trajectory_df['azim'], 5.619960191422111)
        ].empty


def test_get_converted_ftm_trajectory(ftm_project):
    well = ftm_project.wells.find_by_name(WELL_NAME)

    assert well is not None

    trajectory_df = well.trajectory.to_df()

    assert not trajectory_df.empty

    assert not trajectory_df[
        np_is_close(trajectory_df['md'], 0) &
        np_is_close(trajectory_df['incl'], 0) &
        np_is_close(trajectory_df['azim'], 0)
        ].empty
    assert not trajectory_df[
        np_is_close(trajectory_df['md'], 1469.8162729658789) &
        np_is_close(trajectory_df['incl'], 0.40000000000002633) &
        np_is_close(trajectory_df['azim'], 247.80000000001635)
        ].empty
    assert not trajectory_df[
        np_is_close(trajectory_df['md'], 25377.296587926507) &
        np_is_close(trajectory_df['incl'], 1.5000000000000988) &
        np_is_close(trajectory_df['azim'], 157.50000000001032)
        ].empty
    assert not trajectory_df[
        np_is_close(trajectory_df['md'], 37345.80052493438) &
        np_is_close(trajectory_df['incl'], 48.30000000000318) &
        np_is_close(trajectory_df['azim'], 326.00000000002143)
        ].empty
    assert not trajectory_df[
        np_is_close(trajectory_df['md'], 55295.27559055117) &
        np_is_close(trajectory_df['incl'], 88.90000000000586) &
        np_is_close(trajectory_df['azim'], 322.0000000000212)
        ].empty


def test_get_not_converted_ftm_trajectory(ftm_project):
    well = ftm_project.wells.find_by_name(WELL_NAME)

    assert well is not None

    trajectory_df = well.trajectory.to_df(get_converted=False)

    assert not trajectory_df.empty

    assert not trajectory_df[
        np_is_close(trajectory_df['md'], 0) &
        np_is_close(trajectory_df['incl'], 0) &
        np_is_close(trajectory_df['azim'], 0)
        ].empty
    assert not trajectory_df[
        np_is_close(trajectory_df['md'], 447.99999999999994) &
        np_is_close(trajectory_df['incl'], 0.006981317007977778) &
        np_is_close(trajectory_df['azim'], 4.324925886442234)
        ].empty
    assert not trajectory_df[
        np_is_close(trajectory_df['md'], 7735.0) &
        np_is_close(trajectory_df['incl'], 0.026179938779916666) &
        np_is_close(trajectory_df['azim'], 2.7488935718912493)
        ].empty
    assert not trajectory_df[
        np_is_close(trajectory_df['md'], 11383.0) &
        np_is_close(trajectory_df['incl'], 0.8429940287133166) &
        np_is_close(trajectory_df['azim'], 5.689773361501889)
        ].empty
    assert not trajectory_df[
        np_is_close(trajectory_df['md'], 16854.0) &
        np_is_close(trajectory_df['incl'], 1.5515977050230612) &
        np_is_close(trajectory_df['azim'], 5.619960191422111)
        ].empty


def test_get_converted_meter_nested_well(project):
    starred_nested_well = project.wells.find_by_name(WELL_NAME).starred_nested_well

    assert starred_nested_well is not None

    starred_nested_well_df = starred_nested_well.to_df()

    assert not starred_nested_well_df.empty

    assert np_is_close(starred_nested_well_df['xsrf_real'], 100000)
    assert np_is_close(starred_nested_well_df['ysrf_real'], 100000)
    assert not starred_nested_well_df['kb'].isnull().empty
    assert np_is_close(starred_nested_well_df['azimuth'], 325)
    assert np_is_close(starred_nested_well_df['convergence'], 1)


def test_get_not_converted_meter_nested_well(project):
    starred_nested_well = project.wells.find_by_name(WELL_NAME).starred_nested_well

    assert starred_nested_well is not None

    starred_nested_well_df = starred_nested_well.to_df(get_converted=False)

    assert not starred_nested_well_df.empty

    assert np_is_close(starred_nested_well_df['xsrf_real'], 100000)
    assert np_is_close(starred_nested_well_df['ysrf_real'], 100000)
    assert not starred_nested_well_df['kb'].isnull().empty
    assert np_is_close(starred_nested_well_df['azimuth'], 5.672320068981945)
    assert np_is_close(starred_nested_well_df['convergence'], 0.017453292519944444)


def test_get_converted_foot_nested_well(ft_project):
    starred_nested_well = ft_project.wells.find_by_name(WELL_NAME).starred_nested_well

    assert starred_nested_well is not None

    starred_nested_well_df = starred_nested_well.to_df()

    assert not starred_nested_well_df.empty

    assert np_is_close(starred_nested_well_df['xsrf_real'], 100000)
    assert np_is_close(starred_nested_well_df['ysrf_real'], 100000)
    assert not starred_nested_well_df['kb'].isnull().empty
    assert np_is_close(starred_nested_well_df['azimuth'], 325)
    assert np_is_close(starred_nested_well_df['convergence'], 1)


def test_get_not_converted_foot_nested_well(ft_project):
    starred_nested_well = ft_project.wells.find_by_name(WELL_NAME).starred_nested_well

    assert starred_nested_well is not None

    starred_nested_well_df = starred_nested_well.to_df(get_converted=False)

    assert not starred_nested_well_df.empty

    assert np_is_close(starred_nested_well_df['xsrf_real'], 100000)
    assert np_is_close(starred_nested_well_df['ysrf_real'], 100000)
    assert not starred_nested_well_df['kb'].isnull().empty
    assert np_is_close(starred_nested_well_df['azimuth'], 5.672320068981945)
    assert np_is_close(starred_nested_well_df['convergence'], 0.017453292519944444)


def test_get_converted_ftm_nested_well(ftm_project):
    starred_nested_well = ftm_project.wells.find_by_name(WELL_NAME).starred_nested_well

    assert starred_nested_well is not None

    starred_nested_well_df = starred_nested_well.to_df()

    assert not starred_nested_well_df.empty

    assert np_is_close(starred_nested_well_df['xsrf_real'], 100000)
    assert np_is_close(starred_nested_well_df['ysrf_real'], 100000)
    assert not starred_nested_well_df['kb'].isnull().empty
    assert np_is_close(starred_nested_well_df['azimuth'], 325)
    assert np_is_close(starred_nested_well_df['convergence'], 1)


def test_get_not_converted_ftm_nested_well(ftm_project):
    starred_nested_well = ftm_project.wells.find_by_name(WELL_NAME).starred_nested_well

    assert starred_nested_well is not None

    starred_nested_well_df = starred_nested_well.to_df(get_converted=False)

    assert not starred_nested_well_df.empty

    assert np_is_close(starred_nested_well_df['xsrf_real'], 100000)
    assert np_is_close(starred_nested_well_df['ysrf_real'], 100000)
    assert not starred_nested_well_df['kb'].isnull().empty
    assert np_is_close(starred_nested_well_df['azimuth'], 5.672320068981945)
    assert np_is_close(starred_nested_well_df['convergence'], 0.017453292519944444)


def test_get_converted_meter_horizon(project):
    starred_interpretation = project.wells.find_by_name(WELL_NAME).starred_interpretation
    horizon = starred_interpretation.horizons.find_by_name(HORIZON_NAME)

    assert horizon is not None

    horizon_df = horizon.to_df()

    assert 'meta' in horizon_df
    assert 'data' in horizon_df

    horizon_data_df = horizon_df['data']

    assert not horizon_data_df[
        np_is_close(horizon_data_df['md'], 0) &
        horizon_data_df['tvd'].isnull()
        ].empty
    assert not horizon_data_df[
        np_is_close(horizon_data_df['md'], 3858) &
        horizon_data_df['tvd'].isnull()
        ].empty
    assert not horizon_data_df[
        np_is_close(horizon_data_df['md'], 7452) &
        horizon_data_df['tvd'].isnull()
        ].empty
    assert not horizon_data_df[
        np_is_close(horizon_data_df['md'], 11257) &
        horizon_data_df['tvd'].isnull()
        ].empty

    assert not horizon_data_df[
        np_is_close(horizon_data_df['md'], 11288) &
        np_is_close(horizon_data_df['tvd'], 11517.76902768946)
        ].empty
    assert not horizon_data_df[
        np_is_close(horizon_data_df['md'], 13770) &
        np_is_close(horizon_data_df['tvd'], 11462.009984212762)
        ].empty
    assert not horizon_data_df[
        np_is_close(horizon_data_df['md'], 16854) &
        np_is_close(horizon_data_df['tvd'], 11263.199107699302)
        ].empty


def test_get_not_converted_meter_horizon(project):
    starred_interpretation = project.wells.find_by_name(WELL_NAME).starred_interpretation
    horizon = starred_interpretation.horizons.find_by_name(HORIZON_NAME)

    assert horizon is not None

    horizon_df = horizon.to_df(get_converted=False)

    assert 'meta' in horizon_df
    assert 'data' in horizon_df

    horizon_data_df = horizon_df['data']

    assert not horizon_data_df[
        np_is_close(horizon_data_df['md'], 0) &
        horizon_data_df['tvd'].isnull()
        ].empty
    assert not horizon_data_df[
        np_is_close(horizon_data_df['md'], 3858) &
        horizon_data_df['tvd'].isnull()
        ].empty
    assert not horizon_data_df[
        np_is_close(horizon_data_df['md'], 7452) &
        horizon_data_df['tvd'].isnull()
        ].empty
    assert not horizon_data_df[
        np_is_close(horizon_data_df['md'], 11257) &
        horizon_data_df['tvd'].isnull()
        ].empty

    assert not horizon_data_df[
        np_is_close(horizon_data_df['md'], 11288) &
        np_is_close(horizon_data_df['tvd'], 11517.76902768946)
        ].empty
    assert not horizon_data_df[
        np_is_close(horizon_data_df['md'], 13770) &
        np_is_close(horizon_data_df['tvd'], 11462.009984212762)
        ].empty
    assert not horizon_data_df[
        np_is_close(horizon_data_df['md'], 16854) &
        np_is_close(horizon_data_df['tvd'], 11263.199107699302)
        ].empty


def test_get_converted_foot_horizon(ft_project):
    starred_interpretation = ft_project.wells.find_by_name(WELL_NAME).starred_interpretation
    horizon = starred_interpretation.horizons.find_by_name(HORIZON_NAME)

    assert horizon is not None

    horizon_df = horizon.to_df()

    assert 'meta' in horizon_df
    assert 'data' in horizon_df

    horizon_data_df = horizon_df['data']

    assert not horizon_data_df[
        np_is_close(horizon_data_df['md'], 0) &
        horizon_data_df['tvd'].isnull()
        ].empty
    assert not horizon_data_df[
        np_is_close(horizon_data_df['md'], 10196.85039) &
        horizon_data_df['tvd'].isnull()
        ].empty
    assert not horizon_data_df[
        np_is_close(horizon_data_df['md'], 20134.51444) &
        horizon_data_df['tvd'].isnull()
        ].empty
    assert not horizon_data_df[
        np_is_close(horizon_data_df['md'], 30026.24672) &
        horizon_data_df['tvd'].isnull()
        ].empty

    assert not horizon_data_df[
        np_is_close(horizon_data_df['md'], 37034.12073) &
        np_is_close(horizon_data_df['tvd'], 37787.95935)
        ].empty
    assert not horizon_data_df[
        np_is_close(horizon_data_df['md'], 39714.56693) &
        np_is_close(horizon_data_df['tvd'], 37685.00777)
        ].empty
    assert not horizon_data_df[
        np_is_close(horizon_data_df['md'], 55295.27559) &
        np_is_close(horizon_data_df['tvd'], 36952.75298)
        ].empty


def test_get_not_converted_foot_horizon(ft_project):
    starred_interpretation = ft_project.wells.find_by_name(WELL_NAME).starred_interpretation
    horizon = starred_interpretation.horizons.find_by_name(HORIZON_NAME)

    assert horizon is not None

    horizon_df = horizon.to_df(get_converted=False)

    assert 'meta' in horizon_df
    assert 'data' in horizon_df

    horizon_data_df = horizon_df['data']

    assert not horizon_data_df[
        np_is_close(horizon_data_df['md'], 0) &
        horizon_data_df['tvd'].isnull()
        ].empty
    assert not horizon_data_df[
        np_is_close(horizon_data_df['md'], 3858) &
        horizon_data_df['tvd'].isnull()
        ].empty
    assert not horizon_data_df[
        np_is_close(horizon_data_df['md'], 7452) &
        horizon_data_df['tvd'].isnull()
        ].empty
    assert not horizon_data_df[
        np_is_close(horizon_data_df['md'], 11257) &
        horizon_data_df['tvd'].isnull()
        ].empty

    assert not horizon_data_df[
        np_is_close(horizon_data_df['md'], 11288) &
        np_is_close(horizon_data_df['tvd'], 11517.76902768946)
        ].empty
    assert not horizon_data_df[
        np_is_close(horizon_data_df['md'], 13770) &
        np_is_close(horizon_data_df['tvd'], 11462.009984212762)
        ].empty
    assert not horizon_data_df[
        np_is_close(horizon_data_df['md'], 16854) &
        np_is_close(horizon_data_df['tvd'], 11263.199107699302)
        ].empty


def test_get_converted_ftm_horizon(ftm_project):
    starred_interpretation = ftm_project.wells.find_by_name(WELL_NAME).starred_interpretation
    horizon = starred_interpretation.horizons.find_by_name(HORIZON_NAME)

    assert horizon is not None

    horizon_df = horizon.to_df()

    assert 'meta' in horizon_df
    assert 'data' in horizon_df

    horizon_data_df = horizon_df['data']

    assert not horizon_data_df[
        np_is_close(horizon_data_df['md'], 0) &
        horizon_data_df['tvd'].isnull()
        ].empty
    assert not horizon_data_df[
        np_is_close(horizon_data_df['md'], 10196.85039) &
        horizon_data_df['tvd'].isnull()
        ].empty
    assert not horizon_data_df[
        np_is_close(horizon_data_df['md'], 20134.51444) &
        horizon_data_df['tvd'].isnull()
        ].empty
    assert not horizon_data_df[
        np_is_close(horizon_data_df['md'], 30026.24672) &
        horizon_data_df['tvd'].isnull()
        ].empty

    assert not horizon_data_df[
        np_is_close(horizon_data_df['md'], 37034.12073) &
        np_is_close(horizon_data_df['tvd'], 37787.95935)
        ].empty
    assert not horizon_data_df[
        np_is_close(horizon_data_df['md'], 39714.56693) &
        np_is_close(horizon_data_df['tvd'], 37685.00777)
        ].empty
    assert not horizon_data_df[
        np_is_close(horizon_data_df['md'], 55295.27559) &
        np_is_close(horizon_data_df['tvd'], 36952.75298)
        ].empty


def test_get_not_converted_ftm_horizon(ftm_project):
    starred_interpretation = ftm_project.wells.find_by_name(WELL_NAME).starred_interpretation
    horizon = starred_interpretation.horizons.find_by_name(HORIZON_NAME)

    assert horizon is not None

    horizon_df = horizon.to_df(get_converted=False)

    assert 'meta' in horizon_df
    assert 'data' in horizon_df

    horizon_data_df = horizon_df['data']

    assert not horizon_data_df[
        np_is_close(horizon_data_df['md'], 0) &
        horizon_data_df['tvd'].isnull()
        ].empty
    assert not horizon_data_df[
        np_is_close(horizon_data_df['md'], 3858) &
        horizon_data_df['tvd'].isnull()
        ].empty
    assert not horizon_data_df[
        np_is_close(horizon_data_df['md'], 7452) &
        horizon_data_df['tvd'].isnull()
        ].empty
    assert not horizon_data_df[
        np_is_close(horizon_data_df['md'], 11257) &
        horizon_data_df['tvd'].isnull()
        ].empty

    assert not horizon_data_df[
        np_is_close(horizon_data_df['md'], 11288.0) &
        np_is_close(horizon_data_df['tvd'], 11517.76902768946)
        ].empty
    assert not horizon_data_df[
        np_is_close(horizon_data_df['md'], 13770.0) &
        np_is_close(horizon_data_df['tvd'], 11462.009984212762)
        ].empty
    assert not horizon_data_df[
        np_is_close(horizon_data_df['md'], 16854.0) &
        np_is_close(horizon_data_df['tvd'], 11263.199107699302)
        ].empty
