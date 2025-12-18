# 📘 README – Etapa 3: Analiza și Pregătirea Setului de Date pentru Rețele Neuronale

**Disciplina:** Rețele Neuronale  
**Instituție:** POLITEHNICA București – FIIR  
**Student:** Rimboaca Valentina-Bianca
**Data:** [Data]  

---

## Introducere

Acest proiect urmărește dezvoltarea unui sistem bazat pe rețele neuronale capabil să prezică temperatura unui motor electric pe baza unor parametri de funcționare esențiali:

turație

curent

tensiune

Un astfel de sistem este util în aplicații industriale unde monitorizarea termică este critică pentru prevenirea supraîncălzirii, reducerea uzurii componentelor și optimizarea performanței motorului. Predicția precisă a temperaturii permite implementarea unor strategii eficiente de mentenanță și control.

Etapa 3 se concentrează pe analiza și pregătirea setului de date, astfel încât modelul neuronal să poată fi instruit ulterior în condiții optime.

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

* **Origine:** [Descriere sursă date - ex: senzori robot, dataset public, simulare] Date generate prin simulare
* **Modul de achiziție:** ☐ Senzori reali / x Simulare / ☐ Fișier extern / ☐ Generare programatică
* **Perioada / condițiile colectării:** [Ex: Noiembrie 2024 - Ianuarie 2025, condiții experimentale specifice] Decembrie 2024-Ianuarie 2025, 

### 2.2 Caracteristicile dataset-ului

* **Număr total de observații:** [Ex: 15,000] 1000
* **Număr de caracteristici (features):** [Ex: 12] 4
* **Tipuri de date:** x Numerice / ☐ Categoriale / x Temporale / ☐ Imagini
* **Format fișiere:** x CSV / ☐ TXT / ☐ JSON / ☐ PNG / ☐ Altele: [...]

### 2.3 Descrierea fiecărei caracteristici

| **Caracteristică** | **Tip** | **Unitate** | **Descriere** | **Domeniu valori** |
|-------------------|---------|-------------|---------------|--------------------|
| Turatie | numeric | rpm | Viteza de rotatie a motorului | 500-3000 |
| Curent | numeric | A | Curent absorbit de motor | 10-80 |
| Tensiun | numeric | V | Tensiunea de alimentare | 220-400 |
| Temperatura | numeri | °C | Temperatura interna a motorului | 30-120 |
| Temperatura ambientala | numeric | °C | Temperatura mediului ambiant| 0-40 |
| Timestamp | Temporal | s | Momentul inregistrarii observatiei | 0-999 |

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

* Distributia temperaturii este usor neuniforma in zonele de sarcina mare
* Modelul termic utilizat este simplificat si nu include toate fenomenele fizice reale (inertie termica, pierderi prin carcasa).
* Variatii introduse intentionat prin zgomot gaussian pentru simularea erorilor de masurare

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
