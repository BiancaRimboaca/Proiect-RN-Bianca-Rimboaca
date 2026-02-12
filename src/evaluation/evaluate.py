from __future__ import annotations
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
import json
from pathlib import Path
from sklearn.metrics import mean_absolute_error, r2_score
from src.utils.io import ensure_dirs

def main() -> None:
    ensure_dirs()
    
    # 1. Încărcare model și scalere
    # Este crucial să încărcăm scalerele pentru a vedea eroarea în °C 
    model = joblib.load("outputs/models/mlp_regressor.joblib")
    scalers = joblib.load("outputs/models/scalers.joblib")
    scaler_y = scalers["scaler_y"]

    # 2. Pregătire date
    test_df = pd.read_csv("data/test/test.csv")
    X_cols = [c for c in test_df.columns if c.endswith("_z") and c != "T_next_z"]
    X_test = test_df[X_cols].values
    y_test_z = test_df["T_next_z"].values.reshape(-1, 1)

    # 3. Predicție (format z-score)
    y_pred_z = model.predict(X_test).reshape(-1, 1)

    # 4. Denormalizare pentru metrici industriale (°C) 
    y_test_real = scaler_y.inverse_transform(y_test_z).flatten()
    y_pred_real = scaler_y.inverse_transform(y_pred_z).flatten()

    # 5. Calcul metrici 
    mae = mean_absolute_error(y_test_real, y_pred_real)
    r2 = r2_score(y_test_real, y_pred_real)

    # 6. Salvare metrici în JSON (Cerință Etapa 5/6) 
    metrics = {
        "test_accuracy_r2": float(r2),
        "mean_absolute_error_celsius": float(mae),
        "samples_count": len(test_df)
    }
    
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    with open(results_dir / "test_metrics.json", "w") as f:
        json.dump(metrics, f, indent=4)

    # 7. Generare vizualizări (Codul tău original)
    plt.figure()
    plt.plot(y_test_real[:300], label="True")
    plt.plot(y_pred_real[:300], label="Pred")
    plt.title(f"Test: Real vs Pred (°C) - MAE: {mae:.4f}")
    plt.xlabel("Sample")
    plt.ylabel("Temperatura (°C)")
    plt.legend()
    plt.tight_layout()
    plt.savefig("outputs/figures/test_true_vs_pred.png", dpi=150)

    plt.figure()
    plt.scatter(y_test_real, y_pred_real, s=8, alpha=0.5)
    plt.plot([y_test_real.min(), y_test_real.max()], [y_test_real.min(), y_test_real.max()], 'r--')
    plt.title("Scatter: True vs Pred (°C)")
    plt.xlabel("True (°C)")
    plt.ylabel("Pred (°C)")
    plt.tight_layout()
    plt.savefig("outputs/figures/test_scatter.png", dpi=150)

    print(f"[OK] Metrics saved to results/test_metrics.json")
    print(f"[OK] MAE: {mae:.4f} °C, R2: {r2:.4f}")
    print("[OK] Evaluation figures saved.")

if __name__ == "__main__":
    main()