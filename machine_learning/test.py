import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

print("Starte...")

# 1. CSV-Datei sicher finden
base = os.path.dirname(__file__)
file_path = os.path.join(base, "winequality-red.csv")

# 2. Daten laden
df = pd.read_csv(file_path, sep=";")
print(df.head())

# 3. Features und Ziel trennen
X = df.drop("quality", axis=1)
y = df["quality"]

# 4. Trainings- und Testdaten erzeugen
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 5. Skalieren (wichtig für viele Modelle)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 6. Modell trainieren
model = RandomForestClassifier(
    n_estimators=300,
    class_weight="balanced",
    random_state=42
)

model.fit(X_train, y_train)

# 7. Vorhersagen
pred = model.predict(X_test)

# 8. Bewertung
print("Genauigkeit:", accuracy_score(y_test, pred))
print(classification_report(y_test, pred))
