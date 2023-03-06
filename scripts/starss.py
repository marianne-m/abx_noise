import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt


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
    12: "Knock"
}


def cum_dur_by_class_graph(data: pd.DataFrame, fig_name: str) -> None:
    """
    Generate a graph plotting the cumulative duration by class
    """
    cum_dur_df = data[["class_index", "frame_number"]].groupby("class_index", as_index=False).count()
    cum_dur_df = cum_dur_df.rename(columns={"frame_number": "duration"})
    cum_dur_df["duration"] = cum_dur_df["duration"].map(lambda x: x/600) # get the duration in minutes
    cum_dur_df["class_index"] = cum_dur_df["class_index"].map(lambda x: CLASSES[x])
    cum_dur_df = cum_dur_df.set_index("class_index")

    ax = cum_dur_df.plot.bar()
    ax.set_ylabel("Duration (in minutes)")
    ax.set_xlabel("Noise class")

    plt.savefig(fig_name, bbox_inches="tight")


class StarssData:
    """Class that manipulates metadata from the STARSS22 dataset"""
    def __init__(self, path_to_metadata) -> None:
        self.original_data = None
        self.data = None

        list_metadata = self.find_metadata(path_to_metadata)
        for data_path in list_metadata:
            self.read_metadata(data_path)

        self.prepare_data()

    def read_metadata(self, path_to_metadata) -> None:
        df = pd.read_csv(path_to_metadata, names=['frame_number', 'class_index', 'source_index', 'azimuth', 'elevation'])
        df["filename"] = path_to_metadata.stem
        self.original_data = pd.concat([self.original_data, df[["frame_number", "class_index", "filename"]]])

    def find_metadata(self, path) -> None:
        path = Path(path)
        return path.glob("**/*.csv")

    def exclude_multiple_noises(self, df: pd.DataFrame) -> pd.DataFrame:
        df_count = df.groupby(["frame_number", "filename"], as_index=False).size()
        df = pd.merge(df, df_count)
        df = df[df["size"] == 1]
        return df

    def remove_class(self, df: pd.DataFrame, class_index: int = 8) -> pd.DataFrame:
        df = df[df["class_index"] != class_index]
        return df

    def prepare_data(self) -> None:
        self.data = self.exclude_multiple_noises(self.original_data)
        self.data = self.remove_class(self.data)

    def generate_item_files(self, noise_duration: int = 100) -> None:
        pass

    def generate_graphes(self) -> None:
        """
        nb_files / class, cumulative_duration / class for original and filtered data
        """
        pass
