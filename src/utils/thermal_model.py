from __future__ import annotations
import numpy as np

def step_temperature(
    T_prev: float,
    T_amb: float,
    I: float,
    omega: float,
    dt: float,
    C: float,
    k_i2: float,
    k_w: float,
    h0: float,
    h1: float,
) -> float:
    P_loss = k_i2 * (I ** 2) + k_w * omega
    h = h0 + h1 * omega
    cooling = h * (T_prev - T_amb)
    dTdt = (P_loss - cooling) / C
    T_next = T_prev + dt * dTdt
    return float(T_next)

def generate_signals(
    n: int,
    rng: np.random.Generator,
    t_amb_min: float, t_amb_max: float,
    omega_min: float, omega_max: float,
    i_min: float, i_max: float
):
    T_amb = np.empty(n, dtype=float)
    omega = np.empty(n, dtype=float)
    I = np.empty(n, dtype=float)

    T_amb[0] = rng.uniform(t_amb_min, t_amb_max)
    omega[0] = rng.uniform(omega_min, omega_max)
    I[0] = rng.uniform(i_min, i_max)

    for k in range(1, n):
        T_amb[k] = np.clip(T_amb[k-1] + rng.normal(0, 0.05), t_amb_min, t_amb_max)
        omega[k] = np.clip(omega[k-1] + rng.normal(0, 80), omega_min, omega_max)
        I[k] = np.clip(I[k-1] + rng.normal(0, 0.4), i_min, i_max)

    return T_amb, omega, I
