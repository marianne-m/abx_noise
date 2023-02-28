import pandas as pd
from pathlib import Path


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

class StarssData:
    """Class that manipulates metadata from the STARSS22 dataset"""
    def __init__(self, path_to_metadata) -> None:
        self.original_data = None
        self.data = None

        self.read_metadata(path_to_metadata)
        self.prepare_data()  

    def read_metadata(self, path_to_metadata) -> None:
        df = pd.read_csv(path_to_metadata, names=['frame_number', 'class_index', 'source_index', 'azimuth', 'elevation'])
        self.original_data = df[["frame_number", "class_index"]]

    def find_metadata(self, path) -> None:
        path = Path(path)
        self.list_metadata = path.glob("**/*.csv")

    def exclude_multiple_noises(self, df: pd.DataFrame) -> pd.DataFrame:
        df_count = df.groupby("frame_number", as_index=False).size()
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