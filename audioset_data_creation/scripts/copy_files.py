# Copy with symlinks some wanted class into folders named after the label
# On Oberon

import shutil
from pathlib import Path
import pandas as pd
import os


LISTENING_PATH = "/scratch2/mmetais/coml/abx_noise/audioset_listening_session"
SOURCE_PATH = "/scratch1/data/raw_data/audioset/042319/data/unbalanced_train_segments/audio"

wanted_labels =[
    "Car",
    "Subway, metro, underground",
    "Train",
    "White noise",
    "Bark",
    "Purr",
    "Meow",
    "Howl",
    "Moo",
    "Rain",
    "Vacuum cleaner",
    "Baby cry, infant cry",
    "Crying, sobbing",
    "Water tap, faucet",
    "Walk, footsteps",
    "Knock",
    "Microwave oven",
    "Bathtub (filling or washing)",
    "Toilet flush",
    "Air conditioning",
]


class_labels = pd.read_csv("class_labels_indices.csv", index_col="index")
map_id_label = {mid: name for  _, (mid, name) in class_labels.iterrows()}

unbalanced = pd.read_csv("unbalanced_train_segments.csv", quoting=2, sep=',\s+', skiprows=3, names=['YTID', 'start', 'end', 'labels'], engine='python')
unbalanced.labels = unbalanced.labels.map(lambda x: x.replace('"',"").split(","))
unbalanced["num_labels"] = unbalanced.labels.apply(len)
unbalanced = unbalanced[unbalanced["num_labels"] == 1]
unbalanced.labels = unbalanced.labels.map(lambda x: x[0])
unbalanced.labels = unbalanced.labels.map(map_id_label)

# keep only wanted labels
unbalanced["wanted"] = unbalanced.labels.map(lambda x : x in wanted_labels)
unbalanced = unbalanced[unbalanced["wanted"]]

# get name
unbalanced["name"] = unbalanced["YTID"] + "_" + (unbalanced["start"] * 1000).astype(int).astype(str) + "_" \
                    + (unbalanced["end"] * 1000).astype(int).astype(str) + ".flac"

unbalanced.labels = unbalanced.labels.map(lambda x : x.replace(" ", "_"))
# unbalanced = unbalanced[:100]

_labels = [label.replace(" ", "_") for label in wanted_labels]

for lab in _labels:
    os.makedirs(Path(LISTENING_PATH, lab), exist_ok=True)

for _, row in unbalanced.iterrows():
    source = Path(SOURCE_PATH, row["name"])
    dest = Path(LISTENING_PATH, row["labels"], row["name"])
    try:
        shutil.copyfile(source, dest)
    except FileNotFoundError:
        print(f"{row['name']} file does not exist")