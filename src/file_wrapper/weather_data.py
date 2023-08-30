import os
from glob import glob
import pandas as pd
from .mixins import ParquetStoreMixin


class Wind10MinutesData(ParquetStoreMixin):
    frame_names = (
        "station_id",
        "timestamp",
        "quality",
        "avg_speed",
        "avg_direction",
        "eol",
    )

    def __init__(self, wind_folder: os.PathLike):
        if not os.path.isdir(wind_folder):
            raise ValueError("The folder does not exist. The folder is: " + wind_folder)

        files = glob(os.path.join(wind_folder, "produkt_zehn_min_ff*.txt"))

        if len(files) == 0:
            raise ValueError(
                'No file with name "Wind_10min_*.txt" found in folder: ' + wind_folder
            )
        elif len(files) > 1:
            raise ValueError(
                'More than one file with name "Wind_10min_*.txt" found in folder: '
                + wind_folder
            )

        file = files[0]

        self.data = self._get_dataframe(file)

    @classmethod
    def _get_dataframe(cls, file):
        df = pd.read_csv(
            file,
            sep=";",
            header=0,
            encoding="latin-1",
            names=cls.frame_names,
            index_col=False,
            na_values=["-999", "  -999"],
        )

        df["timestamp"] = pd.to_datetime(
            df["timestamp"], format="%Y%m%d%H%M", errors="coerce"
        )

        df.drop(columns=["eol"], inplace=True)

        # Clean data: We only want complete data for this poc.
        df = df.dropna(axis="rows", subset=["avg_speed", "avg_direction"], how="any")

        return df
