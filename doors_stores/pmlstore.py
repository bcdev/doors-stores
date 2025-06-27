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

from .constants import EMPTY_KERCHUNK_FILE
from .constants import KERCHUNK_FILE_TEMPLATE
from .constants import MVP_URL_TEMPLATE
from .constants import SWH_URL_TEMPLATE
from .constants import TIME_FORMAT
from .constants import TIME_URL_TEMPLATE
from .constants import VARCHUNK_TEMPLATE
from .constants import WD_URL_TEMPLATE

# KASSANDRA_DATASET_ATTRIBUTE_STRUCTURE = "https://erddap-danubius.ve.ismar.cnr.it/erddap/griddap/kassandra_bs.das"
# KASSANDRA_DATASET_DESCRIPTOR_STRUCTURE = "https://erddap-danubius.ve.ismar.cnr.it/erddap/griddap/kassandra_bs.dds"
# KASSANDRA_REFERENCE_FILENAME = "erddap_kassandra_mod_blk_phy_wav_for_2km_PT1H-1_202503.json"
# KASSANDRA_VARIABLE_TEMPLATES = {
#     "mean_wave_period": MVP_URL_TEMPLATE,
#     "sign_wave_height": SWH_URL_TEMPLATE,
#     "wave_direction": WD_URL_TEMPLATE
# }

OLCI_REFLECTANCE_VARS = [
    "Rrs400_rep",
    "Rrs412_rep",
    "Rrs443_rep",
    "Rrs490_rep",
    "Rrs510_rep",
    "Rrs560_rep",
    "Rrs620_rep",
    "Rrs665_rep",
    "Rrs674_rep",
    "Rrs681_rep",
    "Rrs709_rep",
    "Rrs754_rep",
    "Rrs760_rep",
    "Rrs764_rep",
    "Rrs767_rep",
    "Rrs779_rep",
    "Rrs865_rep",
    "Rrs885_rep",
    "Rrs900_rep",
    "Rrs940_rep",
    "Rrs1020_rep"
]

OLCI_MSI_VARS = [
    "blended_chla_top_2_reweighted",
    "blended_tsm_top_2_reweighted",
    "owt_dominant_OWT",
    "owt_OWT_01",
    "owt_OWT_02",
    "owt_OWT_03",
    "owt_OWT_04",
    "owt_OWT_05",
    "owt_OWT_06",
    "owt_OWT_07",
    "owt_OWT_08",
    "owt_OWT_09",
    "owt_OWT_10",
    "owt_OWT_11",
    "owt_OWT_12",
    "owt_OWT_13",
    "owt_OWT_14",
    "owt_OWT_15",
    "owt_OWT_16",
    "owt_OWT_17",
    "owt_OWT_18"
]

PML_REFERENCE_FILENAME = "/home/tonio/project_data/doors/kerchunk_ws/pml/pml_refs.json"

ReferenceDataStore = get_data_store_class('reference')


class PmlKerchunkDataStore(ReferenceDataStore):

    def __init__(self):
        with open(PML_REFERENCE_FILENAME, 'r') as fp:
            self._kc_refs = json.load(fp)
        super().__init__(self._kc_refs,
                         remote_protocol="https"
                         # protocol="https", target_options=dict(
            # compression=None
            # consolidated=False,
            # protocol="https"
        # )
        )
