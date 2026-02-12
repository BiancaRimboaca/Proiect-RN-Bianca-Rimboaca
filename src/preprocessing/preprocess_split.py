from __future__ import annotations
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from src.utils.io import ensure_dirs, load_config
import joblib

FEATURES = ["T_amb", "omega", "I", "T_prev"]
TARGET = "T_next"

def main() -> None:
    ensure_dirs()
    cfg = load_config()

    raw_path = cfg["paths"]["data_raw"]
    df = pd.read_csv(raw_path)

    # Curatare minima (optional)
    df = df.dropna().reset_index(drop=True)

    # Split
    train_ratio = float(cfg["dataset"]["train_ratio"])
    val_ratio = float(cfg["dataset"]["val_ratio"])
    test_ratio = float(cfg["dataset"]["test_ratio"])
    assert abs(train_ratio + val_ratio + test_ratio - 1.0) < 1e-6

    train_df, temp_df = train_test_split(df, test_size=(1.0 - train_ratio), random_state=42, shuffle=True)
    # din rest, separi val/test
    val_size = val_ratio / (val_ratio + test_ratio)
    val_df, test_df = train_test_split(temp_df, test_size=(1.0 - val_size), random_state=42, shuffle=True)

    # Standardizare doar pe train
    scaler_X = StandardScaler()
    scaler_y = StandardScaler()

    X_train = scaler_X.fit_transform(train_df[FEATURES].values)
    y_train = scaler_y.fit_transform(train_df[[TARGET]].values)

    X_val = scaler_X.transform(val_df[FEATURES].values)
    y_val = scaler_y.transform(val_df[[TARGET]].values)

    X_test = scaler_X.transform(test_df[FEATURES].values)
    y_test = scaler_y.transform(test_df[[TARGET]].values)

    # Salvam processed (standardizat) in CSV
    def pack(X, y) -> pd.DataFrame:
        out = pd.DataFrame(X, columns=[f"{c}_z" for c in FEATURES])
        out[f"{TARGET}_z"] = y.reshape(-1)
        return out

    train_out = pack(X_train, y_train)
    val_out = pack(X_val, y_val)
    test_out = pack(X_test, y_test)

    processed_path = cfg["paths"]["data_processed"]
    all_processed = pd.concat([train_out.assign(split="train"),
                               val_out.assign(split="validation"),
                               test_out.assign(split="test")], axis=0)
    all_processed.to_csv(processed_path, index=False)

    train_out.to_csv(cfg["paths"]["train_csv"], index=False)
    val_out.to_csv(cfg["paths"]["val_csv"], index=False)
    test_out.to_csv(cfg["paths"]["test_csv"], index=False)

    joblib.dump({"scaler_X": scaler_X, "scaler_y": scaler_y, "features": FEATURES, "target": TARGET},
                "outputs/models/scalers.joblib")

    print("[OK] processed + split saved.")

if __name__ == "__main__":
    main()
