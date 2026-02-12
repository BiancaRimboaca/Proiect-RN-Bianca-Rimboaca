from __future__ import annotations
import numpy as np
import pandas as pd
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
from src.utils.io import ensure_dirs, load_config
from src.utils.db import connect, init_db, insert_run, insert_metrics

def metrics(y_true, y_pred):
    mae = float(mean_absolute_error(y_true, y_pred))
    rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))
    r2 = float(r2_score(y_true, y_pred))
    return mae, rmse, r2

def main() -> None:
    ensure_dirs()
    cfg = load_config()

    train_path = cfg["paths"]["train_csv"]
    val_path = cfg["paths"]["val_csv"]
    test_path = cfg["paths"]["test_csv"]

    train_df = pd.read_csv(train_path)
    val_df = pd.read_csv(val_path)
    test_df = pd.read_csv(test_path)

    # features sunt cele cu _z
    X_cols = [c for c in train_df.columns if c.endswith("_z") and c != "T_next_z"]
    y_col = "T_next_z"

    X_train = train_df[X_cols].values
    y_train = train_df[y_col].values
    X_val = val_df[X_cols].values
    y_val = val_df[y_col].values
    X_test = test_df[X_cols].values
    y_test = test_df[y_col].values

    nn = cfg["nn"]
    model = MLPRegressor(
        hidden_layer_sizes=tuple(nn["hidden_layer_sizes"]),
        activation=str(nn["activation"]),
        alpha=float(nn["alpha"]),
        max_iter=int(nn["max_iter"]),
        random_state=int(nn["random_state"]),
    )
    model.fit(X_train, y_train)

    yhat_train = model.predict(X_train)
    yhat_val = model.predict(X_val)
    yhat_test = model.predict(X_test)

    train_m = metrics(y_train, yhat_train)
    val_m = metrics(y_val, yhat_val)
    test_m = metrics(y_test, yhat_test)

    joblib.dump(model, "outputs/models/mlp_regressor.joblib")

    # log in SQLite
    con = connect(cfg["paths"]["db_path"])
    init_db(con)
    run_id = insert_run(con, n_samples=len(train_df)+len(val_df)+len(test_df), model_name="MLPRegressor", notes="Standardized z-score")
    insert_metrics(con, run_id, "train", *train_m)
    insert_metrics(con, run_id, "validation", *val_m)
    insert_metrics(con, run_id, "test", *test_m)
    con.close()

    # save metrics text
    with open("outputs/metrics/metrics.txt", "w", encoding="utf-8") as f:
        f.write(f"TRAIN: MAE={train_m[0]:.4f} RMSE={train_m[1]:.4f} R2={train_m[2]:.4f}\n")
        f.write(f"VAL:   MAE={val_m[0]:.4f} RMSE={val_m[1]:.4f} R2={val_m[2]:.4f}\n")
        f.write(f"TEST:  MAE={test_m[0]:.4f} RMSE={test_m[1]:.4f} R2={test_m[2]:.4f}\n")

    print("[OK] trained model + metrics saved.")

if __name__ == "__main__":
    main()
