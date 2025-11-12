# trident-ids 🔱

**T**emporal/graph **R**esearch **I**n **D**etection on **E**volving **N**etwork **T**opologies

A Python framework for spatiotemporal intrusion detection system (IDS) ablation studies on network traffic data. This project combines temporal analysis with graph-based spatial representations to detect and analyze network intrusions.

## Features

- **Spatiotemporal Analysis**: Combines temporal patterns with network topology analysis
- **Modular Architecture**: Separate modules for ingestion, feature engineering, modeling, evaluation, and visualization
- **3D Visualization**: Interactive 3D plots for triage and analysis using Plotly
- **CLI Scripts**: Command-line tools with logging and configuration support
- **Jupyter Notebooks**: Interactive analysis and exploration
- **Extensible**: Easy to add new models, features, and evaluation metrics

## Project Structure

```
trident-ids/
├── configs/               # Configuration files
│   └── data_paths.example.yml
├── env/                   # Environment setup
│   └── environment.yml
├── src/                   # Source code
│   ├── ingest/           # Data ingestion
│   ├── features/         # Feature engineering
│   ├── models/           # IDS models
│   ├── eval/             # Evaluation metrics
│   ├── viz/              # Visualization
│   └── utils/            # Utility functions
├── scripts/              # CLI scripts
│   ├── make_features.py  # Feature extraction
│   ├── train.py          # Model training
│   ├── evaluate.py       # Model evaluation
│   └── plot_triage3d.py  # 3D visualization
├── notebooks/            # Jupyter notebooks
│   └── 01_eda.ipynb
└── tests/                # Test suite
```

## Quickstart

### 1. Environment Setup

Create and activate the conda environment:

```bash
conda env create -f env/environment.yml
conda activate trident-ids
```

Or using pip:

```bash
pip install numpy pandas scikit-learn networkx matplotlib plotly pyyaml jupyterlab pytest pytest-cov
```

### 2. Configuration

Copy the example configuration and customize for your data:

```bash
cp configs/data_paths.example.yml configs/data_paths.yml
# Edit configs/data_paths.yml with your data paths
```

### 3. Feature Extraction

Extract spatiotemporal features from raw network data:

```bash
python scripts/make_features.py \
    --config configs/data_paths.yml \
    --input-dir /path/to/raw/data \
    --output-dir data/processed/features \
    --log-level INFO
```

### 4. Model Training

Train an IDS model on extracted features:

```bash
python scripts/train.py \
    --config configs/data_paths.yml \
    --features-dir data/processed/features \
    --model-type spatiotemporal \
    --epochs 100 \
    --batch-size 32 \
    --log-level INFO
```

### 5. Evaluation

Evaluate the trained model:

```bash
python scripts/evaluate.py \
    --config configs/data_paths.yml \
    --model-path models/saved/model.pkl \
    --test-data data/processed/features/test \
    --metrics accuracy precision recall f1 \
    --log-level INFO
```

### 6. 3D Visualization

Generate 3D spatiotemporal visualizations:

```bash
python scripts/plot_triage3d.py \
    --config configs/data_paths.yml \
    --results-dir results/evaluation \
    --plot-type scatter3d \
    --interactive \
    --save-format html \
    --log-level INFO
```

### 7. Interactive Analysis

Launch JupyterLab for interactive exploration:

```bash
jupyter lab notebooks/01_eda.ipynb
```

## CLI Arguments

All scripts support common arguments:

- `--config`: Path to YAML configuration file (default: `configs/data_paths.yml`)
- `--log-level`: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `--log-file`: Optional log file path

Script-specific arguments:

### make_features.py
- `--input-dir`: Input directory containing raw data
- `--output-dir`: Output directory for features

### train.py
- `--features-dir`: Directory containing extracted features
- `--model-type`: Model type (baseline, temporal, spatial, spatiotemporal)
- `--epochs`: Number of training epochs
- `--batch-size`: Batch size for training

### evaluate.py
- `--model-path`: Path to trained model (required)
- `--test-data`: Path to test data
- `--metrics`: Metrics to compute (space-separated list)

### plot_triage3d.py
- `--results-dir`: Directory containing evaluation results
- `--plot-type`: Type of 3D plot (scatter3d, surface, network3d, temporal3d)
- `--interactive`: Generate interactive Plotly visualizations
- `--save-format`: Output format (html, png, pdf, svg)

## Development

### Running Tests

```bash
pytest tests/ -v
```

With coverage:

```bash
pytest tests/ --cov=src --cov-report=html
```

### Code Style

This project follows PEP 8 style guidelines. Format code with:

```bash
black src/ scripts/ tests/
flake8 src/ scripts/ tests/
```

## Dependencies

- **numpy**: Numerical computing
- **pandas**: Data manipulation and analysis
- **scikit-learn**: Machine learning algorithms
- **networkx**: Graph/network analysis
- **matplotlib**: Static plotting
- **plotly**: Interactive 3D visualizations
- **pyyaml**: Configuration file parsing
- **jupyterlab**: Interactive notebooks
- **pytest**: Testing framework

## License

See [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Citation

If you use this code in your research, please cite:

```bibtex
@software{trident_ids,
  title = {trident-ids: Spatiotemporal IDS Framework},
  author = {Your Name},
  year = {2025},
  url = {https://github.com/r4tc0wb0y/trident-ids}
}
```
