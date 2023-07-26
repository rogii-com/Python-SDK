from rogii_solo.base import Convertible
from tests.papi_data import (
    EARTH_MODEL_NAME,
    HORIZON_NAME,
    LOG_NAME,
    TYPEWELL_NAME,
    WELL_NAME,
)
from tests.utils import np_is_close


def test_get_converted_meter_well(project):
    well = project.wells.find_by_name(WELL_NAME)

    assert well is not None

    well_df = well.to_df()

    assert not well_df.empty

    assert np_is_close(
        well_df['xsrf'],
        Convertible.convert_xy(value=well.xsrf, measure_units=project.measure_unit, force_to_meters=True),
    )
    assert np_is_close(
        well_df['ysrf'],
        Convertible.convert_xy(value=well.ysrf, measure_units=project.measure_unit, force_to_meters=True),
    )
    assert np_is_close(well_df['kb'], Convertible.convert_z(value=well.kb, measure_units=project.measure_unit))
    assert np_is_close(well_df['azimuth'], Convertible.convert_angle(well.azimuth))
    assert np_is_close(well_df['convergence'], Convertible.convert_angle(well.convergence))
    assert np_is_close(
        well_df['tie_in_tvd'], Convertible.convert_z(value=well.tie_in_tvd, measure_units=project.measure_unit)
    )
    assert np_is_close(
        well_df['tie_in_ns'], Convertible.convert_xy(value=well.tie_in_ns, measure_units=project.measure_unit)
    )
    assert np_is_close(
        well_df['tie_in_ew'], Convertible.convert_xy(value=well.tie_in_ew, measure_units=project.measure_unit)
    )


def test_get_not_converted_meter_well(project):
    well = project.wells.find_by_name(WELL_NAME)

    assert well is not None

    well_df = well.to_df(get_converted=False)

    assert not well_df.empty

    assert np_is_close(well_df['xsrf'], well.xsrf)
    assert np_is_close(well_df['ysrf'], well.ysrf)
    assert np_is_close(well_df['kb'], well.kb)
    assert np_is_close(well_df['azimuth'], well.azimuth)
    assert np_is_close(well_df['convergence'], well.convergence)
    assert np_is_close(well_df['tie_in_tvd'], well.tie_in_tvd)
    assert np_is_close(well_df['tie_in_ns'], well.tie_in_ns)
    assert np_is_close(well_df['tie_in_ew'], well.tie_in_ew)


def test_get_converted_foot_well(ft_project):
    well = ft_project.wells.find_by_name(WELL_NAME)

    assert well is not None

    well_df = well.to_df()

    assert not well_df.empty

    assert np_is_close(
        well_df['xsrf'],
        Convertible.convert_xy(value=well.xsrf, measure_units=ft_project.measure_unit, force_to_meters=True),
    )
    assert np_is_close(
        well_df['ysrf'],
        Convertible.convert_xy(value=well.ysrf, measure_units=ft_project.measure_unit, force_to_meters=True),
    )
    assert np_is_close(well_df['kb'], Convertible.convert_z(value=well.kb, measure_units=ft_project.measure_unit))
    assert np_is_close(well_df['azimuth'], Convertible.convert_angle(well.azimuth))
    assert np_is_close(well_df['convergence'], Convertible.convert_angle(well.convergence))
    assert np_is_close(
        well_df['tie_in_tvd'], Convertible.convert_z(value=well.tie_in_tvd, measure_units=ft_project.measure_unit)
    )
    assert np_is_close(
        well_df['tie_in_ns'], Convertible.convert_xy(value=well.tie_in_ns, measure_units=ft_project.measure_unit)
    )
    assert np_is_close(
        well_df['tie_in_ew'], Convertible.convert_xy(value=well.tie_in_ew, measure_units=ft_project.measure_unit)
    )


def test_get_not_converted_foot_well(ft_project):
    well = ft_project.wells.find_by_name(WELL_NAME)

    assert well is not None

    well_df = well.to_df(get_converted=False)

    assert not well_df.empty

    assert np_is_close(well_df['xsrf'], well.xsrf)
    assert np_is_close(well_df['ysrf'], well.ysrf)
    assert np_is_close(well_df['kb'], well.kb)
    assert np_is_close(well_df['azimuth'], well.azimuth)
    assert np_is_close(well_df['convergence'], well.convergence)
    assert np_is_close(well_df['tie_in_tvd'], well.tie_in_tvd)
    assert np_is_close(well_df['tie_in_ns'], well.tie_in_ns)
    assert np_is_close(well_df['tie_in_ew'], well.tie_in_ew)


def test_get_converted_ftm_well(ftm_project):
    well = ftm_project.wells.find_by_name(WELL_NAME)

    assert well is not None

    well_df = well.to_df()

    assert not well_df.empty

    assert np_is_close(
        well_df['xsrf'],
        Convertible.convert_xy(value=well.xsrf, measure_units=ftm_project.measure_unit, force_to_meters=True),
    )
    assert np_is_close(
        well_df['ysrf'],
        Convertible.convert_xy(value=well.ysrf, measure_units=ftm_project.measure_unit, force_to_meters=True),
    )
    assert np_is_close(well_df['kb'], Convertible.convert_z(value=well.kb, measure_units=ftm_project.measure_unit))
    assert np_is_close(well_df['azimuth'], Convertible.convert_angle(well.azimuth))
    assert np_is_close(well_df['convergence'], Convertible.convert_angle(well.convergence))
    assert np_is_close(
        well_df['tie_in_tvd'], Convertible.convert_z(value=well.tie_in_tvd, measure_units=ftm_project.measure_unit)
    )
    assert np_is_close(
        well_df['tie_in_ns'], Convertible.convert_xy(value=well.tie_in_ns, measure_units=ftm_project.measure_unit)
    )
    assert np_is_close(
        well_df['tie_in_ew'], Convertible.convert_xy(value=well.tie_in_ew, measure_units=ftm_project.measure_unit)
    )


