# 📘 README – Etapa 3: Analiza și Pregătirea Setului de Date pentru Rețele Neuronale

**Disciplina:** Rețele Neuronale  
**Instituție:** POLITEHNICA București – FIIR  
**Student:** Rîmboacă Valentina-Bianca 
**Data:** [Data]  

---

## Introducere

În această etapă a fost realizată analiza și pregătirea setului de date pentru proiectul:Predicția temperaturii unui motor BLDC utilizat într-un braț robotic

Scopul este antrenarea unei rețele neuronale care prezice temperatura motorului la pasul următor (T_next) pe baza parametrilor fizici ai sistemului.

Datele au fost generate prin simulare folosind un model termic fizic al motorului.

---

##  1. Structura Repository-ului Github (versiunea Etapei 3)

```
project-name/
├── README.md
├── docs/
│   └── datasets/          # descriere seturi de date, surse, diagrame
├── data/
│   ├── raw/               # date brute
│   ├── processed/         # date curățate și transformate
│   ├── train/             # set de instruire
│   ├── validation/        # set de validare
│   └── test/              # set de testare
├── src/
│   ├── preprocessing/     # funcții pentru preprocesare
│   ├── data_acquisition/  # generare / achiziție date (dacă există)
│   └── neural_network/    # implementarea RN (în etapa următoare)
├── config/                # fișiere de configurare
└── requirements.txt       # dependențe Python (dacă aplicabil)
```

---

##  2. Descrierea Setului de Date

### 2.1 Sursa datelor

* **Origine:** Simulare
* **Modul de achiziție:** ☐ Senzori reali / x Simulare / ☐ Fișier extern / x Generare programatică
* **Perioada / condițiile colectării:** Noiembrie 2025 - Februarie 2026, condiții experimentale specifice

### 2.2 Caracteristicile dataset-ului

* **Număr total de observații:** 15,000
* **Număr de caracteristici (features):** 5
* **Tipuri de date:** x Numerice / ☐ Categoriale / ☐ Temporale / ☐ Imagini
* **Format fișiere:** x CSV / ☐ TXT / ☐ JSON / ☐ PNG / ☐ Altele: [...]

### 2.3 Descrierea fiecărei caracteristici

| **Caracteristică** | **Tip** | **Unitate** | **Descriere** | **Domeniu valori** |
|-------------------|---------|-------------|---------------|--------------------|
| T_amb | numeric | °C | Temperatura ambientala | 15-35 |
| omega | numeric | RPM | Turatia motorului | 0-3000 |
| I | numeric | A | Curentul de faza | 0–15 |
| T_prev | numeric | °C | Temperatura curenta | ~25 – 80 |
| T_next | numeric | °C | Tempeatura la pasul urmator | ~25 – 80 |

**Fișier recomandat:**  `data/README.md`

---

##  3. Analiza Exploratorie a Datelor (EDA) – Sintetic

### 3.1 Statistici descriptive aplicate

* **Medie, mediană, deviație standard**
* **Min–max și quartile**
* **Distribuții pe caracteristici** (histograme)
* **Identificarea outlierilor** (IQR / percentile)

### 3.2 Analiza calității datelor

* **Detectarea valorilor lipsă** (% pe coloană)
* **Detectarea valorilor inconsistente sau eronate**
* **Identificarea caracteristicilor redundante sau puternic corelate**

### 3.3 Probleme identificate

* [exemplu] Feature X are 8% valori lipsă
* [exemplu] Distribuția feature Y este puternic neuniformă
* [exemplu] Variabilitate ridicată în clase (class imbalance)

---

##  4. Preprocesarea Datelor

### 4.1 Curățarea datelor

* **Eliminare duplicatelor**
* **Tratarea valorilor lipsă:**
  * Feature A: imputare cu mediană
  * Feature B: eliminare (30% valori lipsă)
* **Tratarea outlierilor:** IQR / limitare percentile

### 4.2 Transformarea caracteristicilor

* **Normalizare:** Min–Max / Standardizare
* **Encoding pentru variabile categoriale**
* **Ajustarea dezechilibrului de clasă** (dacă este cazul)

### 4.3 Structurarea seturilor de date

**Împărțire recomandată:**
* 70–80% – train
* 10–15% – validation
* 10–15% – test

**Principii respectate:**
* Stratificare pentru clasificare
* Fără scurgere de informație (data leakage)
* Statistici calculate DOAR pe train și aplicate pe celelalte seturi

### 4.4 Salvarea rezultatelor preprocesării

* Date preprocesate în `data/processed/`
* Seturi train/val/test în foldere dedicate
* Parametrii de preprocesare în `config/preprocessing_config.*` (opțional)

---

##  5. Fișiere Generate în Această Etapă

* `data/raw/` – date brute
* `data/processed/` – date curățate & transformate
* `data/train/`, `data/validation/`, `data/test/` – seturi finale
* `src/preprocessing/` – codul de preprocesare
* `data/README.md` – descrierea dataset-ului

---

##  6. Stare Etapă (de completat de student)

- [ ] Structură repository configurată
- [ ] Dataset analizat (EDA realizată)
- [ ] Date preprocesate
- [ ] Seturi train/val/test generate
- [ ] Documentație actualizată în README + `data/README.md`

---
