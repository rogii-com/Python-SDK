from tests.utils import np_is_close

from tests.papi_data import (
    WELL_NAME,
    HORIZON_NAME
)
from rogii_solo.base import Convertable


def test_get_converted_meter_well(project):
    well = project.wells.find_by_name(WELL_NAME)

    assert well is not None

    well_df = well.to_df()

    assert not well_df.empty

    assert np_is_close(well_df['xsrf_real'], well.xsrf_real)
    assert np_is_close(well_df['ysrf_real'], well.ysrf_real)
    assert np_is_close(well_df['kb'], Convertable.convert_z(value=well.kb, measure_units=project.measure_unit))
    assert np_is_close(well_df['azimuth'], Convertable.convert_angle(value=well.azimuth))
    assert np_is_close(well_df['convergence'], Convertable.convert_angle(value=well.convergence))


def test_get_not_converted_meter_well(project):
    well = project.wells.find_by_name(WELL_NAME)

    assert well is not None

    well_df = well.to_df(get_converted=False)

    assert not well_df.empty

    assert np_is_close(well_df['xsrf_real'], well.xsrf_real)
    assert np_is_close(well_df['ysrf_real'], well.ysrf_real)
    assert np_is_close(well_df['kb'], well.kb)
    assert np_is_close(well_df['azimuth'], well.azimuth)
    assert np_is_close(well_df['convergence'], well.convergence)


def test_get_converted_foot_well(ft_project):
    well = ft_project.wells.find_by_name(WELL_NAME)

    assert well is not None

    well_df = well.to_df()

    assert not well_df.empty

    assert np_is_close(well_df['xsrf_real'], well.xsrf_real)
    assert np_is_close(well_df['ysrf_real'], well.ysrf_real)
    assert np_is_close(well_df['kb'], Convertable.convert_z(value=well.kb, measure_units=ft_project.measure_unit))
    assert np_is_close(well_df['azimuth'], Convertable.convert_angle(value=well.azimuth))
    assert np_is_close(well_df['convergence'], Convertable.convert_angle(value=well.convergence))


def test_get_not_converted_foot_well(ft_project):
    well = ft_project.wells.find_by_name(WELL_NAME)

    assert well is not None

    well_df = well.to_df(get_converted=False)

    assert not well_df.empty

    assert np_is_close(well_df['xsrf_real'], well.xsrf_real)
    assert np_is_close(well_df['ysrf_real'], well.ysrf_real)
    assert np_is_close(well_df['kb'], well.kb)
    assert np_is_close(well_df['azimuth'], well.azimuth)
    assert np_is_close(well_df['convergence'], well.convergence)


def test_get_converted_ftm_well(ftm_project):
    well = ftm_project.wells.find_by_name(WELL_NAME)

    assert well is not None

    well_df = well.to_df()

    assert not well_df.empty

    assert np_is_close(well_df['xsrf_real'], well.xsrf_real)
    assert np_is_close(well_df['ysrf_real'], well.ysrf_real)
    assert np_is_close(well_df['kb'], Convertable.convert_z(value=well.kb, measure_units=ftm_project.measure_unit))
    assert np_is_close(well_df['azimuth'], Convertable.convert_angle(value=well.azimuth))
    assert np_is_close(well_df['convergence'], Convertable.convert_angle(value=well.convergence))


def test_get_not_converted_ftm_well(ftm_project):
    well = ftm_project.wells.find_by_name(WELL_NAME)

    assert well is not None

    well_df = well.to_df(get_converted=False)

    assert not well_df.empty

    assert np_is_close(well_df['xsrf_real'], well.xsrf_real)
    assert np_is_close(well_df['ysrf_real'], well.ysrf_real)
    assert np_is_close(well_df['kb'], well.kb)
    assert np_is_close(well_df['azimuth'], well.azimuth)
    assert np_is_close(well_df['convergence'], well.convergence)


def test_get_converted_meter_trajectory(project):
    well = project.wells.find_by_name(WELL_NAME)

    assert well is not None

    trajectory = well.trajectory
    trajectory_df = trajectory.to_df()

    assert trajectory
    assert not trajectory_df.empty
    assert len(trajectory) == len(trajectory_df.index)

    for idx, trajectory_point in enumerate(trajectory):
        assert np_is_close(trajectory_df.at[idx, 'md'], Convertable.convert_z(
            value=trajectory_point.md,
            measure_units=well.project.measure_unit
        ))
        assert np_is_close(trajectory_df.at[idx, 'incl'], Convertable.convert_angle(trajectory_point.incl))
        assert np_is_close(trajectory_df.at[idx, 'azim'], Convertable.convert_angle(trajectory_point.azim))


