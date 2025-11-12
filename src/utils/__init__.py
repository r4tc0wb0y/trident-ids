"""
Utility functions and helpers for trident-ids.
"""

import logging
import yaml
from pathlib import Path


def setup_logging(log_level="INFO", log_file=None):
    """
    Set up logging configuration.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional log file path
    """
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    handlers = [logging.StreamHandler()]
    if log_file:
        handlers.append(logging.FileHandler(log_file))
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=log_format,
        handlers=handlers
    )


def load_config(config_path):
    """
    Load YAML configuration file.
    
    Args:
        config_path: Path to YAML configuration file
        
    Returns:
        Dictionary containing configuration
    """
    config_path = Path(config_path)
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    return config


def ensure_dir(directory):
    """
    Ensure directory exists, create if it doesn't.
    
    Args:
        directory: Path to directory
    """
    Path(directory).mkdir(parents=True, exist_ok=True)
