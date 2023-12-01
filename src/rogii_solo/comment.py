from typing import Any, Dict, Optional

from pandas import DataFrame

import rogii_solo.well
from rogii_solo.base import BaseObject, ObjectRepository
from rogii_solo.types import DataList


class Comment(BaseObject):
    def __init__(self, well: 'rogii_solo.well.Well', **kwargs):
        self.well = well

        self.comment_id = None
        self.name = None

        self._comment_boxes_data: Optional[DataList] = None
        self._comment_boxes: Optional[ObjectRepository[CommentBox]] = None

        self.__dict__.update(kwargs)

    def to_dict(self, get_converted: bool = True) -> Dict[str, Any]:
        return {'comment_id': self.comment_id, 'name': self.name}

    def to_df(self, get_converted: bool = True) -> DataFrame:
        return DataFrame([self.to_dict(get_converted)])

    @property
    def comment_boxes(self) -> ObjectRepository['CommentBox']:
        if self._comment_boxes is None:
            self._comment_boxes = ObjectRepository(
                objects=[CommentBox(comment=self, **item) for item in self._comment_boxes_data]
            )

        return self._comment_boxes


class CommentBox(BaseObject):
    def __init__(self, comment: Comment, **kwargs):
        self.comment = comment

        self.commentbox_id = None
        self.text = None
        self.anchor_md = None

        self.__dict__.update(kwargs)

    def to_dict(self, get_converted: bool = True) -> Dict[str, Any]:
        measure_units = self.comment.well.project.measure_unit

        return {
            'commentbox_id': self.commentbox_id,
            'text': self.text,
            'anchor_md': self.safe_round(self.convert_z(value=self.anchor_md, measure_units=measure_units))
            if get_converted
            else self.anchor_md,
        }

    def to_df(self, get_converted: bool = True) -> DataFrame:
        return DataFrame([self.to_dict(get_converted)])
