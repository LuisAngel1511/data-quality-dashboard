import pandas as pd
from pathlib import Path
from ..models import Dataset, Column, Profile

def infer_role(series: pd.Series) -> str:
    if pd.api.types.is_numeric_dtype(series):
        return "numeric"
    if pd.api.types.is_datetime64_any_dtype(series):
        return "datetime"
    try:
        ratio = series.nunique(dropna=True) / max(len(series), 1)
        if ratio < 0.05:
            return "categorical"
    except Exception:
        pass
    return "text"

def load_and_profile(dataset: Dataset) -> None:
    """Lee el archivo (CSV o Parquet), infiere columnas y guarda perfil básico."""
    path = Path(dataset.file.path)
    if path.suffix.lower() in [".parquet", ".pq", ".parq"]:
        df = pd.read_parquet(path)
    else:
        df = pd.read_csv(path, low_memory=False)

    dataset.n_rows, dataset.n_cols = df.shape
    dataset.save()

    dataset.columns.all().delete()
    for col in df.columns:
        dtype = str(df[col].dtype)
        role = infer_role(df[col])
        Column.objects.create(dataset=dataset, name=col, dtype_detected=dtype, role=role)

    total_nulls = int(df.isna().sum().sum())
    total_vals = int(df.size)
    stats = {
        "rows": int(df.shape[0]),
        "cols": int(df.shape[1]),
        "nulls_total": total_nulls,
        "nulls_pct": float(total_nulls / total_vals) if total_vals else 0.0,
        "duplicates": int(df.duplicated().sum()),
    }
    Profile.objects.update_or_create(dataset=dataset, defaults={"stats_json": stats})