def test_get_not_converted_meter_trajectory(project):
    well = project.wells.find_by_name(WELL_NAME)

    assert well is not None

    trajectory = well.trajectory
    trajectory_df = trajectory.to_df(get_converted=False)

    assert trajectory
    assert not trajectory_df.empty
    assert len(trajectory) == len(trajectory_df.index)

    for idx, trajectory_point in enumerate(trajectory):
        assert np_is_close(trajectory_df.at[idx, 'md'], trajectory_point.md)
        assert np_is_close(trajectory_df.at[idx, 'incl'], trajectory_point.incl)
        assert np_is_close(trajectory_df.at[idx, 'azim'], trajectory_point.azim)


def test_get_converted_foot_trajectory(ft_project):
    well = ft_project.wells.find_by_name(WELL_NAME)

    assert well is not None

    trajectory = well.trajectory
    trajectory_df = trajectory.to_df()

    assert trajectory
    assert not trajectory_df.empty
    assert len(trajectory) == len(trajectory_df.index)

    for idx, trajectory_point in enumerate(trajectory):
        assert np_is_close(trajectory_df.at[idx, 'md'], Convertable.convert_z(
            value=trajectory_point.md,
            measure_units=well.project.measure_unit
        ))
        assert np_is_close(trajectory_df.at[idx, 'incl'], Convertable.convert_angle(trajectory_point.incl))
        assert np_is_close(trajectory_df.at[idx, 'azim'], Convertable.convert_angle(trajectory_point.azim))


def test_get_not_converted_foot_trajectory(ft_project):
    well = ft_project.wells.find_by_name(WELL_NAME)

    assert well is not None

    trajectory = well.trajectory
    trajectory_df = trajectory.to_df(get_converted=False)

    assert trajectory
    assert not trajectory_df.empty
    assert len(trajectory) == len(trajectory_df.index)

    for idx, trajectory_point in enumerate(trajectory):
        assert np_is_close(trajectory_df.at[idx, 'md'], trajectory_point.md)
        assert np_is_close(trajectory_df.at[idx, 'incl'], trajectory_point.incl)
        assert np_is_close(trajectory_df.at[idx, 'azim'], trajectory_point.azim)


def test_get_converted_ftm_trajectory(ftm_project):
    well = ftm_project.wells.find_by_name(WELL_NAME)

    assert well is not None

    trajectory = well.trajectory
    trajectory_df = trajectory.to_df()

    assert trajectory
    assert not trajectory_df.empty
    assert len(trajectory) == len(trajectory_df.index)

    for idx, trajectory_point in enumerate(trajectory):
        assert np_is_close(trajectory_df.at[idx, 'md'], Convertable.convert_z(
            value=trajectory_point.md,
            measure_units=well.project.measure_unit
        ))
        assert np_is_close(trajectory_df.at[idx, 'incl'], Convertable.convert_angle(trajectory_point.incl))
        assert np_is_close(trajectory_df.at[idx, 'azim'], Convertable.convert_angle(trajectory_point.azim))


def test_get_not_converted_ftm_trajectory(ftm_project):
    well = ftm_project.wells.find_by_name(WELL_NAME)

    assert well is not None

    trajectory = well.trajectory
    trajectory_df = trajectory.to_df(get_converted=False)

    assert trajectory
    assert not trajectory_df.empty
    assert len(trajectory) == len(trajectory_df.index)

    for idx, trajectory_point in enumerate(trajectory):
        assert np_is_close(trajectory_df.at[idx, 'md'], trajectory_point.md)
        assert np_is_close(trajectory_df.at[idx, 'incl'], trajectory_point.incl)
        assert np_is_close(trajectory_df.at[idx, 'azim'], trajectory_point.azim)


def test_get_converted_meter_nested_well(project):
    starred_nested_well = project.wells.find_by_name(WELL_NAME).starred_nested_well

    assert starred_nested_well is not None

    starred_nested_well_df = starred_nested_well.to_df()

    assert not starred_nested_well_df.empty

    assert np_is_close(starred_nested_well_df['xsrf_real'], starred_nested_well.xsrf_real)
    assert np_is_close(starred_nested_well_df['ysrf_real'], starred_nested_well.ysrf_real)
    assert not starred_nested_well_df['kb'].isnull().empty
    assert np_is_close(
        starred_nested_well_df['azimuth'],
        Convertable.convert_angle(value=starred_nested_well.azimuth)
    )
    assert np_is_close(
        starred_nested_well_df['convergence'],
        Convertable.convert_angle(value=starred_nested_well.convergence)
    )


