from abc import ABC, abstractmethod
import pandas as pd

class DataFrameLoader(ABC):
    @abstractmethod
    def load(self, csv_bytes: bytes) -> pd.DataFrame:
        pass