def test_get_not_converted_ftm_well(ftm_project):
    well = ftm_project.wells.find_by_name(WELL_NAME)

    assert well is not None

    well_df = well.to_df(get_converted=False)

    assert not well_df.empty

    assert np_is_close(well_df['xsrf'], well.xsrf)
    assert np_is_close(well_df['ysrf'], well.ysrf)
    assert np_is_close(well_df['kb'], well.kb)
    assert np_is_close(well_df['azimuth'], well.azimuth)
    assert np_is_close(well_df['convergence'], well.convergence)
    assert np_is_close(well_df['tie_in_tvd'], well.tie_in_tvd)
    assert np_is_close(well_df['tie_in_ns'], well.tie_in_ns)
    assert np_is_close(well_df['tie_in_ew'], well.tie_in_ew)


def test_get_converted_meter_well_trajectory(project):
    well = project.wells.find_by_name(WELL_NAME)

    assert well is not None

    trajectory = well.trajectory
    trajectory_df = trajectory.to_df()

    assert trajectory
    assert not trajectory_df.empty
    assert len(trajectory) == len(trajectory_df.index)

    for idx, trajectory_point in enumerate(trajectory):
        assert np_is_close(
            trajectory_df.at[idx, 'md'],
            Convertible.convert_z(value=trajectory_point.md, measure_units=well.project.measure_unit),
        )
        assert np_is_close(trajectory_df.at[idx, 'incl'], Convertible.convert_angle(trajectory_point.incl))
        assert np_is_close(trajectory_df.at[idx, 'azim'], Convertible.convert_angle(trajectory_point.azim))


def test_get_not_converted_meter_well_trajectory(project):
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


def test_get_converted_foot_well_trajectory(ft_project):
    well = ft_project.wells.find_by_name(WELL_NAME)

    assert well is not None

    trajectory = well.trajectory
    trajectory_df = trajectory.to_df()

    assert trajectory
    assert not trajectory_df.empty
    assert len(trajectory) == len(trajectory_df.index)

    for idx, trajectory_point in enumerate(trajectory):
        assert np_is_close(
            trajectory_df.at[idx, 'md'],
            Convertible.convert_z(value=trajectory_point.md, measure_units=well.project.measure_unit),
        )
        assert np_is_close(trajectory_df.at[idx, 'incl'], Convertible.convert_angle(trajectory_point.incl))
        assert np_is_close(trajectory_df.at[idx, 'azim'], Convertible.convert_angle(trajectory_point.azim))


def test_get_not_converted_foot_well_trajectory(ft_project):
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


def test_get_converted_ftm_well_trajectory(ftm_project):
    well = ftm_project.wells.find_by_name(WELL_NAME)

    assert well is not None

    trajectory = well.trajectory
    trajectory_df = trajectory.to_df()

    assert trajectory
    assert not trajectory_df.empty
    assert len(trajectory) == len(trajectory_df.index)

    for idx, trajectory_point in enumerate(trajectory):
        assert np_is_close(
            trajectory_df.at[idx, 'md'],
            Convertible.convert_z(value=trajectory_point.md, measure_units=well.project.measure_unit),
        )
        assert np_is_close(trajectory_df.at[idx, 'incl'], Convertible.convert_angle(trajectory_point.incl))
        assert np_is_close(trajectory_df.at[idx, 'azim'], Convertible.convert_angle(trajectory_point.azim))


def test_get_not_converted_ftm_well_trajectory(ftm_project):
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

    assert np_is_close(
        starred_nested_well_df['xsrf'],
        Convertible.convert_xy(
            value=starred_nested_well.xsrf, measure_units=project.measure_unit, force_to_meters=True
        ),
    )
    assert np_is_close(
        starred_nested_well_df['ysrf'],
        Convertible.convert_xy(
            value=starred_nested_well.ysrf, measure_units=project.measure_unit, force_to_meters=True
        ),
    )
    assert np_is_close(
        starred_nested_well_df['kb'],
        Convertible.convert_z(value=starred_nested_well.kb, measure_units=project.measure_unit),
    )
    assert np_is_close(starred_nested_well_df['azimuth'], Convertible.convert_angle(starred_nested_well.azimuth))
    assert np_is_close(
        starred_nested_well_df['convergence'], Convertible.convert_angle(starred_nested_well.convergence)
    )
    assert np_is_close(
        starred_nested_well_df['tie_in_tvd'],
        Convertible.convert_z(value=starred_nested_well.tie_in_tvd, measure_units=project.measure_unit),
    )
    assert np_is_close(
        starred_nested_well_df['tie_in_ns'],
        Convertible.convert_xy(value=starred_nested_well.tie_in_ns, measure_units=project.measure_unit),
    )
    assert np_is_close(
        starred_nested_well_df['tie_in_ew'],
        Convertible.convert_xy(value=starred_nested_well.tie_in_ew, measure_units=project.measure_unit),
    )


def test_get_not_converted_meter_nested_well(project):
    starred_nested_well = project.wells.find_by_name(WELL_NAME).starred_nested_well

    assert starred_nested_well is not None

    starred_nested_well_df = starred_nested_well.to_df(get_converted=False)

    assert not starred_nested_well_df.empty

    assert np_is_close(starred_nested_well_df['xsrf'], starred_nested_well.xsrf)
    assert np_is_close(starred_nested_well_df['ysrf'], starred_nested_well.ysrf)
    assert np_is_close(starred_nested_well_df['kb'], starred_nested_well.kb)
    assert np_is_close(starred_nested_well_df['azimuth'], starred_nested_well.azimuth)
    assert np_is_close(starred_nested_well_df['convergence'], starred_nested_well.convergence)
    assert np_is_close(starred_nested_well_df['tie_in_tvd'], starred_nested_well.tie_in_tvd)
    assert np_is_close(starred_nested_well_df['tie_in_ns'], starred_nested_well.tie_in_ns)
    assert np_is_close(starred_nested_well_df['tie_in_ew'], starred_nested_well.tie_in_ew)


