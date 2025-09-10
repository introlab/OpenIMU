# libopenimu

OpenIMU - Data Analyser for Inertial Measurement Units and Actimetry Data

## Description

OpenIMU aims to provide an open source and free generic data importer, viewer, manager, processor and exporter for Inertial Measurement Units (IMU) and actimetry data. By using a common sensor data format and structure, data from different sources can be imported and managed in the software.

This package contains the core library for OpenIMU, including algorithms, database management, importers, models, streamers, and tools.

## Features

### Current features

* Common file format (SQLite) managed by OpenIMU, but that can also be opened from other software

* Import recorded data from sensors:
  * [Actigraph GTX3 series](https://www.actigraphcorp.com/actigraph-wgt3x-bt)
  * [OpenIMU-MiniLogger](https://github.com/introlab/OpenIMU-MiniLogger)
  * AppleWatch SensorLogger (Custom research app for data collection)

* Transfer data directly from sensors:
  * AppleWatch SensorLogger (Custom research app for data collection)

* Data organization
  * By participants groups
  * By participants
  * By recordsets
  * By results

* Data viewing
  * Temporal display of recordsets to quickly see when data was recorded
  * Sensor graph view plotting with zoom functions
  * GPS viewer for GPS data

* Data processing
  * Processing module, currently supporting:
    * Freedson Activity Algorithm (Freedson PS1, Melanson E, Sirard J., Calibration of the Computer Science and Applications, Inc. accelerometer., Med Sci Sports Exerc. 1998 May;30(5):777-81)
    * Evenson Activity Algorithm (Kelly R. Evenson, Diane J. Catellier, Karminder Gill, Kristin S. Ondrak & Robert G. McMurray (2008) Calibration of two objective measures of physical activity for children, Journal of Sports Sciences, 26:14, 1557-1565, DOI: 10.1080/02640410802334196 )
  * Processed results viewer

* Data exporter
  * CSV format
  * Matlab format
  * Data export selector

## Installation

```bash
pip install libopenimu
```

## Usage

```python
import libopenimu
```

## Authors

* Dominic Létourneau (@doumdi)
* Simon Brière (@sbriere)

## License

See LICENSE.TXT
