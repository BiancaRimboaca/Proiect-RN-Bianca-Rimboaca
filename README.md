# 📘 README – Etapa 3: Analiza și Pregătirea Setului de Date pentru Rețele Neuronale

**Disciplina:** Rețele Neuronale  
**Instituție:** POLITEHNICA București – FIIR  
**Student:** Rîmboacă Valentina-Bianca  
**Data:** 25-11-2025  

---

## Introducere

Acest proiect urmărește dezvoltarea unui sistem bazat pe rețele neuronale capabil să prezică temperatura unui motor electric pe baza unor parametri de funcționare esențiali:

turație

curent

tensiune

Un astfel de sistem este util în aplicații industriale unde monitorizarea termică este critică pentru prevenirea supraîncălzirii, reducerea uzurii componentelor și optimizarea performanței motorului. Predicția precisă a temperaturii permite implementarea unor strategii eficiente de mentenanță și control.

Etapa 3 se concentrează pe analiza și pregătirea setului de date, astfel încât modelul neuronal să poată fi instruit ulterior în condiții optime.


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

* **Origine:** Date sintetice generate programatic pentru simularea comportamentului termic al unui motor electric.
* **Modul de achiziție:** ☐ Generare programatică
* **Perioada / condițiile colectării:** Datele simulează funcționarea unui motor electric într-un interval de timp continuu (ex. o zi de funcționare), acoperind variații ale turației, curentului și tensiunii în regimuri diferite de operare.

### 2.2 Caracteristicile dataset-ului
a
* **Număr total de observații:** 60
* **Număr de caracteristici (features):** 4 variabile de intrare + o variabilă țintă
    -Intrări: turație(rpm), curent(A), tensiune (V), timestamp
    -Ieșire: temperatura motorului (grade C)
* **Tipuri de date:** x Numerice / x Temporale
* **Format fișiere:** x CSV / ☐ TXT / ☐ JSON / ☐ PNG / ☐ Altele: [...]

### 2.3 Descrierea fiecărei caracteristici

| **Caracteristică** | **Tip** | **Unitate** | **Descriere** | **Domeniu valori** |
|-------------------|---------|-------------|---------------|--------------------|
| Curent | numeric | A | Curentul electric absorbit de motor. Indicator direct de sarcină | 0–150 |
| Turație | numeric | rpm | Turația motorului. Corelată cu frecarea și ventilația | {A, B, C} |
| Tensiune | numeric | V | [...] | 0–2.5 |
| ... | ... | ... | ... | ... |

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