def test_get_converted_foot_nested_well(ft_project):
    starred_nested_well = ft_project.wells.find_by_name(WELL_NAME).starred_nested_well

    assert starred_nested_well is not None

    starred_nested_well_df = starred_nested_well.to_df()

    assert not starred_nested_well_df.empty

    assert np_is_close(
        starred_nested_well_df['xsrf'],
        Convertible.convert_xy(
            value=starred_nested_well.xsrf, measure_units=ft_project.measure_unit, force_to_meters=True
        ),
    )
    assert np_is_close(
        starred_nested_well_df['ysrf'],
        Convertible.convert_xy(
            value=starred_nested_well.ysrf, measure_units=ft_project.measure_unit, force_to_meters=True
        ),
    )
    assert np_is_close(
        starred_nested_well_df['kb'],
        Convertible.convert_z(value=starred_nested_well.kb, measure_units=ft_project.measure_unit),
    )
    assert np_is_close(starred_nested_well_df['azimuth'], Convertible.convert_angle(starred_nested_well.azimuth))
    assert np_is_close(
        starred_nested_well_df['convergence'], Convertible.convert_angle(starred_nested_well.convergence)
    )
    assert np_is_close(
        starred_nested_well_df['tie_in_tvd'],
        Convertible.convert_z(value=starred_nested_well.tie_in_tvd, measure_units=ft_project.measure_unit),
    )
    assert np_is_close(
        starred_nested_well_df['tie_in_ns'],
        Convertible.convert_xy(value=starred_nested_well.tie_in_ns, measure_units=ft_project.measure_unit),
    )
    assert np_is_close(
        starred_nested_well_df['tie_in_ew'],
        Convertible.convert_xy(value=starred_nested_well.tie_in_ew, measure_units=ft_project.measure_unit),
    )


def test_get_not_converted_foot_nested_well(ft_project):
    starred_nested_well = ft_project.wells.find_by_name(WELL_NAME).starred_nested_well

    assert starred_nested_well is not None

    starred_nested_well_df = starred_nested_well.to_df(get_converted=False)

    assert not starred_nested_well_df.empty

    assert np_is_close(starred_nested_well_df['xsrf'], starred_nested_well.xsrf)
    assert np_is_close(starred_nested_well_df['ysrf'], starred_nested_well.ysrf)
    assert np_is_close(starred_nested_well_df['kb'], starred_nested_well.kb)
    assert np_is_close(starred_nested_well_df['azimuth'], starred_nested_well.azimuth)
    assert np_is_close(starred_nested_well_df['convergence'], starred_nested_well.convergence)
    assert np_is_close(starred_nested_well_df['tie_in_tvd'], starred_nested_well.tie_in_tvd)
    assert np_is_close(starred_nested_well_df['tie_in_ns'], starred_nested_well.tie_in_ns)
    assert np_is_close(starred_nested_well_df['tie_in_ew'], starred_nested_well.tie_in_ew)


def test_get_converted_ftm_nested_well(ftm_project):
    starred_nested_well = ftm_project.wells.find_by_name(WELL_NAME).starred_nested_well

    assert starred_nested_well is not None

    starred_nested_well_df = starred_nested_well.to_df()

    assert not starred_nested_well_df.empty

    assert np_is_close(
        starred_nested_well_df['xsrf'],
        Convertible.convert_xy(
            value=starred_nested_well.xsrf, measure_units=ftm_project.measure_unit, force_to_meters=True
        ),
    )
    assert np_is_close(
        starred_nested_well_df['ysrf'],
        Convertible.convert_xy(
            value=starred_nested_well.ysrf, measure_units=ftm_project.measure_unit, force_to_meters=True
        ),
    )
    assert np_is_close(
        starred_nested_well_df['kb'],
        Convertible.convert_z(value=starred_nested_well.kb, measure_units=ftm_project.measure_unit),
    )
    assert np_is_close(starred_nested_well_df['azimuth'], Convertible.convert_angle(starred_nested_well.azimuth))
    assert np_is_close(
        starred_nested_well_df['convergence'], Convertible.convert_angle(starred_nested_well.convergence)
    )
    assert np_is_close(
        starred_nested_well_df['tie_in_tvd'],
        Convertible.convert_z(value=starred_nested_well.tie_in_tvd, measure_units=ftm_project.measure_unit),
    )
    assert np_is_close(
        starred_nested_well_df['tie_in_ns'],
        Convertible.convert_xy(value=starred_nested_well.tie_in_ns, measure_units=ftm_project.measure_unit),
    )
    assert np_is_close(
        starred_nested_well_df['tie_in_ew'],
        Convertible.convert_xy(value=starred_nested_well.tie_in_ew, measure_units=ftm_project.measure_unit),
    )


def test_get_not_converted_ftm_nested_well(ftm_project):
    starred_nested_well = ftm_project.wells.find_by_name(WELL_NAME).starred_nested_well

    assert starred_nested_well is not None

    starred_nested_well_df = starred_nested_well.to_df(get_converted=False)

    assert not starred_nested_well_df.empty

    assert np_is_close(starred_nested_well_df['xsrf'], starred_nested_well.xsrf)
    assert np_is_close(starred_nested_well_df['ysrf'], starred_nested_well.ysrf)
    assert np_is_close(starred_nested_well_df['kb'], starred_nested_well.kb)
    assert np_is_close(starred_nested_well_df['azimuth'], starred_nested_well.azimuth)
    assert np_is_close(starred_nested_well_df['convergence'], starred_nested_well.convergence)
    assert np_is_close(starred_nested_well_df['tie_in_tvd'], starred_nested_well.tie_in_tvd)
    assert np_is_close(starred_nested_well_df['tie_in_ns'], starred_nested_well.tie_in_ns)
    assert np_is_close(starred_nested_well_df['tie_in_ew'], starred_nested_well.tie_in_ew)


