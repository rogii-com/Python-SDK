from rogii_solo.base import Convertible
from rogii_solo.calculations.converters import feet_to_meters
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

    well_data = well.to_dict()
    assert well_data

    assert np_is_close(
        well_data['xsrf'],
        Convertible.convert_xy(value=well.xsrf, measure_units=project.measure_unit, force_to_meters=True),
    )
    assert np_is_close(
        well_data['ysrf'],
        Convertible.convert_xy(value=well.ysrf, measure_units=project.measure_unit, force_to_meters=True),
    )
    assert np_is_close(well_data['kb'], Convertible.convert_z(value=well.kb, measure_units=project.measure_unit))
    assert np_is_close(well_data['azimuth'], Convertible.convert_angle(well.azimuth))
    assert np_is_close(well_data['convergence'], Convertible.convert_angle(well.convergence))
    assert np_is_close(
        well_data['tie_in_tvd'], Convertible.convert_z(value=well.tie_in_tvd, measure_units=project.measure_unit)
    )
    assert np_is_close(
        well_data['tie_in_ns'], Convertible.convert_xy(value=well.tie_in_ns, measure_units=project.measure_unit)
    )
    assert np_is_close(
        well_data['tie_in_ew'], Convertible.convert_xy(value=well.tie_in_ew, measure_units=project.measure_unit)
    )

    linked_typewell = well.linked_typewells[0]
    assert linked_typewell

    linked_typewell_data = linked_typewell.to_dict()
    assert linked_typewell_data

    assert np_is_close(linked_typewell_data['shift'], linked_typewell.shift)


def test_get_not_converted_meter_well(project):
    well = project.wells.find_by_name(WELL_NAME)
    assert well is not None

    well_data = well.to_dict(get_converted=False)
    assert well_data

    assert np_is_close(well_data['xsrf'], well.xsrf)
    assert np_is_close(well_data['ysrf'], well.ysrf)
    assert np_is_close(well_data['kb'], well.kb)
    assert np_is_close(well_data['azimuth'], well.azimuth)
    assert np_is_close(well_data['convergence'], well.convergence)
    assert np_is_close(well_data['tie_in_tvd'], well.tie_in_tvd)
    assert np_is_close(well_data['tie_in_ns'], well.tie_in_ns)
    assert np_is_close(well_data['tie_in_ew'], well.tie_in_ew)

    linked_typewell = well.linked_typewells[0]
    assert linked_typewell

    linked_typewell_data = linked_typewell.to_dict(get_converted=False)
    assert linked_typewell_data

    assert np_is_close(linked_typewell_data['shift'], feet_to_meters(linked_typewell.shift))


def test_get_converted_foot_well(ft_project):
    well = ft_project.wells.find_by_name(WELL_NAME)
    assert well is not None

    well_data = well.to_dict()
    assert well_data

    assert np_is_close(
        well_data['xsrf'],
        Convertible.convert_xy(value=well.xsrf, measure_units=ft_project.measure_unit, force_to_meters=True),
    )
    assert np_is_close(
        well_data['ysrf'],
        Convertible.convert_xy(value=well.ysrf, measure_units=ft_project.measure_unit, force_to_meters=True),
    )
    assert np_is_close(well_data['kb'], Convertible.convert_z(value=well.kb, measure_units=ft_project.measure_unit))
    assert np_is_close(well_data['azimuth'], Convertible.convert_angle(well.azimuth))
    assert np_is_close(well_data['convergence'], Convertible.convert_angle(well.convergence))
    assert np_is_close(
        well_data['tie_in_tvd'], Convertible.convert_z(value=well.tie_in_tvd, measure_units=ft_project.measure_unit)
    )
    assert np_is_close(
        well_data['tie_in_ns'], Convertible.convert_xy(value=well.tie_in_ns, measure_units=ft_project.measure_unit)
    )
    assert np_is_close(
        well_data['tie_in_ew'], Convertible.convert_xy(value=well.tie_in_ew, measure_units=ft_project.measure_unit)
    )

    linked_typewell = well.linked_typewells[0]
    assert linked_typewell

    linked_typewell_data = linked_typewell.to_dict()
    assert linked_typewell_data

    assert np_is_close(linked_typewell_data['shift'], linked_typewell.shift)


def test_get_not_converted_foot_well(ft_project):
    well = ft_project.wells.find_by_name(WELL_NAME)
    assert well is not None

    well_data = well.to_dict(get_converted=False)
    assert well_data

    assert np_is_close(well_data['xsrf'], well.xsrf)
    assert np_is_close(well_data['ysrf'], well.ysrf)
    assert np_is_close(well_data['kb'], well.kb)
    assert np_is_close(well_data['azimuth'], well.azimuth)
    assert np_is_close(well_data['convergence'], well.convergence)
    assert np_is_close(well_data['tie_in_tvd'], well.tie_in_tvd)
    assert np_is_close(well_data['tie_in_ns'], well.tie_in_ns)
    assert np_is_close(well_data['tie_in_ew'], well.tie_in_ew)

    linked_typewell = well.linked_typewells[0]
    assert linked_typewell

    linked_typewell_data = linked_typewell.to_dict(get_converted=False)
    assert linked_typewell_data

    assert np_is_close(linked_typewell_data['shift'], feet_to_meters(linked_typewell.shift))


def test_get_converted_ftm_well(ftm_project):
    well = ftm_project.wells.find_by_name(WELL_NAME)
    assert well is not None

    well_data = well.to_dict()
    assert well_data

    assert np_is_close(
        well_data['xsrf'],
        Convertible.convert_xy(value=well.xsrf, measure_units=ftm_project.measure_unit, force_to_meters=True),
    )
    assert np_is_close(
        well_data['ysrf'],
        Convertible.convert_xy(value=well.ysrf, measure_units=ftm_project.measure_unit, force_to_meters=True),
    )
    assert np_is_close(well_data['kb'], Convertible.convert_z(value=well.kb, measure_units=ftm_project.measure_unit))
    assert np_is_close(well_data['azimuth'], Convertible.convert_angle(well.azimuth))
    assert np_is_close(well_data['convergence'], Convertible.convert_angle(well.convergence))
    assert np_is_close(
        well_data['tie_in_tvd'], Convertible.convert_z(value=well.tie_in_tvd, measure_units=ftm_project.measure_unit)
    )
    assert np_is_close(
        well_data['tie_in_ns'], Convertible.convert_xy(value=well.tie_in_ns, measure_units=ftm_project.measure_unit)
    )
    assert np_is_close(
        well_data['tie_in_ew'], Convertible.convert_xy(value=well.tie_in_ew, measure_units=ftm_project.measure_unit)
    )

    linked_typewell = well.linked_typewells[0]
    assert linked_typewell

    linked_typewell_data = linked_typewell.to_dict()
    assert linked_typewell_data

    assert np_is_close(linked_typewell_data['shift'], linked_typewell.shift)


