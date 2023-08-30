import pandas as pd
import os


class ParquetStoreMixin:
    def to_parquet(self, path: os.PathLike):
        self.data.to_parquet(path)

    def from_parquet(self, path: os.PathLike):
        self.data = pd.read_parquet(
            path
        )  # pylint: disable=attribute-defined-outside-init
