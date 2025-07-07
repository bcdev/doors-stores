## Changes in 0.1.6
* Updated PML Data: 
  - Fixed reflectance ranges
  - Fixed offsets of MSI chlorophyll, tsm, and dominant_owt
  - Added missing OLCI times

## Changes in 0.1.5
* Include package data

## Changes in 0.1.4
* Integrated PML Data: There is now an MsiKerchunkDataStore (to access PML MSI Data
  over a THREDDS server) and an OlciKerchunkDataStore (to access PML OLCI Data).
  Both Stores use Reference File Systems.

## Changes in 0.1.3
* Fixed checking of response validity

## Changes in 0.1.2
* Added default file to KASSANDRA kerchunk store to account for case when no online
  data is found

## Changes in 0.1.1
* Removed log norm

## Changes in 0.1
* First version of KASSANDRA Kerchunk Store
 