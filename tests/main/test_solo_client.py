from math import fabs

import pytest

from rogii_solo.calculations.interpretation import get_last_segment_dip
from rogii_solo.exceptions import InvalidProjectException, ProjectNotFoundException
from tests.papi_data import (
    EARTH_MODEL_NAME,
    EI_ABSENT_HORIZONS_LAST_SEGMENT_OUT_ID,
    EI_ALL_SEGMENTS_OUT_ID,
    EI_LAST_SEGMENT_EXTENDED_ID,
    EI_LAST_SEGMENT_OUT_ID,
    HORIZON_NAME,
    INTERPRETATION_LAST_SEGMENT_ONE_POINT_ABSENT_HORIZONS_ID,
    INTERPRETATION_LAST_SEGMENT_ONE_POINT_ID,
    INTERPRETATION_NAME,
    LOG_NAME,
    METER_PROJECT_NAME,
    MUDLOG_NAME,
    NESTED_WELL_NAME,
    STARRED_HORIZON_BOTTOM_NAME,
    STARRED_HORIZON_CENTER_NAME,
    STARRED_HORIZON_TOP_NAME,
    STARRED_INTERPRETATION_NAME,
    STARRED_NESTED_WELL_NAME,
    STARRED_TARGET_LINE_NAME,
    STARRED_TOP_BOTTOM_NAME,
    STARRED_TOP_CENTER_NAME,
    STARRED_TOP_TOP_NAME,
    STARRED_TOPSET_NAME,
    TARGET_LINE_NAME,
    TYPEWELL_NAME,
    WELL_NAME,
)

DELTA_EI_DIP = 0.001


def test_get_projects(solo_client):
    projects_data = solo_client.projects.to_dict()
    projects_df = solo_client.projects.to_df()

    assert projects_data
    assert not projects_df.empty


def test_set_non_existent_project(solo_client):
    with pytest.raises(ProjectNotFoundException):
        solo_client.set_project_by_name('Non-existent project')


def test_set_none_project(solo_client):
    with pytest.raises(ProjectNotFoundException):
        solo_client.set_project_by_name(None)


def test_set_invalid_project(solo_client):
    with pytest.raises(InvalidProjectException):
        solo_client.set_project({})


def test_set_project(project):
    assert project is not None

    project_data = project.to_dict()
    project_df = project.to_df()

    assert project_data['name'] == METER_PROJECT_NAME
    assert project_df.at[0, 'name'] == METER_PROJECT_NAME


def test_get_project_wells(project):
    wells_data = project.wells.to_dict()
    wells_df = project.wells.to_df()

    assert wells_data
    assert not wells_df.empty


def test_get_well(project):
    well = project.wells.find_by_name(WELL_NAME)

    assert well is not None

    well_data = well.to_dict()
    well_df = well.to_df()

    assert well_data['name'] == WELL_NAME
    assert well_df.at[0, 'name'] == WELL_NAME


def test_get_well_trajectory(project):
    trajectory = project.wells.find_by_name(WELL_NAME).trajectory

    trajectory_data = trajectory.to_dict()
    trajectory_df = trajectory.to_df()

    assert trajectory_data
    assert not trajectory_df.empty


def test_get_well_interpretations(project):
    interpretations = project.wells.find_by_name(WELL_NAME).interpretations

    interpretations_data = interpretations.to_dict()
    interpretations_df = interpretations.to_df()

    assert interpretations_data
    assert not interpretations_df.empty


def test_get_well_interpretation(project):
    interpretation = project.wells.find_by_name(WELL_NAME).interpretations.find_by_name(INTERPRETATION_NAME)

    assert interpretation is not None

    interpretation_data = interpretation.to_dict()
    interpretation_df = interpretation.to_df()

    assert 'meta' in interpretation_data
    assert 'horizons' in interpretation_data
    assert 'segments' in interpretation_data

    assert interpretation_data['meta']['name'] == INTERPRETATION_NAME
    assert interpretation_df['meta'].at[0, 'name'] == INTERPRETATION_NAME


