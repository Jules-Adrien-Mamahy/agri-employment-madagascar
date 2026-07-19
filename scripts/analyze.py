"""
Analyse : évolution de l'emploi agricole à Madagascar (1991-2025)
Comparaison avec Kenya, Tanzanie, Mozambique, Afrique subsaharienne, Monde.
"""

import pandas as pd
import matplotlib.pyplot as plt

DATA_PATH = "data/processed/agri_employment_clean.csv"
OUT_DIR = "outputs"

COLORS = {
    "Madagascar": "#1F3864",
    "Kenya": "#BF8F00",
    "Tanzanie": "#548235",
    "Mozambique": "#C00000",
    "Afrique subsaharienne": "#7F7F7F",
    "Monde": "#000000",
}


def load():
    return pd.read_csv(DATA_PATH)


def plot_evolution(df):
    plt.figure(figsize=(10, 6))
    for pays, sous_df in df.groupby("Pays"):
        style = "-" if pays == "Madagascar" else "--"
        lw = 3 if pays == "Madagascar" else 1.5
        plt.plot(
            sous_df["Annee"], sous_df["Taux_emploi_agricole"],
            label=pays, color=COLORS.get(pays), linestyle=style, linewidth=lw,
        )
    plt.title("Évolution de l'emploi agricole (% de l'emploi total), 1991-2025")
    plt.xlabel("Année")
    plt.ylabel("% de l'emploi total")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/evolution_emploi_agricole.png", dpi=150)
    plt.close()


def plot_variation_par_decennie(df):
    mdg = df[df["Pays"] == "Madagascar"].copy()
    mdg["Decennie"] = (mdg["Annee"] // 10) * 10
    decennie = mdg.groupby("Decennie")["Taux_emploi_agricole"].mean()

    plt.figure(figsize=(8, 5))
    decennie.plot(kind="bar", color="#1F3864")
    plt.title("Madagascar — Taux moyen d'emploi agricole par décennie")
    plt.xlabel("Décennie")
    plt.ylabel("% moyen de l'emploi total")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/madagascar_par_decennie.png", dpi=150)
    plt.close()


def resume_chiffres(df):
    mdg = df[df["Pays"] == "Madagascar"].sort_values("Annee")
    premiere = mdg.iloc[0]
    derniere = mdg.iloc[-1]
    variation = derniere["Taux_emploi_agricole"] - premiere["Taux_emploi_agricole"]

    print("--- Résumé Madagascar ---")
    print(f"{int(premiere['Annee'])} : {premiere['Taux_emploi_agricole']:.1f}%")
    print(f"{int(derniere['Annee'])} : {derniere['Taux_emploi_agricole']:.1f}%")
    print(f"Variation totale : {variation:+.1f} points sur {int(derniere['Annee']) - int(premiere['Annee'])} ans")

    dernier_par_pays = df.sort_values("Annee").groupby("Pays").last()["Taux_emploi_agricole"]
    print("\n--- Comparaison en 2025 ---")
    print(dernier_par_pays.sort_values(ascending=False))


if __name__ == "__main__":
    df = load()
    plot_evolution(df)
    plot_variation_par_decennie(df)
    resume_chiffres(df)
    print("\nGraphiques enregistrés dans outputs/")