def test_get_converted_meter_horizon(project):
    starred_interpretation = project.wells.find_by_name(WELL_NAME).starred_interpretation
    horizon = starred_interpretation.horizons.find_by_name(HORIZON_NAME)

    assert horizon is not None

    horizon_data = horizon.to_dict()
    horizon_df = horizon.to_df()

    assert 'uuid' in horizon_data
    assert 'name' in horizon_data
    assert horizon_data['uuid'] == horizon_df.at[0, 'uuid']
    assert horizon_data['name'] == horizon_df.at[0, 'name']

    points = horizon.points
    points_df = points.to_df()

    assert len(points) == len(points_df.index)

    measure_units = horizon.interpretation.well.project.measure_unit

    for idx, horizon_trajectory_point in enumerate(points):
        assert np_is_close(
            points_df.at[idx, 'md'],
            Convertible.convert_z(value=horizon_trajectory_point.md, measure_units=measure_units),
        )
        assert np_is_close(
            points_df.at[idx, 'tvd'],
            Convertible.convert_z(value=horizon_trajectory_point.tvd, measure_units=measure_units),
        )


def test_get_not_converted_meter_horizon(project):
    starred_interpretation = project.wells.find_by_name(WELL_NAME).starred_interpretation
    horizon = starred_interpretation.horizons.find_by_name(HORIZON_NAME)

    assert horizon is not None

    horizon_data = horizon.to_dict()
    horizon_df = horizon.to_df()

    assert 'uuid' in horizon_data
    assert 'name' in horizon_data
    assert horizon_data['uuid'] == horizon_df.at[0, 'uuid']
    assert horizon_data['name'] == horizon_df.at[0, 'name']

    points = horizon.points
    points_df = points.to_df(get_converted=False)

    assert len(points) == len(points_df.index)

    for idx, horizon_trajectory_point in enumerate(points):
        assert np_is_close(points_df.at[idx, 'md'], horizon_trajectory_point.md)
        assert np_is_close(points_df.at[idx, 'tvd'], horizon_trajectory_point.tvd)


def test_get_converted_foot_horizon(ft_project):
    starred_interpretation = ft_project.wells.find_by_name(WELL_NAME).starred_interpretation
    horizon = starred_interpretation.horizons.find_by_name(HORIZON_NAME)

    assert horizon is not None

    horizon_data = horizon.to_dict()
    horizon_df = horizon.to_df()

    assert 'uuid' in horizon_data
    assert 'name' in horizon_data
    assert horizon_data['uuid'] == horizon_df.at[0, 'uuid']
    assert horizon_data['name'] == horizon_df.at[0, 'name']

    points = horizon.points
    points_df = points.to_df()

    assert len(points) == len(points_df.index)

    measure_units = horizon.interpretation.well.project.measure_unit

    for idx, horizon_trajectory_point in enumerate(points):
        assert np_is_close(
            points_df.at[idx, 'md'],
            Convertible.convert_z(value=horizon_trajectory_point.md, measure_units=measure_units),
        )
        assert np_is_close(
            points_df.at[idx, 'tvd'],
            Convertible.convert_z(value=horizon_trajectory_point.tvd, measure_units=measure_units),
        )


def test_get_not_converted_foot_horizon(ft_project):
    starred_interpretation = ft_project.wells.find_by_name(WELL_NAME).starred_interpretation
    horizon = starred_interpretation.horizons.find_by_name(HORIZON_NAME)

    assert horizon is not None

    horizon_data = horizon.to_dict()
    horizon_df = horizon.to_df()

    assert 'uuid' in horizon_data
    assert 'name' in horizon_data
    assert horizon_data['uuid'] == horizon_df.at[0, 'uuid']
    assert horizon_data['name'] == horizon_df.at[0, 'name']

    points = horizon.points
    points_df = points.to_df(get_converted=False)

    assert len(points) == len(points_df.index)

    for idx, horizon_trajectory_point in enumerate(points):
        assert np_is_close(points_df.at[idx, 'md'], horizon_trajectory_point.md)
        assert np_is_close(points_df.at[idx, 'tvd'], horizon_trajectory_point.tvd)


def test_get_converted_ftm_horizon(ftm_project):
    starred_interpretation = ftm_project.wells.find_by_name(WELL_NAME).starred_interpretation
    horizon = starred_interpretation.horizons.find_by_name(HORIZON_NAME)

    assert horizon is not None

    horizon_data = horizon.to_dict()
    horizon_df = horizon.to_df()

    assert 'uuid' in horizon_data
    assert 'name' in horizon_data
    assert horizon_data['uuid'] == horizon_df.at[0, 'uuid']
    assert horizon_data['name'] == horizon_df.at[0, 'name']

    points = horizon.points
    points_df = points.to_df()

    assert len(points) == len(points_df.index)

    measure_units = horizon.interpretation.well.project.measure_unit

    for idx, horizon_trajectory_point in enumerate(points):
        assert np_is_close(
            points_df.at[idx, 'md'],
            Convertible.convert_z(value=horizon_trajectory_point.md, measure_units=measure_units),
        )
        assert np_is_close(
            points_df.at[idx, 'tvd'],
            Convertible.convert_z(value=horizon_trajectory_point.tvd, measure_units=measure_units),
        )


def test_get_not_converted_ftm_horizon(ftm_project):
    starred_interpretation = ftm_project.wells.find_by_name(WELL_NAME).starred_interpretation
    horizon = starred_interpretation.horizons.find_by_name(HORIZON_NAME)

    assert horizon is not None

    horizon_data = horizon.to_dict()
    horizon_df = horizon.to_df()

    assert 'uuid' in horizon_data
    assert 'name' in horizon_data
    assert horizon_data['uuid'] == horizon_df.at[0, 'uuid']
    assert horizon_data['name'] == horizon_df.at[0, 'name']

    points = horizon.points
    points_df = points.to_df(get_converted=False)

    assert len(points) == len(points_df.index)

    for idx, horizon_trajectory_point in enumerate(points):
        assert np_is_close(points_df.at[idx, 'md'], horizon_trajectory_point.md)
        assert np_is_close(points_df.at[idx, 'tvd'], horizon_trajectory_point.tvd)


