import os
import sys
import pandas as pd

input_path = sys.argv[1]
output_file = sys.argv[2]
list_with_taxonomy_path = sys.argv[3]

full_list_genomes = os.listdir(input_path)

list_with_taxonomy = pd.read_csv(list_with_taxonomy_path)

genomes_without_gtdb_tax = list_with_taxonomy.loc[list_with_taxonomy["Domain GTDB"].isnull()]

genomes_to_search = "|".join([f"^{s}" for s in genomes_without_gtdb_tax["Assembly Accession"]])

full_list_genomes_series = pd.Series(full_list_genomes)
genomes_for_tax_searching = full_list_genomes_series[full_list_genomes_series.str.contains(genomes_to_search, regex=True)]

out_file_path = os.path.join(output_file)
genomes_for_tax_searching.to_csv(output_file, index=False)
