from typing import Any, Dict, Optional

from pandas import DataFrame

import rogii_solo.well
from rogii_solo.base import BaseObject, ObjectRepository
from rogii_solo.types import DataList


class Comment(BaseObject):
    """
    Represent a :class:`Comment` associated with a specific :class:`~rogii_solo.well.Well`.
    Provides properties such as `name` and `id`.

    :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')

            # Get Comments of the Well
            comments = well.comments

            # Get a Comment name
            comment = comments.find_by_name('Comment1')
            print(comment.name)

            # Get a Comment id
            comment = comments.find_by_id('CommentID')
            print(comment.comment_id)
    """

    def __init__(self, well: 'rogii_solo.well.Well', **kwargs):
        self.well = well
        """Reference to the :class:`~rogii_solo.well.Well` instance this :class:`Comment` belongs to."""

        self.comment_id: Optional[str] = None
        """Unique identifier of the :class:`Comment`."""

        self.name: Optional[str] = None
        """Name of the :class:`Comment`."""

        self._comment_boxes_data: Optional[DataList] = None
        self._comment_boxes: Optional[ObjectRepository[CommentBox]] = None

        self.__dict__.update(kwargs)

    @property
    def comment_boxes(self) -> ObjectRepository['CommentBox']:
        """
        Get :class:`CommentBox` objects of the :class:`Comment`.

        :return: A :class:`CommentBox` instance of the :class:`Comment`.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ...  # Input your client ID
            client_secret = ...  # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            comments = well.comments
            comment = comments.find_by_name('Comment1')

            # Get a CommentBox of the Comment
            comment_box = comment.comment_boxes.find_by_id('CommentBoxID')
            print(comment_box.to_dict())
        """
        if self._comment_boxes is None:
            self._comment_boxes = ObjectRepository(
                objects=[CommentBox(comment=self, **item) for item in self._comment_boxes_data]
            )

        return self._comment_boxes

    def to_dict(self, get_converted: bool = True) -> Dict[str, Any]:
        """
        Convert the :class:`Comment` instance to a dictionary.

        :return: Dictionary representation of the :class:`Comment`.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            comments = well.comments
            comment = comments.find_by_name('Comment1')

            # Convert the Comment to a dictionary
            comment_dict = comment.to_dict()
            print(comment_dict)
        """
        return {'comment_id': self.comment_id, 'name': self.name}

    def to_df(self, get_converted: bool = True) -> DataFrame:
        """
        Convert the :class:`Comment` instance to a Pandas DataFrame.

        :return: DataFrame representation of the :class:`Comment`.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            comments = well.comments
            comment = comments.find_by_name('Comment1')

            # Convert the Comment to a DataFrame
            comment_df = comment.to_df()
            print(comment_df)
        """
        return DataFrame([self.to_dict(get_converted)])


class CommentBox(BaseObject):
    """
    Represent a :class:`CommentBox` associated with a specific :class:`Comment`.
    Provides properties such as `text`, `anchor_md`, and `id`.

    :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')

            # Get a CommentBox of the Comment
            comments = well.comments
            comment = comments.find_by_name('Comment1')
            comment_box = comment.comment_boxes.find_by_id('CommentBoxID')

            # Get a CommentBox id
            comment_box_id = comment_box.commentbox_id
            print(comment_box_id)

            # Get a CommentBox anchor md
            comment_box_anchor_md = comment_box.anchor_md
            print(comment_box_anchor_md)

            # Get a CommentBox text
            comment_box_text = comment_box.text
            print(comment_box_text)
    """

    def __init__(self, comment: Comment, **kwargs):
        self.comment = comment
        """Reference to the :class:`Comment` instance this :class:`CommentBox` belongs to."""

        self.commentbox_id: Optional[str] = None
        """Unique identifier of the :class:`CommentBox`."""

        self.text: Optional[str] = None
        """Text of the :class:`CommentBox`."""

        self.anchor_md: Optional[float] = None
        """Anchor MD of the :class:`CommentBox`."""

        self.__dict__.update(kwargs)

    def to_dict(self, get_converted: bool = True) -> Dict[str, Any]:
        """
        Convert the :class:`CommentBox` instance to a dictionary.

        :return: Dictionary representation of the :class:`CommentBox`.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            comments = well.comments
            comment = comments.find_by_name('Comment1')
            comment_box = comment.comment_boxes.find_by_id('CommentBoxID')

            # Convert the CommentBox to a dictionary
            comment_box_dict = comment_box.to_dict()
            print(comment_box_dict)
        """

        measure_units = self.comment.well.project.measure_unit

        return {
            'commentbox_id': self.commentbox_id,
            'text': self.text,
            'anchor_md': self.safe_round(self.convert_z(value=self.anchor_md, measure_units=measure_units))
            if get_converted
            else self.anchor_md,
        }

    def to_df(self, get_converted: bool = True) -> DataFrame:
        """
        Convert the :class:`CommentBox` instance to a Pandas DataFrame.

        :return: DataFrame representation of the :class:`CommentBox`.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            comments = well.comments
            comment = comments.find_by_name('Comment1')
            comment_box = comment.comment_boxes.find_by_id('CommentBoxID')

            # Convert the CommentBox to a DataFrame
            comment_box_df = comment_box.to_df()
            print(comment_box_df)
        """
        return DataFrame([self.to_dict(get_converted)])
