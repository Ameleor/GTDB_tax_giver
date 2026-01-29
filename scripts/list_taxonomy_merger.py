import pandas as pd
import os
import sys

list_NCBI = sys.argv[1]
list_gtdbtk = sys.argv[2]
out_list = sys.argv[3]

df_NCBI = pd.read_csv(list_NCBI, low_memory=False)
df_gtdbtk = pd.read_csv(list_gtdbtk, sep="\t", header=None, names=["file_name", "GTDB_tax"])

df_gtdbtk["Assembly"] = df_gtdbtk["file_name"].str.split("_").str[:2].str.join("_")

# Sépare la colonne par le point-virgule (;)
# puis étend les résultats dans de nouvelles colonnes
df_gtdbtk[['temp_k', 'temp_p', 'temp_c', 'temp_o', 'temp_f', 'temp_g', 'temp_s']] = df_gtdbtk['GTDB_tax'].str.split(';', expand=True)

# Nettoie les nouvelles colonnes en retirant le préfixe (d__, p__, c__, etc.)
# et renomme les colonnes
df_gtdbtk["Domain GTDB"] = df_gtdbtk["temp_k"].str.split("__").str[1]
df_gtdbtk["Phylum GTDB"] = df_gtdbtk["temp_p"].str.split("__").str[1]
df_gtdbtk["Class GTDB"] = df_gtdbtk["temp_c"].str.split("__").str[1]
df_gtdbtk["Order GTDB"] = df_gtdbtk["temp_o"].str.split("__").str[1]
df_gtdbtk["Family GTDB"] = df_gtdbtk["temp_f"].str.split("__").str[1]
df_gtdbtk["Genus GTDB"] = df_gtdbtk["temp_g"].str.split("__").str[1]
df_gtdbtk["Species GTDB"] = df_gtdbtk["temp_s"].str.split("__").str[1]

# Supprime les colonnes temporaires
df_gtdbtk = df_gtdbtk.drop(columns=['temp_k', 'temp_p', 'temp_c', 'temp_o', 'temp_f', 'temp_g', 'temp_s'])

print(len(df_NCBI[df_NCBI["Domain GTDB"].isna()]))

df_merged = df_NCBI.merge(df_gtdbtk, how="left", right_on="Assembly", left_on="Assembly Accession")

print(df_merged.columns)
print(len(df_merged[df_merged["Domain GTDB_x"].isna()]))
print(len(df_merged[df_merged["Domain GTDB_y"].isna()]))

clades = ['Domain GTDB', 'Phylum GTDB', 'Class GTDB', 'Order GTDB', 'Family GTDB', 'Genus GTDB', 'Species GTDB']

print(len(df_merged.columns))

for clade in clades:
    df_merged[clade] = df_merged[f"{clade}_x"].fillna(df_merged[f"{clade}_y"])
    df_merged.drop(columns=[f"{clade}_x", f"{clade}_y"], inplace=True)

print(len(df_merged[df_merged["Domain GTDB"].isna()]))
print(len(df_merged.columns))

os.makedirs(os.path.dirname(out_list), exist_ok=True)

df_merged.reset_index().to_csv(out_list, sep="\t")