"""
MODIS satellite data downloader using NASA EARTHDATA API.

This module provides functionality to download MODIS (Moderate Resolution Imaging
Spectroradiometer) land products from NASA's EARTHDATA system.
"""

from pathlib import Path
from typing import List, Optional, Tuple, Dict
from datetime import datetime, timedelta
import earthaccess

from landsurface.downloaders.base import BaseDownloader


class MODISDownloader(BaseDownloader):
    """
    Download MODIS land products from NASA EARTHDATA.
    
    Supported products include vegetation indices (MOD13), leaf area index (MOD15),
    land surface temperature (MOD11), and land cover (MCD12Q1).
    
    Requires NASA EARTHDATA credentials. Register at https://urs.earthdata.nasa.gov
    
    Parameters
    ----------
    username : str, optional
        NASA EARTHDATA username
    password : str, optional
        NASA EARTHDATA password
    output_dir : str, optional
        Directory to save downloaded files. Default is './data/modis'
    verbose : bool, optional
        Enable verbose logging. Default is True
        
    Examples
    --------
    >>> downloader = MODISDownloader(username='user', password='pass')
    >>> files = downloader.download_product(
    ...     product='MOD13A2',
    ...     bbox=(-120, 35, -115, 40),
    ...     start_date='2024-01-01',
    ...     end_date='2024-12-31'
    ... )
    """
    
    # Supported MODIS products with descriptions
    SUPPORTED_PRODUCTS = {
        'MOD13A2': 'MODIS/Terra Vegetation Indices 16-Day L3 Global 1km',
        'MOD13Q1': 'MODIS/Terra Vegetation Indices 16-Day L3 Global 250m',
        'MYD13A2': 'MODIS/Aqua Vegetation Indices 16-Day L3 Global 1km',
        'MYD13Q1': 'MODIS/Aqua Vegetation Indices 16-Day L3 Global 250m',
        'MOD15A2H': 'MODIS/Terra Leaf Area Index/FPAR 8-Day L4 Global 500m',
        'MYD15A2H': 'MODIS/Aqua Leaf Area Index/FPAR 8-Day L4 Global 500m',
        'MOD11A2': 'MODIS/Terra Land Surface Temperature/Emissivity 8-Day L3 Global 1km',
        'MYD11A2': 'MODIS/Aqua Land Surface Temperature/Emissivity 8-Day L3 Global 1km',
        'MCD12Q1': 'MODIS/Terra+Aqua Land Cover Type Yearly L3 Global 500m',
        'MOD09A1': 'MODIS/Terra Surface Reflectance 8-Day L3 Global 500m',
        'MYD09A1': 'MODIS/Aqua Surface Reflectance 8-Day L3 Global 500m',
    }
    
    def __init__(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        output_dir: str = './data/modis',
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
        List all supported MODIS products.
        
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
        Download MODIS product for specified area and time period.
        
        Parameters
        ----------
        product : str
            MODIS product code (e.g., 'MOD13A2', 'MOD15A2H')
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
            Maximum number of files to download. Useful for testing
            
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
        --------
        >>> downloader = MODISDownloader(username='user', password='pass')
        >>> files = downloader.download_product(
        ...     product='MOD13A2',
        ...     bbox=(-120, 35, -115, 40),
        ...     start_date='2024-01-01',
        ...     end_date='2024-03-31'
        ... )
        >>> print(f"Downloaded {len(files)} files")
        """
        # Validate inputs
        if product not in self.SUPPORTED_PRODUCTS:
            raise ValueError(
                f"Product '{product}' not supported. "
                f"Supported products: {list(self.SUPPORTED_PRODUCTS.keys())}"
            )
        
        self._validate_bbox(bbox)
        start_dt, end_dt = self._validate_dates(start_date, end_date)
        
        # Set output directory
        if output_dir:
            save_dir = Path(output_dir)
        else:
            save_dir = self.output_dir / product.lower()
        save_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger.info(f"Searching for {product} data")
        self.logger.info(f"Area: {bbox}")
        self.logger.info(f"Period: {start_date} to {end_date}")
        
        try:
            # Search for granules
            results = earthaccess.search_data(
                short_name=product,
                temporal=(start_date, end_date),
                bounding_box=bbox
            )
            
            if not results:
                self.logger.warning("No granules found for the specified parameters")
                return []
            
            self.logger.info(f"Found {len(results)} granules")
            
            # Limit number of files if specified
            if max_files and len(results) > max_files:
                self.logger.info(f"Limiting download to {max_files} files")
                results = results[:max_files]
            
            # Download files
            downloaded_files = []
            for i, granule in enumerate(results, 1):
                self.logger.info(f"Downloading file {i}/{len(results)}")
                
                # Download granule
                local_files = earthaccess.download(
                    granule,
                    str(save_dir)
                )
                
                if local_files:
                    downloaded_files.extend([Path(f) for f in local_files])
            
            self.logger.info(f"Successfully downloaded {len(downloaded_files)} files")
            return downloaded_files
            
        except Exception as e:
            self.logger.error(f"Download failed: {e}")
            raise RuntimeError(f"Failed to download {product} data: {e}")
    
    def get_product_info(self, product: str) -> Dict[str, any]:
        """
        Get information about a MODIS product.
        
        Parameters
        ----------
        product : str
            MODIS product code
            
        Returns
        -------
        dict
            Product information including description and temporal resolution
            
        Raises
        ------
        ValueError
            If product is not supported
        """
        if product not in self.SUPPORTED_PRODUCTS:
            raise ValueError(f"Product '{product}' not supported")
        
        # Determine temporal resolution from product code
        if '13' in product:
            temporal_res = '16-day'
        elif '15' in product or '11' in product or '09' in product:
            temporal_res = '8-day'
        elif '12' in product:
            temporal_res = 'yearly'
        else:
            temporal_res = 'varies'
        
        # Determine spatial resolution
        if 'Q1' in product or '250m' in self.SUPPORTED_PRODUCTS[product]:
            spatial_res = '250m'
        elif 'A2' in product and '13' in product:
            spatial_res = '1km'
        elif '500m' in self.SUPPORTED_PRODUCTS[product]:
            spatial_res = '500m'
        else:
            spatial_res = '1km'
        
        return {
            'product_code': product,
            'description': self.SUPPORTED_PRODUCTS[product],
            'spatial_resolution': spatial_res,
            'temporal_resolution': temporal_res,
            'platform': 'Terra' if product.startswith('MOD') else 
                       'Aqua' if product.startswith('MYD') else 'Terra+Aqua'
        }
