from collections import defaultdict
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import logging
from os import makedirs

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

# fig, ax = plt.subplots(1,1, figsize=(H*cm,W*cm), constrained_layout=True)

CLASSES = {
    0: "Female speech, woman speaking",
    1: "Male speech, man speaking",
    2: "Clapping",
    3: "Telephone",
    4: "Laughter",
    5: "Domestic sounds",
    6: "Walk, footsteps",
    7: "Door, open or close",
    8: "Music",
    9: "Musical instrument",
    10: "Water tap, faucet",
    11: "Bell",
    12: "Knock",
    13: "Vacuum cleaner",
    14: "Air conditioning"
}

CLASSES_NAME = {
    0: "Female_speech",
    1: "Male_speech",
    2: "Clapping",
    3: "Telephone",
    4: "Laughter",
    5: "Domestic_sounds",
    6: "Walkfootsteps",
    7: "Door",
    8: "Music",
    9: "Musical_instrument",
    10: "Watertap",
    11: "Bell",
    12: "Knock",
    13: "Vacuumcleaner",
    14: "Airconditioning"
}

REMOVED_CLASSES = [3, 4, 7, 8, 9, 11]


logger = logging.getLogger(__name__)


def cum_dur_by_class_graph(
        data: pd.DataFrame,
        fig_name: str,
        frame_dur: int = 100,
        classes_index: bool = True,
        ms_to_min: int = 60000
) -> None:
    """
    Generate a graph plotting the cumulative duration by class
    """
    cum_dur_df = data[["class_index", "frame_number"]].groupby("class_index", as_index=False).count()
    cum_dur_df = cum_dur_df.rename(columns={"frame_number": "duration"})
    cum_dur_df["duration"] = cum_dur_df["duration"] * frame_dur / ms_to_min # get the duration in minutes
    if classes_index:
        cum_dur_df["class_index"] = cum_dur_df["class_index"].map(lambda x: CLASSES[x])
    cum_dur_df = cum_dur_df.set_index("class_index")

    ax = cum_dur_df.plot.bar()
    ax.set_ylabel("Duration (in minutes)")
    ax.set_xlabel("Noise class")

    plt.savefig(fig_name, bbox_inches="tight")


def cum_dur_by_multiple_classes(
        data: pd.DataFrame,
        fig_name: str,
        max_classes: int = 2,
        max_classes_on_graph: int = 15
) -> None:
    """
    Generate a graph plotting the cumulative duration by class and combination
    of two classes
    """
    # finding the combination of classes and only keeping 2 classes or less
    cum_dur_df = data.groupby(["frame_number", "filename"], as_index=False).agg({'class_index': set})
    cum_dur_df = cum_dur_df[cum_dur_df.class_index.map(len) <= max_classes]
    cum_dur_df = cum_dur_df.astype({"class_index": "str"})

    cum_dur_df = cum_dur_df[["class_index", "frame_number"]].groupby("class_index", as_index=False).count()
    cum_dur_df = cum_dur_df.rename(columns={"frame_number": "duration"})
    cum_dur_df["duration"] = cum_dur_df["duration"] / 600 # get the duration in minutes
    cum_dur_df = cum_dur_df.set_index("class_index")
    cum_dur_df = cum_dur_df.sort_values("duration", ascending=False)

    ax = cum_dur_df[:max_classes_on_graph].plot.bar()
    ax.set_ylabel("Duration (in minutes)")
    ax.set_xlabel("Noise class")

    plt.savefig(fig_name, bbox_inches="tight")    


def nb_of_files_by_class_graph(data: pd.DataFrame, fig_name: str) -> None:
    """
    Generate a graph plotting the cumulative duration by class
    """
    nb_of_files = data[["class_index", "filename"]].drop_duplicates() \
                                                   .groupby("class_index", as_index=False) \
                                                   .count()
    nb_of_files = nb_of_files.rename(columns={"filename": "nb_of_files"})
    nb_of_files["class_index"] = nb_of_files["class_index"].map(lambda x: CLASSES[x])
    nb_of_files = nb_of_files.set_index("class_index")

    ax = nb_of_files.plot.bar()
    ax.set_ylabel("Number of files")
    ax.set_xlabel("Noise class")

    plt.savefig(fig_name, bbox_inches="tight")


