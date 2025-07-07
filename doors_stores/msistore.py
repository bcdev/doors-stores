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


import fsspec
import json
import os
import time
import xarray as xr
import warnings

from collections.abc import MutableMapping

from xcube.core.store.datatype import DataType
from xcube.core.store import get_data_store_class

_DATASETS = {
    "certo-v2-danube-msi-v2": {
        "reference_file": "certo-v2-danube-msi-v2.json",
        "descriptor_file": "certo-v2-danube-msi-v2-desc.json"
    },
    "certo-v2-danube-msi-refls-v2": {
        "reference_file": "certo-v2-danube-msi-refls-v2.json",
        "descriptor_file": "certo-v2-danube-msi-refls-v2-desc.json"
    }
}

ReferenceDataStore = get_data_store_class('reference')


class MsiKerchunkDataStore(ReferenceDataStore):

    def __init__(self):
        base_path =  os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
        references = []
        for dataset_title, dataset_dict in _DATASETS.items():
            ref_path = os.path.join(base_path, dataset_dict.get("reference_file"))
            ref_dict = dict(
                ref_path=ref_path
            )
            desc_path = os.path.join(base_path, dataset_dict.get("descriptor_file"))
            with open(desc_path, 'r') as fp:
                ref_dict["data_descriptor"] = json.load(fp)
            references.append(ref_dict)
        self._references = references

        target_options = {
            "block_size": 0,
            "simple_links": True,
            "retry_options": {
                "retries": 5,
                "backoff_factor": 0.5,
                "status_forcelist": [400, 500, 502, 503, 504]
            }
        }
        super().__init__(self._references, target_options=target_options)

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

            def __init__(self, original_mapper, reference):
                self.original_mapper = original_mapper
                self._reference = reference

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
                data = None
                retries = 0
                while data is None and retries < 5:
                    try:
                        data = self.original_mapper[key]
                    except:
                        retries+=1
                        time.sleep(1)
                if data is not None:
                    ref = self._reference.get("refs").get(key)
                    if isinstance(ref, list) and len(ref) >= 2:
                        if len(data) > ref[2]:
                            data = data[ref[1]:ref[1] + ref[2]]
                return data

        ref_mapping = fsspec.get_mapper("reference://", fo=ref_path, **self._ref_kwargs)

        reference_file = _DATASETS[data_id]["reference_file"]
        reference_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'data',
            reference_file
        )
        with open(reference_path, 'r') as fp:
            reference = json.load(fp)


        ref_mapping = ByteSubsetMapper(ref_mapping, reference)

        return xr.open_zarr(ref_mapping, consolidated=False, **open_params)