def test_get_not_converted_ftm_well(ftm_project):
    well = ftm_project.wells.find_by_name(WELL_NAME)
    assert well is not None

    well_data = well.to_dict(get_converted=False)
    assert well_data

    assert np_is_close(well_data['xsrf'], well.xsrf)
    assert np_is_close(well_data['ysrf'], well.ysrf)
    assert np_is_close(well_data['kb'], well.kb)
    assert np_is_close(well_data['azimuth'], well.azimuth)
    assert np_is_close(well_data['convergence'], well.convergence)
    assert np_is_close(well_data['tie_in_tvd'], well.tie_in_tvd)
    assert np_is_close(well_data['tie_in_ns'], well.tie_in_ns)
    assert np_is_close(well_data['tie_in_ew'], well.tie_in_ew)

    linked_typewell = well.linked_typewells[0]
    assert linked_typewell

    linked_typewell_data = linked_typewell.to_dict(get_converted=False)
    assert linked_typewell_data

    assert np_is_close(linked_typewell_data['shift'], feet_to_meters(linked_typewell.shift))


def test_get_converted_meter_well_trajectory(project):
    well = project.wells.find_by_name(WELL_NAME)
    assert well is not None

    trajectory = well.trajectory
    trajectory_data = trajectory.to_dict()
    assert trajectory
    assert trajectory_data
    assert len(trajectory) == len(trajectory_data)

    for idx, trajectory_point in enumerate(trajectory):
        assert np_is_close(
            trajectory_data[idx]['md'],
            Convertible.convert_z(value=trajectory_point.md, measure_units=well.project.measure_unit),
        )
        assert np_is_close(trajectory_data[idx]['incl'], Convertible.convert_angle(trajectory_point.incl))
        assert np_is_close(trajectory_data[idx]['azim'], Convertible.convert_angle(trajectory_point.azim))


def test_get_not_converted_meter_well_trajectory(project):
    well = project.wells.find_by_name(WELL_NAME)
    assert well is not None

    trajectory = well.trajectory
    trajectory_data = trajectory.to_dict(get_converted=False)
    assert trajectory
    assert trajectory_data
    assert len(trajectory) == len(trajectory_data)

    for idx, trajectory_point in enumerate(trajectory):
        assert np_is_close(trajectory_data[idx]['md'], trajectory_point.md)
        assert np_is_close(trajectory_data[idx]['incl'], trajectory_point.incl)
        assert np_is_close(trajectory_data[idx]['azim'], trajectory_point.azim)


def test_get_converted_foot_well_trajectory(ft_project):
    well = ft_project.wells.find_by_name(WELL_NAME)
    assert well is not None

    trajectory = well.trajectory
    trajectory_data = trajectory.to_dict()
    assert trajectory
    assert trajectory_data
    assert len(trajectory) == len(trajectory_data)

    for idx, trajectory_point in enumerate(trajectory):
        assert np_is_close(
            trajectory_data[idx]['md'],
            Convertible.convert_z(value=trajectory_point.md, measure_units=well.project.measure_unit),
        )
        assert np_is_close(trajectory_data[idx]['incl'], Convertible.convert_angle(trajectory_point.incl))
        assert np_is_close(trajectory_data[idx]['azim'], Convertible.convert_angle(trajectory_point.azim))


def test_get_not_converted_foot_well_trajectory(ft_project):
    well = ft_project.wells.find_by_name(WELL_NAME)
    assert well is not None

    trajectory = well.trajectory
    trajectory_data = trajectory.to_dict(get_converted=False)
    assert trajectory
    assert trajectory_data
    assert len(trajectory) == len(trajectory_data)

    for idx, trajectory_point in enumerate(trajectory):
        assert np_is_close(trajectory_data[idx]['md'], trajectory_point.md)
        assert np_is_close(trajectory_data[idx]['incl'], trajectory_point.incl)
        assert np_is_close(trajectory_data[idx]['azim'], trajectory_point.azim)


def test_get_converted_ftm_well_trajectory(ftm_project):
    well = ftm_project.wells.find_by_name(WELL_NAME)
    assert well is not None

    trajectory = well.trajectory
    trajectory_data = trajectory.to_dict()
    assert trajectory
    assert trajectory_data
    assert len(trajectory) == len(trajectory_data)

    for idx, trajectory_point in enumerate(trajectory):
        assert np_is_close(
            trajectory_data[idx]['md'],
            Convertible.convert_z(value=trajectory_point.md, measure_units=well.project.measure_unit),
        )
        assert np_is_close(trajectory_data[idx]['incl'], Convertible.convert_angle(trajectory_point.incl))
        assert np_is_close(trajectory_data[idx]['azim'], Convertible.convert_angle(trajectory_point.azim))


def test_get_not_converted_ftm_well_trajectory(ftm_project):
    well = ftm_project.wells.find_by_name(WELL_NAME)
    assert well is not None

    trajectory = well.trajectory
    trajectory_data = trajectory.to_dict(get_converted=False)
    assert trajectory
    assert trajectory_data
    assert len(trajectory) == len(trajectory_data)

    for idx, trajectory_point in enumerate(trajectory):
        assert np_is_close(trajectory_data[idx]['md'], trajectory_point.md)
        assert np_is_close(trajectory_data[idx]['incl'], trajectory_point.incl)
        assert np_is_close(trajectory_data[idx]['azim'], trajectory_point.azim)


def test_get_converted_meter_nested_well(project):
    starred_nested_well = project.wells.find_by_name(WELL_NAME).starred_nested_well
    assert starred_nested_well is not None

    starred_nested_well_data = starred_nested_well.to_dict()
    assert starred_nested_well_data

    assert np_is_close(
        starred_nested_well_data['xsrf'],
        Convertible.convert_xy(
            value=starred_nested_well.xsrf, measure_units=project.measure_unit, force_to_meters=True
        ),
    )
    assert np_is_close(
        starred_nested_well_data['ysrf'],
        Convertible.convert_xy(
            value=starred_nested_well.ysrf, measure_units=project.measure_unit, force_to_meters=True
        ),
    )
    assert np_is_close(
        starred_nested_well_data['kb'],
        Convertible.convert_z(value=starred_nested_well.kb, measure_units=project.measure_unit),
    )
    assert np_is_close(starred_nested_well_data['azimuth'], Convertible.convert_angle(starred_nested_well.azimuth))
    assert np_is_close(
        starred_nested_well_data['convergence'], Convertible.convert_angle(starred_nested_well.convergence)
    )
    assert np_is_close(
        starred_nested_well_data['tie_in_tvd'],
        Convertible.convert_z(value=starred_nested_well.tie_in_tvd, measure_units=project.measure_unit),
    )
    assert np_is_close(
        starred_nested_well_data['tie_in_ns'],
        Convertible.convert_xy(value=starred_nested_well.tie_in_ns, measure_units=project.measure_unit),
    )
    assert np_is_close(
        starred_nested_well_data['tie_in_ew'],
        Convertible.convert_xy(value=starred_nested_well.tie_in_ew, measure_units=project.measure_unit),
    )