def test_get_converted_meter_nested_well_trajectory(project):
    starred_nested_well = project.wells.find_by_name(WELL_NAME).starred_nested_well

    assert starred_nested_well is not None

    trajectory = starred_nested_well.trajectory
    trajectory_df = trajectory.to_df()

    assert trajectory
    assert not trajectory_df.empty
    assert len(trajectory) == len(trajectory_df.index)

    for idx, trajectory_point in enumerate(trajectory):
        assert np_is_close(
            trajectory_df.at[idx, 'md'],
            Convertible.convert_z(
                value=trajectory_point.md, measure_units=starred_nested_well.well.project.measure_unit
            ),
        )
        assert np_is_close(trajectory_df.at[idx, 'incl'], Convertible.convert_angle(trajectory_point.incl))
        assert np_is_close(trajectory_df.at[idx, 'azim'], Convertible.convert_angle(trajectory_point.azim))


def test_get_not_converted_meter_nested_well_trajectory(project):
    starred_nested_well = project.wells.find_by_name(WELL_NAME).starred_nested_well

    assert starred_nested_well is not None

    trajectory = starred_nested_well.trajectory
    trajectory_df = trajectory.to_df(get_converted=False)

    assert trajectory
    assert not trajectory_df.empty
    assert len(trajectory) == len(trajectory_df.index)

    for idx, trajectory_point in enumerate(trajectory):
        assert np_is_close(trajectory_df.at[idx, 'md'], trajectory_point.md)
        assert np_is_close(trajectory_df.at[idx, 'incl'], trajectory_point.incl)
        assert np_is_close(trajectory_df.at[idx, 'azim'], trajectory_point.azim)


def test_get_converted_foot_nested_well_trajectory(ft_project):
    starred_nested_well = ft_project.wells.find_by_name(WELL_NAME).starred_nested_well

    assert starred_nested_well is not None

    trajectory = starred_nested_well.trajectory
    trajectory_df = trajectory.to_df()

    assert trajectory
    assert not trajectory_df.empty
    assert len(trajectory) == len(trajectory_df.index)

    for idx, trajectory_point in enumerate(trajectory):
        assert np_is_close(
            trajectory_df.at[idx, 'md'],
            Convertible.convert_z(
                value=trajectory_point.md, measure_units=starred_nested_well.well.project.measure_unit
            ),
        )
        assert np_is_close(trajectory_df.at[idx, 'incl'], Convertible.convert_angle(trajectory_point.incl))
        assert np_is_close(trajectory_df.at[idx, 'azim'], Convertible.convert_angle(trajectory_point.azim))


def test_get_not_converted_foot_nested_well_trajectory(ft_project):
    starred_nested_well = ft_project.wells.find_by_name(WELL_NAME).starred_nested_well

    assert starred_nested_well is not None

    trajectory = starred_nested_well.trajectory
    trajectory_df = trajectory.to_df(get_converted=False)

    assert trajectory
    assert not trajectory_df.empty
    assert len(trajectory) == len(trajectory_df.index)

    for idx, trajectory_point in enumerate(trajectory):
        assert np_is_close(trajectory_df.at[idx, 'md'], trajectory_point.md)
        assert np_is_close(trajectory_df.at[idx, 'incl'], trajectory_point.incl)
        assert np_is_close(trajectory_df.at[idx, 'azim'], trajectory_point.azim)


def test_get_converted_ftm_nested_well_trajectory(ftm_project):
    starred_nested_well = ftm_project.wells.find_by_name(WELL_NAME).starred_nested_well

    assert starred_nested_well is not None

    trajectory = starred_nested_well.trajectory
    trajectory_df = trajectory.to_df()

    assert trajectory
    assert not trajectory_df.empty
    assert len(trajectory) == len(trajectory_df.index)

    for idx, trajectory_point in enumerate(trajectory):
        assert np_is_close(
            trajectory_df.at[idx, 'md'],
            Convertible.convert_z(
                value=trajectory_point.md, measure_units=starred_nested_well.well.project.measure_unit
            ),
        )
        assert np_is_close(trajectory_df.at[idx, 'incl'], Convertible.convert_angle(trajectory_point.incl))
        assert np_is_close(trajectory_df.at[idx, 'azim'], Convertible.convert_angle(trajectory_point.azim))


def test_get_not_converted_ftm_nested_well_trajectory(ftm_project):
    starred_nested_well = ftm_project.wells.find_by_name(WELL_NAME).starred_nested_well

    assert starred_nested_well is not None

    trajectory = starred_nested_well.trajectory
    trajectory_df = trajectory.to_df(get_converted=False)

    assert trajectory
    assert not trajectory_df.empty
    assert len(trajectory) == len(trajectory_df.index)

    for idx, trajectory_point in enumerate(trajectory):
        assert np_is_close(trajectory_df.at[idx, 'md'], trajectory_point.md)
        assert np_is_close(trajectory_df.at[idx, 'incl'], trajectory_point.incl)
        assert np_is_close(trajectory_df.at[idx, 'azim'], trajectory_point.azim)


def test_get_converted_meter_log(project):
    logs = project.wells.find_by_name(WELL_NAME).logs
    log = logs.find_by_name(LOG_NAME)

    assert log is not None

    log_data = log.to_dict()
    log_df = log.to_df()

    assert 'uuid' in log_data
    assert 'name' in log_data
    assert log_data['uuid'] == log_df.at[0, 'uuid']
    assert log_data['name'] == log_df.at[0, 'name']

    points = log.points
    points_df = points.to_df()

    assert len(points) == len(points_df.index)

    measure_units = log.well.project.measure_unit

    for idx, log_point in enumerate(points):
        assert np_is_close(
            points_df.at[idx, 'md'], Convertible.convert_z(value=log_point.md, measure_units=measure_units)
        )


def test_get_not_converted_meter_log(project):
    logs = project.wells.find_by_name(WELL_NAME).logs
    log = logs.find_by_name(LOG_NAME)

    assert log is not None

    log_data = log.to_dict()
    log_df = log.to_df()

    assert 'uuid' in log_data
    assert 'name' in log_data
    assert log_data['uuid'] == log_df.at[0, 'uuid']
    assert log_data['name'] == log_df.at[0, 'name']

    points = log.points
    points_df = points.to_df(get_converted=False)

    assert len(points) == len(points_df.index)

    for idx, log_point in enumerate(points):
        assert np_is_close(points_df.at[idx, 'md'], log_point.md)


