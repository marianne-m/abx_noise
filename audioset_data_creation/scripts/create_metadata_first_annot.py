import argparse
from pathlib import Path
import dataclasses
import typing 
import csv
import logging
import tqdm
import pandas as pd


ANNOT_PATH = Path("/home/marianne/Work/Projects/abx_noise/abx_noise/audioset_metadata/dataset_creation/class_first_annotation/")
ANNOT_NAME = "Annotation AudioSet - "
METADATA_OUT = "./first_annot_metadata.csv"

labels = [
    "Air_conditioning",
    "Baby_cry",
    "Bathtub",
    "Car",
    "Knock",
    "Purr",
    "Rain",
    "Vacuum_cleaner",
    "Walk,footsteps",
    "Water_tap,faucet"
]

one_annot = {"Air_conditioning", "Baby_cry", "Purr", "Rain", "Vacuum_cleaner", "Walk,footsteps"}
two_annot = {"Bathtub", "Knock", "Water_tap,faucet"}

metadata = pd.DataFrame()

for noise in labels:
    filename = ANNOT_NAME + noise + ".csv"
    annot = pd.read_csv(ANNOT_PATH / filename)
    if noise in one_annot:
        annot = annot[["File", "Duration", "Is taken"]].fillna("n")
        annot = annot[annot["Is taken"] == "y"]
        annot["Label"] = noise
        metadata = pd.concat([metadata, annot[["File", "Duration", "Label"]]]).reset_index(drop=True)

    elif noise in two_annot:
        annot = annot[["File", "Duration", "Is taken (Marianne)", "Is taken (Marvin)"]].fillna("n")
        annot = annot[(annot["Is taken (Marianne)"] == "y") | (annot["Is taken (Marvin)"] == "y")]
        annot["Label"] = noise
        metadata = pd.concat([metadata, annot[["File", "Duration", "Label"]]]).reset_index(drop=True)

    else:
        assert noise == "Car"
        annot = annot[["File", "Duration", "Is taken", "Notes"]].fillna("n")
        annot = annot[annot["Is taken"] == "y"]
        annot = annot.replace({"trafic": "traffic", "moteur": "motor"})
        annot["Label"] = noise
        metadata = pd.concat([metadata, annot[["File", "Duration", "Label", "Notes"]]]).reset_index(drop=True)


metadata.to_csv(METADATA_OUT)