def test_get_not_converted_meter_nested_well(project):
    starred_nested_well = project.wells.find_by_name(WELL_NAME).starred_nested_well
    assert starred_nested_well is not None

    starred_nested_well_data = starred_nested_well.to_dict(get_converted=False)
    assert starred_nested_well_data

    assert np_is_close(starred_nested_well_data['xsrf'], starred_nested_well.xsrf)
    assert np_is_close(starred_nested_well_data['ysrf'], starred_nested_well.ysrf)
    assert np_is_close(starred_nested_well_data['kb'], starred_nested_well.kb)
    assert np_is_close(starred_nested_well_data['azimuth'], starred_nested_well.azimuth)
    assert np_is_close(starred_nested_well_data['convergence'], starred_nested_well.convergence)
    assert np_is_close(starred_nested_well_data['tie_in_tvd'], starred_nested_well.tie_in_tvd)
    assert np_is_close(starred_nested_well_data['tie_in_ns'], starred_nested_well.tie_in_ns)
    assert np_is_close(starred_nested_well_data['tie_in_ew'], starred_nested_well.tie_in_ew)


def test_get_converted_foot_nested_well(ft_project):
    starred_nested_well = ft_project.wells.find_by_name(WELL_NAME).starred_nested_well
    assert starred_nested_well is not None

    starred_nested_well_data = starred_nested_well.to_dict()
    assert starred_nested_well_data

    assert np_is_close(
        starred_nested_well_data['xsrf'],
        Convertible.convert_xy(
            value=starred_nested_well.xsrf, measure_units=ft_project.measure_unit, force_to_meters=True
        ),
    )
    assert np_is_close(
        starred_nested_well_data['ysrf'],
        Convertible.convert_xy(
            value=starred_nested_well.ysrf, measure_units=ft_project.measure_unit, force_to_meters=True
        ),
    )
    assert np_is_close(
        starred_nested_well_data['kb'],
        Convertible.convert_z(value=starred_nested_well.kb, measure_units=ft_project.measure_unit),
    )
    assert np_is_close(starred_nested_well_data['azimuth'], Convertible.convert_angle(starred_nested_well.azimuth))
    assert np_is_close(
        starred_nested_well_data['convergence'], Convertible.convert_angle(starred_nested_well.convergence)
    )
    assert np_is_close(
        starred_nested_well_data['tie_in_tvd'],
        Convertible.convert_z(value=starred_nested_well.tie_in_tvd, measure_units=ft_project.measure_unit),
    )
    assert np_is_close(
        starred_nested_well_data['tie_in_ns'],
        Convertible.convert_xy(value=starred_nested_well.tie_in_ns, measure_units=ft_project.measure_unit),
    )
    assert np_is_close(
        starred_nested_well_data['tie_in_ew'],
        Convertible.convert_xy(value=starred_nested_well.tie_in_ew, measure_units=ft_project.measure_unit),
    )


def test_get_not_converted_foot_nested_well(ft_project):
    starred_nested_well = ft_project.wells.find_by_name(WELL_NAME).starred_nested_well
    assert starred_nested_well is not None

    starred_nested_well_data = starred_nested_well.to_dict(get_converted=False)
    assert starred_nested_well_data

    assert np_is_close(starred_nested_well_data['xsrf'], starred_nested_well.xsrf)
    assert np_is_close(starred_nested_well_data['ysrf'], starred_nested_well.ysrf)
    assert np_is_close(starred_nested_well_data['kb'], starred_nested_well.kb)
    assert np_is_close(starred_nested_well_data['azimuth'], starred_nested_well.azimuth)
    assert np_is_close(starred_nested_well_data['convergence'], starred_nested_well.convergence)
    assert np_is_close(starred_nested_well_data['tie_in_tvd'], starred_nested_well.tie_in_tvd)
    assert np_is_close(starred_nested_well_data['tie_in_ns'], starred_nested_well.tie_in_ns)
    assert np_is_close(starred_nested_well_data['tie_in_ew'], starred_nested_well.tie_in_ew)


def test_get_converted_ftm_nested_well(ftm_project):
    starred_nested_well = ftm_project.wells.find_by_name(WELL_NAME).starred_nested_well
    assert starred_nested_well is not None

    starred_nested_well_data = starred_nested_well.to_dict()
    assert starred_nested_well_data

    assert np_is_close(
        starred_nested_well_data['xsrf'],
        Convertible.convert_xy(
            value=starred_nested_well.xsrf, measure_units=ftm_project.measure_unit, force_to_meters=True
        ),
    )
    assert np_is_close(
        starred_nested_well_data['ysrf'],
        Convertible.convert_xy(
            value=starred_nested_well.ysrf, measure_units=ftm_project.measure_unit, force_to_meters=True
        ),
    )
    assert np_is_close(
        starred_nested_well_data['kb'],
        Convertible.convert_z(value=starred_nested_well.kb, measure_units=ftm_project.measure_unit),
    )
    assert np_is_close(starred_nested_well_data['azimuth'], Convertible.convert_angle(starred_nested_well.azimuth))
    assert np_is_close(
        starred_nested_well_data['convergence'], Convertible.convert_angle(starred_nested_well.convergence)
    )
    assert np_is_close(
        starred_nested_well_data['tie_in_tvd'],
        Convertible.convert_z(value=starred_nested_well.tie_in_tvd, measure_units=ftm_project.measure_unit),
    )
    assert np_is_close(
        starred_nested_well_data['tie_in_ns'],
        Convertible.convert_xy(value=starred_nested_well.tie_in_ns, measure_units=ftm_project.measure_unit),
    )
    assert np_is_close(
        starred_nested_well_data['tie_in_ew'],
        Convertible.convert_xy(value=starred_nested_well.tie_in_ew, measure_units=ftm_project.measure_unit),
    )


def test_get_not_converted_ftm_nested_well(ftm_project):
    starred_nested_well = ftm_project.wells.find_by_name(WELL_NAME).starred_nested_well
    assert starred_nested_well is not None

    starred_nested_well_data = starred_nested_well.to_dict(get_converted=False)
    assert starred_nested_well_data

    assert np_is_close(starred_nested_well_data['xsrf'], starred_nested_well.xsrf)
    assert np_is_close(starred_nested_well_data['ysrf'], starred_nested_well.ysrf)
    assert np_is_close(starred_nested_well_data['kb'], starred_nested_well.kb)
    assert np_is_close(starred_nested_well_data['azimuth'], starred_nested_well.azimuth)
    assert np_is_close(starred_nested_well_data['convergence'], starred_nested_well.convergence)
    assert np_is_close(starred_nested_well_data['tie_in_tvd'], starred_nested_well.tie_in_tvd)
    assert np_is_close(starred_nested_well_data['tie_in_ns'], starred_nested_well.tie_in_ns)
    assert np_is_close(starred_nested_well_data['tie_in_ew'], starred_nested_well.tie_in_ew)


