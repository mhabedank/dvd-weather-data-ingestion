import os
from glob import glob
import pandas as pd
import re
from .mixins import ParquetStoreMixin


class GeographieMeta(ParquetStoreMixin):
    frame_names = (
        "station_id",
        "altitude",
        "latitude",
        "longitude",
        "from_date",
        "to_date",
        "station_name",
    )

    def __init__(self, meta_data_folder: os.PathLike):
        if not os.path.isdir(meta_data_folder):
            raise ValueError(
                "The folder does not exist. The folder is: " + meta_data_folder
            )

        # get file with name "Metadaten_Geographie_*.txt"
        # e.g. Metadaten_Geographie_0001.txt
        files = glob(os.path.join(meta_data_folder, "Metadaten_Geographie_*.txt"))

        if len(files) == 0:
            raise ValueError(
                'No file with name "Metadaten_Geographie_*.txt" found in folder: '
                + meta_data_folder
            )
        elif len(files) > 1:
            raise ValueError(
                'More than one file with name "Metadaten_Geographie_*.txt" found in folder: '
                + meta_data_folder
            )

        file = files[0]

        self.data = self._get_dataframe(file)

    @classmethod
    def _get_dataframe(cls, file) -> pd.DataFrame:
        df = pd.read_csv(
            file,
            sep=";",
            skiprows=1,
            header=None,
            encoding="latin-1",
            names=cls.frame_names,
        )

        df["from_date"] = pd.to_datetime(
            df["from_date"], format="%Y%m%d", errors="coerce"
        )
        df["to_date"] = pd.to_datetime(df["to_date"], format="%Y%m%d", errors="coerce")

        return df


class StationNameMeta(ParquetStoreMixin):
    row_regex = re.compile(
        "^\s*(?P<station_id>\d+);(?P<name>[^;]+);(?P<from_date>\d{8});(?P<to_date>\d{8})?$"
    )

    def __init__(self, folder: str):
        if not os.path.isdir(folder):
            raise ValueError("The folder does not exist. The folder is: " + folder)

        files = glob(os.path.join(folder, "Metadaten_Stationsname*.txt"))

        if len(files) == 0:
            raise ValueError(
                'No file with name "Metadaten_Stationsname*.txt" found in folder: '
                + folder
            )
        elif len(files) > 1:
            raise ValueError(
                'More than one file with name "Metadaten_Stationsname*.txt" found in folder: '
                + folder
            )

        file = files[0]

        self.data = self._get_dataframe(file)

    @staticmethod
    def _get_dataframe(file) -> pd.DataFrame:
        with open(file, "r", encoding="latin-1") as f:
            lines = f.readlines()
            data = []

        for line in lines[1:]:
            match = StationNameMeta.row_regex.match(line)
            if match:
                data.append(match.groupdict())
            else:
                break

        df = pd.DataFrame(data)
        df["from_date"] = pd.to_datetime(
            df["from_date"], format="%Y%m%d", errors="coerce"
        )
        df["to_date"] = pd.to_datetime(df["to_date"], format="%Y%m%d", errors="coerce")

        return df
