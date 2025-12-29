import pandas as pd
import io

class CsvDataFrameLoader:
    def load(self, csv_bytes: bytes) -> pd.DataFrame:
        try:
            return pd.read_csv(io.BytesIO(csv_bytes))
        except Exception as e:
            raise ValueError("Invalid CSV format") from e