def test_get_converted_meter_horizon(project):
    starred_interpretation = project.wells.find_by_name(WELL_NAME).starred_interpretation
    horizon = starred_interpretation.horizons.find_by_name(HORIZON_NAME)
    assert horizon is not None

    points = horizon.points
    points_data = points.to_dict()
    assert points_data
    assert len(points) == len(points_data)

    measure_units = horizon.interpretation.well.project.measure_unit

    for idx, horizon_trajectory_point in enumerate(points):
        assert np_is_close(
            points_data[idx]['md'],
            Convertible.convert_z(value=horizon_trajectory_point.md, measure_units=measure_units),
        )
        assert np_is_close(
            points_data[idx]['tvd'],
            Convertible.convert_z(value=horizon_trajectory_point.tvd, measure_units=measure_units),
        )


def test_get_not_converted_meter_horizon(project):
    starred_interpretation = project.wells.find_by_name(WELL_NAME).starred_interpretation
    horizon = starred_interpretation.horizons.find_by_name(HORIZON_NAME)
    assert horizon is not None

    points = horizon.points
    points_data = points.to_dict(get_converted=False)
    assert points_data
    assert len(points) == len(points_data)

    for idx, horizon_trajectory_point in enumerate(points):
        assert np_is_close(points_data[idx]['md'], horizon_trajectory_point.md)
        assert np_is_close(points_data[idx]['tvd'], horizon_trajectory_point.tvd)


def test_get_converted_foot_horizon(ft_project):
    starred_interpretation = ft_project.wells.find_by_name(WELL_NAME).starred_interpretation
    horizon = starred_interpretation.horizons.find_by_name(HORIZON_NAME)
    assert horizon is not None

    points = horizon.points
    points_data = points.to_dict()
    assert points_data
    assert len(points) == len(points_data)

    measure_units = horizon.interpretation.well.project.measure_unit

    for idx, horizon_trajectory_point in enumerate(points):
        assert np_is_close(
            points_data[idx]['md'],
            Convertible.convert_z(value=horizon_trajectory_point.md, measure_units=measure_units),
        )
        assert np_is_close(
            points_data[idx]['tvd'],
            Convertible.convert_z(value=horizon_trajectory_point.tvd, measure_units=measure_units),
        )


def test_get_not_converted_foot_horizon(ft_project):
    starred_interpretation = ft_project.wells.find_by_name(WELL_NAME).starred_interpretation
    horizon = starred_interpretation.horizons.find_by_name(HORIZON_NAME)
    assert horizon is not None

    points = horizon.points
    points_data = points.to_dict(get_converted=False)
    assert points_data
    assert len(points) == len(points_data)

    for idx, horizon_trajectory_point in enumerate(points):
        assert np_is_close(points_data[idx]['md'], horizon_trajectory_point.md)
        assert np_is_close(points_data[idx]['tvd'], horizon_trajectory_point.tvd)


def test_get_converted_ftm_horizon(ftm_project):
    starred_interpretation = ftm_project.wells.find_by_name(WELL_NAME).starred_interpretation
    horizon = starred_interpretation.horizons.find_by_name(HORIZON_NAME)
    assert horizon is not None

    points = horizon.points
    points_data = points.to_dict()
    assert points_data
    assert len(points) == len(points_data)

    measure_units = horizon.interpretation.well.project.measure_unit

    for idx, horizon_trajectory_point in enumerate(points):
        assert np_is_close(
            points_data[idx]['md'],
            Convertible.convert_z(value=horizon_trajectory_point.md, measure_units=measure_units),
        )
        assert np_is_close(
            points_data[idx]['tvd'],
            Convertible.convert_z(value=horizon_trajectory_point.tvd, measure_units=measure_units),
        )


def test_get_not_converted_ftm_horizon(ftm_project):
    starred_interpretation = ftm_project.wells.find_by_name(WELL_NAME).starred_interpretation
    horizon = starred_interpretation.horizons.find_by_name(HORIZON_NAME)
    assert horizon is not None

    points = horizon.points
    points_data = points.to_dict(get_converted=False)
    assert points_data
    assert len(points) == len(points_data)

    for idx, horizon_trajectory_point in enumerate(points):
        assert np_is_close(points_data[idx]['md'], horizon_trajectory_point.md)
        assert np_is_close(points_data[idx]['tvd'], horizon_trajectory_point.tvd)


def test_get_converted_meter_nested_well_trajectory(project):
    starred_nested_well = project.wells.find_by_name(WELL_NAME).starred_nested_well
    assert starred_nested_well is not None

    trajectory = starred_nested_well.trajectory
    trajectory_data = trajectory.to_dict()
    assert trajectory_data
    assert len(trajectory) == len(trajectory_data)

    for idx, trajectory_point in enumerate(trajectory):
        assert np_is_close(
            trajectory_data[idx]['md'],
            Convertible.convert_z(
                value=trajectory_point.md, measure_units=starred_nested_well.well.project.measure_unit
            ),
        )
        assert np_is_close(trajectory_data[idx]['incl'], Convertible.convert_angle(trajectory_point.incl))
        assert np_is_close(trajectory_data[idx]['azim'], Convertible.convert_angle(trajectory_point.azim))


def test_get_not_converted_meter_nested_well_trajectory(project):
    starred_nested_well = project.wells.find_by_name(WELL_NAME).starred_nested_well
    assert starred_nested_well is not None

    trajectory = starred_nested_well.trajectory
    trajectory_data = trajectory.to_dict(get_converted=False)
    assert trajectory_data
    assert len(trajectory) == len(trajectory_data)

    for idx, trajectory_point in enumerate(trajectory):
        assert np_is_close(trajectory_data[idx]['md'], trajectory_point.md)
        assert np_is_close(trajectory_data[idx]['incl'], trajectory_point.incl)
        assert np_is_close(trajectory_data[idx]['azim'], trajectory_point.azim)


def test_get_converted_foot_nested_well_trajectory(ft_project):
    starred_nested_well = ft_project.wells.find_by_name(WELL_NAME).starred_nested_well
    assert starred_nested_well is not None

    trajectory = starred_nested_well.trajectory
    trajectory_data = trajectory.to_dict()
    assert trajectory_data
    assert len(trajectory) == len(trajectory_data)

    for idx, trajectory_point in enumerate(trajectory):
        assert np_is_close(
            trajectory_data[idx]['md'],
            Convertible.convert_z(
                value=trajectory_point.md, measure_units=starred_nested_well.well.project.measure_unit
            ),
        )
        assert np_is_close(trajectory_data[idx]['incl'], Convertible.convert_angle(trajectory_point.incl))
        assert np_is_close(trajectory_data[idx]['azim'], Convertible.convert_angle(trajectory_point.azim))


