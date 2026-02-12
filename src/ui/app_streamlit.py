# src/ui/app_streamlit.py
from __future__ import annotations

import sys
import time
from pathlib import Path
from datetime import datetime

import joblib
import numpy as np
import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from src.utils.thermal_model import step_temperature  


st.set_page_config(
    page_title="BLDC Thermal Monitor",
    layout="wide",

)


@st.cache_resource
def load_assets():
    model_path = ROOT / "outputs" / "models" / "mlp_regressor.joblib"
    scaler_path = ROOT / "outputs" / "models" / "scalers.joblib"

    if not model_path.exists():
        raise FileNotFoundError(f"Nu găsesc modelul: {model_path}")
    if not scaler_path.exists():
        raise FileNotFoundError(f"Nu găsesc scalerele: {scaler_path}")

    model = joblib.load(model_path)
    scalers = joblib.load(scaler_path)
    return model, scalers


try:
    model, scalers = load_assets()

  
    scaler_X = scalers["scaler_X"]
    scaler_y = scalers["scaler_y"]
    FEATURES = scalers["features"]  
except Exception as e:
    st.error(f"Eroare la încărcarea modelului/scalerelor: {e}")
    st.stop()


if "history" not in st.session_state:
    st.session_state.history = pd.DataFrame(
        columns=["Timestamp", "T_real", "T_pred", "Error", "State", "I", "Omega", "T_amb"]
    )

if "current_temp" not in st.session_state:
    st.session_state.current_temp = 25.0

if "is_running" not in st.session_state:
    st.session_state.is_running = False

if "last_status" not in st.session_state:
    st.session_state.last_status = "IDLE"



st.sidebar.header("🕹️ Control")

col_btn1, col_btn2 = st.sidebar.columns(2)
with col_btn1:
    start_btn = st.button("▶️ Start", use_container_width=True, type="primary")
with col_btn2:
    stop_btn = st.button("🛑 Stop", use_container_width=True)

if start_btn:
    st.session_state.is_running = True
if stop_btn:
    st.session_state.is_running = False
    st.session_state.last_status = "STOP"

st.sidebar.divider()
st.sidebar.subheader("Setări simulare")

sim_speed = st.sidebar.slider("Viteză refresh (sec)", 0.05, 1.0, 0.2, 0.05)

T_amb = st.sidebar.number_input("Temperatură ambient (°C)", 10.0, 50.0, 25.0, 0.5)

st.sidebar.subheader("Sarcină / semnale")

I_input = st.sidebar.slider("Curent fază I (A)", 0.0, 20.0, 5.0, 0.1)
omega_input = st.sidebar.slider("Turație ω (RPM)", 0, 4000, 1500, 10)

st.sidebar.divider()
st.sidebar.subheader("Praguri protecție")
warning_thr = st.sidebar.number_input("Warning ≥ (°C)", 0.0, 200.0, 70.0, 1.0)
shutdown_thr = st.sidebar.number_input("Shutdown ≥ (°C)", 0.0, 200.0, 80.0, 1.0)

st.sidebar.divider()
st.sidebar.subheader("Parametri model termic (simulare)")

C = st.sidebar.number_input("C (capacitate termică)", 1.0, 1000.0, 120.0, 1.0)
k_i2 = st.sidebar.number_input("k_i2 (pierderi I²)", 0.0, 10.0, 0.02, 0.001, format="%.4f")
k_w = st.sidebar.number_input("k_w (pierderi ω)", 0.0, 1.0, 0.0005, 0.0001, format="%.6f")
h0 = st.sidebar.number_input("h0 (convecție baza)", 0.0, 10.0, 0.015, 0.001, format="%.4f")
h1 = st.sidebar.number_input("h1 (convecție ~ω)", 0.0, 1.0, 0.00005, 0.00001, format="%.6f")

dt = 0.1  # pas fix pentru demo (poți expune și în UI dacă vrei)


# -----------------------------
# HEADER
# -----------------------------
st.title("🔥 BLDC Temperature Prediction & Monitoring")
st.caption(
    "Scop: simulare temperatură + predicție RN (pas următor) + logică de protecție (warning/shutdown)."
)

status_badge = "🟢 RUN" if st.session_state.is_running else "⚪ STOP/PAUSE"
st.write(f"**Status:** {status_badge}")

# -----------------------------
# MAIN METRICS ROW
# -----------------------------
m1, m2, m3, m4 = st.columns(4)