def test_get_well_starred_interpretation(project):
    starred_interpretation = project.wells.find_by_name(WELL_NAME).starred_interpretation

    assert starred_interpretation is not None

    starred_interpretation_data = starred_interpretation.to_dict()
    starred_interpretation_df = starred_interpretation.to_df()

    assert 'meta' in starred_interpretation_data
    assert 'horizons' in starred_interpretation_data
    assert 'segments' in starred_interpretation_data

    assert starred_interpretation_data['meta']['name'] == STARRED_INTERPRETATION_NAME
    assert starred_interpretation_df['meta'].at[0, 'name'] == STARRED_INTERPRETATION_NAME


def test_get_horizon(project):
    starred_interpretation = project.wells.find_by_name(WELL_NAME).starred_interpretation
    horizon = starred_interpretation.horizons.find_by_name(HORIZON_NAME)

    assert horizon is not None

    horizon_data = horizon.to_dict()
    horizon_df = horizon.to_df()

    assert 'uuid' in horizon_data
    assert 'name' in horizon_data
    assert horizon_data['uuid'] == horizon_df.at[0, 'uuid']
    assert horizon_data['name'] == horizon_df.at[0, 'name']

    assert horizon_data['name'] == HORIZON_NAME


def test_get_well_target_lines(project):
    target_lines = project.wells.find_by_name(WELL_NAME).target_lines

    target_lines_data = target_lines.to_dict()
    target_lines_df = target_lines.to_df()

    assert target_lines_data
    assert not target_lines_df.empty


def test_get_well_target_line(project):
    target_line = project.wells.find_by_name(WELL_NAME).target_lines.find_by_name(TARGET_LINE_NAME)

    assert target_line is not None

    target_line_data = target_line.to_dict()
    target_line_df = target_line.to_df()

    assert target_line_data['name'] == TARGET_LINE_NAME
    assert target_line_df.at[0, 'name'] == TARGET_LINE_NAME


def test_get_well_starred_target_line(project):
    starred_target_line = project.wells.find_by_name(WELL_NAME).starred_target_line

    assert starred_target_line is not None

    starred_target_line_data = starred_target_line.to_dict()
    starred_target_line_df = starred_target_line.to_df()

    assert starred_target_line_data['name'] == STARRED_TARGET_LINE_NAME
    assert starred_target_line_df.at[0, 'name'] == STARRED_TARGET_LINE_NAME


def test_get_well_nested_wells(project):
    nested_wells = project.wells.find_by_name(WELL_NAME).nested_wells

    nested_wells_data = nested_wells.to_dict()
    nested_wells_df = nested_wells.to_df()

    assert nested_wells_data
    assert not nested_wells_df.empty


def test_get_well_nested_well(project):
    nested_well = project.wells.find_by_name(WELL_NAME).nested_wells.find_by_name(NESTED_WELL_NAME)

    assert nested_well is not None

    nested_well_data = nested_well.to_dict()
    nested_well_df = nested_well.to_df()

    assert nested_well_data['name'] == NESTED_WELL_NAME
    assert nested_well_df.at[0, 'name'] == NESTED_WELL_NAME


def test_get_well_starred_nested_well(project):
    starred_nested_well = project.wells.find_by_name(WELL_NAME).starred_nested_well

    assert starred_nested_well is not None

    starred_nested_well_data = starred_nested_well.to_dict()
    starred_nested_well_df = starred_nested_well.to_df()

    assert starred_nested_well_data['name'] == STARRED_NESTED_WELL_NAME
    assert starred_nested_well_df.at[0, 'name'] == STARRED_NESTED_WELL_NAME


