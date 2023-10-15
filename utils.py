# Importation des bibliothèques nécessaires
import streamlit as st
import pandas as pd
import os


def clean_characteristics(df):
    df["hour"] = df["hrmn"].str.split(":").str[0].astype(int)
    df["minute"] = df["hrmn"].str.split(":").str[1].astype(int)
    df.drop(columns=["hrmn"], inplace=True)

    df["dep"] = pd.to_numeric(df["dep"], errors="coerce").fillna(0).astype(int)

    def convert_latitude(latitude):
        try:
            # Convertir la valeur en chaîne de caractères, puis supprimer les virgules et les espaces, puis convertir en float
            latitude_str = str(latitude).replace(",", ".").replace(" ", "")
            return float(latitude_str)
        except ValueError:
            # Si la conversion échoue, renvoyer une valeur par défaut (par exemple, -1)
            return -1  # Vous pouvez choisir une valeur appropriée ici
        # Appliquer la fonction de conversion à la colonne 'latitude'

    df["lat"] = df["lat"].apply(convert_latitude)
    df["long"] = df["long"].apply(convert_latitude)

    # Maintenant, la colonne 'latitude' contient des valeurs float

    return df


def load_data(year):
    base_path = f"assets/{year}"
    caracteristiques = pd.read_csv(
        os.path.join(base_path, f"caracteristiques-{year}.csv"), sep=";"
    )

    caracteristiques = clean_characteristics(caracteristiques)
    lieux = pd.read_csv(os.path.join(base_path, f"lieux-{year}.csv"), sep=";")
    usagers = pd.read_csv(os.path.join(base_path, f"usagers-{year}.csv"), sep=";")
    vehicules = pd.read_csv(os.path.join(base_path, f"vehicules-{year}.csv"), sep=";")
    return caracteristiques, lieux, usagers, vehicules


def alignement(numb):
    for _ in range(numb):
        st.write("\n")