# -----------------------------
# SIMULATION + INFERENCE STEP
# -----------------------------
if st.session_state.is_running:
    # 1) THERMAL STEP (ground truth / simulated)
    T_prev = float(st.session_state.current_temp)

    thermal_params = dict(C=float(C), k_i2=float(k_i2), k_w=float(k_w), h0=float(h0), h1=float(h1))
    T_next_real = step_temperature(
        T_prev=T_prev,
        T_amb=float(T_amb),
        I=float(I_input),
        omega=float(omega_input),
        dt=float(dt),
        **thermal_params,
    )

    
    x_dict = {
        "T_amb": float(T_amb),
        "omega": float(omega_input),
    
        "I": float(I_input),
        
        "T_prev": float(T_prev),
    }
    try:
        X_raw = np.array([[x_dict[f] for f in FEATURES]], dtype=float)
    except KeyError as e:
        st.error(
            f"FEATURES din scalers.joblib conține un feature necunoscut: {e}. "
            f"FEATURES={FEATURES} | chei disponibile={list(x_dict.keys())}"
        )
        st.stop()

    X_scaled = scaler_X.transform(X_raw)
    y_pred_scaled = model.predict(X_scaled).reshape(-1, 1)
    T_next_pred = float(scaler_y.inverse_transform(y_pred_scaled)[0, 0])

    # 3) DECISION / PROTECTION LOGIC
    status = "NORMAL"
    if T_next_pred >= shutdown_thr or T_next_real >= shutdown_thr:
        status = "SHUTDOWN"
    elif T_next_pred >= warning_thr or T_next_real >= warning_thr:
        status = "WARNING"

    st.session_state.last_status = status

    # Optional: auto-stop if shutdown
    if status == "SHUTDOWN":
        st.session_state.is_running = False

    # 4) SAVE TO HISTORY (last N rows)
    err = abs(T_next_real - T_next_pred)
    new_row = {
        "Timestamp": datetime.now().strftime("%H:%M:%S"),
        "T_real": T_next_real,
        "T_pred": T_next_pred,
        "Error": err,
        "State": status,
        "I": float(I_input),
        "Omega": float(omega_input),
        "T_amb": float(T_amb),
    }
    st.session_state.history = pd.concat(
        [st.session_state.history, pd.DataFrame([new_row])],
        ignore_index=True,
    )

    # update current temp
    st.session_state.current_temp = float(T_next_real)

    # keep last 200 points for smooth plots
    st.session_state.history = st.session_state.history.tail(200)

# -----------------------------
# DISPLAY METRICS (from history)
# -----------------------------
hist = st.session_state.history
if not hist.empty:
    last = hist.iloc[-1]
    m1.metric("T_real (°C)", f"{last['T_real']:.2f}")
    m2.metric("T_pred_next (°C)", f"{last['T_pred']:.2f}", delta=f"{(last['T_pred']-last['T_real']):.3f}")
    m3.metric("Stare", str(last["State"]))
    m4.metric("Eroare |T_real - T_pred|", f"{last['Error']:.4f}")

# -----------------------------
# STATUS MESSAGE
# -----------------------------
if st.session_state.last_status == "NORMAL":
    st.success("✅ SAFE: Temperatura în limite normale.")
elif st.session_state.last_status == "WARNING":
    st.warning(f"⚠️ WARNING: Temperatura a depășit {warning_thr:.1f}°C (real sau prezis).")
elif st.session_state.last_status == "SHUTDOWN":
    st.error(f"🚨 SHUTDOWN: Temperatura a depășit {shutdown_thr:.1f}°C. Motor oprit (simulat).")
elif st.session_state.last_status == "STOP":
    st.info("⏹️ Oprit manual.")

# -----------------------------
# TABS: MONITORING + EVALUATION
# -----------------------------
tab1, tab2 = st.tabs(["📊 Live Monitoring", "🎯 Analiză / Logs"])

with tab1:
    if hist.empty:
        st.info("Apasă **Start** ca să înceapă simularea.")
    else:
        st.subheader("Evoluție temperatură (Real vs Predicție)")
        chart_df = hist[["Timestamp", "T_real", "T_pred"]].copy()
        chart_df = chart_df.set_index("Timestamp")
        st.line_chart(chart_df)

        c1, c2, c3 = st.columns(3)
        with c1:
            st.subheader("Curent I (A)")
            st.area_chart(hist.set_index("Timestamp")[["I"]])
        with c2:
            st.subheader("Turație ω (RPM)")
            st.area_chart(hist.set_index("Timestamp")[["Omega"]])
        with c3:
            st.subheader("Temperatură ambient (°C)")
            st.area_chart(hist.set_index("Timestamp")[["T_amb"]])

with tab2:
    if hist.empty:
        st.info("Nu există date încă.")
    else:
        st.subheader("Reziduuri / eroare")
        st.bar_chart(hist.set_index("Timestamp")[["Error"]])

        st.write("### Statistici sesiune (utile pentru Etapa 6)")
        col_s1, col_s2, col_s3 = st.columns(3)
        col_s1.write(f"**Eroare max:** {hist['Error'].max():.4f} °C")
        col_s2.write(f"**Eroare medie:** {hist['Error'].mean():.4f} °C")
        col_s3.write(f"**Eroare mediană:** {hist['Error'].median():.4f} °C")

        st.write("### Log (ultimele 20 rânduri)")
        st.dataframe(hist.tail(20), use_container_width=True)

        # Export CSV (manual)
        st.write("### Export")
        csv_bytes = hist.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Descarcă log-ul ca CSV",
            data=csv_bytes,
            file_name="bldc_streamlit_log.csv",
            mime="text/csv",
        )

# -----------------------------
# AUTO-REFRESH LOOP
# -----------------------------
if st.session_state.is_running:
    time.sleep(float(sim_speed))
    st.rerun()

