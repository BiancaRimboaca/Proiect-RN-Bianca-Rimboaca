from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path
import csv
import joblib
import numpy as np

# Windows-only: pentru taste non-blocking (p / q)
import msvcrt

from src.utils.io import load_config  # doar config
from src.utils.thermal_model import step_temperature


# -----------------------------
# State machine states
# -----------------------------
IDLE = "IDLE"
RUN = "RUN"
PAUSE = "PAUSE"
SHUTDOWN = "SHUTDOWN"
STOP = "STOP"


@dataclass
class Context:
    T: float
    T_amb: float
    omega: float
    I: float
    k: int = 0
    state: str = IDLE


def _key_pressed() -> str | None:
    """Returnează o tastă apăsată (lowercase) sau None."""
    if msvcrt.kbhit():
        ch = msvcrt.getch()
        try:
            return ch.decode("utf-8").lower()
        except Exception:
            return None
    return None


def _random_walk(x: float, step: float, lo: float, hi: float, rng: np.random.Generator) -> float:
    return float(np.clip(x + rng.normal(0.0, step), lo, hi))


def main() -> None:
    cfg = load_config("config/config.yaml")

    # --- Config (cu fallback-uri)
    dt = float(cfg.get("simulation", {}).get("dt", cfg.get("dataset", {}).get("dt", 0.1)))
    T0 = float(cfg.get("simulation", {}).get("T0", 25.0))
    sleep_s = float(cfg.get("state_machine", {}).get("sleep_s", 0.1))
    shutdown_temp = float(cfg.get("state_machine", {}).get("shutdown_temp", 80.0))
    warn_temp = float(cfg.get("state_machine", {}).get("warning_temp", 70.0))

    # Thermal params: folosim thermal_model din config (în proiectul tău există thermal_model)
    tm = cfg.get("thermal_model", {})
    C = float(tm.get("C", 120.0))
    k_i2 = float(tm.get("k_i2", 0.02))
    k_w = float(tm.get("k_w", 0.0005))
    h0 = float(tm.get("h0", 0.015))
    h1 = float(tm.get("h1", 5e-5))

    # Signals
    sig = cfg.get("signals", {})
    t_amb_min = float(sig.get("t_amb_min", 15.0))
    t_amb_max = float(sig.get("t_amb_max", 35.0))
    omega_min = float(sig.get("omega_min", 0.0))
    omega_max = float(sig.get("omega_max", 3000.0))
    i_min = float(sig.get("i_min", 0.0))
    i_max = float(sig.get("i_max", 15.0))

    # Paths
    log_csv = cfg.get("state_machine", {}).get("log_csv", "outputs/logs/state_machine_log.csv")
    log_path = Path(log_csv)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    # Print path absolut (ca să știi sigur unde scrie)
    print("LOG PATH (absolute):", str(log_path.resolve()))

    # Load ML model + scalers (folosim cheile din scalers.joblib din proiectul tău: scaler_X, scaler_y)
    model = joblib.load("outputs/models/mlp_regressor.joblib")
    scalers = joblib.load("outputs/models/scalers.joblib")
    scaler_X = scalers["scaler_X"]
    scaler_y = scalers["scaler_y"]

    rng = np.random.default_rng(int(cfg.get("dataset", {}).get("seed", 42)))

    ctx = Context(
        T=T0,
        T_amb=float(rng.uniform(t_amb_min, t_amb_max)),
        omega=float(rng.uniform(omega_min, omega_max)),
        I=float(rng.uniform(i_min, i_max)),
        state=RUN,  # pornește direct
    )

    # Deschidem fișierul o singură dată (mai sigur + mai rapid)
    new_file = not log_path.exists()
    f = log_path.open("a", newline="", encoding="utf-8")
    writer = csv.writer(f)
    if new_file:
        writer.writerow(["timestamp", "k", "state", "T", "T_pred_next", "T_amb", "omega", "I", "event"])
        f.flush()

    print("\nControls: [p]=Pause/Resume  [q]=Quit\n")

    try:
        while ctx.state != STOP:
            key = _key_pressed()

            if key == "q":
                ctx.state = STOP
                break

            if key == "p":
                if ctx.state == RUN:
                    ctx.state = PAUSE
                elif ctx.state in (PAUSE, IDLE):
                    ctx.state = RUN

            if ctx.state == PAUSE:
                time.sleep(0.05)
                continue

            if ctx.state == RUN:
                # update semnale
                ctx.T_amb = _random_walk(ctx.T_amb, step=0.05, lo=t_amb_min, hi=t_amb_max, rng=rng)
                ctx.omega = _random_walk(ctx.omega, step=80.0, lo=omega_min, hi=omega_max, rng=rng)
                ctx.I = _random_walk(ctx.I, step=0.4, lo=i_min, hi=i_max, rng=rng)

                T_prev = ctx.T

                # temperatura "adevărată" (simulată)
                T_next_true = step_temperature(
                    T_prev=T_prev,
                    T_amb=ctx.T_amb,
                    I=ctx.I,
                    omega=ctx.omega,
                    dt=dt,
                    C=C,
                    k_i2=k_i2,
                    k_w=k_w,
                    h0=h0,
                    h1=h1,
                )

            
                X = np.array([[ctx.T_amb, ctx.omega, ctx.I, T_prev]], dtype=float)
                Xs = scaler_X.transform(X)
                y_pred_s = model.predict(Xs).reshape(-1, 1)
                T_pred_next = float(scaler_y.inverse_transform(y_pred_s)[0, 0])

                ctx.T = float(T_next_true)
                ctx.k += 1

                event = ""
                next_state = RUN
                if ctx.T >= shutdown_temp or T_pred_next >= shutdown_temp:
                    next_state = SHUTDOWN
                    event = "AUTO_SHUTDOWN"
                elif ctx.T >= warn_temp or T_pred_next >= warn_temp:
                    event = "WARNING"

                ts = time.time()
                writer.writerow([ts, ctx.k, ctx.state, f"{ctx.T:.4f}", f"{T_pred_next:.4f}",
                                 f"{ctx.T_amb:.4f}", f"{ctx.omega:.2f}", f"{ctx.I:.4f}", event])
                f.flush()

                print(f"T={ctx.T:6.2f}C | pred_next={T_pred_next:6.2f}C | omega={ctx.omega:6.0f} | I={ctx.I:5.2f} | {event}")

                ctx.state = next_state
                time.sleep(sleep_s)

            if ctx.state == SHUTDOWN:
                ts = time.time()
                writer.writerow([ts, ctx.k, "SHUTDOWN", f"{ctx.T:.4f}", "", f"{ctx.T_amb:.4f}",
                                 f"{ctx.omega:.2f}", f"{ctx.I:.4f}", "SHUTDOWN_DONE"])
                f.flush()
                print(f"\n[SHUTDOWN] Triggered at T={ctx.T:.2f}C (threshold={shutdown_temp}C). Motor stopped.\n")
                ctx.state = STOP

    except KeyboardInterrupt:
        print("\n[STOP] Ctrl+C pressed. Exiting...")

    finally:
        f.close()

    print(f"[OK] log saved: {log_path.resolve()}")


if __name__ == "__main__":
    main()

