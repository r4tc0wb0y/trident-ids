#!/usr/bin/env python
"""
Model training script for trident-ids.

Trains IDS models on spatiotemporal features.
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
        description="Train IDS models on spatiotemporal features"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="configs/data_paths.yml",
        help="Path to configuration file"
    )
    parser.add_argument(
        "--features-dir",
        type=str,
        help="Directory containing extracted features (overrides config)"
    )
    parser.add_argument(
        "--model-type",
        type=str,
        default="baseline",
        help="Model type to train (baseline, temporal, spatial, spatiotemporal)"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        help="Output directory for trained models (overrides config)"
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=100,
        help="Number of training epochs"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=32,
        help="Batch size for training"
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
    """Main training pipeline."""
    args = parse_args()
    
    # Setup logging
    setup_logging(log_level=args.log_level, log_file=args.log_file)
    logger = logging.getLogger(__name__)
    
    logger.info("Starting model training pipeline")
    
    try:
        # Load configuration
        if Path(args.config).exists():
            config = load_config(args.config)
            logger.info(f"Loaded configuration from {args.config}")
        else:
            logger.warning(f"Config file not found: {args.config}, using defaults")
            config = {}
        
        # Set directories
        features_dir = args.features_dir or config.get("processed_data", {}).get("features_dir", "data/processed/features")
        output_dir = args.output_dir or config.get("models", {}).get("saved_models_dir", "models/saved")
        
        # Ensure output directory exists
        ensure_dir(output_dir)
        
        logger.info(f"Features directory: {features_dir}")
        logger.info(f"Model type: {args.model_type}")
        logger.info(f"Output directory: {output_dir}")
        logger.info(f"Training parameters: epochs={args.epochs}, batch_size={args.batch_size}")
        
        # TODO: Implement training logic
        logger.info("Model training would run here")
        logger.info("This is a placeholder - implement actual model training")
        
        logger.info("Model training completed successfully")
        
    except Exception as e:
        logger.error(f"Model training failed: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