def test_get_nested_well_trajectory(project):
    starred_nested_well = project.wells.find_by_name(WELL_NAME).starred_nested_well

    assert starred_nested_well is not None

    trajectory = starred_nested_well.trajectory

    trajectory_data = trajectory.to_dict()
    trajectory_df = trajectory.to_df()

    assert trajectory_data
    assert not trajectory_df.empty


def test_get_log(project):
    logs = project.wells.find_by_name(WELL_NAME).logs
    log = logs.find_by_name(LOG_NAME)

    assert log is not None

    log_data = log.to_dict()
    log_df = log.to_df()

    assert 'uuid' in log_data
    assert 'name' in log_data
    assert log_data['uuid'] == log_df.at[0, 'uuid']
    assert log_data['name'] == log_df.at[0, 'name']

    assert log_data['name'] == LOG_NAME
    assert log_df.at[0, 'name'] == LOG_NAME


def test_get_project_typewells(project):
    typewells_data = project.typewells.to_dict()
    typewells_df = project.typewells.to_df()

    assert typewells_data
    assert not typewells_df.empty

    assert typewells_data[0]['uuid'] == typewells_df.at[0, 'uuid']
    assert typewells_data[0]['name'] == typewells_df.at[0, 'name']


def test_get_typewell(project):
    typewell = project.typewells.find_by_name(TYPEWELL_NAME)

    assert typewell is not None

    typewell_data = typewell.to_dict()
    typewell_df = typewell.to_df()

    assert typewell_data['name'] == TYPEWELL_NAME
    assert typewell_df.at[0, 'name'] == TYPEWELL_NAME


def test_get_typewell_trajectory(project):
    trajectory = project.typewells.find_by_name(TYPEWELL_NAME).trajectory

    trajectory_data = trajectory.to_dict()
    trajectory_df = trajectory.to_df()

    assert trajectory_data
    assert not trajectory_df.empty


def test_get_topset_tops(project):
    well = project.wells.find_by_name(WELL_NAME)

    assert well is not None

    topset = well.topsets.find_by_name(STARRED_TOPSET_NAME)

    assert topset is not None

    tops = topset.tops

    assert tops is not None

    tops_data = tops.to_dict()
    tops_df = tops.to_df()

    assert tops_data
    assert not tops_df.empty


def test_get_interpretation_starred_horizons(project):
    starred_interpretation = project.wells.find_by_name(WELL_NAME).starred_interpretation

    assert starred_interpretation is not None
    assert starred_interpretation.starred_horizon_top is not None

    starred_horizon_top_data = starred_interpretation.starred_horizon_top.to_dict()
    starred_horizon_top_df = starred_interpretation.starred_horizon_top.to_df()

    starred_horizon_center_data = starred_interpretation.starred_horizon_center.to_dict()
    starred_horizon_center_df = starred_interpretation.starred_horizon_center.to_df()

    starred_horizon_bottom_data = starred_interpretation.starred_horizon_bottom.to_dict()
    starred_horizon_bottom_df = starred_interpretation.starred_horizon_bottom.to_df()

    assert starred_horizon_top_data['name'] == STARRED_HORIZON_TOP_NAME
    assert starred_horizon_top_df.at[0, 'name'] == STARRED_HORIZON_TOP_NAME

    assert starred_horizon_center_data['name'] == STARRED_HORIZON_CENTER_NAME
    assert starred_horizon_center_df.at[0, 'name'] == STARRED_HORIZON_CENTER_NAME

    assert starred_horizon_bottom_data['name'] == STARRED_HORIZON_BOTTOM_NAME
    assert starred_horizon_bottom_df.at[0, 'name'] == STARRED_HORIZON_BOTTOM_NAME


