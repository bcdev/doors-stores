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

from abc import abstractmethod
import unittest
import xarray as xr

from doors_stores.olcistore import OlciKerchunkDataStore

class OlciKerchunkDataStoreTest(unittest.TestCase):

    @abstractmethod
    def get_store(self) -> OlciKerchunkDataStore:
        return OlciKerchunkDataStore()

    def test_list_data_ids(self):
        store = self.get_store()
        data_ids = store.list_data_ids()
        self.assertIsNotNone(data_ids)
        self.assertEqual(8, len(data_ids))
        self.assertIn("CERTO_blk_OLCI_RES300_final_l3_product_ref", data_ids)
        self.assertIn("CERTO_blk_OLCI_RES300_final_l3_product_owt", data_ids)

    def test_open_olci_data(self):
        store = self.get_store()
        ds = store.open_data("CERTO_blk_OLCI_RES300_final_l3_product_ref")
        self.assert_cube_ok(ds)

    def assert_cube_ok(self, cube: xr.Dataset):
        self.assertEqual({"time": 2143, "lat": 3163, "lon": 6913}, cube.sizes)
        self.assertEqual({"lon", "time", "lat"}, set(cube.coords))
