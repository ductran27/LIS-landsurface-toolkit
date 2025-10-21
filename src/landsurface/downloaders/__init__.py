"""
Data downloaders for various satellite and reanalysis products.

This module provides classes for downloading data from:
- NASA EARTHDATA (MODIS, SMAP, VIIRS)
- Copernicus Climate Data Store (ERA5)
- USGS Earth Explorer (SRTM)
"""

from landsurface.downloaders.modis import MODISDownloader
from landsurface.downloaders.smap import SMAPDownloader
from landsurface.downloaders.base import BaseDownloader

__all__ = [
    'BaseDownloader',
    'MODISDownloader',
    'SMAPDownloader',
]