def test_get_not_converted_meter_nested_well(project):
    starred_nested_well = project.wells.find_by_name(WELL_NAME).starred_nested_well

    assert starred_nested_well is not None

    starred_nested_well_df = starred_nested_well.to_df(get_converted=False)

    assert not starred_nested_well_df.empty

    assert np_is_close(starred_nested_well_df['xsrf_real'], starred_nested_well.xsrf_real)
    assert np_is_close(starred_nested_well_df['ysrf_real'], starred_nested_well.ysrf_real)
    assert not starred_nested_well_df['kb'].isnull().empty
    assert np_is_close(starred_nested_well_df['azimuth'], starred_nested_well.azimuth)
    assert np_is_close(starred_nested_well_df['convergence'], starred_nested_well.convergence)


def test_get_converted_foot_nested_well(ft_project):
    starred_nested_well = ft_project.wells.find_by_name(WELL_NAME).starred_nested_well

    assert starred_nested_well is not None

    starred_nested_well_df = starred_nested_well.to_df()

    assert not starred_nested_well_df.empty

    assert np_is_close(starred_nested_well_df['xsrf_real'], starred_nested_well.xsrf_real)
    assert np_is_close(starred_nested_well_df['ysrf_real'], starred_nested_well.ysrf_real)
    assert not starred_nested_well_df['kb'].isnull().empty
    assert np_is_close(
        starred_nested_well_df['azimuth'],
        Convertable.convert_angle(value=starred_nested_well.azimuth)
    )
    assert np_is_close(
        starred_nested_well_df['convergence'],
        Convertable.convert_angle(value=starred_nested_well.convergence)
    )


def test_get_not_converted_foot_nested_well(ft_project):
    starred_nested_well = ft_project.wells.find_by_name(WELL_NAME).starred_nested_well

    assert starred_nested_well is not None

    starred_nested_well_df = starred_nested_well.to_df(get_converted=False)

    assert not starred_nested_well_df.empty

    assert np_is_close(starred_nested_well_df['xsrf_real'], starred_nested_well.xsrf_real)
    assert np_is_close(starred_nested_well_df['ysrf_real'], starred_nested_well.ysrf_real)
    assert not starred_nested_well_df['kb'].isnull().empty
    assert np_is_close(starred_nested_well_df['azimuth'], starred_nested_well.azimuth)
    assert np_is_close(starred_nested_well_df['convergence'], starred_nested_well.convergence)


def test_get_converted_ftm_nested_well(ftm_project):
    starred_nested_well = ftm_project.wells.find_by_name(WELL_NAME).starred_nested_well

    assert starred_nested_well is not None

    starred_nested_well_df = starred_nested_well.to_df()

    assert not starred_nested_well_df.empty

    assert np_is_close(starred_nested_well_df['xsrf_real'], starred_nested_well.xsrf_real)
    assert np_is_close(starred_nested_well_df['ysrf_real'], starred_nested_well.ysrf_real)
    assert not starred_nested_well_df['kb'].isnull().empty
    assert np_is_close(
        starred_nested_well_df['azimuth'],
        Convertable.convert_angle(value=starred_nested_well.azimuth)
    )
    assert np_is_close(
        starred_nested_well_df['convergence'],
        Convertable.convert_angle(value=starred_nested_well.convergence)
    )


def test_get_not_converted_ftm_nested_well(ftm_project):
    starred_nested_well = ftm_project.wells.find_by_name(WELL_NAME).starred_nested_well

    assert starred_nested_well is not None

    starred_nested_well_df = starred_nested_well.to_df(get_converted=False)

    assert not starred_nested_well_df.empty

    assert np_is_close(starred_nested_well_df['xsrf_real'], starred_nested_well.xsrf_real)
    assert np_is_close(starred_nested_well_df['ysrf_real'], starred_nested_well.ysrf_real)
    assert not starred_nested_well_df['kb'].isnull().empty
    assert np_is_close(starred_nested_well_df['azimuth'], starred_nested_well.azimuth)
    assert np_is_close(starred_nested_well_df['convergence'], starred_nested_well.convergence)


def test_get_converted_meter_horizon(project):
    starred_interpretation = project.wells.find_by_name(WELL_NAME).starred_interpretation
    horizon = starred_interpretation.horizons.find_by_name(HORIZON_NAME)

    assert horizon is not None

    horizon_data = horizon.to_dict(get_converted=False)
    horizon_df = horizon.to_df()

    assert 'meta' in horizon_df
    assert 'points' in horizon_df

    points = horizon_data['points']
    points_df = horizon_df['points']

    assert len(points) == len(points_df.index)

    measure_units = horizon.interpretation.well.project.measure_unit

    for idx, horizon_trajectory_point in enumerate(points):
        assert np_is_close(
            points_df.at[idx, 'md'],
            Convertable.convert_z(value=horizon_trajectory_point['md'], measure_units=measure_units)
        )
        assert np_is_close(
            points_df.at[idx, 'tvd'],
            Convertable.convert_z(value=horizon_trajectory_point['tvd'], measure_units=measure_units)
        )


