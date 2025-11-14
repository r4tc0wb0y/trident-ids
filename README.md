# trident-ids 🔱
Temporal/graph Research In Detection on Evolving Network Topologies

Course-scale spatiotemporal IDS on NPS traffic. Compare: tabular vs +temporal vs +graph.
**Metrics:** PR-AUC, ROC@~1% FPR, F1, alert latency.

## Data & privacy
NPS-provided, de-identified. Raw data **never** committed. Configure local paths in `configs/data_paths.yml`.

## Quickstart
conda env create -f env/environment.yml
conda activate trident-ids
python scripts/make_features.py --config configs/data_paths.yml
python scripts/train.py --ablation tabular
python scripts/evaluate.py --run last