class StarssData:
    """Class that manipulates metadata from the STARSS22 dataset"""
    def __init__(self, path_to_metadata) -> None:
        self.original_data = None
        self.data = None
        self.item_file = None
        self.metadata_classes = None

        list_metadata = self.find_metadata(path_to_metadata)
        for data_path in list_metadata:
            self.read_metadata(data_path)

        self.prepare_data()
        self.generate_metadata_classes()

    def read_metadata(self, path_to_metadata) -> None:
        df = pd.read_csv(path_to_metadata, names=['frame_number', 'class_index', 'source_index', 'azimuth', 'elevation'])
        df["filename"] = path_to_metadata.stem
        self.original_data = pd.concat([self.original_data, df[["frame_number", "class_index", "filename"]]])

    def find_metadata(self, path) -> None:
        path = Path(path)
        return path.glob("**/*.csv")

    def exclude_multiple_noises(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.drop_duplicates()
        df_count = df.groupby(["frame_number", "filename"], as_index=False).size()
        df = pd.merge(df, df_count)
        df = df[df["size"] == 1]
        return df

    def remove_class(self, df: pd.DataFrame, class_index: int = 8) -> pd.DataFrame:
        df = df[df["class_index"] != class_index]
        return df

    def prepare_data(self) -> None:
        self.data = self.exclude_multiple_noises(self.original_data)
        for index in REMOVED_CLASSES:
            self.data = self.remove_class(self.data, index)

    def save_metadata_classes(self, path: str) -> None:
        self.metadata_classes.to_csv(path)

    def convert_df_to_item_file(self, dataframe: pd.DataFrame) -> None:
        if "onset" not in dataframe.columns or "offset" not in dataframe.columns:
            dataframe["onset"] = dataframe["frame_number"] / 10
            dataframe["offset"] = dataframe["frame_number"] / 10

        dataframe["label_1"] = "X"
        dataframe["label_3"] = "X"
        dataframe["speaker"] = "noise"

        dataframe["class_index"] = dataframe["class_index"].map(CLASSES_NAME)
        self.item_file = dataframe[["filename", "onset", "offset", "class_index", "label_1", "label_3", "speaker"]]

    def save_item_file(self, path: str = ".") -> None:
        if self.item_file is None:
            logger.warning("The item file is empty. Please call 'generate_item_files' method.")
        else:
            makedirs(path, exist_ok=True)
            self.item_file.to_csv(
                Path(path) / f"starss_{self.noise_duration}ms.item",
                sep=" ",
                header=["#file", "onset", "offset", "#phone", "prev-phone", "next-phone", "speaker"],
                index=False
            )

    def generate_item_files(self, noise_duration: int = 100) -> None:
        """
        Generates .item files with noise duration (in ms)
        """
        self.noise_duration = noise_duration
        if noise_duration == 100:
            self.convert_df_to_item_file(self.data)

        else:
            previous_class = None
            previous_frame_nb = -10
            previous_filename = str()
            counter = 1

            grouping = int(noise_duration / 100)
            grouped = defaultdict(list)

            for row in self.data.iterrows():
                frame_nb = row[1]["frame_number"]
                class_id = row[1]["class_index"]
                filename = row[1]["filename"]

                if (previous_frame_nb + 1 == frame_nb) \
                        and (previous_class == class_id) \
                        and (previous_filename == filename):
                    counter += 1
                else:
                    counter = 1

                if counter == grouping:
                    onset = (frame_nb - grouping + 1) / 10
                    offset = (frame_nb + 1) / 10

                    grouped["onset"].append(onset)
                    grouped["offset"].append(offset)
                    grouped["class_index"].append(class_id)
                    grouped["filename"].append(filename)

                    counter = 0

                previous_class = class_id
                previous_frame_nb = frame_nb
                previous_filename = filename

            self.convert_df_to_item_file(pd.DataFrame.from_dict(grouped))

    def generate_graphes(self, path_to_graph: str) -> None:
        """
        Generates the following plots :
            - cumulative duration by class for original data
            - cumulative duration by clase for filtered data
            - number of files by class for original data
            - number of files by class for filtered data
            - cumulative duration by multiple classes for original data
        """
        makedirs(path_to_graph, exist_ok=True)

        cum_dur_by_class_graph(self.original_data, Path(path_to_graph) / "cum_dur_by_class_before_filter.png")
        cum_dur_by_class_graph(self.data, Path(path_to_graph) / "cum_dur_by_class_filtered.png")

        nb_of_files_by_class_graph(self.original_data, Path(path_to_graph) / "nb_of_files_by_class_before_filter.png")
        nb_of_files_by_class_graph(self.data, Path(path_to_graph) / "nb_of_files_by_class_filtered.png")

        cum_dur_by_multiple_classes(self.original_data, Path(path_to_graph) / "cum_dur_by_multiple_classes_original_data.png")

    def generate_metadata_classes(self) -> None:
        """
        Create a metadata file with classes, onset and offset for each sound
        """
        onset, offset, current_file, current_class, current_frame_number = -1, -1, "", -1, -10
        noise = []

        for index, row in self.data.iterrows():
            if (row["filename"] == current_file) and \
                    (row["class_index"] == current_class) and \
                    (current_frame_number == (row["frame_number"] - 1)):
                offset = row["frame_number"]
            else:
                if index > 0:
                    noise.append([current_file, onset, offset, current_class])
                onset = row["frame_number"]
                offset = row["frame_number"]
            current_frame_number, current_class, current_file, _ = row

        noise.append([current_file, onset, offset, current_class])

        data_df = pd.DataFrame(noise, columns=["file", "onset", "offset", "class"])
        data_df["onset"] = data_df["onset"] / 10
        data_df["offset"] = data_df["offset"] / 10

        self.metadata_classes = data_df