def test_get_not_converted_foot_nested_well_trajectory(ft_project):
    starred_nested_well = ft_project.wells.find_by_name(WELL_NAME).starred_nested_well
    assert starred_nested_well is not None

    trajectory = starred_nested_well.trajectory
    trajectory_data = trajectory.to_dict(get_converted=False)
    assert trajectory_data
    assert len(trajectory) == len(trajectory_data)

    for idx, trajectory_point in enumerate(trajectory):
        assert np_is_close(trajectory_data[idx]['md'], trajectory_point.md)
        assert np_is_close(trajectory_data[idx]['incl'], trajectory_point.incl)
        assert np_is_close(trajectory_data[idx]['azim'], trajectory_point.azim)


def test_get_converted_ftm_nested_well_trajectory(ftm_project):
    starred_nested_well = ftm_project.wells.find_by_name(WELL_NAME).starred_nested_well
    assert starred_nested_well is not None

    trajectory = starred_nested_well.trajectory
    trajectory_data = trajectory.to_dict()
    assert trajectory_data
    assert len(trajectory) == len(trajectory_data)

    for idx, trajectory_point in enumerate(trajectory):
        assert np_is_close(
            trajectory_data[idx]['md'],
            Convertible.convert_z(
                value=trajectory_point.md, measure_units=starred_nested_well.well.project.measure_unit
            ),
        )
        assert np_is_close(trajectory_data[idx]['incl'], Convertible.convert_angle(trajectory_point.incl))
        assert np_is_close(trajectory_data[idx]['azim'], Convertible.convert_angle(trajectory_point.azim))


def test_get_not_converted_ftm_nested_well_trajectory(ftm_project):
    starred_nested_well = ftm_project.wells.find_by_name(WELL_NAME).starred_nested_well
    assert starred_nested_well is not None

    trajectory = starred_nested_well.trajectory
    trajectory_data = trajectory.to_dict(get_converted=False)
    assert trajectory_data
    assert len(trajectory) == len(trajectory_data)

    for idx, trajectory_point in enumerate(trajectory):
        assert np_is_close(trajectory_data[idx]['md'], trajectory_point.md)
        assert np_is_close(trajectory_data[idx]['incl'], trajectory_point.incl)
        assert np_is_close(trajectory_data[idx]['azim'], trajectory_point.azim)


def test_get_converted_meter_log(project):
    log = project.wells.find_by_name(WELL_NAME).logs.find_by_name(LOG_NAME)
    assert log is not None

    points = log.points
    points_data = points.to_dict()
    assert points_data
    assert len(points) == len(points_data)

    measure_units = log.well.project.measure_unit

    for idx, log_point in enumerate(points):
        assert np_is_close(
            points_data[idx]['md'], Convertible.convert_z(value=log_point.md, measure_units=measure_units)
        )


def test_get_not_converted_meter_log(project):
    log = project.wells.find_by_name(WELL_NAME).logs.find_by_name(LOG_NAME)
    assert log is not None

    points = log.points
    points_data = points.to_dict(get_converted=False)
    assert points_data
    assert len(points) == len(points_data)

    for idx, log_point in enumerate(points):
        assert np_is_close(points_data[idx]['md'], log_point.md)


def test_get_converted_foot_log(ft_project):
    log = ft_project.wells.find_by_name(WELL_NAME).logs.find_by_name(LOG_NAME)
    assert log is not None

    points = log.points
    points_data = points.to_dict()
    assert points_data
    assert len(points) == len(points_data)

    measure_units = log.well.project.measure_unit

    for idx, log_point in enumerate(points):
        assert np_is_close(
            points_data[idx]['md'], Convertible.convert_z(value=log_point.md, measure_units=measure_units)
        )


def test_get_not_converted_foot_log(ft_project):
    log = ft_project.wells.find_by_name(WELL_NAME).logs.find_by_name(LOG_NAME)
    assert log is not None

    points = log.points
    points_data = points.to_dict(get_converted=False)
    assert points_data
    assert len(points) == len(points_data)

    for idx, log_point in enumerate(points):
        assert np_is_close(points_data[idx]['md'], log_point.md)


def test_get_converted_ftm_log(ftm_project):
    log = ftm_project.wells.find_by_name(WELL_NAME).logs.find_by_name(LOG_NAME)
    assert log is not None

    points = log.points
    points_data = points.to_dict()
    assert points_data
    assert len(points) == len(points_data)

    measure_units = log.well.project.measure_unit

    for idx, log_point in enumerate(points):
        assert np_is_close(
            points_data[idx]['md'], Convertible.convert_z(value=log_point.md, measure_units=measure_units)
        )


def test_get_not_converted_ftm_log(ftm_project):
    log = ftm_project.wells.find_by_name(WELL_NAME).logs.find_by_name(LOG_NAME)
    assert log is not None

    points = log.points
    points_data = points.to_dict(get_converted=False)
    assert points_data
    assert len(points) == len(points_data)

    for idx, log_point in enumerate(points):
        assert np_is_close(points_data[idx]['md'], log_point.md)


def test_get_converted_meter_typewell(project):
    typewell = project.typewells.find_by_name(TYPEWELL_NAME)
    assert typewell is not None

    typewell_data = typewell.to_dict()
    assert typewell_data

    assert np_is_close(
        typewell_data['xsrf'],
        Convertible.convert_xy(value=typewell.xsrf, measure_units=project.measure_unit, force_to_meters=True),
    )
    assert np_is_close(
        typewell_data['ysrf'],
        Convertible.convert_xy(value=typewell.ysrf, measure_units=project.measure_unit, force_to_meters=True),
    )
    assert np_is_close(
        typewell_data['kb'], Convertible.convert_z(value=typewell.kb, measure_units=project.measure_unit)
    )
    assert np_is_close(typewell_data['convergence'], Convertible.convert_angle(typewell.convergence))
    assert np_is_close(
        typewell_data['tie_in_tvd'],
        Convertible.convert_z(value=typewell.tie_in_tvd, measure_units=project.measure_unit),
    )
    assert np_is_close(
        typewell_data['tie_in_ns'], Convertible.convert_xy(value=typewell.tie_in_ns, measure_units=project.measure_unit)
    )
    assert np_is_close(
        typewell_data['tie_in_ew'], Convertible.convert_xy(value=typewell.tie_in_ew, measure_units=project.measure_unit)
    )