def test_get_converted_foot_log(ft_project):
    logs = ft_project.wells.find_by_name(WELL_NAME).logs
    log = logs.find_by_name(LOG_NAME)

    assert log is not None

    log_data = log.to_dict()
    log_df = log.to_df()

    assert 'uuid' in log_data
    assert 'name' in log_data
    assert log_data['uuid'] == log_df.at[0, 'uuid']
    assert log_data['name'] == log_df.at[0, 'name']

    points = log.points
    points_df = points.to_df()

    assert len(points) == len(points_df.index)

    measure_units = log.well.project.measure_unit

    for idx, log_point in enumerate(points):
        assert np_is_close(
            points_df.at[idx, 'md'], Convertible.convert_z(value=log_point.md, measure_units=measure_units)
        )


def test_get_not_converted_foot_log(ft_project):
    logs = ft_project.wells.find_by_name(WELL_NAME).logs
    log = logs.find_by_name(LOG_NAME)

    assert log is not None

    log_data = log.to_dict()
    log_df = log.to_df()

    assert 'uuid' in log_data
    assert 'name' in log_data
    assert log_data['uuid'] == log_df.at[0, 'uuid']
    assert log_data['name'] == log_df.at[0, 'name']

    points = log.points
    points_df = points.to_df(get_converted=False)

    assert len(points) == len(points_df.index)

    for idx, log_point in enumerate(points):
        assert np_is_close(points_df.at[idx, 'md'], log_point.md)


def test_get_converted_ftm_log(ftm_project):
    logs = ftm_project.wells.find_by_name(WELL_NAME).logs
    log = logs.find_by_name(LOG_NAME)

    assert log is not None

    log_data = log.to_dict()
    log_df = log.to_df()

    assert 'uuid' in log_data
    assert 'name' in log_data
    assert log_data['uuid'] == log_df.at[0, 'uuid']
    assert log_data['name'] == log_df.at[0, 'name']

    points = log.points
    points_df = points.to_df()

    assert len(points) == len(points_df.index)

    measure_units = log.well.project.measure_unit

    for idx, log_point in enumerate(points):
        assert np_is_close(
            points_df.at[idx, 'md'], Convertible.convert_z(value=log_point.md, measure_units=measure_units)
        )


def test_get_not_converted_ftm_log(ftm_project):
    logs = ftm_project.wells.find_by_name(WELL_NAME).logs
    log = logs.find_by_name(LOG_NAME)

    assert log is not None

    log_data = log.to_dict()
    log_df = log.to_df()

    assert 'uuid' in log_data
    assert 'name' in log_data
    assert log_data['uuid'] == log_df.at[0, 'uuid']
    assert log_data['name'] == log_df.at[0, 'name']

    points = log.points
    points_df = points.to_df(get_converted=False)

    assert len(points) == len(points_df.index)

    for idx, log_point in enumerate(points):
        assert np_is_close(points_df.at[idx, 'md'], log_point.md)


def test_get_converted_meter_typewell(project):
    typewell = project.typewells.find_by_name(TYPEWELL_NAME)

    assert typewell is not None

    typewell_df = typewell.to_df()

    assert not typewell_df.empty

    assert np_is_close(
        typewell_df['xsrf'],
        Convertible.convert_xy(value=typewell.xsrf, measure_units=project.measure_unit, force_to_meters=True),
    )
    assert np_is_close(
        typewell_df['ysrf'],
        Convertible.convert_xy(value=typewell.ysrf, measure_units=project.measure_unit, force_to_meters=True),
    )
    assert np_is_close(typewell_df['kb'], Convertible.convert_z(value=typewell.kb, measure_units=project.measure_unit))
    assert np_is_close(typewell_df['convergence'], Convertible.convert_angle(typewell.convergence))
    assert np_is_close(
        typewell_df['tie_in_tvd'], Convertible.convert_z(value=typewell.tie_in_tvd, measure_units=project.measure_unit)
    )
    assert np_is_close(
        typewell_df['tie_in_ns'], Convertible.convert_xy(value=typewell.tie_in_ns, measure_units=project.measure_unit)
    )
    assert np_is_close(
        typewell_df['tie_in_ew'], Convertible.convert_xy(value=typewell.tie_in_ew, measure_units=project.measure_unit)
    )


def test_get_not_converted_meter_typewell(project):
    typewell = project.typewells.find_by_name(TYPEWELL_NAME)

    assert typewell is not None

    typewell_df = typewell.to_df(get_converted=False)

    assert not typewell_df.empty

    assert np_is_close(typewell_df['xsrf'], typewell.xsrf)
    assert np_is_close(typewell_df['ysrf'], typewell.ysrf)
    assert np_is_close(typewell_df['kb'], typewell.kb)
    assert np_is_close(typewell_df['convergence'], typewell.convergence)
    assert np_is_close(typewell_df['tie_in_tvd'], typewell.tie_in_tvd)
    assert np_is_close(typewell_df['tie_in_ns'], typewell.tie_in_ns)
    assert np_is_close(typewell_df['tie_in_ew'], typewell.tie_in_ew)


def test_get_converted_foot_typewell(ft_project):
    typewell = ft_project.typewells.find_by_name(TYPEWELL_NAME)

    assert typewell is not None

    typewell_df = typewell.to_df()

    assert not typewell_df.empty

    assert np_is_close(
        typewell_df['xsrf'],
        Convertible.convert_xy(value=typewell.xsrf, measure_units=ft_project.measure_unit, force_to_meters=True),
    )
    assert np_is_close(
        typewell_df['ysrf'],
        Convertible.convert_xy(value=typewell.ysrf, measure_units=ft_project.measure_unit, force_to_meters=True),
    )
    assert np_is_close(
        typewell_df['kb'], Convertible.convert_z(value=typewell.kb, measure_units=ft_project.measure_unit)
    )
    assert np_is_close(typewell_df['convergence'], Convertible.convert_angle(typewell.convergence))
    assert np_is_close(
        typewell_df['tie_in_tvd'],
        Convertible.convert_z(value=typewell.tie_in_tvd, measure_units=ft_project.measure_unit),
    )
    assert np_is_close(
        typewell_df['tie_in_ns'],
        Convertible.convert_xy(value=typewell.tie_in_ns, measure_units=ft_project.measure_unit),
    )
    assert np_is_close(
        typewell_df['tie_in_ew'],
        Convertible.convert_xy(value=typewell.tie_in_ew, measure_units=ft_project.measure_unit),
    )


