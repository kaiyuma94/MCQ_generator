import pandas as pd
from typing import List, Dict
import logging
from pathlib import Path

class InputHandler:
    def __init__(self, config: Dict) -> None:
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.required_columns = set([config['input']['question_column']] + 
                                  config['input']['answers_columns'])

    def read_excel(self, file_path: str) -> pd.DataFrame:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
            
        try:
            df = pd.read_excel(file_path)
            self._validate_dataframe(df)
            return df.fillna('')
        except Exception as e:
            self.logger.error(f"Error processing {file_path}: {str(e)}")
            raise

    def _validate_dataframe(self, df: pd.DataFrame) -> None:
        missing_cols = self.required_columns - set(df.columns)
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")