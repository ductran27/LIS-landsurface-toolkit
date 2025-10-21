"""
Base downloader class providing common functionality for all data downloaders.
"""

import os
import logging
from pathlib import Path
from typing import Optional, Tuple, Dict, Any
from datetime import datetime
import requests
from tqdm import tqdm


class BaseDownloader:
    """
    Base class for data downloaders.
    
    Provides common functionality including authentication, file management,
    and progress tracking that is shared across all downloader implementations.
    
    Parameters
    ----------
    username : str, optional
        Username for authentication
    password : str, optional
        Password for authentication
    output_dir : str, optional
        Directory to save downloaded files. Default is './data'
    verbose : bool, optional
        Enable verbose logging. Default is True
    """
    
    def __init__(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        output_dir: str = './data',
        verbose: bool = True
    ):
        self.username = username
        self.password = password
        self.output_dir = Path(output_dir)
        self.verbose = verbose
        
        # Set up logging
        self.logger = self._setup_logger()
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Session for HTTP requests
        self.session = requests.Session()
        if username and password:
            self.session.auth = (username, password)
    
    def _setup_logger(self) -> logging.Logger:
        """Configure logging for the downloader."""
        logger = logging.getLogger(self.__class__.__name__)
        
        if self.verbose:
            logger.setLevel(logging.INFO)
        else:
            logger.setLevel(logging.WARNING)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _validate_bbox(self, bbox: Tuple[float, float, float, float]) -> None:
        """
        Validate bounding box coordinates.
        
        Parameters
        ----------
        bbox : tuple
            Bounding box as (west, south, east, north) in decimal degrees
            
        Raises
        ------
        ValueError
            If bounding box coordinates are invalid
        """
        west, south, east, north = bbox
        
        if not (-180 <= west <= 180):
            raise ValueError(f"Western longitude {west} must be between -180 and 180")
        if not (-180 <= east <= 180):
            raise ValueError(f"Eastern longitude {east} must be between -180 and 180")
        if not (-90 <= south <= 90):
            raise ValueError(f"Southern latitude {south} must be between -90 and 90")
        if not (-90 <= north <= 90):
            raise ValueError(f"Northern latitude {north} must be between -90 and 90")
        if west >= east:
            raise ValueError("Western longitude must be less than eastern longitude")
        if south >= north:
            raise ValueError("Southern latitude must be less than northern latitude")
    
    def _validate_dates(
        self,
        start_date: str,
        end_date: str,
        date_format: str = '%Y-%m-%d'
    ) -> Tuple[datetime, datetime]:
        """
        Validate and parse date strings.
        
        Parameters
        ----------
        start_date : str
            Start date string
        end_date : str
            End date string
        date_format : str, optional
            Expected date format. Default is '%Y-%m-%d'
            
        Returns
        -------
        tuple
            Parsed datetime objects (start_dt, end_dt)
            
        Raises
        ------
        ValueError
            If dates are invalid or in wrong order
        """
        try:
            start_dt = datetime.strptime(start_date, date_format)
            end_dt = datetime.strptime(end_date, date_format)
        except ValueError as e:
            raise ValueError(f"Invalid date format. Expected {date_format}: {e}")
        
        if start_dt > end_dt:
            raise ValueError("Start date must be before end date")
        
        return start_dt, end_dt
    
    def _download_file(
        self,
        url: str,
        output_path: Path,
        show_progress: bool = True,
        chunk_size: int = 8192
    ) -> Path:
        """
        Download a file from a URL with progress tracking.
        
        Parameters
        ----------
        url : str
            URL to download from
        output_path : Path
            Path to save the downloaded file
        show_progress : bool, optional
            Show download progress bar. Default is True
        chunk_size : int, optional
            Download chunk size in bytes. Default is 8192
            
        Returns
        -------
        Path
            Path to the downloaded file
            
        Raises
        ------
        requests.exceptions.RequestException
            If download fails
        """
        self.logger.info(f"Downloading from {url}")
        
        response = self.session.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'wb') as f:
            if show_progress and total_size > 0:
                with tqdm(total=total_size, unit='B', unit_scale=True, desc=output_path.name) as pbar:
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        if chunk:
                            f.write(chunk)
                            pbar.update(len(chunk))
            else:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
        
        self.logger.info(f"Downloaded to {output_path}")
        return output_path
    
    def _check_file_exists(self, filepath: Path, skip_existing: bool = True) -> bool:
        """
        Check if a file already exists.
        
        Parameters
        ----------
        filepath : Path
            Path to check
        skip_existing : bool, optional
            If True, skip download if file exists. Default is True
            
        Returns
        -------
        bool
            True if file exists and should be skipped, False otherwise
        """
        if filepath.exists() and skip_existing:
            self.logger.info(f"File already exists, skipping: {filepath}")
            return True
        return False
    
    def get_credentials(self) -> Tuple[Optional[str], Optional[str]]:
        """
        Get stored credentials.
        
        Returns
        -------
        tuple
            Username and password
        """
        return self.username, self.password
    
    def set_credentials(self, username: str, password: str) -> None:
        """
        Update authentication credentials.
        
        Parameters
        ----------
        username : str
            New username
        password : str
            New password
        """
        self.username = username
        self.password = password
        self.session.auth = (username, password)
        self.logger.info("Credentials updated")