def test_get_not_converted_foot_typewell(ft_project):
    typewell = ft_project.typewells.find_by_name(TYPEWELL_NAME)

    assert typewell is not None

    typewell_df = typewell.to_df(get_converted=False)

    assert not typewell_df.empty

    assert np_is_close(typewell_df['xsrf'], typewell.xsrf)
    assert np_is_close(typewell_df['ysrf'], typewell.ysrf)
    assert np_is_close(typewell_df['kb'], typewell.kb)
    assert np_is_close(typewell_df['convergence'], typewell.convergence)
    assert np_is_close(typewell_df['tie_in_tvd'], typewell.tie_in_tvd)
    assert np_is_close(typewell_df['tie_in_ns'], typewell.tie_in_ns)
    assert np_is_close(typewell_df['tie_in_ew'], typewell.tie_in_ew)


def test_get_converted_ftm_typewell(ftm_project):
    typewell = ftm_project.typewells.find_by_name(TYPEWELL_NAME)

    assert typewell is not None

    typewell_df = typewell.to_df()

    assert not typewell_df.empty

    assert np_is_close(
        typewell_df['xsrf'],
        Convertible.convert_xy(value=typewell.xsrf, measure_units=ftm_project.measure_unit, force_to_meters=True),
    )
    assert np_is_close(
        typewell_df['ysrf'],
        Convertible.convert_xy(value=typewell.ysrf, measure_units=ftm_project.measure_unit, force_to_meters=True),
    )
    assert np_is_close(
        typewell_df['kb'], Convertible.convert_z(value=typewell.kb, measure_units=ftm_project.measure_unit)
    )
    assert np_is_close(typewell_df['convergence'], Convertible.convert_angle(typewell.convergence))
    assert np_is_close(
        typewell_df['tie_in_tvd'],
        Convertible.convert_z(value=typewell.tie_in_tvd, measure_units=ftm_project.measure_unit),
    )
    assert np_is_close(
        typewell_df['tie_in_ns'],
        Convertible.convert_xy(value=typewell.tie_in_ns, measure_units=ftm_project.measure_unit),
    )
    assert np_is_close(
        typewell_df['tie_in_ew'],
        Convertible.convert_xy(value=typewell.tie_in_ew, measure_units=ftm_project.measure_unit),
    )


def test_get_not_converted_ftm_typewell(ftm_project):
    typewell = ftm_project.typewells.find_by_name(TYPEWELL_NAME)

    assert typewell is not None

    typewell_df = typewell.to_df(get_converted=False)

    assert not typewell_df.empty

    assert np_is_close(typewell_df['xsrf'], typewell.xsrf)
    assert np_is_close(typewell_df['ysrf'], typewell.ysrf)
    assert np_is_close(typewell_df['kb'], typewell.kb)
    assert np_is_close(typewell_df['convergence'], typewell.convergence)
    assert np_is_close(typewell_df['tie_in_tvd'], typewell.tie_in_tvd)
    assert np_is_close(typewell_df['tie_in_ns'], typewell.tie_in_ns)
    assert np_is_close(typewell_df['tie_in_ew'], typewell.tie_in_ew)


def test_get_converted_meter_earth_model(project):
    starred_interpretation = project.wells.find_by_name(WELL_NAME).starred_interpretation
    earth_model = starred_interpretation.earth_models.find_by_name(EARTH_MODEL_NAME)

    assert earth_model is not None

    earth_model_data = earth_model.to_dict()
    earth_model_df = earth_model.to_df()

    assert 'uuid' in earth_model_data
    assert 'name' in earth_model_data
    assert 'uuid' in earth_model_df
    assert 'name' in earth_model_df
    assert earth_model_data['uuid'] == earth_model_df.at[0, 'uuid']

    sections = earth_model.sections
    sections_df = sections.to_df()

    assert len(sections) == len(sections_df.index)
    assert sections[0].uuid == sections_df.at[0, 'uuid']

    measure_units = earth_model.interpretation.well.project.measure_unit

    for idx, section in enumerate(sections):
        assert np_is_close(
            sections_df.at[idx, 'md'],
            Convertible.convert_z(value=section.md, measure_units=measure_units),
        )

    layers = sections[0].layers
    layers_df = layers.to_df()

    assert len(layers) == len(layers_df.index)
    assert layers[0].thickness == layers_df.at[0, 'thickness']

    for idx, layer in enumerate(layers):
        # Must be changed when public method with layer tvd is available
        assert np_is_close(
            layers_df.at[idx, 'tvt'], Convertible.convert_z(value=layer.tvd, measure_units=measure_units)
        )


def test_get_not_converted_meter_earth_model(project):
    starred_interpretation = project.wells.find_by_name(WELL_NAME).starred_interpretation
    earth_model = starred_interpretation.earth_models.find_by_name(EARTH_MODEL_NAME)

    assert earth_model is not None

    earth_model_data = earth_model.to_dict()
    earth_model_df = earth_model.to_df()

    assert 'uuid' in earth_model_data
    assert 'name' in earth_model_data
    assert 'uuid' in earth_model_df
    assert 'name' in earth_model_df
    assert earth_model_data['uuid'] == earth_model_df.at[0, 'uuid']

    sections = earth_model.sections
    sections_df = sections.to_df(get_converted=False)

    assert len(sections) == len(sections_df.index)
    assert sections[0].uuid == sections_df.at[0, 'uuid']

    for idx, section in enumerate(sections):
        assert np_is_close(sections_df.at[idx, 'md'], section.md)

    layers = sections[0].layers
    layers_df = layers.to_df(get_converted=False)

    assert len(layers) == len(layers_df.index)
    assert layers[0].thickness == layers_df.at[0, 'thickness']

    for idx, layer in enumerate(layers):
        # Must be changed when public method with layer tvd is available
        assert np_is_close(layers_df.at[idx, 'tvt'], layer.tvd)


