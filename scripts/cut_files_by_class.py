import os
import pandas as pd
from pathlib import Path
from pydub import AudioSegment
from tqdm import tqdm


CLASSES_NAME = {
    0: "Female_speech",
    1: "Male_speech",
    2: "Clapping",
    3: "Telephone",
    4: "Laughter",
    5: "Domestic_sounds",
    6: "Walk_footsteps",
    7: "Door",
    8: "Music",
    9: "Musical_instrument",
    10: "Water_tap",
    11: "Bell",
    12: "Knock"
}

INPUT = Path("/scratch1/data/raw_data/STARSS22")
OUTPUT = Path("/scratch2/mmetais/coml/abx_noise/dcase_cut_by_class")

metadata = pd.read_csv("/scratch2/mmetais/coml/abx_noise/starss_by_class.csv", index_col=0)

for class_name in CLASSES_NAME.values():
    os.makedirs(OUTPUT / class_name, exist_ok=True)


for index, row in tqdm(metadata.iterrows()):
    filename, onset, offset, class_index = row

    source = next(INPUT.rglob(f"{filename}.wav"))

    new_segment = AudioSegment.from_wav(source)
    new_segment = new_segment[int(onset * 1000): int(offset * 1000)]

    class_name = CLASSES_NAME[class_index]
    filename = filename + f"_{index}.wav"
    new_segment.export(OUTPUT / class_name / filename, format="wav")

    # cut file and save it