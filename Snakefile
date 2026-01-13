import os
from glob import glob
import pandas as pd

configfile: "config.yaml"

DATASET = config["dataset"]
DIR_IN = config["dir_in"]
DIR_OUT = config["dir_out"]