# Getting Started with Land Surface Toolkit

## Quick Start Guide

This guide will help you set up and start using the Land Surface Toolkit.

## Step 1: Installation

### Prerequisites

Ensure you have Python 3.9 or higher:
```bash
python --version
```

### Install the Package

```bash
cd landsurface-toolkit
pip install -e .
```

This installs the package in editable mode, allowing you to modify the code and see changes immediately.

## Step 2: NASA EARTHDATA Registration

To download MODIS data, you need a free NASA EARTHDATA account:

1. Go to https://urs.earthdata.nasa.gov
2. Click "Register"
3. Fill out the registration form
4. Verify your email address
5. Save your username and password

## Step 3: Set Up Credentials

### Option 1: Environment Variables (Recommended)

Add to your `.bashrc` or `.zshrc`:
```bash
export EARTHDATA_USERNAME='your_username'
export EARTHDATA_PASSWORD='your_password'
```

Then reload:
```bash
source ~/.bashrc  # or ~/.zshrc
```

### Option 2: Pass Directly in Code

```python
from landsurface.downloaders import MODISDownloader

downloader = MODISDownloader(
    username='your_username',
    password='your_password'
)
```

## Step 4: Test the Installation

### Interactive Python Test

```python
# Start Python
python

# Import the package
from landsurface.downloaders import MODISDownloader

# Create downloader instance
downloader = MODISDownloader()

# List supported products
products = downloader.list_products()
print(f"Supported products: {len(products)}")

# Get info about a specific product
info = downloader.get_product_info('MOD13A2')
print(info)
```

Expected output:
```
Supported products: 11
{'product_code': 'MOD13A2', 
 'description': 'MODIS/Terra Vegetation Indices 16-Day L3 Global 1km',
 'spatial_resolution': '1km',
 'temporal_resolution': '16-day',
 'platform': 'Terra'}
```

## Step 5: Download Your First Dataset

### Run the Example Script

```bash
cd examples
python download_modis.py
```

This will download a small test dataset (5 files) of MODIS vegetation data.

### Or Use Interactively

```python
from landsurface.downloaders import MODISDownloader

# Initialize
downloader = MODISDownloader(
    username='your_username',
    password='your_password'
)

# Download data for a small area
files = downloader.download_product(
    product='MOD13A2',           # 16-day NDVI product
    bbox=(-120, 35, -119, 36),   # Small area in California
    start_date='2024-01-01',
    end_date='2024-01-31',       # One month only
    max_files=3                   # Limit for testing
)

print(f"Downloaded {len(files)} files")
```

## Common Use Cases

### 1. Vegetation Monitoring

Download NDVI data to monitor vegetation health:

```python
from landsurface.downloaders import MODISDownloader

downloader = MODISDownloader(username='user', password='pass')

# Download annual vegetation data
files = downloader.download_product(
    product='MOD13A2',
    bbox=(-120, 35, -115, 40),  # Your study area
    start_date='2024-01-01',
    end_date='2024-12-31'
)
```

### 2. Temperature Analysis

Download land surface temperature data:

```python
files = downloader.download_product(
    product='MOD11A2',           # 8-day LST
    bbox=(-105, 38, -103, 40),   # Colorado
    start_date='2024-06-01',
    end_date='2024-08-31'        # Summer season
)
```

### 3. Land Cover Classification

Download annual land cover data:

```python
files = downloader.download_product(
    product='MCD12Q1',           # Yearly land cover
    bbox=(-90, 30, -85, 35),     # Southeast US
    start_date='2023-01-01',
    end_date='2023-12-31'
)
```

## Understanding MODIS Products

### Vegetation Products

**MOD13A2 / MYD13A2** (Recommended for most users)
- NDVI and EVI vegetation indices
- 16-day composite
- 1 km resolution
- Good for regional vegetation monitoring

**MOD13Q1 / MYD13Q1**
- Higher resolution version
- 16-day composite
- 250 m resolution
- Better for detailed studies

**MOD15A2H / MYD15A2H**
- Leaf Area Index (LAI)
- 8-day composite
- 500 m resolution
- Useful for crop monitoring

### Temperature Products

**MOD11A2 / MYD11A2**
- Land surface temperature
- 8-day composite
- 1 km resolution
- Day and night temperatures

### Land Cover

**MCD12Q1**
- Annual land cover classification
- Multiple classification schemes
- 500 m resolution
- Updated yearly

## Troubleshooting

### Authentication Errors

**Problem:** "Authentication failed"

**Solutions:**
1. Verify credentials at https://urs.earthdata.nasa.gov
2. Check for typos in username/password
3. Ensure account is activated via email

### No Data Found

**Problem:** "No granules found"

**Possible causes:**
1. Area outside data coverage
2. Dates before satellite launch
3. No data for that specific area/time

**Solutions:**
1. Check product availability dates
2. Adjust bounding box coordinates
3. Try different time period

### Download Fails

**Problem:** Download stops or fails

**Solutions:**
1. Check internet connection
2. Try smaller date range
3. Use max_files parameter to limit downloads
4. Check available disk space

## Next Steps

### Expand Functionality

The toolkit is designed to be extended. Consider adding:

1. **Data Processing:**
   - Time series analysis
   - Anomaly detection
   - Trend calculation

2. **Visualization:**
   - Maps and plots
   - Interactive dashboards
   - Animation generation

3. **Additional Data Sources:**
   - SMAP soil moisture
   - ERA5 reanalysis
   - Sentinel data

### Learn More

- Read the full documentation in `docs/`
- Explore additional examples in `examples/`
- Check PROJECT_STATUS.md for development roadmap
- See LISF_TECHNICAL_ASSESSMENT.md for technical details

## Getting Help

If you encounter issues:

1. Check this guide first
2. Review the examples in `examples/`
3. Read the docstrings in the source code
4. Open an issue on GitHub (when repository is public)

## Contributing

We welcome contributions! Areas where you can help:

- Add new data downloaders (SMAP, ERA5, Sentinel)
- Implement processing algorithms
- Create visualization tools
- Write documentation
- Report bugs
- Suggest features

## Resources

### NASA EARTHDATA
- Registration: https://urs.earthdata.nasa.gov
- Data catalog: https://search.earthdata.nasa.gov
- Documentation: https://earthdata.nasa.gov/learn

### MODIS Information
- Product descriptions: https://modis.gsfc.nasa.gov
- User guides: https://lpdaac.usgs.gov/data/
- Data quality flags: https://lpdaac.usgs.gov/data/get-started-data/quality-information/

## Summary

You now have:
- Working Python environment
- NASA EARTHDATA credentials
- Installed Land Surface Toolkit
- Downloaded test data
- Understanding of basic usage

Start exploring your land surface data!
