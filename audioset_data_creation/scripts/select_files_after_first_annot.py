#!/usr/bin/env python

import shutil
from pathlib import Path
import pandas as pd
import os



BEFORE_PATH = Path("/scratch2/mmetais/coml/abx_noise/audioset_filtered")
AFTER_PATH = Path("/scratch2/mmetais/coml/abx_noise/audioset_filtered_annot")
METADATA="/scratch2/mmetais/coml/abx_noise/first_annot_metadata.csv"

metadata = pd.read_csv(METADATA)

for _, row in metadata.iterrows():
    os.makedirs(AFTER_PATH / row["Label"], exist_ok=True)
    if row["Label"] == "Car":
        os.makedirs(AFTER_PATH / row["Label"] / row["Notes"], exist_ok=True)
        dest = AFTER_PATH / row["Label"] / row["Notes"] / row["File"]
    else:
        dest = AFTER_PATH / row["Label"] / row["File"]
    source = next(BEFORE_PATH.rglob(row["File"]))
    shutil.copyfile(source, dest)
