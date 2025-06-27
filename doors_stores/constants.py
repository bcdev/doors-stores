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

KASSANDRA_DATA_STORE_ID = "kassandra_ref"
MSI_DATA_STORE_ID = "msi_ref"
OLCI_DATA_STORE_ID = "olci_ref"

KERCHUNK_FILE_TEMPLATE = {
    "version": 1,
    "refs": {
        ".zgroup": {
            "zarr_format": 2
        },
        ".zattrs": {},
        "time/.zarray": {
            "shape": 0,
            "chunks": 0,
            "fill_value": None,
            "order": "C",
            "filters": None,
            "dimension_separator": ".",
            "compressor": None,
            "zarr_format": 2,
            "dtype": ">f8"
        },
        "time/.zattrs": {
            "_ARRAY_DIMENSIONS": ["time"],
            "standard_name": "time",
            "units": "seconds since 1970-01-01 00:00:00 UTC",
            "calendar": "standard",
            "axis": "T"
        },
        "time/0": [
            "",
            3248,
            0
        ],
        "lat/.zarray": {
            "shape": [288],
            "chunks": [288],
            "fill_value": None,
            "order": "C",
            "filters": None,
            "dimension_separator": ".",
            "compressor": None,
            "zarr_format": 2,
            "dtype": ">f4"
        },
        "lat/.zattrs": {
            "_ARRAY_DIMENSIONS": ["lat"],
            "standard_name": "latitude",
            "long_name": "latitude",
            "units": "degrees_north",
            "axis": "Y"
        },
        "lat/0": [
            "https://erddap-danubius.ve.ismar.cnr.it/erddap/griddap/kassandra_bs.nc?latitude%5B(40.9):1:(46.64)%5D",
            3236,
            1152
        ],
        "lon/.zarray": {
            "shape": [717],
            "chunks": [717],
            "fill_value": None,
            "order": "C",
            "filters": None,
            "dimension_separator": ".",
            "compressor": None,
            "zarr_format": 2,
            "dtype": ">f4"
        },
        "lon/.zattrs": {
            "_ARRAY_DIMENSIONS": ["lon"],
            "standard_name": "longitude",
            "long_name": "longitude",
            "units": "degrees_east",
            "axis": "X"
        },
        "lon/0": [
            "https://erddap-danubius.ve.ismar.cnr.it/erddap/griddap/kassandra_bs.nc?longitude%5B(27.46):1:(41.78)%5D",
            3240,
            2868
        ],
        "mean_wave_period/.zarray": {
            "shape": [0, 288, 717],
            "chunks": [1, 288, 717],
            "fill_value": -999.0,
            "order": "C",
            "filters": None,
            "dimension_separator": ".",
            "compressor": None,
            "zarr_format": 2,
            "dtype": ">f4"
        },
        "mean_wave_period/.zattrs": {
            "_ARRAY_DIMENSIONS": ["time", "lat", "lon"],
            "standard_name": "sea_surface_swell_wave_period",
            "long_name": "Mean Wave Period",
            "units": "s",
            "cell_methods": "level: mean",
            "color_value_min": 0.0,
            "color_value_max": 20.0,
        },
        "sign_wave_height/.zarray": {
            "shape": [0, 288, 717],
            "chunks": [1, 288, 717],
            "fill_value": -999.0,
            "order": "C",
            "filters": None,
            "dimension_separator": ".",
            "compressor": None,
            "zarr_format": 2,
            "dtype": ">f4"
        },
        "sign_wave_height/.zattrs": {
            "_ARRAY_DIMENSIONS": ["time", "lat", "lon"],
            "standard_name": "sea_surface_wave_significant_height",
            "long_name": "Significant Wave Height",
            "units": "m",
            "cell_methods": "level: mean",
            "color_value_min": 0.0,
            "color_value_max": 10.0,
        },
        "wave_direction/.zarray": {
            "shape": [0, 288, 717],
            "chunks": [1, 288, 717],
            "fill_value": -999.0,
            "order": "C",
            "filters": None,
            "dimension_separator": ".",
            "compressor": None,
            "zarr_format": 2,
            "dtype": ">f4"
        },
        "wave_direction/.zattrs": {
            "_ARRAY_DIMENSIONS": ["time", "lat", "lon"],
            "standard_name": "sea_surface_wave_to_direction",
            "long_name": "Mean Wave Direction",
            "units": "deg",
            "cell_methods": "level: mean",
            "color_value_min": 0.0,
            "color_value_max": 360.0,
            "color_bar_name": "twilight_shifted"
        },
    }
}