def test_get_not_converted_meter_typewell(project):
    typewell = project.typewells.find_by_name(TYPEWELL_NAME)
    assert typewell is not None

    typewell_data = typewell.to_dict(get_converted=False)
    assert typewell_data

    assert np_is_close(typewell_data['xsrf'], typewell.xsrf)
    assert np_is_close(typewell_data['ysrf'], typewell.ysrf)
    assert np_is_close(typewell_data['kb'], typewell.kb)
    assert np_is_close(typewell_data['convergence'], typewell.convergence)
    assert np_is_close(typewell_data['tie_in_tvd'], typewell.tie_in_tvd)
    assert np_is_close(typewell_data['tie_in_ns'], typewell.tie_in_ns)
    assert np_is_close(typewell_data['tie_in_ew'], typewell.tie_in_ew)


def test_get_converted_foot_typewell(ft_project):
    typewell = ft_project.typewells.find_by_name(TYPEWELL_NAME)
    assert typewell is not None

    typewell_data = typewell.to_dict()
    assert typewell_data

    assert np_is_close(
        typewell_data['xsrf'],
        Convertible.convert_xy(value=typewell.xsrf, measure_units=ft_project.measure_unit, force_to_meters=True),
    )
    assert np_is_close(
        typewell_data['ysrf'],
        Convertible.convert_xy(value=typewell.ysrf, measure_units=ft_project.measure_unit, force_to_meters=True),
    )
    assert np_is_close(
        typewell_data['kb'], Convertible.convert_z(value=typewell.kb, measure_units=ft_project.measure_unit)
    )
    assert np_is_close(typewell_data['convergence'], Convertible.convert_angle(typewell.convergence))
    assert np_is_close(
        typewell_data['tie_in_tvd'],
        Convertible.convert_z(value=typewell.tie_in_tvd, measure_units=ft_project.measure_unit),
    )
    assert np_is_close(
        typewell_data['tie_in_ns'],
        Convertible.convert_xy(value=typewell.tie_in_ns, measure_units=ft_project.measure_unit),
    )
    assert np_is_close(
        typewell_data['tie_in_ew'],
        Convertible.convert_xy(value=typewell.tie_in_ew, measure_units=ft_project.measure_unit),
    )


def test_get_not_converted_foot_typewell(ft_project):
    typewell = ft_project.typewells.find_by_name(TYPEWELL_NAME)
    assert typewell is not None

    typewell_data = typewell.to_dict(get_converted=False)
    assert typewell_data

    assert np_is_close(typewell_data['xsrf'], typewell.xsrf)
    assert np_is_close(typewell_data['ysrf'], typewell.ysrf)
    assert np_is_close(typewell_data['kb'], typewell.kb)
    assert np_is_close(typewell_data['convergence'], typewell.convergence)
    assert np_is_close(typewell_data['tie_in_tvd'], typewell.tie_in_tvd)
    assert np_is_close(typewell_data['tie_in_ns'], typewell.tie_in_ns)
    assert np_is_close(typewell_data['tie_in_ew'], typewell.tie_in_ew)


def test_get_converted_ftm_typewell(ftm_project):
    typewell = ftm_project.typewells.find_by_name(TYPEWELL_NAME)
    assert typewell is not None

    typewell_data = typewell.to_dict()
    assert typewell_data

    assert np_is_close(
        typewell_data['xsrf'],
        Convertible.convert_xy(value=typewell.xsrf, measure_units=ftm_project.measure_unit, force_to_meters=True),
    )
    assert np_is_close(
        typewell_data['ysrf'],
        Convertible.convert_xy(value=typewell.ysrf, measure_units=ftm_project.measure_unit, force_to_meters=True),
    )
    assert np_is_close(
        typewell_data['kb'], Convertible.convert_z(value=typewell.kb, measure_units=ftm_project.measure_unit)
    )
    assert np_is_close(typewell_data['convergence'], Convertible.convert_angle(typewell.convergence))
    assert np_is_close(
        typewell_data['tie_in_tvd'],
        Convertible.convert_z(value=typewell.tie_in_tvd, measure_units=ftm_project.measure_unit),
    )
    assert np_is_close(
        typewell_data['tie_in_ns'],
        Convertible.convert_xy(value=typewell.tie_in_ns, measure_units=ftm_project.measure_unit),
    )
    assert np_is_close(
        typewell_data['tie_in_ew'],
        Convertible.convert_xy(value=typewell.tie_in_ew, measure_units=ftm_project.measure_unit),
    )


def test_get_not_converted_ftm_typewell(ftm_project):
    typewell = ftm_project.typewells.find_by_name(TYPEWELL_NAME)
    assert typewell is not None

    typewell_data = typewell.to_dict(get_converted=False)
    assert typewell_data

    assert np_is_close(typewell_data['xsrf'], typewell.xsrf)
    assert np_is_close(typewell_data['ysrf'], typewell.ysrf)
    assert np_is_close(typewell_data['kb'], typewell.kb)
    assert np_is_close(typewell_data['convergence'], typewell.convergence)
    assert np_is_close(typewell_data['tie_in_tvd'], typewell.tie_in_tvd)
    assert np_is_close(typewell_data['tie_in_ns'], typewell.tie_in_ns)
    assert np_is_close(typewell_data['tie_in_ew'], typewell.tie_in_ew)


def test_get_converted_meter_top(project):
    starred_topset = project.wells.find_by_name(WELL_NAME).starred_topset
    assert starred_topset is not None

    starred_top_center = starred_topset.starred_top_center
    assert starred_top_center

    starred_top_center_data = starred_top_center.to_dict()
    assert starred_top_center_data

    assert np_is_close(starred_top_center_data['md'], starred_top_center.md)


def test_get_not_converted_meter_top(project):
    starred_topset = project.wells.find_by_name(WELL_NAME).starred_topset
    assert starred_topset is not None

    starred_top_center = starred_topset.starred_top_center
    assert starred_top_center

    starred_top_center_data = starred_top_center.to_dict(get_converted=False)
    assert starred_top_center_data

    assert np_is_close(starred_top_center_data['md'], feet_to_meters(starred_top_center.md))


def test_get_converted_foot_top(ft_project):
    starred_topset = ft_project.wells.find_by_name(WELL_NAME).starred_topset
    assert starred_topset is not None

    starred_top_center = starred_topset.starred_top_center
    assert starred_top_center

    starred_top_center_data = starred_top_center.to_dict()
    assert starred_top_center_data

    assert np_is_close(starred_top_center_data['md'], starred_top_center.md)


def test_get_not_converted_foot_top(ft_project):
    starred_topset = ft_project.wells.find_by_name(WELL_NAME).starred_topset
    assert starred_topset is not None

    starred_top_center = starred_topset.starred_top_center
    assert starred_top_center

    starred_top_center_data = starred_top_center.to_dict(get_converted=False)
    assert starred_top_center_data

    assert np_is_close(starred_top_center_data['md'], feet_to_meters(starred_top_center.md))


