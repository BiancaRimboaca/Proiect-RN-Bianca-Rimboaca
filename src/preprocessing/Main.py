import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

#Generarea setului de date
np.random.seed(42)
N_samples = 1000

#Generează date de intrare
Turație = np.random.uniform(500, 3000, N_samples)
Curent = np.random.uniform(10, 80, N_samples)
Tensiune = np.random.uniform(220, 400, N_samples)

#Formula simpla pentru a simula dependenya temperaturii
Baza_Termică = 40
Zgomot = np.random.normal(0, 3, N_samples) 
Temperatura_Estimată = Baza_Termică + (Curent * Tensiune / 200) + (Turație / 1000) + Zgomot
Temperatura_Estimată = np.clip(Temperatura_Estimată, 40, 120) 

data = pd.DataFrame({
    'Turație': Turație,
    'Curent': Curent,
    'Tensiune': Tensiune,
    'Temperatura': Temperatura_Estimată
})

X = data[['Turație', 'Curent', 'Tensiune']]
y = data['Temperatura']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("Date preprocesate. Gata de antrenare.")

model = MLPRegressor(
    hidden_layer_sizes=(64, 32),
    activation='relu',      
    solver='adam',          
    max_iter=500,           
    random_state=42,
    verbose=True           
)

print("\nÎncepe Antrenarea Modelului MLPRegressor...")

#Antrenarea modelului

model.fit(X_train_scaled, y_train) 

print("\nAntrenarea s-a finalizat.")


y_pred = model.predict(X_test_scaled)


mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Eroarea Medie Pătratică (MSE) pe setul de test: {mse:.2f}")
print(f"Acuratețea R2 a modelului: {r2:.4f}")

#Exemplu de Predicție in timp real

valori_noi = pd.DataFrame({
    'Turație': [1500],  
    'Curent': [55],     
    'Tensiune': [380]   
})

valori_noi_scaled = scaler.transform(valori_noi)
temperatura_prezisă = model.predict(valori_noi_scaled)[0]

print(f"\nPredicție în timp real")
print(f"Temperatura estimată este: {temperatura_prezisă:.2f} °C") 

#Grafic comparativ

plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, alpha=0.6)
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--', lw=2)
plt.title('Compararea Temperaturii Reale vs. Temperaturii Predise')
plt.xlabel('Temperatura Reală (°C)')
plt.ylabel('Temperatura Predisă (°C)')
plt.grid(True)
plt.show()
