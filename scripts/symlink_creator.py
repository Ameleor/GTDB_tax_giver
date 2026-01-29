import os
import sys
import subprocess

input_dir_path = sys.argv[1]
output_dir_path = sys.argv[2]
input_list_path = sys.argv[3]

os.makedirs(output_dir_path, exist_ok=True)


with open(input_list_path, 'r') as input_list:
    for genome in input_list.readlines():
        genome = genome.replace("\n", "")
        try:
            genome_nt_folder = os.path.join(input_dir_path, genome)
            genome_zipped_nt = os.path.join(genome_nt_folder, f"{genome}_genomic.fna.gz")
            print(genome_zipped_nt)
            subprocess.call(['ln', '-s', genome_zipped_nt, output_dir_path])
        except Exception as e:
            print(f"Error handling nt genome for {genome}: {e}")
