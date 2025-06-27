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

from doors_stores.kassandrastore import KassandraKerchunkDataStore

class KassandraKerchunkDataStoreTest(unittest.TestCase):

    @abstractmethod
    def get_store(self) -> KassandraKerchunkDataStore:
        return KassandraKerchunkDataStore()

    def test_open_erddap_data(self):
        store = self.get_store()
        erddap_cube = store.open_data("erddap_kassandra_mod_blk_phy_wav_for_2km_PT1H-1_202503")
        self.assert_erddap_cube_ok(erddap_cube)

    def assert_erddap_cube_ok(self, cube: xr.Dataset):
        self.assertEqual({"time": 8040, "lat": 288, "lon": 717}, cube.sizes)
        self.assertEqual({"lon", "time", "lat"}, set(cube.coords))
        self.assertEqual(
            {"mean_wave_period", "sign_wave_height", "wave_direction"},
            set(cube.data_vars),
        )
        erddap_ts = cube.isel(time=slice(0, 5), lat=144, lon=350).compute()
        erddap_data = erddap_ts.mean_wave_period.values
        self.assertAlmostEqual(1.9393034, erddap_data[0], 2)
        self.assertAlmostEqual(1.9095887, erddap_data[1], 2)
        self.assertAlmostEqual(1.823673, erddap_data[2], 2)
        self.assertAlmostEqual(1.6955256, erddap_data[3], 2)
        self.assertAlmostEqual(1.5880507, erddap_data[4], 2)
