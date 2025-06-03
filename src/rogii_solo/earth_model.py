from typing import Dict, Optional

from pandas import DataFrame

import rogii_solo.interpretation
from rogii_solo.base import BaseObject, ComplexObject, ObjectRepository
from rogii_solo.calculations.enums import EMeasureUnits
from rogii_solo.calculations.types import Segment
from rogii_solo.papi.client import PapiClient
from rogii_solo.types import DataList


class EarthModel(ComplexObject):
    """
    Represent an :class:`EarthModel`, which is a collection of :class:`EarthModelSection` and :class:`EarthModelLayer`
    associated with an :class:`Interpretation`.

    :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            interpretation = well.interpretations.find_by_name('Interpretation1')
            earth_model = interpretation.earth_models.find_by_name('EarthModel1')

            # Get the Interpretation associated with this Earth Model
            interpretation = earth_model.interpretation
            print(interpretation.name)

            # Get the unique ID of the Earth Model
            earth_model_uuid = earth_model.uuid
            print(earth_model_uuid)

            # Get the name of the Earth Model
            earth_model_name = earth_model.name
            print(earth_model_name)
    """

    def __init__(self, papi_client: PapiClient, interpretation: 'rogii_solo.interpretation.Interpretation', **kwargs):
        super().__init__(papi_client)

        self.interpretation = interpretation
        """:class:`~rogii_solo.interpretation.Interpretation` object associated with the :class:`EarthModel`."""

        self.uuid: Optional[str] = None
        """Unique identifier of the :class:`EarthModel`."""

        self.name: Optional[str] = None
        """Name of the :class:`EarthModel`."""

        self.__dict__.update(kwargs)

        self._sections: Optional[ObjectRepository[EarthModelSection]] = None

    @property
    def sections(self) -> ObjectRepository['EarthModelSection']:
        """
        Get the Sections of the :class:`EarthModel`.

        :return: :class:`ObjectRepository` containing :class:`EarthModelSection` instances.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            interpretation = well.interpretations.find_by_name('Interpretation1')
            earth_model = interpretation.earth_models.find_by_name('EarthModel1')

            # Get the Sections of the Earth Model
            sections = earth_model.sections
            print(sections.to_dict())
        """
        if self._sections is None:
            self._sections = ObjectRepository(
                [EarthModelSection(earth_model=self, **section_data) for section_data in self._get_sections_data()]
            )

        return self._sections

    def to_dict(self) -> Dict:
        """
        Convert the :class:`EarthModel` instance to a dictionary.

        :return: Dictionary representation of the :class:`EarthModel`.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            interpretation = well.interpretations.find_by_name('Interpretation1')
            earth_model = interpretation.earth_models.find_by_name('EarthModel1')

            # Convert the Earth Model to a dictionary
            earth_model_dict = earth_model.to_dict()
            print(earth_model_dict)
        """
        return {'uuid': self.uuid, 'name': self.name}

    def to_df(self) -> DataFrame:
        """
        Convert the :class:`EarthModelLayer` instance to a Pandas DataFrame.

        :return: DataFrame representation of the :class:`EarthModel`.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            interpretation = well.interpretations.find_by_name('Interpretation1')
            earth_model = interpretation.earth_models.find_by_name('EarthModel1')

            # Convert the Earth Model to a DataFrame
            earth_model_df = earth_model.to_df()
            print(earth_model_df)
        """
        return DataFrame([self.to_dict()])

    def _get_sections_data(self) -> DataList:
        sections = []
        segments_reversed = list(enumerate(self.interpretation.assembled_segments['segments'], 1))[::-1]

        for uuid, section_data in self._papi_client.fetch_earth_model_sections(earth_model_id=self.uuid).items():
            section_data = self._papi_client.parse_papi_data(section_data)
            section_data['uuid'] = uuid
            section_data['_raw_layers'] = section_data.pop('layers')

            for i, segment in segments_reversed:
                if segment['md'] <= section_data['md']:
                    section_data['interpretation_segment'] = i
                    break

            sections.append(section_data)

        return sorted(sections, key=lambda section: section['md'])