def test_get_topset_starred_tops(project):
    starred_topset = project.wells.find_by_name(WELL_NAME).starred_topset

    assert starred_topset is not None

    starred_top_top_data = starred_topset.starred_top_top.to_dict()
    starred_top_top_df = starred_topset.starred_top_top.to_df()

    assert starred_top_top_data['name'] == STARRED_TOP_TOP_NAME
    assert starred_top_top_df.at[0, 'name'] == STARRED_TOP_TOP_NAME

    starred_top_center_data = starred_topset.starred_top_center.to_dict()
    starred_top_center_df = starred_topset.starred_top_center.to_df()

    assert starred_top_center_data['name'] == STARRED_TOP_CENTER_NAME
    assert starred_top_center_df.at[0, 'name'] == STARRED_TOP_CENTER_NAME

    starred_top_bottom_data = starred_topset.starred_top_bottom.to_dict()
    starred_top_bottom_df = starred_topset.starred_top_bottom.to_df()

    assert starred_top_bottom_data['name'] == STARRED_TOP_BOTTOM_NAME
    assert starred_top_bottom_df.at[0, 'name'] == STARRED_TOP_BOTTOM_NAME


def test_get_mudlog(project):
    mudlogs = project.wells.find_by_name(WELL_NAME).mudlogs
    mudlog = mudlogs.find_by_name(MUDLOG_NAME)

    assert mudlog is not None

    mudlog_data = mudlog.to_dict()
    mudlog_df = mudlog.to_df()

    assert 'uuid' in mudlog_data
    assert 'name' in mudlog_data

    assert mudlog_data['name'] == MUDLOG_NAME
    assert mudlog_data['uuid'] == mudlog_df.at[0, 'uuid']
    assert mudlog_data['name'] == mudlog_df.at[0, 'name']

    assert mudlog.logs.to_df().at[0, 'MD'] == mudlog.logs[0].points.to_dict()[0]['md']


def test_get_well_linked_typewells(project):
    well = project.wells.find_by_name(WELL_NAME)
    typewell = project.typewells.find_by_name(TYPEWELL_NAME)
    assert well is not None
    assert typewell is not None

    linked_typewells = well.linked_typewells.to_dict()
    assert linked_typewells[0]['uuid'] == typewell.uuid


def test_ei_last_segment_extended(project):
    well = project.wells.find_by_name(WELL_NAME)
    assert well is not None

    interpretation = well.starred_interpretation
    endless_interpretation = well.interpretations.find_by_id(EI_LAST_SEGMENT_EXTENDED_ID)
    assert interpretation is not None
    assert endless_interpretation is not None

    _test_ei_case(
        well=well,
        interpretation=interpretation,
        endless_interpretation=endless_interpretation,
        measure_units=project.measure_unit,
    )


def test_ei_last_segment_out(project):
    well = project.wells.find_by_name(WELL_NAME)
    assert well is not None

    interpretation = well.interpretations.find_by_id(INTERPRETATION_LAST_SEGMENT_ONE_POINT_ID)
    endless_interpretation = well.interpretations.find_by_id(EI_LAST_SEGMENT_OUT_ID)
    assert interpretation is not None
    assert endless_interpretation is not None

    _test_ei_case(
        well=well,
        interpretation=interpretation,
        endless_interpretation=endless_interpretation,
        measure_units=project.measure_unit,
    )


def test_ei_absent_horizons_last_segment_out(project):
    well = project.wells.find_by_name(WELL_NAME)
    assert well is not None

    absent_horizons_interpretation = well.interpretations.find_by_id(
        INTERPRETATION_LAST_SEGMENT_ONE_POINT_ABSENT_HORIZONS_ID
    )
    endless_interpretation = well.interpretations.find_by_id(EI_ABSENT_HORIZONS_LAST_SEGMENT_OUT_ID)
    assert absent_horizons_interpretation is not None
    assert endless_interpretation is not None

    _test_ei_case(
        well=well,
        interpretation=absent_horizons_interpretation,
        endless_interpretation=endless_interpretation,
        measure_units=project.measure_unit,
    )


