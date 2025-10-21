"""
SMAP soil moisture data downloader using NASA EARTHDATA API.

This module provides functionality to download SMAP (Soil Moisture Active Passive)
soil moisture products from NASA's EARTHDATA system.
"""

from pathlib import Path
from typing import List, Optional, Tuple, Dict
from datetime import datetime
import earthaccess

from landsurface.downloaders.base import BaseDownloader


class SMAPDownloader(BaseDownloader):
    """
    Download SMAP soil moisture products from NASA EARTHDATA.
    
    SMAP provides global soil moisture measurements at various resolutions
    and processing levels. This downloader supports the most commonly used
    Level 3 and Level 4 products.
    
    Requires NASA EARTHDATA credentials. Register at https://urs.earthdata.nasa.gov
    
    Parameters
    ----------
    username : str, optional
        NASA EARTHDATA username
    password : str, optional
        NASA EARTHDATA password
    output_dir : str, optional
        Directory to save downloaded files. Default is './data/smap'
    verbose : bool, optional
        Enable verbose logging. Default is True
        
    Examples
    --------
    >>> downloader = SMAPDownloader(username='user', password='pass')
    >>> files = downloader.download_product(
    ...     product='SPL3SMP',
    ...     bbox=(-120, 35, -115, 40),
    ...     start_date='2024-01-01',
    ...     end_date='2024-01-31'
    ... )
    """
    
    # Supported SMAP products
    SUPPORTED_PRODUCTS = {
        'SPL3SMP': 'SMAP L3 Radiometer Global Daily 36km Soil Moisture',
        'SPL3SMP_E': 'SMAP L3 Enhanced Global Daily 9km Soil Moisture',
        'SPL4SMAU': 'SMAP L4 Global 3-hourly 9km Surface/Root Zone Soil Moisture Analysis Update',
        'SPL4SMGP': 'SMAP L4 Global 3-hourly 9km Surface/Root Zone Soil Moisture Geophysical Data',
        'SPL4CMDL': 'SMAP L4 Global Daily 9km Carbon Net Ecosystem Exchange',
    }
    
    def __init__(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        output_dir: str = './data/smap',
        verbose: bool = True
    ):
        super().__init__(username, password, output_dir, verbose)
        
        # Authenticate with NASA EARTHDATA
        if username and password:
            self._authenticate()
    
    def _authenticate(self) -> None:
        """Authenticate with NASA EARTHDATA system."""
        try:
            earthaccess.login(username=self.username, password=self.password)
            self.logger.info("Successfully authenticated with NASA EARTHDATA")
        except Exception as e:
            self.logger.error(f"Authentication failed: {e}")
            raise
    
    def list_products(self) -> Dict[str, str]:
        """
        List all supported SMAP products.
        
        Returns
        -------
        dict
            Dictionary mapping product codes to descriptions
        """
        return self.SUPPORTED_PRODUCTS.copy()
    
    def download_product(
        self,
        product: str,
        bbox: Tuple[float, float, float, float],
        start_date: str,
        end_date: str,
        output_dir: Optional[str] = None,
        skip_existing: bool = True,
        max_files: Optional[int] = None
    ) -> List[Path]:
        """
        Download SMAP product for specified area and time period.
        
        Parameters
        ----------
        product : str
            SMAP product code (e.g., 'SPL3SMP', 'SPL3SMP_E')
        bbox : tuple
            Bounding box as (west, south, east, north) in decimal degrees
        start_date : str
            Start date in format 'YYYY-MM-DD'
        end_date : str
            End date in format 'YYYY-MM-DD'
        output_dir : str, optional
            Override default output directory
        skip_existing : bool, optional
            Skip downloading if file already exists. Default is True
        max_files : int, optional
            Maximum number of files to download
            
        Returns
        -------
        list
            List of Path objects for downloaded files
            
        Raises
        ------
        ValueError
            If product is not supported or parameters are invalid
        RuntimeError
            If download fails
            
        Examples