EMPTY_KERCHUNK_FILE = {
    "version": 1,
    "refs": {
        ".zgroup": {
            "zarr_format": 2
        },
        ".zattrs": {
            "CDI": "Climate Data Interface version 1.9.10 (https://mpimet.mpg.de/cdi)",
            "Conventions": "CF-1.4",
            "source": "Model data produced by SHYFEM at ISMAR-CNR",
            "institution": "ISMAR-CNR, Venice, Italy",
            "title": "storm surge forecast in the black sea",
            "references": "Model info: http://www.ismar.cnr.it/shyfem",
            "contact": "email: georg.umgiesser@ismar.cnr.it",
            "comment": "Data restriction: for academic research use only",
            "NCO": "netCDF Operators version 4.9.7 (Homepage = http://nco.sf.net, Code = http://github.com/nco/nco)",
            "CDO":"Climate Data Operators version 1.9.10 (https://mpimet.mpg.de/cdo)"
        },
        "lat/.zarray": {
            "chunks":[3], "compressor": None, "dtype": "<f8", "fill_value": "NaN", "filters": None, "order": "C",
            "shape": [3], "zarr_format": 2
        },
        "lat/.zattrs": {
            "_ARRAY_DIMENSIONS":["lat"], "long_name": "latitude", "standard_name": "latitude", "units": "degrees_north"
        },
        "lat/0": "base64:AAAAAAAATsAAAAAAAAAAAAAAAAAAAE5A",
        "lon/.zarray": {
            "chunks":[6], "compressor": None, "dtype": "<f8", "fill_value": "NaN", "filters": None, "order": "C",
            "shape": [6], "zarr_format":2
        },
        "lon/.zattrs": {
            "_ARRAY_DIMENSIONS":["lon"],"long_name":"longitude","standard_name":"longitude","units":"degrees_east"
        },
        "lon/0": "base64:AAAAAADAYsAAAAAAAIBWwAAAAAAAAD7AAAAAAAAAPkAAAAAAAIBWQAAAAAAAwGJA",
        "mean_wave_period/.zarray": {
            "chunks": [2,3,6], "compressor": None, "dtype": "<f8", "fill_value": "NaN", "filters": None, "order": "C",
            "shape": [2,3,6], "zarr_format":2
        },
        "mean_wave_period/.zattrs": {"_ARRAY_DIMENSIONS":["time", "lat", "lon"]},
        "mean_wave_period/0.0.0":
            "base64:AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/",
        "sign_wave_height/.zarray": {
            "chunks": [2,3,6], "compressor": None, "dtype": "<f8", "fill_value": "NaN", "filters": None, "order":"C",
            "shape": [2,3,6], "zarr_format": 2
        },
        "sign_wave_height/.zattrs": {"_ARRAY_DIMENSIONS":["time", "lat", "lon"]},
        "sign_wave_height/0.0.0": "base64:AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/",
        "time/.zarray": {"chunks": [2], "compressor": None,"dtype": "<i8", "fill_value": None, "filters": None,
                         "order": "C", "shape":[2], "zarr_format": 2},
        "time/.zattrs": {
            "_ARRAY_DIMENSIONS": ["time"], "calendar": "proleptic_gregorian", "units": "seconds since 1970-01-01"
        },
        "time/0": "base64:YKLCZwAAAAAgS8NnAAAAAA==",
        "wave_direction/.zarray": {
            "chunks": [2,3,6], "compressor": None, "dtype": "<f8", "fill_value": "NaN", "filters": None, "order": "C",
            "shape": [2,3,6], "zarr_format": 2
        },
        "wave_direction/.zattrs": {"_ARRAY_DIMENSIONS": ["time", "lat", "lon"]},
        "wave_direction/0.0.0":
            "base64:AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/AAAAAAAA+H8AAAAAAAD4fwAAAAAAAPh/"
    }
}

VARCHUNK_TEMPLATE = [
    "",
    8744,
    825984
]

TIME_URL_TEMPLATE = "https://erddap-danubius.ve.ismar.cnr.it/erddap/griddap/kassandra_bs.nc?time%5B(2024-06-30T00:00:00Z):1:({timestep})%5D"
MVP_URL_TEMPLATE = "https://erddap-danubius.ve.ismar.cnr.it/erddap/griddap/kassandra_bs.nc?mean_wave_period%5B({timestep}):1:({timestep})%5D%5B(40.9):1:(46.64)%5D%5B(27.46):1:(41.78)%5D"
SWH_URL_TEMPLATE = "https://erddap-danubius.ve.ismar.cnr.it/erddap/griddap/kassandra_bs.nc?sign_wave_height%5B({timestep}):1:({timestep})%5D%5B(40.9):1:(46.64)%5D%5B(27.46):1:(41.78)%5D"
WD_URL_TEMPLATE = "https://erddap-danubius.ve.ismar.cnr.it/erddap/griddap/kassandra_bs.nc?wave_direction%5B({timestep}):1:({timestep})%5D%5B(40.9):1:(46.64)%5D%5B(27.46):1:(41.78)%5D"

TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