class EarthModelSection(BaseObject):
    """
    Represent a section of an :class:`EarthModel`, containing :class:`EarthModelLayer` and metadata.

    :example:

    .. code-block:: python

        from rogii_solo import SoloClient

        client_id = ... # Input your client ID
        client_secret = ... # Input your client secret

        solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
        project = solo_client.set_project_by_name('Project1')
        well = project.wells.find_by_name('Well1')
        interpretation = well.interpretations.find_by_name('Interpretation1')
        earth_model = interpretation.earth_models.find_by_name('EarthModel1')

        # Get the first Section of the Earth Model
        section = earth_model.sections[0]
        print(section.to_dict())

        # Get the unique ID of the Section
        section_uuid = section.uuid
        print(section_uuid)

        # Get the measure units of the project
        measure_units = section.measure_units
        print(measure_units)

        # Get the measured depth of the Section
        section_md = section.md
        print(section_md)

        # Get the dip angle of the Section
        section_dip = section.dip
        print(section_dip)

        # Get the interpretation segment associated with the Section
        interpretation_segment = section.interpretation_segment
        print(interpretation_segment)
    """

    def __init__(self, earth_model: EarthModel, **kwargs):
        self.earth_model = earth_model
        """Reference to the :class:`EarthModel` instance this :class:`EarthModelSection` belongs to."""

        self.measure_units = earth_model.interpretation.well.project.measure_unit
        """Measurement units used in the project."""

        self.uuid: Optional[str] = None
        """Unique identifier of the :class:`EarthModelSection`."""

        self.md: Optional[float] = None
        """Measured depth at which this :class:`EarthModelSection` is located."""

        self.dip: Optional[float] = None
        """Dip angle of the formation at this :class:`EarthModelSection`."""

        self.interpretation_segment: Optional[Segment] = None
        """Segment of the interpretation associated with this :class:`EarthModelSection`."""

        self._raw_layers: DataList = []

        self.__dict__.update(kwargs)

        self._layers: Optional[ObjectRepository[EarthModelLayer]] = None

    @property
    def layers(self) -> ObjectRepository['EarthModelLayer']:
        """
        Retrieve the layers of the :class:`EarthModelSection`.

        :return: :class:`ObjectRepository` containing :class:`EarthModelLayer` instances.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            interpretation = well.interpretations.find_by_name('Interpretation1')
            earth_model = interpretation.earth_models.find_by_name('EarthModel1')

            # Get the first Section of the Earth Model
            section = earth_model.sections[0]

            # Get the Layers of the Section
            layers = section.layers
            print(layers.to_dict())
        """
        if self._layers is None:
            layers = [EarthModelLayer(earth_model_section=self, **self._raw_layers[0])]

            for i, raw_layer in enumerate(self._raw_layers[1:-1], 1):
                raw_layer['thickness'] = self._raw_layers[i + 1]['tvd'] - raw_layer['tvd']
                layers.append(EarthModelLayer(earth_model_section=self, **raw_layer))

            layers.append(EarthModelLayer(earth_model_section=self, **self._raw_layers[-1]))
            self._layers = ObjectRepository(
                [EarthModelLayer(earth_model_section=self, **layer_data) for layer_data in self._get_layers_data()]
            )

        return self._layers

    def to_dict(self, get_converted: bool = True) -> Dict:
        """
        Convert the :class:`EarthModelSection` instance to a dictionary.

        :param get_converted: (Optional) Whether to convert measure units. Default is True.
        :return: Dictionary representation of the :class:`EarthModelSection`.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            interpretation = well.interpretations.find_by_name('Interpretation1')
            earth_model = interpretation.earth_models.find_by_name('EarthModel1')

            # Get the first Section of the Earth Model
            section = earth_model.sections[0]

            # Convert the Section to a dictionary
            section_dict = section.to_dict()
            print(section_dict)
        """
        return {
            'uuid': self.uuid,
            'md': self.safe_round(self.convert_z(self.md, measure_units=self.measure_units))
            if get_converted
            else self.md,
            'interpretation_segment': self.interpretation_segment,
        }

    def to_df(self, get_converted: bool = True) -> DataFrame:
        """
        Convert the :class:`EarthModelSection` instance to a Pandas DataFrame.

        :param get_converted: (Optional) Whether to convert measure units. Default is True.
        :return: DataFrame representation of the :class:`EarthModelSection`.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            interpretation = well.interpretations.find_by_name('Interpretation1')
            earth_model = interpretation.earth_models.find_by_name('EarthModel1')

            # Get the first Section of the Earth Model
            section = earth_model.sections[0]

            # Convert the Section to a DataFrame
            section_df = section.to_df()
            print(section_df)
        """
        return DataFrame([self.to_dict(get_converted)])

    def _get_layers_data(self) -> DataList:
        layers_data = [self._raw_layers[0]]

        for i, raw_layer in enumerate(self._raw_layers[1:-1], 1):
            raw_layer['thickness'] = self._raw_layers[i + 1]['tvd'] - raw_layer['tvd']
            layers_data.append(raw_layer)

        layers_data.append(self._raw_layers[-1])

        return layers_data