def test_ei_all_segments_out(project):
    well = project.wells.find_by_name(WELL_NAME)
    assert well is not None

    interpretation = well.starred_interpretation
    endless_interpretation = well.interpretations.find_by_id(EI_ALL_SEGMENTS_OUT_ID)
    assert interpretation is not None
    assert endless_interpretation is not None

    endless_interpretation_data = endless_interpretation.to_dict()
    assert endless_interpretation_data['horizons'] is None
    assert endless_interpretation_data['segments'] is None


def _test_ei_case(well, interpretation, endless_interpretation, measure_units):
    interpretation_data = interpretation.to_dict()
    endless_interpretation_data = endless_interpretation.to_dict()

    last_segment = interpretation_data['segments'][-1]
    ei_last_segment = endless_interpretation_data['segments'][-1]
    assert last_segment['md'] == ei_last_segment['md']

    last_segment_dip = get_last_segment_dip(
        well=well, assembled_segments=interpretation.assembled_segments, measure_units=measure_units
    )
    ei_last_segment_dip = get_last_segment_dip(
        well=well, assembled_segments=endless_interpretation.assembled_segments, measure_units=measure_units
    )
    assert fabs(last_segment_dip - ei_last_segment_dip) < DELTA_EI_DIP


def test_interpretation_segments_vs(project):
    well = project.wells.find_by_name(WELL_NAME)
    assert well is not None

    interpretation = well.starred_interpretation
    assert interpretation is not None

    interpretation_data = interpretation.to_dict()

    for segment in interpretation_data['segments']:
        assert segment['vs'] is not None


def test_get_well_comments(project):
    well = project.wells.find_by_name(WELL_NAME)
    assert well is not None

    comments = well.comments
    assert comments is not None

    comments_data = comments.to_dict()
    comments_df = comments.to_df()
    assert comments_data
    assert not comments_df.empty


def test_get_comment_boxes(project):
    well = project.wells.find_by_name(WELL_NAME)
    assert well is not None

    comments = well.comments
    assert comments is not None

    first_comment = comments[0]
    comment_boxes = first_comment.comment_boxes
    assert comment_boxes is not None

    comment_boxes_data = comment_boxes.to_dict()
    comment_boxes_df = comment_boxes.to_df()
    assert comment_boxes_data
    assert not comment_boxes_df.empty

    second_comment = comments[1]
    comment_boxes = second_comment.comment_boxes
    assert comment_boxes is not None

    comment_boxes_data = comment_boxes.to_dict()
    comment_boxes_df = comment_boxes.to_df()
    assert not comment_boxes_data
    assert comment_boxes_df.empty


def test_get_well_attributes(project):
    well = project.wells.find_by_name(WELL_NAME)
    assert well is not None

    attributes = well.attributes
    assert attributes is not None

    attributes_data = attributes.to_dict()
    attributes_df = attributes.to_df()
    assert attributes_data
    assert not attributes_df.empty

    assert attributes_data['Name']
    assert attributes_data['API']
    assert attributes_data['Operator']
    assert attributes_data['KB']
    assert attributes_data['Azimuth VS']
    assert attributes_data['Convergence']
    assert attributes_data['X-srf']
    assert attributes_data['Y-srf']


def test_get_earth_model(project):
    starred_interpretation = project.wells.find_by_name(WELL_NAME).starred_interpretation
    earth_model = starred_interpretation.earth_models.find_by_name(EARTH_MODEL_NAME)
    assert earth_model is not None

    earth_model_data = earth_model.to_dict()
    earth_model_df = earth_model.to_df()
    assert earth_model_data
    assert not earth_model_df.empty

    sections = earth_model.sections
    sections_data = sections.to_dict()
    sections_df = sections.to_df()
    assert sections_data
    assert not sections_df.empty
    assert len(sections_data) == len(sections_df)

    layers = sections[0].layers
    layers_data = layers.to_dict()
    layers_df = layers.to_df()
    assert layers_data
    assert not layers_df.empty
    assert len(layers) == len(layers_data)