def test_get_converted_ftm_top(ftm_project):
    starred_topset = ftm_project.wells.find_by_name(WELL_NAME).starred_topset
    assert starred_topset is not None

    starred_top_center = starred_topset.starred_top_center
    assert starred_top_center

    starred_top_center_data = starred_top_center.to_dict()
    assert starred_top_center_data

    assert np_is_close(starred_top_center_data['md'], starred_top_center.md)


def test_get_not_converted_ftm_top(ftm_project):
    starred_topset = ftm_project.wells.find_by_name(WELL_NAME).starred_topset
    assert starred_topset is not None

    starred_top_center = starred_topset.starred_top_center
    assert starred_top_center

    starred_top_center_data = starred_top_center.to_dict(get_converted=False)
    assert starred_top_center_data

    assert np_is_close(starred_top_center_data['md'], feet_to_meters(starred_top_center.md))


def test_get_converted_meter_earth_model(project):
    starred_interpretation = project.wells.find_by_name(WELL_NAME).starred_interpretation
    earth_model = starred_interpretation.earth_models.find_by_name(EARTH_MODEL_NAME)
    assert earth_model is not None

    sections = earth_model.sections
    sections_data = sections.to_dict()
    assert sections_data
    assert len(sections) == len(sections_data)

    measure_units = earth_model.interpretation.well.project.measure_unit

    for idx, section in enumerate(sections):
        assert np_is_close(
            sections_data[idx]['md'],
            Convertible.convert_z(value=section.md, measure_units=measure_units),
        )

    layers = sections[0].layers
    layers_data = layers.to_dict()
    assert layers_data
    assert len(layers) == len(layers_data)

    for idx, layer in enumerate(layers):
        # Must be changed when public method with layer tvd is available
        assert np_is_close(layers_data[idx]['tvt'], Convertible.convert_z(value=layer.tvt, measure_units=measure_units))


def test_get_not_converted_meter_earth_model(project):
    starred_interpretation = project.wells.find_by_name(WELL_NAME).starred_interpretation
    earth_model = starred_interpretation.earth_models.find_by_name(EARTH_MODEL_NAME)
    assert earth_model is not None

    sections = earth_model.sections
    sections_data = sections.to_dict(get_converted=False)
    assert sections_data
    assert len(sections) == len(sections_data)

    for idx, section in enumerate(sections):
        assert np_is_close(sections_data[idx]['md'], section.md)

    layers = sections[0].layers
    layers_data = layers.to_dict(get_converted=False)
    assert layers_data
    assert len(layers) == len(layers_data)

    for idx, layer in enumerate(layers):
        # Must be changed when public method with layer tvd is available
        assert np_is_close(layers_data[idx]['tvt'], layer.tvt)


def test_get_converted_foot_earth_model(ft_project):
    starred_interpretation = ft_project.wells.find_by_name(WELL_NAME).starred_interpretation
    earth_model = starred_interpretation.earth_models.find_by_name(EARTH_MODEL_NAME)
    assert earth_model is not None

    sections = earth_model.sections
    sections_data = sections.to_dict()
    assert sections_data
    assert len(sections) == len(sections_data)

    measure_units = earth_model.interpretation.well.project.measure_unit

    for idx, section in enumerate(sections):
        assert np_is_close(
            sections_data[idx]['md'],
            Convertible.convert_z(value=section.md, measure_units=measure_units),
        )

    layers = sections[0].layers
    layers_data = layers.to_dict()
    assert layers_data
    assert len(layers) == len(layers_data)

    for idx, layer in enumerate(layers):
        # Must be changed when public method with layer tvd is available
        assert np_is_close(layers_data[idx]['tvt'], Convertible.convert_z(value=layer.tvt, measure_units=measure_units))


def test_get_not_converted_foot_earth_model(ft_project):
    starred_interpretation = ft_project.wells.find_by_name(WELL_NAME).starred_interpretation
    earth_model = starred_interpretation.earth_models.find_by_name(EARTH_MODEL_NAME)
    assert earth_model is not None

    sections = earth_model.sections
    sections_data = sections.to_dict(get_converted=False)
    assert sections_data
    assert len(sections) == len(sections_data)

    for idx, section in enumerate(sections):
        assert np_is_close(sections_data[idx]['md'], section.md)

    layers = sections[0].layers
    layers_data = layers.to_dict(get_converted=False)
    assert layers_data
    assert len(layers) == len(layers_data)

    for idx, layer in enumerate(layers):
        # Must be changed when public method with layer tvd is available
        assert np_is_close(layers_data[idx]['tvt'], layer.tvt)


def test_get_converted_ftm_earth_model(ftm_project):
    starred_interpretation = ftm_project.wells.find_by_name(WELL_NAME).starred_interpretation
    earth_model = starred_interpretation.earth_models.find_by_name(EARTH_MODEL_NAME)
    assert earth_model is not None

    sections = earth_model.sections
    sections_data = sections.to_dict()
    assert sections_data
    assert len(sections) == len(sections_data)

    measure_units = earth_model.interpretation.well.project.measure_unit

    for idx, section in enumerate(sections):
        assert np_is_close(
            sections_data[idx]['md'],
            Convertible.convert_z(value=section.md, measure_units=measure_units),
        )

    layers = sections[0].layers
    layers_data = layers.to_dict()
    assert layers_data
    assert len(layers) == len(layers_data)

    for idx, layer in enumerate(layers):
        # Must be changed when public method with layer tvd is available
        assert np_is_close(layers_data[idx]['tvt'], Convertible.convert_z(value=layer.tvt, measure_units=measure_units))


def test_get_not_converted_ftm_earth_model(ftm_project):
    starred_interpretation = ftm_project.wells.find_by_name(WELL_NAME).starred_interpretation
    earth_model = starred_interpretation.earth_models.find_by_name(EARTH_MODEL_NAME)
    assert earth_model is not None

    sections = earth_model.sections
    sections_data = sections.to_dict(get_converted=False)
    assert sections_data
    assert len(sections) == len(sections_data)

    for idx, section in enumerate(sections):
        assert np_is_close(sections_data[idx]['md'], section.md)

    layers = sections[0].layers
    layers_data = layers.to_dict(get_converted=False)
    assert layers_data
    assert len(layers) == len(layers_data)

    for idx, layer in enumerate(layers):
        # Must be changed when public method with layer tvd is available
        assert np_is_close(layers_data[idx]['tvt'], layer.tvt)


def test_get_converted_meter_well_attributes(project):
    well = project.wells.find_by_name(WELL_NAME)
    assert well is not None

    well_data = well.to_dict()
    assert well_data

    attributes = well.attributes
    assert attributes is not None

    attributes_data = attributes.to_dict()
    assert attributes_data

    assert np_is_close(well_data['kb'], attributes_data['KB'])
    assert np_is_close(well_data['azimuth'], attributes_data['Azimuth VS'])
    assert np_is_close(well_data['convergence'], attributes_data['Convergence'])
    assert np_is_close(well_data['xsrf_real'], attributes_data['X-srf'])
    assert np_is_close(well_data['ysrf_real'], attributes_data['Y-srf'])