class EarthModelLayer(BaseObject):
    """
    Represent a :class:`EarthModelLayer` within an :class:`EarthModelSection`, containing physical properties.

    :example:

    .. code-block:: python

        from rogii_solo import SoloClient

        client_id = ... # Input your client ID
        client_secret = ... # Input your client secret

        solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
        project = solo_client.set_project_by_name('Project1')
        well = project.wells.find_by_name('Well1')
        interpretation = well.interpretations.find_by_name('Interpretation1')
        earth_model = interpretation.earth_models.find_by_name('EarthModel1')

        # Get the first Section of the Earth Model
        section = earth_model.sections[0]

        # Get the first Earth Model Layer of the Section
        layer = section.layers[0]

        # Get the measure units of the project
        measure_units = layer.measure_units
        print(measure_units)

        # Get the unique ID of the Earth Model Layer
        layer_uuid = layer.uuid
        print(layer_uuid)

        # Get the vertical resistivity of the Earth Model Layer
        layer_resistivity_vertical = layer.resistivity_vertical
        print(layer_resistivity_vertical)

        # Get the horizontal resistivity of the Earth Model Layer
        layer_resistivity_horizontal = layer.resistivity_horizontal
        print(layer_resistivity_horizontal)

        # Get the true vertical thickness of the Earth Model Layer
        layer_tvt = layer.tvt
        print(layer_tvt)

        # Get the calculated thickness of the Earth Model Layer
        layer_thickness = layer.thickness
        print(layer_thickness)

        # Get the anisotropy of the Earth Model Layer
        layer_anisotropy = layer.anisotropy
        print(layer_anisotropy)
    """

    def __init__(self, earth_model_section: EarthModelSection, **kwargs):
        self.earth_model_section: EarthModelSection = earth_model_section
        """Reference to the :class:`EarthModelSection` this :class:`EarthModelLayer` belongs to."""

        self.measure_units: EMeasureUnits = earth_model_section.earth_model.interpretation.well.project.measure_unit
        """Measurement units used in the project."""

        self.uuid: Optional[str] = None
        """Unique identifier of the :class:`EarthModelLayer`."""

        self.resistivity_vertical: Optional[float] = None
        """Vertical resistivity of the :class:`EarthModelLayer`."""

        self.resistivity_horizontal: Optional[float] = None
        """Horizontal resistivity of the :class:`EarthModelLayer`."""

        self.tvt: Optional[float] = None  # TODO Replace with TVD when PAPI method is available
        """True vertical thickness of the :class:`EarthModelLayer`."""

        self.thickness: float = float('inf')
        """Calculated thickness of the :class:`EarthModelLayer`."""

        self.anisotropy: Optional[float] = None
        """Anisotropy of the :class:`EarthModelLayer`."""

        self.__dict__.update(kwargs)

        if self.tvt is None or self.tvt == -100000:
            self.tvt = float('nan')

        if self.resistivity_vertical is not None and self.resistivity_horizontal is not None:
            self.anisotropy = self.resistivity_vertical / self.resistivity_horizontal

    def to_dict(self, get_converted: bool = True) -> Dict:
        """
        Convert the :class:`EarthModelLayer` instance to a dictionary.

        :param get_converted: (Optional) Whether to convert measure units. Default is True.
        :return: Dictionary representation of the :class:`EarthModelLayer`.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            interpretation = well.interpretations.find_by_name('Interpretation1')
            earth_model = interpretation.earth_models.find_by_name('EarthModel1')

            # Get the first Section of the Earth Model
            section = earth_model.sections[0]

            # Get the first Earth Model Layer of the Section
            layer = section.layers[0]

            # Convert the Earth Model Layer to a dictionary
            layer_dict = layer.to_dict()
            print(layer_dict)
        """
        return {
            'tvt': self.safe_round(self.convert_z(self.tvt, measure_units=self.measure_units))
            if get_converted
            else self.tvt,
            'thickness': self.thickness,
            'resistivity_horizontal': self.resistivity_horizontal,
            'anisotropy': self.anisotropy,
        }

    def to_df(self, get_converted: bool = True) -> DataFrame:
        """
        Convert the :class:`EarthModelLayer` instance to a Pandas DataFrame.

        :param get_converted: (Optional) Whether to convert measure units. Default is True.
        :return: DataFrame representation of the :class:`EarthModelLayer`.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            interpretation = well.interpretations.find_by_name('Interpretation1')
            earth_model = interpretation.earth_models.find_by_name('EarthModel1')

            # Get the first Section of the Earth Model
            section = earth_model.sections[0]

            # Get the first Earth Model Layer of the Section
            layer = section.layers[0]

            # Convert the Earth Model Layer to a DataFrame
            layer_df = layer.to_df()
            print(layer_df)
        """
        return DataFrame([self.to_dict(get_converted)])
