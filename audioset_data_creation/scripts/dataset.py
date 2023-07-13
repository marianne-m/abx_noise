from pathlib import Path
from dataclasses import dataclass
from typing import Iterable, Optional, List
from os import makedirs
from matplotlib import pyplot as plt
import pandas as pd
import json


# making plots look good
import matplotlib

plt.rcParams['text.usetex'] = False
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.serif'] = 'Arial'
matplotlib.rcParams.update({'font.size': 14, 'legend.handleheight':1, 'hatch.linewidth': 1.0,
                           'lines.markersize':4, 'lines.linewidth':1.5,'xtick.labelsize':14})

cm = 1/2.54
H = 14.56
W = 9


def find_label_name(filename: str):
    lab_name = ''.join(Path(filename).stem.split('-')[1:])
    return lab_name.split('_')[0]


def find_filename(filename: str):
    lab_name = ''.join(Path(filename).stem.split('-')[1:])
    return '_'.join(lab_name.split('_')[1:])


def find_duration(label: list):
    duration = 0
    for lab in label:
        duration += lab['end'] - lab['start']
    return duration


@dataclass 
class AnnotatedAudioset:
    path_audiofiles: Path
    annotation_json: Path

    def __post_init__(self):
        with open(self.annotation_json, "r") as json_file:
            annot_json = json.load(json_file)
        
        self.annotations = pd.DataFrame(annot_json)
        self.annotations["noise_label"] = self.annotations["audio"].map(find_label_name)
        self.annotations["filename"] = self.annotations["audio"].apply(find_filename)
        self.annotations = self.annotations[["filename", "label", "noise_label"]]
        self.annotations.dropna(inplace=True)
        self.annotations["label_duration"] = self.annotations["label"].map(find_duration)

    def create_item_file(self, noise_duration: int) -> pd.DataFrame:
        df = pd.DataFrame()
        for _, row in self.annotations.iterrows():
            for lab in row.label:
                total = int((lab["end"] - lab["start"])*1000/noise_duration)
                onsets = [round((lab["start"]*1000 + x*noise_duration)/1000, 2) for x in range(total)]
                offsets = [round((lab["start"]*1000 + x*noise_duration)/1000, 2) for x in range(1, total+1)]
                df_item = pd.DataFrame.from_dict(
                    {
                        "#file": row.filename,
                        "onset": onsets,
                        "offset": offsets,
                        "#phone": row.noise_label,
                        "prev-phone": "X",
                        "next-phone": "X",
                        "speaker": "noise"
                    }
                )
                df = pd.concat([df, df_item])
        return df
    
    def generate_item_files(self, path: str = ".", durations: List[int] = [300, 500, 1000]):
        for duration in durations:
            item_file = self.create_item_file(duration)
            self.save_item_file(item_file, duration, path)

    def save_item_file(self, item_df: pd.DataFrame, noise_duration: int, path: str = ".") -> None:
        makedirs(path, exist_ok=True)
        item_df.to_csv(
            Path(path) / f"audioset_{noise_duration}ms.item",
            sep=" ",
            index=False
        )

    def plot_duration_by_class(self, fig_path: str = "./duration.png") -> None:
        durations = self.annotations.groupby("noise_label").sum().reset_index()
        durations["label_duration"] = durations["label_duration"] / 60
        durations = durations.sort_values(by="label_duration", ascending=False)

        durations.plot(x="noise_label", y="label_duration", kind="bar")
        plt.xlabel('Label')
        plt.ylabel('Duration (in minutes)')
        plt.savefig(fig_path, bbox_inches = "tight")
