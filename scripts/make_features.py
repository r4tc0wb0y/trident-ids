#!/usr/bin/env python
"""
Feature extraction script for trident-ids.

Extracts spatiotemporal features from raw network data.
"""

import argparse
import logging
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils import setup_logging, load_config, ensure_dir


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Extract spatiotemporal features from network data"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="configs/data_paths.yml",
        help="Path to configuration file"
    )
    parser.add_argument(
        "--input-dir",
        type=str,
        help="Input directory containing raw data (overrides config)"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        help="Output directory for features (overrides config)"
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging level"
    )
    parser.add_argument(
        "--log-file",
        type=str,
        help="Log file path (optional)"
    )
    
    return parser.parse_args()


def main():
    """Main feature extraction pipeline."""
    args = parse_args()
    
    # Setup logging
    setup_logging(log_level=args.log_level, log_file=args.log_file)
    logger = logging.getLogger(__name__)
    
    logger.info("Starting feature extraction pipeline")
    
    try:
        # Load configuration
        if Path(args.config).exists():
            config = load_config(args.config)
            logger.info(f"Loaded configuration from {args.config}")
        else:
            logger.warning(f"Config file not found: {args.config}, using defaults")
            config = {}
        
        # Set input/output directories
        input_dir = args.input_dir or config.get("raw_data", {}).get("pcap_dir", "data/raw")
        output_dir = args.output_dir or config.get("processed_data", {}).get("features_dir", "data/processed/features")
        
        # Ensure output directory exists
        ensure_dir(output_dir)
        
        logger.info(f"Input directory: {input_dir}")
        logger.info(f"Output directory: {output_dir}")
        
        # TODO: Implement feature extraction logic
        logger.info("Feature extraction pipeline would run here")
        logger.info("This is a placeholder - implement actual feature extraction")
        
        logger.info("Feature extraction completed successfully")
        
    except Exception as e:
        logger.error(f"Feature extraction failed: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
