<p align="center">
  <img src="logo/lisf_logo.png" alt="Land Surface Toolkit Logo" width="400"/>
</p>

# Land Surface Data Toolkit

A Python-based system for acquiring, processing, and analyzing land surface data from satellite observations and reanalysis products.

*This project is inspired by the [Land Information System Framework (LISF)](https://github.com/NASA-LIS/LISF) by NASA.*

## Overview

The Land Surface Data Toolkit provides tools for working with geospatial data commonly used in hydrology, agriculture, and environmental monitoring. The toolkit focuses on making satellite data accessible and easy to process for regional and continental-scale studies.

## Features

### Data Acquisition
- Download MODIS vegetation products (NDVI, LAI, EVI)
- Access SMAP soil moisture data
- Retrieve ERA5 meteorological reanalysis
- Download SRTM elevation data

### Geospatial Processing
- Coordinate system transformations
- Grid resampling and interpolation
- Spatial aggregation
- Land/water masking

### Parameter Generation
- Vegetation indices calculation
- Terrain analysis (slope, aspect, TWI)
- Soil property mapping
- Climate statistics

### Quality Control
- Data validation and range checking
- Gap detection and filling
- Statistical analysis
- Visualization tools

## Installation

### Requirements
- Python 3.9 or higher
- GDAL 3.0 or higher

### Install from source

```bash
git clone https://github.com/ductran27/LIS-landsurface-toolkit.git
cd LIS-landsurface-toolkit
pip install -e .
```

## Quick Start

### Download MODIS NDVI data

```python
from landsurface.downloaders import MODISDownloader

# Initialize downloader with NASA Earthdata credentials
downloader = MODISDownloader(username='your_username', password='your_password')

# Download data for study area
data = downloader.download_product(
    product='MOD13A2',
    bbox=(-120, 35, -115, 40),  # (west, south, east, north)
    start_date='2024-01-01',
    end_date='2024-12-31',
    output_dir='./data/modis'
)
```

### Calculate vegetation indices

```python
from landsurface.parameters import VegetationIndices

# Load NDVI data
vi = VegetationIndices('data/modis/MOD13A2_2024.nc')

# Calculate monthly averages
monthly_ndvi = vi.temporal_average(period='monthly')

# Detect anomalies
anomalies = vi.calculate_anomalies(baseline_period=(2015, 2023))

# Save results
monthly_ndvi.to_netcdf('monthly_ndvi_2024.nc')
```

### Process elevation data

```python
from landsurface.processing import DEMProcessor

# Load SRTM data
dem = DEMProcessor('data/srtm/elevation.tif')

# Calculate terrain parameters
slope = dem.calculate_slope(units='degrees')
aspect = dem.calculate_aspect(units='degrees')
twi = dem.topographic_wetness_index()

# Save results
slope.to_geotiff('slope.tif')
aspect.to_geotiff('aspect.tif')
```

## Data Sources

The toolkit works with data from the following sources:

### NASA EARTHDATA
- MODIS land products
- SMAP soil moisture
- VIIRS vegetation
- SRTM elevation

Registration required at https://urs.earthdata.nasa.gov

### Copernicus Climate Data Store
- ERA5 reanalysis
- Satellite products

Registration required at https://cds.climate.copernicus.eu

## Documentation

Full documentation is available at https://landsurface-toolkit.readthedocs.io

## Examples

See the `examples/` directory for complete working examples:
- `download_modis.py` - Download and process MODIS data
- `vegetation_analysis.py` - Analyze vegetation trends
- `terrain_processing.py` - Generate terrain parameters
- `soil_moisture_analysis.py` - Process SMAP data

## Contributing

Contributions are welcome. Please read CONTRIBUTING.md for guidelines.

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Citation

If you use this toolkit in your research, please cite:

```
Land Surface Data Toolkit (2025). 
A Python toolkit for land surface data processing.
https://github.com/ductran27/LIS-landsurface-toolkit
```

## Acknowledgments

This toolkit was developed to provide accessible tools for land surface data analysis. It uses data from NASA, NOAA, and the European Space Agency.

## Contact

For questions and support, please open an issue on GitHub.
