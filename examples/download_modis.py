"""
Example: Download MODIS Vegetation Index Data

This script demonstrates how to download MODIS NDVI data using the
Land Surface Toolkit.
"""

import os
from landsurface.downloaders import MODISDownloader


def main():
    """Download MODIS vegetation index data for a study area."""
    
    # Get NASA EARTHDATA credentials from environment variables
    # Register at https://urs.earthdata.nasa.gov
    username = os.getenv('EARTHDATA_USERNAME')
    password = os.getenv('EARTHDATA_PASSWORD')
    
    if not username or not password:
        print("Please set EARTHDATA_USERNAME and EARTHDATA_PASSWORD environment variables")
        print("Register at https://urs.earthdata.nasa.gov")
        return
    
    # Initialize MODIS downloader
    downloader = MODISDownloader(
        username=username,
        password=password,
        output_dir='./data/modis',
        verbose=True
    )
    
    # List available products
    print("Available MODIS products:")
    products = downloader.list_products()
    for code, description in products.items():
        print(f"  {code}: {description}")
    
    print("\n" + "="*80 + "\n")
    
    # Define study area (example: California Central Valley)
    bbox = (-122.0, 36.0, -119.0, 38.0)  # (west, south, east, north)
    
    # Define time period
    start_date = '2024-01-01'
    end_date = '2024-03-31'
    
    # Download MOD13A2 (16-day 1km NDVI/EVI)
    print(f"Downloading MOD13A2 data for area {bbox}")
    print(f"Time period: {start_date} to {end_date}")
    print("\nThis may take several minutes depending on data availability...\n")
    
    try:
        files = downloader.download_product(
            product='MOD13A2',
            bbox=bbox,
            start_date=start_date,
            end_date=end_date,
            max_files=5  # Limit to 5 files for testing
        )
        
        print(f"\nSuccessfully downloaded {len(files)} files:")
        for f in files:
            print(f"  - {f}")
        
        print("\nDownload complete!")
        print(f"Files saved to: {downloader.output_dir}")
        
    except Exception as e:
        print(f"Error during download: {e}")
        print("\nTroubleshooting:")
        print("1. Check your NASA EARTHDATA credentials")
        print("2. Verify internet connection")
        print("3. Try reducing the date range or area")


if __name__ == '__main__':
    main()
