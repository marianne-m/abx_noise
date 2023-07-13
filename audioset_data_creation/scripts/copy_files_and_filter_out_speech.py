import shutil
from pathlib import Path
import pandas as pd
import os



AUDIO_PATH = "/scratch2/mmetais/coml/abx_noise/audioset_16k"
RTTM_PATH = "/scratch2/mmetais/coml/abx_noise/audioset_brouhaha_output/rttm_files"
FILTER_PATH = "/scratch2/mmetais/coml/abx_noise/audioset_filtered"

audiofiles = Path(AUDIO_PATH).rglob("*.wav")
labels = Path(AUDIO_PATH).iterdir()

for lab in labels:
    os.makedirs(Path(FILTER_PATH, lab.stem), exist_ok=True)

for file in audiofiles:
    # check if rttm is empty
    rttm_file = Path(RTTM_PATH, file.stem + ".rttm")
    is_empty = os.stat(rttm_file).st_size == 0

    if is_empty:
        # copy the files with the category
        source = file
        dest = Path(FILTER_PATH, file.parent.stem, file.name)
        shutil.copyfile(source, dest)
