# Have to finish the parsing, for the paths for instance

import os
import sys
import subprocess
import argparse
from datetime import datetime
from Bio import SeqIO
import pandas as pd

parser = argparse.ArgumentParser(description='Extract gz fasta files of the nucleotidic genomes sequences plus metadata for a list of seqIDs from DATA-tamriel.')
parser.add_argument('-lg', '--listgenomes', default='/DATA2/bouvetem/4-scripts/pipeline_gtdb_genomes_taxonomy_annotation/1-data/1-list_genomes_tobeanalyzed/20250701_bis_test_bis/gtdbtk.bac120.disappearing_genomes_getgenomesIDs_bis.txt',
                    help='Path to the file where the genomes IDs of interest are stored.')
args = parser.parse_args()
list_of_genomes = args.listgenomes

tamriel_nt_path = '/DATA-tamriel/databases/NCBI/genomes/2023-08-22_NCBI-genomes'
bouvetem_results_folder = '/DATA2/bouvetem/4-scripts/pipeline_gtdb_genomes_taxonomy_annotation/1-data/2-genomes_to_be_analyzed/20250701_bis_test_bis/'

pattern_nt = '_genomic.fna'
pattern_nt_gz = '_genomic.fna.gz'

def run_ln_unzip(ZIPPED, SYMLINK_FOLDER, ZIPPED_SYMLINK):  # Crée un lien symbolique et décompresse un fichier gz
    subprocess.call(['ln', '-s', ZIPPED, SYMLINK_FOLDER])
    subprocess.call(['gzip', '-k', '-d', '-f', ZIPPED_SYMLINK])

def run_ln(ZIPPED, SYMLINK_FOLDER):
    subprocess.call(['ln', '-s', ZIPPED,SYMLINK_FOLDER])

def run_rm_temp_file(FILE):
    subprocess.call(['rm', FILE])

list_of_genomes_of_interest = open(list_of_genomes, 'r')

for genome in list_of_genomes_of_interest.readlines():
    genome = genome.replace("\n","")
    print(f"\n--- Processing genome {genome} ---\n")

    try:
        genome_nt_folder = os.path.join(tamriel_nt_path, genome)
        print(f"\n-> genome_nt_folder: {genome_nt_folder}\n")

        genome_zipped_nt = os.path.join(genome_nt_folder, genome + pattern_nt_gz)
        
        print(f"\n-> genome_zipped_nt: {genome_zipped_nt}\n")

#        genome_zipped_nt_symlink = os.path.join(bouvetem_results_folder, genome + pattern_nt_gz)
#        print(f"\n-> genome_zipped_nt_symlink: {genome_zipped_nt_symlink}\n")

#        run_ln_unzip(ZIPPED=genome_zipped_nt, SYMLINK_FOLDER=bouvetem_results_folder, ZIPPED_SYMLINK=genome_zipped_nt_symlink)

        run_ln(ZIPPED=genome_zipped_nt, SYMLINK_FOLDER=bouvetem_results_folder)

#        genome_unzipped_nt = os.path.join(bouvetem_results_folder, genome + pattern_nt)
#        print(f"\n-> genome_unzipped_nt: {genome_unzipped_nt}\n")

#        run_rm_temp_file(genome_unzipped_cds)

    except Exception as e:
        print(f"Error handling nt genome for {genome}: {e}")

print(f"\nFinito pipoto.")
