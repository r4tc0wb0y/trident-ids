#!/usr/bin/env python
"""
Model evaluation script for trident-ids.

Evaluates trained IDS models on test data.
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
        description="Evaluate trained IDS models"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="configs/data_paths.yml",
        help="Path to configuration file"
    )
    parser.add_argument(
        "--model-path",
        type=str,
        required=True,
        help="Path to trained model"
    )
    parser.add_argument(
        "--test-data",
        type=str,
        help="Path to test data (overrides config)"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        help="Output directory for evaluation results (overrides config)"
    )
    parser.add_argument(
        "--metrics",
        type=str,
        nargs="+",
        default=["accuracy", "precision", "recall", "f1"],
        help="Metrics to compute"
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
    """Main evaluation pipeline."""
    args = parse_args()
    
    # Setup logging
    setup_logging(log_level=args.log_level, log_file=args.log_file)
    logger = logging.getLogger(__name__)
    
    logger.info("Starting model evaluation pipeline")
    
    try:
        # Load configuration
        if Path(args.config).exists():
            config = load_config(args.config)
            logger.info(f"Loaded configuration from {args.config}")
        else:
            logger.warning(f"Config file not found: {args.config}, using defaults")
            config = {}
        
        # Set directories
        test_data = args.test_data or config.get("processed_data", {}).get("features_dir", "data/processed/features")
        output_dir = args.output_dir or config.get("evaluation", {}).get("results_dir", "results/evaluation")
        
        # Ensure output directory exists
        ensure_dir(output_dir)
        
        logger.info(f"Model path: {args.model_path}")
        logger.info(f"Test data: {test_data}")
        logger.info(f"Output directory: {output_dir}")
        logger.info(f"Metrics: {', '.join(args.metrics)}")
        
        # TODO: Implement evaluation logic
        logger.info("Model evaluation would run here")
        logger.info("This is a placeholder - implement actual model evaluation")
        
        logger.info("Model evaluation completed successfully")
        
    except Exception as e:
        logger.error(f"Model evaluation failed: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
