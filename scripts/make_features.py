import argparse, os, pandas as pd, numpy as np
from pathlib import Path

# Mapea aquí los nombres de columnas de tu dataset NPS
DEFAULTS = dict(
    ts_col="ts",            # timestamp (segundos UNIX o ISO8601)
    dur_col="duration",     # duración del flow en seg
    src_col="src",          # host origen (pseudonimizado)
    dst_col="dst",          # host destino (pseudonimizado)
    bytes_col="bytes",      # bytes totales del flow
    pkts_col="pkts"         # paquetes totales del flow
)

def build(df, cfg):
    # Normaliza timestamp -> epoch (segundos)
    if np.issubdtype(df[cfg['ts_col']].dtype, np.number):
        t = pd.to_datetime(df[cfg['ts_col']], unit='s', errors='coerce')
    else:
        t = pd.to_datetime(df[cfg['ts_col']], errors='coerce')
    df = df.copy()
    df["ts"] = t
    df["time_min"] = (df["ts"] - df["ts"].min()).dt.total_seconds()/60.0

    # Evita división por cero
    eps = 1e-6
    df["duration_s"] = df[cfg["dur_col"]].astype(float).clip(lower=eps)
    df["bps_60s"] = df[cfg["bytes_col"]].astype(float) / df["duration_s"]
    df["pps_60s"] = df[cfg["pkts_col"]].astype(float) / df["duration_s"]

    # Ventanas de 60s para grado (número de pares únicos por host)
    df["t_bucket"] = (df["ts"].astype("int64") // 10**9 // 60)  # minuto
    # grado por src (n° destinos distintos en cada minuto)
    deg = (df.groupby(["src", "t_bucket"])["dst"]
             .nunique()
             .rename("deg_60s")
             .reset_index())
    df = df.merge(deg, how="left", left_on=["src","t_bucket"], right_on=["src","t_bucket"])
    df["deg_60s"] = df["deg_60s"].fillna(0)

    # Tamaño de marcador (flows por ventana y host)
    size = (df.groupby(["src","t_bucket"]).size()
              .rename("size_flow")
              .reset_index())
    df = df.merge(size, on=["src","t_bucket"], how="left")

    # Columnas finales sugeridas
    keep = ["time_min","deg_60s","bps_60s","pps_60s","size_flow","src","dst","t_bucket"]
    return df[keep].sort_values("time_min")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=False, default="data/raw/flows_sample.csv",
                    help="CSV/parquet con flows (mínimo: ts,duration,src,dst,bytes,pkts)")
    ap.add_argument("--output", default="data/processed/features.parquet")
    ap.add_argument("--ts_col", default=DEFAULTS["ts_col"])
    ap.add_argument("--dur_col", default=DEFAULTS["dur_col"])
    ap.add_argument("--src_col", default=DEFAULTS["src_col"])
    ap.add_argument("--dst_col", default=DEFAULTS["dst_col"])
    ap.add_argument("--bytes_col", default=DEFAULTS["bytes_col"])
    ap.add_argument("--pkts_col", default=DEFAULTS["pkts_col"])
    args = vars(ap.parse_args())

    # Lee CSV o Parquet
    in_path = Path(args["input"])
    if in_path.suffix.lower() == ".parquet":
        df = pd.read_parquet(in_path)
    else:
        df = pd.read_csv(in_path)

    cfg = {k: args[k] for k in ["ts_col","dur_col","src_col","dst_col","bytes_col","pkts_col"]}
    df = df.rename(columns={
        cfg["ts_col"]:"ts", cfg["dur_col"]:"duration",
        cfg["src_col"]:"src", cfg["dst_col"]:"dst",
        cfg["bytes_col"]:"bytes", cfg["pkts_col"]:"pkts"
    })

    out = build(df, cfg)
    Path(args["output"]).parent.mkdir(parents=True, exist_ok=True)
    out.to_parquet(args["output"], index=False)
    print(f"[OK] Saved features -> {args['output']}  Rows={len(out)}")

if __name__ == "__main__":
    main()
