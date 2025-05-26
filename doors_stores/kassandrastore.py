# The MIT License (MIT)
# Copyright (c) 2025 Tonio Fincke
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import copy
import fsspec
import json
import requests
import xarray as xr
import warnings

from collections.abc import MutableMapping
from datetime import datetime
from datetime import timedelta
from pydap.parsers.das import parse_das
from pydap.parsers.dds import DDSParser
from typing import Dict

from xcube.core.store.datatype import DataType
from xcube.core.store import get_data_store_class

from .kassandraconstants import EMPTY_KERCHUNK_FILE
from .kassandraconstants import KERCHUNK_FILE_TEMPLATE
from .kassandraconstants import MVP_URL_TEMPLATE
from .kassandraconstants import SWH_URL_TEMPLATE
from .kassandraconstants import TIME_FORMAT
from .kassandraconstants import TIME_URL_TEMPLATE
from .kassandraconstants import VARCHUNK_TEMPLATE
from .kassandraconstants import WD_URL_TEMPLATE

KASSANDRA_DATASET_ATTRIBUTE_STRUCTURE = "https://erddap-danubius.ve.ismar.cnr.it/erddap/griddap/kassandra_bs.das"
KASSANDRA_DATASET_DESCRIPTOR_STRUCTURE = "https://erddap-danubius.ve.ismar.cnr.it/erddap/griddap/kassandra_bs.dds"
KASSANDRA_REFERENCE_FILENAME = "erddap_kassandra_mod_blk_phy_wav_for_2km_PT1H-1_202503.json"
KASSANDRA_VARIABLE_TEMPLATES = {
    "mean_wave_period": MVP_URL_TEMPLATE,
    "sign_wave_height": SWH_URL_TEMPLATE,
    "wave_direction": WD_URL_TEMPLATE
}

ReferenceDataStore = get_data_store_class('reference')


class KassandraKerchunkDataStore(ReferenceDataStore):

    def __init__(self):
        self._kass_ref = self._get_kassandra_reference_dictionary()
        with open(KASSANDRA_REFERENCE_FILENAME, "w") as krf:
            json.dump(self._kass_ref, krf, indent=4)
        super().__init__([KASSANDRA_REFERENCE_FILENAME])

    def _read_das(self) -> Dict:
        response = requests.get(KASSANDRA_DATASET_ATTRIBUTE_STRUCTURE)
        if not response.ok:
            return {}
        das_content = response.text
        return parse_das(das_content)

    def _get_num_timesteps(self) -> int:
        response = requests.get(KASSANDRA_DATASET_DESCRIPTOR_STRUCTURE)
        if not response.ok:
            return 0
        dds = DDSParser(response.text).parse()
        return dds.get("time").size

    def _get_kassandra_reference_dictionary(self) -> Dict:
        das = self._read_das()
        first_timestep = (das.get("NC_GLOBAL", {}).
                          get("time_coverage_start", "2024-06-30T00:00:00Z"))
        last_timestep = (das.get("NC_GLOBAL", {}).
                         get("time_coverage_end", "2024-06-30T00:00:00Z"))
        num_time_steps = self._get_num_timesteps()
        if num_time_steps == 0:
            return EMPTY_KERCHUNK_FILE

        kass_ref = KERCHUNK_FILE_TEMPLATE.copy()
        kass_ref["refs"][".zattrs"] = das.get("NC_GLOBAL", {})
        kass_ref["refs"]["time/.zarray"]["shape"] = [num_time_steps]
        kass_ref["refs"]["time/.zarray"]["chunks"] = [num_time_steps]
        kass_ref["refs"]["time/0"][0] = TIME_URL_TEMPLATE.format(timestep=last_timestep)
        kass_ref["refs"]["time/0"][2] = num_time_steps * 8
        kass_ref["refs"]["mean_wave_period/.zarray"]["shape"] = [num_time_steps, 288, 717]
        kass_ref["refs"]["sign_wave_height/.zarray"]["shape"] = [num_time_steps, 288, 717]
        kass_ref["refs"]["wave_direction/.zarray"]["shape"] = [num_time_steps, 288, 717]
        current_time = datetime.strptime(first_timestep, TIME_FORMAT)
        one_hour = timedelta(hours=1)
        for i in range(num_time_steps):
            ctf = current_time.strftime(TIME_FORMAT)
            for kass_var_name, template in KASSANDRA_VARIABLE_TEMPLATES.items():
                url = template.format(timestep=ctf)
                var_chunk = copy.deepcopy(VARCHUNK_TEMPLATE)
                var_chunk[0] = url
                kass_ref["refs"][f"{kass_var_name}/{i}.0.0"] = var_chunk
            current_time += one_hour
        return kass_ref

    def _get_start_and_end(self, key: str):
        ref = self._kass_ref.get("refs").get(key)
        return ref[1], ref[1] + ref[2]

    def open_data(
        self, data_id: str, opener_id: str = None, **open_params
    ) -> xr.Dataset:
        data_type = open_params.pop("data_type", None)
        if DataType.normalize(data_type).alias == "mldataset":
            warnings.warn(
                "ReferenceDataStore can only represent the data resource as xr.Dataset."
            )
        if open_params:
            warnings.warn(
                f"open_params are not supported yet,"
                f" but passing forward {', '.join(open_params.keys())}"
            )
        ref_path = self._refs[data_id]["ref_path"]
        open_params.pop("consolidated", False)

        class ByteSubsetMapper(MutableMapping):

            def __init__(self, original_mapper, kass_ref):
                self.original_mapper = original_mapper
                self._kass_ref = kass_ref

            def keys(self):
                return self.original_mapper.keys()

            def values(self):
                return self.original_mapper.values()

            def get(self, key):
                return self.original_mapper.get(key)

            def __setitem__(self, key: str, value: bytes) -> None:
                self.original_mapper.__set_item__(key, value)

            def __delitem__(self, key: str) -> None:
                self.original_mapper.__del_item__(key)

            def __contains__(self, item):
                return self.original_mapper.__contains__(item)

            def __iter__(self):
                return self.original_mapper.__iter__()

            def __len__(self):
                return self.original_mapper.__len__()

            def __getitem__(self, key):
                data = self.original_mapper[key]
                ref = self._kass_ref.get("refs").get(key)
                if isinstance(ref, list) and len(ref) >= 2:
                    if len(data) > ref[2]:
                        data = data[ref[1]:ref[1] + ref[2]]
                return data

        ref_mapping = fsspec.get_mapper("reference://", fo=ref_path, **self._ref_kwargs)

        ref_mapping = ByteSubsetMapper(ref_mapping, self._kass_ref)

        return xr.open_zarr(ref_mapping, consolidated=False, **open_params)
