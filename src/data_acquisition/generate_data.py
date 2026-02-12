from __future__ import annotations
import numpy as np
import pandas as pd
from src.utils.io import ensure_dirs, load_config, atomic_write_text
from src.utils.thermal_model import step_temperature, generate_signals

def main() -> None:
    ensure_dirs()
    cfg = load_config()

    n = int(cfg["dataset"]["n_samples"])
    dt = float(cfg["dataset"]["dt"])
    seed = int(cfg["dataset"]["seed"])
    rng = np.random.default_rng(seed)

    s = cfg["signals"]
    T_amb, omega, I = generate_signals(
        n=n,
        rng=rng,
        t_amb_min=float(s["t_amb_min"]),
        t_amb_max=float(s["t_amb_max"]),
        omega_min=float(s["omega_min"]),
        omega_max=float(s["omega_max"]),
        i_min=float(s["i_min"]),
        i_max=float(s["i_max"]),
    )

    tm = cfg["thermal_model"]
    C = float(tm["C"]); k_i2 = float(tm["k_i2"]); k_w = float(tm["k_w"])
    h0 = float(tm["h0"]); h1 = float(tm["h1"])

    # inițial temperatura motorului
    T = np.empty(n, dtype=float)
    T[0] = float(T_amb[0] + 2.0)  # pornește puțin peste ambient

    for k in range(1, n):
        T[k] = step_temperature(
            T_prev=float(T[k-1]),
            T_amb=float(T_amb[k]),
            I=float(I[k]),
            omega=float(omega[k]),
            dt=dt, C=C, k_i2=k_i2, k_w=k_w, h0=h0, h1=h1,
        )

    # Construim dataset de tip supervised: X=[T_amb, omega, I, T_prev], y=T_next
    noise_std = float(s["noise_std_temp"])
    T_noisy = T + rng.normal(0, noise_std, size=n)

    df = pd.DataFrame({
        "T_amb": T_amb[:-1],
        "omega": omega[:-1],
        "I": I[:-1],
        "T_prev": T_noisy[:-1],
        "T_next": T_noisy[1:],
    })

    raw_path = cfg["paths"]["data_raw"]
    df.to_csv(raw_path, index=False)

    # data/README.md
    text = f"""# Dataset BLDC Temperature (RAW)

**Task:** predictie temperatura urmatoare a motorului BLDC.

## Coloane
- T_amb [°C] - temperatura ambientala
- omega [rpm] - turatie
- I [A] - curent (simulat)
- T_prev [°C] - temperatura curenta (cu zgomot)
- T_next [°C] - temperatura urmatoare (cu zgomot)

## Cum au fost generate
Simulare model termic 1st order:
dT/dt = (P_loss - h(omega)*(T - T_amb)) / C
P_loss = k_i2 * I^2 + k_w * omega
h(omega)=h0+h1*omega

N={len(df)} exemple, dt={dt}s, seed={seed}.
"""
    atomic_write_text("data/README.md", text)

    # docs/datasets/dataset_description.md
    atomic_write_text("docs/datasets/dataset_description.md", text)

    print(f"[OK] wrote raw dataset: {raw_path} rows={len(df)}")

if __name__ == "__main__":
    main()
