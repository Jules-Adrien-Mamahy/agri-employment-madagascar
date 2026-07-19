"""
Nettoyage des données Banque Mondiale — Emploi agricole (% emploi total)
Source : API_SL_AGR_EMPL_ZS_DS2 (World Bank / ILO modeled estimate)

Transforme le fichier Excel brut (format "wide", 1 colonne par année)
en un CSV propre au format "long" (1 ligne = 1 pays + 1 année + 1 valeur),
filtré sur Madagascar et quelques pays/régions de comparaison.
"""

import pandas as pd

RAW_PATH = "data/raw/agri_employment_worldbank.xls"
OUTPUT_PATH = "data/processed/agri_employment_clean.csv"

# Pays et régions de comparaison pertinents pour Madagascar
COUNTRIES = ["Madagascar", "Kenya", "Tanzanie", "Mozambique", "Afrique subsaharienne", "Monde"]


def clean():
    # La feuille "Data" du fichier Banque Mondiale a 3 lignes d'en-tête à sauter
    df = pd.read_excel(RAW_PATH, sheet_name="Data", header=3)

    # Colonnes d'année (ex: '1960', '1961', ...)
    year_cols = [c for c in df.columns if str(c).isdigit()]

    # Filtrer sur les pays/régions choisis
    df = df[df["Country Name"].isin(COUNTRIES)]

    # Passage du format "wide" (1 colonne par année) au format "long"
    df_long = df.melt(
        id_vars=["Country Name", "Country Code"],
        value_vars=year_cols,
        var_name="Annee",
        value_name="Taux_emploi_agricole",
    )

    df_long["Annee"] = df_long["Annee"].astype(int)
    df_long = df_long.dropna(subset=["Taux_emploi_agricole"])
    df_long = df_long.sort_values(["Country Name", "Annee"]).reset_index(drop=True)
    df_long = df_long.rename(columns={"Country Name": "Pays", "Country Code": "Code"})

    df_long.to_csv(OUTPUT_PATH, index=False)
    print(f"OK : {len(df_long)} lignes écrites dans {OUTPUT_PATH}")
    print(df_long.groupby("Pays")["Annee"].agg(["min", "max", "count"]))


if __name__ == "__main__":
    clean()
