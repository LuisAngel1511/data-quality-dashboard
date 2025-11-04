import pandas as pd
from pathlib import Path

def _read(path: str) -> pd.DataFrame:
    p = Path(path)
    if p.suffix.lower() in [".parquet", ".pq", ".parq"]:
        return pd.read_parquet(p)
    return pd.read_csv(p, low_memory=False)

def nulls_per_column(file_path: str):
    df = _read(file_path)
    total = len(df)
    per_col = []
    for c in df.columns:
        cnt = int(df[c].isna().sum())
        per_col.append({"col": c, "count": cnt, "pct": float(cnt/total) if total else 0.0})
    per_col.sort(key=lambda x: x["pct"], reverse=True)
    return {"total_pct": float(df.isna().sum().sum() / (df.size or 1)), "per_column": per_col}

def duplicates_info(file_path: str, sample=5):
    df = _read(file_path)
    dup_mask = df.duplicated()
    count = int(dup_mask.sum())
    sample_rows = df[dup_mask].head(sample).to_dict(orient="records")
    return {"count": count, "sample_rows": sample_rows}

def distribution(file_path: str, column: str, bins: int = 20):
    df = _read(file_path)
    if column not in df.columns:
        return {"error": f"columna {column} inexistente"}
    s = df[column].dropna()
    if s.dtype == "object" or s.dtype.name.startswith("datetime"):
        vc = s.astype(str).value_counts().head(50)
        return {"type": "categorical", "values": [{"label": k, "count": int(v)} for k, v in vc.items()]}
    hist = pd.cut(s, bins=bins, include_lowest=True, right=False, duplicates="drop").value_counts().sort_index()
    result = [{"bin": str(idx), "count": int(val)} for idx, val in hist.items()]
    return {"type": "numeric", "values": result}
