import requests
import sqlite3
import datetime
import matplotlib.pyplot as plt
import csv
from fpdf import FPDF

# Liste des villes à interroger
villes = [
    {"nom": "Biarritz", "lat": 43.48, "lon": -1.56},
    {"nom": "Paris", "lat": 48.85, "lon": 2.35},
    {"nom": "Marseille", "lat": 43.30, "lon": 5.37}
]

# Connexion à la base SQLite
conn = sqlite3.connect("meteo_multi.db")
cursor = conn.cursor()

# Création de la table relevés (météo instantanée)
cursor.execute("""
CREATE TABLE IF NOT EXISTS relevés (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_heure TEXT,
    temperature REAL,
    vent REAL,
    ville TEXT
)
""")

# Création de la table previsions (prévisions sur plusieurs jours) avec contrainte UNIQUE
cursor.execute("""
CREATE TABLE IF NOT EXISTS previsions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    ville TEXT,
    temp_max REAL,
    temp_min REAL,
    UNIQUE(date, ville)
)
""")

# Boucle sur chaque ville pour météo actuelle et prévisions
for ville in villes:
    url = f"https://api.open-meteo.com/v1/forecast?latitude={ville['lat']}&longitude={ville['lon']}&current_weather=true"
    response = requests.get(url)
    data = response.json()

    temperature = data["current_weather"]["temperature"]
    vent = data["current_weather"]["windspeed"]
    temps = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    cursor.execute("INSERT INTO relevés (date_heure, temperature, vent, ville) VALUES (?, ?, ?, ?)",
                   (temps, temperature, vent, ville["nom"]))

    print(f"{ville['nom']} : {temperature}°C / {vent} km/h")

    # Récupération des prévisions pour chaque ville
    url_previsions = f"https://api.open-meteo.com/v1/forecast?latitude={ville['lat']}&longitude={ville['lon']}&daily=temperature_2m_max,temperature_2m_min&timezone=Europe%2FParis"
    response_previsions = requests.get(url_previsions)
    data_previsions = response_previsions.json()

    dates = data_previsions["daily"]["time"]
    temps_max = data_previsions["daily"]["temperature_2m_max"]
    temps_min = data_previsions["daily"]["temperature_2m_min"]

    for i in range(len(dates)):
        cursor.execute("""
            INSERT OR IGNORE INTO previsions (date, ville, temp_max, temp_min)
            VALUES (?, ?, ?, ?)
        """, (dates[i], ville["nom"], temps_max[i], temps_min[i]))

# Commit après toutes les insertions
conn.commit()

# 📊 Graphique température actuelle par ville
cursor.execute("SELECT ville, temperature FROM relevés ORDER BY date_heure DESC LIMIT 3")
data = cursor.fetchall()

villes_graph = [d[0] for d in data]
temperatures_graph = [d[1] for d in data]

plt.bar(villes_graph, temperatures_graph, color='skyblue')
plt.xlabel("Ville")
plt.ylabel("Température (°C)")
plt.title("Température actuelle par ville")
plt.show()

# 📊 Graphiques prévisions pour chaque ville
for ville in villes:
    cursor.execute("SELECT date, temp_max, temp_min FROM previsions WHERE ville = ? ORDER BY date", (ville["nom"],))
    data_ville = cursor.fetchall()

    dates = [d[0] for d in data_ville]
    maxs = [d[1] for d in data_ville]
    mins = [d[2] for d in data_ville]

    plt.figure()
    plt.plot(dates, maxs, label="Max", color='red')
    plt.plot(dates, mins, label="Min", color='blue')
    plt.xlabel("Date")
    plt.ylabel("Température (°C)")
    plt.title(f"Prévisions pour {ville['nom']}")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# 📄 Export CSV des prévisions
with open("previsions.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Date", "Ville", "Température Max", "Température Min"])

    cursor.execute("SELECT date, ville, temp_max, temp_min FROM previsions ORDER BY date, ville")
    lignes = cursor.fetchall()

    for ligne in lignes:
        writer.writerow(ligne)

print("✅ Export CSV terminé.")

# 📄 Génération du PDF propre
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="Rapport météo - Prévisions sur plusieurs jours", ln=True, align="C")
pdf.ln(10)

cursor.execute("SELECT date, ville, temp_max, temp_min FROM previsions ORDER BY date, ville")
lignes = cursor.fetchall()

for ligne in lignes:
    texte = f"{ligne[0]} - {ligne[1]} : Max {ligne[2]}°C / Min {ligne[3]}°C"
    pdf.cell(200, 8, txt=texte, ln=True)

pdf.output("rapport_previsions.pdf")

print("✅ Rapport PDF généré.")

# Maintenir la fenêtre ouverte
input("Appuyez sur Entrée pour quitter...")

# Fermeture finale
conn.close()