import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connexion à la base
conn = sqlite3.connect("meteo_multi.db")

# Lecture des relevés
df_releves = pd.read_sql_query("SELECT * FROM relevés", conn)

# Lecture des prévisions
df_previsions = pd.read_sql_query("SELECT * FROM previsions", conn)

# Titre appli
st.title("Dashboard Météo")

# Affichage des relevés
st.subheader("Températures actuelles")
st.dataframe(df_releves)

# Sélection de ville pour affichage graphique
villes = df_previsions["ville"].unique()
ville_selection = st.selectbox("Choisissez une ville :", villes)

# Filtrer les prévisions pour la ville sélectionnée
df_ville = df_previsions[df_previsions["ville"] == ville_selection]

# Graphique
fig, ax = plt.subplots()
ax.plot(df_ville["date"], df_ville["temp_max"], label="Max")
ax.plot(df_ville["date"], df_ville["temp_min"], label="Min")
plt.xlabel("Date")
plt.ylabel("Température (°C)")
plt.title(f"Prévisions météo pour {ville_selection}")
plt.xticks(rotation=45)
plt.legend()
st.pyplot(fig)

# Fermeture
conn.close()
