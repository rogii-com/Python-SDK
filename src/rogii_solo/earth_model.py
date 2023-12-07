from typing import Dict, Optional

from pandas import DataFrame

import rogii_solo.interpretation
from rogii_solo.base import BaseObject, ComplexObject, ObjectRepository
from rogii_solo.papi.client import PapiClient
from rogii_solo.types import DataList


class EarthModel(ComplexObject):
    def __init__(self, papi_client: PapiClient, interpretation: 'rogii_solo.interpretation.Interpretation', **kwargs):
        super().__init__(papi_client)

        self.interpretation = interpretation

        self.uuid = None
        self.name = None

        self.__dict__.update(kwargs)

        self._sections: Optional[ObjectRepository[EarthModelSection]] = None

    def to_dict(self) -> Dict:
        return {'uuid': self.uuid, 'name': self.name}

    def to_df(self) -> DataFrame:
        return DataFrame([self.to_dict()])

    @property
    def sections(self) -> ObjectRepository['EarthModelSection']:
        if self._sections is None:
            self._sections = ObjectRepository(
                [EarthModelSection(earth_model=self, **section_data) for section_data in self._get_sections_data()]
            )

        return self._sections

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
    def __init__(self, earth_model: EarthModel, **kwargs):
        self.earth_model = earth_model
        self.measure_units = earth_model.interpretation.well.project.measure_unit
        self.uuid = None
        self.md = None
        self.dip = None
        self.interpretation_segment = None
        self._raw_layers: DataList = []

        self.__dict__.update(kwargs)

        self._layers: Optional[ObjectRepository[EarthModelLayer]] = None

    def to_dict(self, get_converted: bool = True) -> Dict:
        return {
            'uuid': self.uuid,
            'md': self.safe_round(self.convert_z(self.md, measure_units=self.measure_units))
            if get_converted
            else self.md,
            'interpretation_segment': self.interpretation_segment,
        }

    def to_df(self, get_converted: bool = True) -> DataFrame:
        return DataFrame([self.to_dict(get_converted)])

    @property
    def layers(self) -> ObjectRepository['EarthModelLayer']:
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

    def _get_layers_data(self) -> DataList:
        layers_data = [self._raw_layers[0]]

        for i, raw_layer in enumerate(self._raw_layers[1:-1], 1):
            raw_layer['thickness'] = self._raw_layers[i + 1]['tvd'] - raw_layer['tvd']
            layers_data.append(raw_layer)

        layers_data.append(self._raw_layers[-1])

        return layers_data


class EarthModelLayer(BaseObject):
    def __init__(self, earth_model_section: EarthModelSection, **kwargs):
        self.earth_model_section = earth_model_section
        self.measure_units = earth_model_section.earth_model.interpretation.well.project.measure_unit

        self.uuid = None
        self.resistivity_vertical = None
        self.resistivity_horizontal = None
        self.tvt = None  # TODO Replace with TVD when PAPI method is available
        self.thickness = float('inf')
        self.anisotropy = None

        self.__dict__.update(kwargs)

        if self.tvt is None or self.tvt == -100000:
            self.tvt = float('nan')

        if self.resistivity_vertical is not None and self.resistivity_horizontal is not None:
            self.anisotropy = self.resistivity_vertical / self.resistivity_horizontal

    def to_dict(self, get_converted: bool = True) -> Dict:
        return {
            'tvt': self.safe_round(self.convert_z(self.tvt, measure_units=self.measure_units))
            if get_converted
            else self.tvt,
            'thickness': self.thickness,
            'resistivity_horizontal': self.resistivity_horizontal,
            'anisotropy': self.anisotropy,
        }

    def to_df(self, get_converted: bool = True) -> DataFrame:
        return DataFrame([self.to_dict(get_converted)])
