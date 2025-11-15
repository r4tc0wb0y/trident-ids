#!/usr/bin/env python3
import argparse, sys
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="data/processed/features.parquet")
    ap.add_argument("--output_html", default="figures/triage_3d.html")
    args = ap.parse_args()

    print(f"[INFO] CWD={Path.cwd()}")
    print(f"[INFO] Reading: {args.input}")
    p = Path(args.input)
    if not p.exists():
        print(f"[ERROR] Input not found: {p.resolve()}", file=sys.stderr)
        sys.exit(2)

    try:
        df = pd.read_parquet(p) if p.suffix==".parquet" else pd.read_csv(p)
    except Exception as e:
        print(f"[ERROR] Failed to read {p}: {e}", file=sys.stderr)
        sys.exit(3)

    # Valores por defecto si faltan
    if "score" not in df.columns: df["score"] = 0.5
    if "scenario" not in df.columns: df["scenario"] = "unknown"
    if "size_flow" not in df.columns: df["size_flow"] = 8

    print(f"[INFO] Rows={len(df)}  Cols={list(df.columns)}")

    fig = go.Figure()
    for sc, sub in df.groupby("scenario"):
        fig.add_trace(go.Scatter3d(
            x=sub["time_min"], y=sub["deg_60s"], z=sub["bps_60s"],
            mode="markers", name=str(sc),
            marker=dict(size=sub["size_flow"].clip(5,22),
                        color=sub["score"], colorscale="Viridis", opacity=0.85)
        ))

    out = Path(args.output_html)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(str(out), include_plotlyjs="cdn")
    print(f"[OK] Wrote {out.resolve()}")

if __name__ == "__main__":
    main()