def test_get_not_converted_meter_horizon(project):
    starred_interpretation = project.wells.find_by_name(WELL_NAME).starred_interpretation
    horizon = starred_interpretation.horizons.find_by_name(HORIZON_NAME)

    assert horizon is not None

    horizon_data = horizon.to_dict(get_converted=False)
    horizon_df = horizon.to_df(get_converted=False)

    assert 'meta' in horizon_df
    assert 'points' in horizon_df

    points = horizon_data['points']
    points_df = horizon_df['points']

    assert len(points) == len(points_df.index)

    for idx, horizon_trajectory_point in enumerate(points):
        assert np_is_close(points_df.at[idx, 'md'], horizon_trajectory_point['md'])
        assert np_is_close(points_df.at[idx, 'tvd'], horizon_trajectory_point['tvd'])


def test_get_converted_foot_horizon(ft_project):
    starred_interpretation = ft_project.wells.find_by_name(WELL_NAME).starred_interpretation
    horizon = starred_interpretation.horizons.find_by_name(HORIZON_NAME)

    assert horizon is not None

    horizon_data = horizon.to_dict(get_converted=False)
    horizon_df = horizon.to_df()

    assert 'meta' in horizon_df
    assert 'points' in horizon_df

    points = horizon_data['points']
    points_df = horizon_df['points']

    assert len(points) == len(points_df.index)

    measure_units = horizon.interpretation.well.project.measure_unit

    for idx, horizon_trajectory_point in enumerate(points):
        assert np_is_close(
            points_df.at[idx, 'md'],
            Convertable.convert_z(value=horizon_trajectory_point['md'], measure_units=measure_units)
        )
        assert np_is_close(
            points_df.at[idx, 'tvd'],
            Convertable.convert_z(value=horizon_trajectory_point['tvd'], measure_units=measure_units)
        )


def test_get_not_converted_foot_horizon(ft_project):
    starred_interpretation = ft_project.wells.find_by_name(WELL_NAME).starred_interpretation
    horizon = starred_interpretation.horizons.find_by_name(HORIZON_NAME)

    assert horizon is not None

    horizon_data = horizon.to_dict(get_converted=False)
    horizon_df = horizon.to_df(get_converted=False)

    assert 'meta' in horizon_df
    assert 'points' in horizon_df

    points = horizon_data['points']
    points_df = horizon_df['points']

    assert len(points) == len(points_df.index)

    for idx, horizon_trajectory_point in enumerate(points):
        assert np_is_close(points_df.at[idx, 'md'], horizon_trajectory_point['md'])
        assert np_is_close(points_df.at[idx, 'tvd'], horizon_trajectory_point['tvd'])


def test_get_converted_ftm_horizon(ftm_project):
    starred_interpretation = ftm_project.wells.find_by_name(WELL_NAME).starred_interpretation
    horizon = starred_interpretation.horizons.find_by_name(HORIZON_NAME)

    assert horizon is not None

    horizon_data = horizon.to_dict(get_converted=False)
    horizon_df = horizon.to_df()

    assert 'meta' in horizon_df
    assert 'points' in horizon_df

    points = horizon_data['points']
    points_df = horizon_df['points']

    assert len(points) == len(points_df.index)

    measure_units = horizon.interpretation.well.project.measure_unit

    for idx, horizon_trajectory_point in enumerate(points):
        assert np_is_close(
            points_df.at[idx, 'md'],
            Convertable.convert_z(value=horizon_trajectory_point['md'], measure_units=measure_units)
        )
        assert np_is_close(
            points_df.at[idx, 'tvd'],
            Convertable.convert_z(value=horizon_trajectory_point['tvd'], measure_units=measure_units)
        )


def test_get_not_converted_ftm_horizon(ftm_project):
    starred_interpretation = ftm_project.wells.find_by_name(WELL_NAME).starred_interpretation
    horizon = starred_interpretation.horizons.find_by_name(HORIZON_NAME)

    assert horizon is not None

    horizon_data = horizon.to_dict(get_converted=False)
    horizon_df = horizon.to_df(get_converted=False)

    assert 'meta' in horizon_df
    assert 'points' in horizon_df

    points = horizon_data['points']
    points_df = horizon_df['points']

    assert len(points) == len(points_df.index)

    for idx, horizon_trajectory_point in enumerate(points):
        assert np_is_close(points_df.at[idx, 'md'], horizon_trajectory_point['md'])
        assert np_is_close(points_df.at[idx, 'tvd'], horizon_trajectory_point['tvd'])
