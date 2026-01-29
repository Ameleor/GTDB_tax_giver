import os
from glob import glob
import pandas as pd

configfile: "config.yaml"

DATASET = config["dataset"]
DIR_IN = config["dir_in"]
DIR_OUT = config["dir_out"]
CPU = config["cpu"]

DATASET_IN = os.path.join(DIR_IN, DATASET)
LISTS_IN = os.path.join(DIR_IN, "lists")
DATASET_OUT = os.path.join(DIR_OUT, DATASET)

HARD_PATH_FOR_FNA = os.path.join("/DATA-tamriel", "databases", "NCBI", "genomes", "2025-04-NCBI-eubacteria")

rule all:
    input:
        os.path.join(DATASET_OUT, "list_genome_to_search.csv"),
        os.path.join(DATASET_OUT, ".symlink_done"),
        os.path.join(DATASET_OUT, "genomes"),
        os.path.join(DATASET_OUT, "genomes_done"),
        os.path.join(DATASET_OUT, "SCRATCH_DIR")


rule genomes_name_gatherer:
    output:
        list_genome_to_search = os.path.join(DATASET_OUT, "list_genome_to_search.csv")
    shell:
        """
        python3 scripts/no_tax_assembly_gatherer.py {DATASET_IN} {output.list_genome_to_search} {LISTS_IN}/list_with_taxonomy.csv
        """

rule symlink_creator:
    input:
        list_genome_to_search = os.path.join(DATASET_OUT, "list_genome_to_search.csv")
    output:
        file_check = os.path.join(DATASET_OUT, ".symlink_done"),
        out_dir = directory(os.path.join(DATASET_OUT, "genomes"))
    shell:
        """
        python3 scripts/symlink_creator.py {HARD_PATH_FOR_FNA} {output.out_dir} {input.list_genome_to_search}
        touch {output.file_check}
        rm {output.out_dir}/0_genomic.fna
        """

rule gtdbtk:
    input:
        input_dir = os.path.join(DATASET_OUT, "genomes")
    output:
        out_dir = os.path.join(DATASET_OUT, "genomes_done"),
        scratch_dir = os.path.join(DATASET_OUT, "SCRATCH_DIR")
    shell:
        """
        mkdir -p {output.scratch_dir}
        mkdir -p {output.out_dir}
        gtdbtk classify_wf --genome_dir {input.input_dir} --out_dir {output.out_dir} -x gz --cpus {CPU} --debug --scratch_dir {output.scratch_dir} --skip_ani_screen
        """