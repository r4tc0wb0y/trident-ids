"""
Tests for utility functions.
"""

import pytest
import tempfile
import yaml
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils import setup_logging, load_config, ensure_dir


def test_ensure_dir():
    """Test directory creation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_dir = Path(tmpdir) / "test" / "nested" / "dir"
        ensure_dir(test_dir)
        assert test_dir.exists()
        assert test_dir.is_dir()


def test_load_config():
    """Test configuration loading."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
        config_data = {'key': 'value', 'nested': {'key2': 'value2'}}
        yaml.dump(config_data, f)
        config_path = f.name
    
    try:
        config = load_config(config_path)
        assert config['key'] == 'value'
        assert config['nested']['key2'] == 'value2'
    finally:
        Path(config_path).unlink()


def test_load_config_not_found():
    """Test configuration loading with non-existent file."""
    with pytest.raises(FileNotFoundError):
        load_config("nonexistent_config.yml")


def test_setup_logging():
    """Test logging setup."""
    # Should not raise any exceptions
    setup_logging(log_level="INFO")
    setup_logging(log_level="DEBUG")