def test_get_not_converted_meter_well_attributes(project):
    well = project.wells.find_by_name(WELL_NAME)
    assert well is not None

    well_data = well.to_dict(get_converted=False)
    assert well_data

    attributes = well.attributes
    assert attributes is not None

    attributes_data = attributes.to_dict(get_converted=False)
    assert attributes_data

    assert np_is_close(well_data['kb'], attributes_data['KB'])
    assert np_is_close(well_data['azimuth'], attributes_data['Azimuth VS'])
    assert np_is_close(well_data['convergence'], attributes_data['Convergence'])
    assert np_is_close(well_data['xsrf_real'], attributes_data['X-srf'])
    assert np_is_close(well_data['ysrf_real'], attributes_data['Y-srf'])


def test_get_converted_foot_well_attributes(ft_project):
    well = ft_project.wells.find_by_name(WELL_NAME)
    assert well is not None

    well_data = well.to_dict()
    assert well_data

    attributes = well.attributes
    assert attributes is not None

    attributes_data = attributes.to_dict()
    assert attributes_data

    assert np_is_close(well_data['kb'], attributes_data['KB'])
    assert np_is_close(well_data['azimuth'], attributes_data['Azimuth VS'])
    assert np_is_close(well_data['convergence'], attributes_data['Convergence'])
    assert np_is_close(well_data['xsrf_real'], attributes_data['X-srf'])
    assert np_is_close(well_data['ysrf_real'], attributes_data['Y-srf'])


def test_get_not_converted_foot_well_attributes(ft_project):
    well = ft_project.wells.find_by_name(WELL_NAME)
    assert well is not None

    well_data = well.to_dict(get_converted=False)
    assert well_data

    attributes = well.attributes
    assert attributes is not None

    attributes_data = attributes.to_dict(get_converted=False)
    assert attributes_data

    assert np_is_close(well_data['kb'], attributes_data['KB'])
    assert np_is_close(well_data['azimuth'], attributes_data['Azimuth VS'])
    assert np_is_close(well_data['convergence'], attributes_data['Convergence'])
    assert np_is_close(well_data['xsrf_real'], attributes_data['X-srf'])
    assert np_is_close(well_data['ysrf_real'], attributes_data['Y-srf'])


def test_get_converted_ftm_well_attributes(ftm_project):
    well = ftm_project.wells.find_by_name(WELL_NAME)
    assert well is not None

    well_data = well.to_dict()
    assert well_data

    attributes = well.attributes
    assert attributes is not None

    attributes_data = attributes.to_dict()
    assert attributes_data

    assert np_is_close(well_data['kb'], attributes_data['KB'])
    assert np_is_close(well_data['azimuth'], attributes_data['Azimuth VS'])
    assert np_is_close(well_data['convergence'], attributes_data['Convergence'])
    assert np_is_close(well_data['xsrf_real'], attributes_data['X-srf'])
    assert np_is_close(well_data['ysrf_real'], attributes_data['Y-srf'])


def test_get_not_converted_ftm_well_attributes(ftm_project):
    well = ftm_project.wells.find_by_name(WELL_NAME)
    assert well is not None

    well_data = well.to_dict(get_converted=False)
    assert well_data

    attributes = well.attributes
    assert attributes is not None

    attributes_data = attributes.to_dict(get_converted=False)
    assert attributes_data

    assert np_is_close(well_data['kb'], attributes_data['KB'])
    assert np_is_close(well_data['azimuth'], attributes_data['Azimuth VS'])
    assert np_is_close(well_data['convergence'], attributes_data['Convergence'])
    assert np_is_close(well_data['xsrf_real'], attributes_data['X-srf'])
    assert np_is_close(well_data['ysrf_real'], attributes_data['Y-srf'])


def test_get_converted_meter_comment_box(project):
    well = project.wells.find_by_name(WELL_NAME)
    assert well is not None

    comments = well.comments
    assert comments is not None

    comment_box = comments[0].comment_boxes[0]
    assert comment_box is not None

    comment_box_data = comment_box.to_dict()
    assert comment_box_data

    assert np_is_close(
        comment_box_data['anchor_md'],
        Convertible.convert_z(value=comment_box.anchor_md, measure_units=project.measure_unit),
    )


def test_get_not_converted_meter_comment_box(project):
    well = project.wells.find_by_name(WELL_NAME)
    assert well is not None

    comments = well.comments
    assert comments is not None

    comment_box = comments[0].comment_boxes[0]
    assert comment_box is not None

    comment_box_data = comment_box.to_dict(get_converted=False)
    assert comment_box_data

    assert np_is_close(comment_box_data['anchor_md'], comment_box.anchor_md)


def test_get_converted_ft_comment_box(ft_project):
    well = ft_project.wells.find_by_name(WELL_NAME)
    assert well is not None

    comments = well.comments
    assert comments is not None

    comment_box = comments[0].comment_boxes[0]
    assert comment_box is not None

    comment_box_data = comment_box.to_dict()
    assert comment_box_data

    assert np_is_close(
        comment_box_data['anchor_md'],
        Convertible.convert_z(value=comment_box.anchor_md, measure_units=ft_project.measure_unit),
    )


def test_get_not_converted_ft_comment_box(ft_project):
    well = ft_project.wells.find_by_name(WELL_NAME)
    assert well is not None

    comments = well.comments
    assert comments is not None

    comment_box = comments[0].comment_boxes[0]
    assert comment_box is not None

    comment_box_data = comment_box.to_dict(get_converted=False)
    assert comment_box_data

    assert np_is_close(comment_box_data['anchor_md'], comment_box.anchor_md)


def test_get_converted_ftm_comment_box(ftm_project):
    well = ftm_project.wells.find_by_name(WELL_NAME)
    assert well is not None

    comments = well.comments
    assert comments is not None

    comment_box = comments[0].comment_boxes[0]
    assert comment_box is not None

    comment_box_data = comment_box.to_dict()
    assert comment_box_data

    assert np_is_close(
        comment_box_data['anchor_md'],
        Convertible.convert_z(value=comment_box.anchor_md, measure_units=ftm_project.measure_unit),
    )


def test_get_not_converted_ftm_comment_box(ftm_project):
    well = ftm_project.wells.find_by_name(WELL_NAME)
    assert well is not None

    comments = well.comments
    assert comments is not None

    comment_box = comments[0].comment_boxes[0]
    assert comment_box is not None

    comment_box_data = comment_box.to_dict(get_converted=False)
    assert comment_box_data

    assert np_is_close(comment_box_data['anchor_md'], comment_box.anchor_md)
