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
    Represents an Earth Model, which is a collection of sections and layers
    associated with a geological interpretation.
    """

    def __init__(self, papi_client: PapiClient, interpretation: 'rogii_solo.interpretation.Interpretation', **kwargs):
        super().__init__(papi_client)

        self.interpretation = interpretation
        """Geological interpretation object associated with the :class:`EarthModel`."""

        self.uuid: Optional[str] = None
        """Unique identifier of the :class:`EarthModel`."""

        self.name: Optional[str] = None
        """:class:`EarthModel` name."""

        self.__dict__.update(kwargs)

        self._sections: Optional[ObjectRepository[EarthModelSection]] = None

    @property
    def sections(self) -> ObjectRepository['EarthModelSection']:
        """
        Retrieves the sections of the :class:`EarthModel`.

        :return: :class:`ObjectRepository` containing :class:`EarthModelSection` instances.
        """
        if self._sections is None:
            self._sections = ObjectRepository(
                [EarthModelSection(earth_model=self, **section_data) for section_data in self._get_sections_data()]
            )

        return self._sections

    def to_dict(self) -> Dict:
        """
        Converts the :class:`EarthModel` instance to a dictionary.

        :return: Dictionary representation of the :class:`EarthModel`.
        """
        return {'uuid': self.uuid, 'name': self.name}

    def to_df(self) -> DataFrame:
        """
        Converts the :class:`EarthModelLayer` instance to a Pandas DataFrame.

        :return: DataFrame representation of the :class:`EarthModel`.
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
    Represents a section of an :class:`EarthModel`, containing :class:`EarthModelLayer` and metadata.
    """

    def __init__(self, earth_model: EarthModel, **kwargs):
        self.earth_model = earth_model
        """Reference to the :class:`EarthModel` instance this section belongs to."""

        self.measure_units = earth_model.interpretation.well.project.measure_unit
        """Measurement units used in the project."""

        self.uuid: Optional[str] = None
        """Unique identifier of the section."""

        self.md: Optional[float] = None
        """Measured depth at which this section is located."""

        self.dip: Optional[float] = None
        """Dip angle of the formation at this section."""

        self.interpretation_segment: Optional[Segment] = None
        """Segment of the interpretation associated with this section."""

        self._raw_layers: DataList = []
        """Raw layer data as fetched from PAPI."""

        self.__dict__.update(kwargs)

        self._layers: Optional[ObjectRepository[EarthModelLayer]] = None
        """Repository of :class:`EarthModelLayer` instances."""

    @property
    def layers(self) -> ObjectRepository['EarthModelLayer']:
        """
        Retrieves the layers of the :class:`EarthModelSection`.

        :return: :class:`ObjectRepository` containing :class:`EarthModelLayer` instances.
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
        Converts the :class:`EarthModelSection` instance to a dictionary.

        :param get_converted: Whether to convert measure units.
        :return: Dictionary representation of the :class:`EarthModelSection`.
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
        Converts the :class:`EarthModelSection` instance to a Pandas DataFrame.

        :param get_converted: Whether to convert measure units.
        :return: DataFrame representation of the :class:`EarthModelSection`.
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
    Represents a layer within an :class:`EarthModelSection`, containing physical properties.
    """

    def __init__(self, earth_model_section: EarthModelSection, **kwargs):
        self.earth_model_section: EarthModelSection = earth_model_section
        """Reference to the EarthModelSection this layer belongs to."""

        self.measure_units: EMeasureUnits = earth_model_section.earth_model.interpretation.well.project.measure_unit
        """Measurement units used in the project."""

        self.uuid: Optional[str] = None
        """Unique identifier of the layer."""

        self.resistivity_vertical: Optional[float] = None
        """Vertical resistivity of the layer."""

        self.resistivity_horizontal: Optional[float] = None
        """Horizontal resistivity of the layer."""

        self.tvt: Optional[float] = None  # TODO Replace with TVD when PAPI method is available
        """True vertical thickness."""

        self.thickness: float = float('inf')
        """Calculated thickness of the layer."""

        self.anisotropy: Optional[float] = None
        """Anisotropy of the layer."""

        self.__dict__.update(kwargs)

        if self.tvt is None or self.tvt == -100000:
            self.tvt = float('nan')

        if self.resistivity_vertical is not None and self.resistivity_horizontal is not None:
            self.anisotropy = self.resistivity_vertical / self.resistivity_horizontal

    def to_dict(self, get_converted: bool = True) -> Dict:
        """
        Converts the :class:`EarthModelLayer` instance to a dictionary.

        :param get_converted: Whether to convert measure units.
        :return: Dictionary representation of the :class:`EarthModelLayer`.
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
        Converts the :class:`EarthModelLayer` instance to a Pandas DataFrame.

        :param get_converted: Whether to convert measure units.
        :return: DataFrame representation of the :class:`EarthModelLayer`.
        """
        return DataFrame([self.to_dict(get_converted)])
