# Dataset BLDC Temperature (RAW)

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

N=4999 exemple, dt=0.1s, seed=42.