def test_get_converted_foot_earth_model(ft_project):
    starred_interpretation = ft_project.wells.find_by_name(WELL_NAME).starred_interpretation
    earth_model = starred_interpretation.earth_models.find_by_name(EARTH_MODEL_NAME)

    assert earth_model is not None

    earth_model_data = earth_model.to_dict()
    earth_model_df = earth_model.to_df()

    assert 'uuid' in earth_model_data
    assert 'name' in earth_model_data
    assert 'uuid' in earth_model_df
    assert 'name' in earth_model_df
    assert earth_model_data['uuid'] == earth_model_df.at[0, 'uuid']

    sections = earth_model.sections
    sections_df = sections.to_df()

    assert len(sections) == len(sections_df.index)
    assert sections[0].uuid == sections_df.at[0, 'uuid']

    measure_units = earth_model.interpretation.well.project.measure_unit

    for idx, section in enumerate(sections):
        assert np_is_close(
            sections_df.at[idx, 'md'],
            Convertible.convert_z(value=section.md, measure_units=measure_units),
        )

    layers = sections[0].layers
    layers_df = layers.to_df()

    assert len(layers) == len(layers_df.index)
    assert layers[0].thickness == layers_df.at[0, 'thickness']

    for idx, layer in enumerate(layers):
        # Must be changed when public method with layer tvd is available
        assert np_is_close(
            layers_df.at[idx, 'tvt'], Convertible.convert_z(value=layer.tvd, measure_units=measure_units)
        )


def test_get_not_converted_foot_earth_model(ft_project):
    starred_interpretation = ft_project.wells.find_by_name(WELL_NAME).starred_interpretation
    earth_model = starred_interpretation.earth_models.find_by_name(EARTH_MODEL_NAME)

    assert earth_model is not None

    earth_model_data = earth_model.to_dict()
    earth_model_df = earth_model.to_df()

    assert 'uuid' in earth_model_data
    assert 'name' in earth_model_data
    assert 'uuid' in earth_model_df
    assert 'name' in earth_model_df
    assert earth_model_data['uuid'] == earth_model_df.at[0, 'uuid']

    sections = earth_model.sections
    sections_df = sections.to_df(get_converted=False)

    assert len(sections) == len(sections_df.index)
    assert sections[0].uuid == sections_df.at[0, 'uuid']

    for idx, section in enumerate(sections):
        assert np_is_close(sections_df.at[idx, 'md'], section.md)

    layers = sections[0].layers
    layers_df = layers.to_df(get_converted=False)

    assert len(layers) == len(layers_df.index)
    assert layers[0].thickness == layers_df.at[0, 'thickness']

    for idx, layer in enumerate(layers):
        # Must be changed when public method with layer tvd is available
        assert np_is_close(layers_df.at[idx, 'tvt'], layer.tvd)


def test_get_converted_ftm_earth_model(ftm_project):
    starred_interpretation = ftm_project.wells.find_by_name(WELL_NAME).starred_interpretation
    earth_model = starred_interpretation.earth_models.find_by_name(EARTH_MODEL_NAME)

    assert earth_model is not None

    earth_model_data = earth_model.to_dict()
    earth_model_df = earth_model.to_df()

    assert 'uuid' in earth_model_data
    assert 'name' in earth_model_data
    assert 'uuid' in earth_model_df
    assert 'name' in earth_model_df
    assert earth_model_data['uuid'] == earth_model_df.at[0, 'uuid']

    sections = earth_model.sections
    sections_df = sections.to_df()

    assert len(sections) == len(sections_df.index)
    assert sections[0].uuid == sections_df.at[0, 'uuid']

    measure_units = earth_model.interpretation.well.project.measure_unit

    for idx, section in enumerate(sections):
        assert np_is_close(
            sections_df.at[idx, 'md'],
            Convertible.convert_z(value=section.md, measure_units=measure_units),
        )

    layers = sections[0].layers
    layers_df = layers.to_df()

    assert len(layers) == len(layers_df.index)
    assert layers[0].thickness == layers_df.at[0, 'thickness']

    for idx, layer in enumerate(layers):
        # Must be changed when public method with layer tvd is available
        assert np_is_close(
            layers_df.at[idx, 'tvt'], Convertible.convert_z(value=layer.tvd, measure_units=measure_units)
        )


def test_get_not_converted_ftm_earth_model(ftm_project):
    starred_interpretation = ftm_project.wells.find_by_name(WELL_NAME).starred_interpretation
    earth_model = starred_interpretation.earth_models.find_by_name(EARTH_MODEL_NAME)

    assert earth_model is not None

    earth_model_data = earth_model.to_dict()
    earth_model_df = earth_model.to_df()

    assert 'uuid' in earth_model_data
    assert 'name' in earth_model_data
    assert 'uuid' in earth_model_df
    assert 'name' in earth_model_df
    assert earth_model_data['uuid'] == earth_model_df.at[0, 'uuid']

    sections = earth_model.sections
    sections_df = sections.to_df(get_converted=False)

    assert len(sections) == len(sections_df.index)
    assert sections[0].uuid == sections_df.at[0, 'uuid']

    for idx, section in enumerate(sections):
        assert np_is_close(sections_df.at[idx, 'md'], section.md)

    layers = sections[0].layers
    layers_df = layers.to_df(get_converted=False)

    assert len(layers) == len(layers_df.index)
    assert layers[0].thickness == layers_df.at[0, 'thickness']

    for idx, layer in enumerate(layers):
        # Must be changed when public method with layer tvd is available
        assert np_is_close(layers_df.at[idx, 'tvt'], layer.tvd)
