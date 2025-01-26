from pathlib import Path
import pandas as pd
from typing import List, Dict
import logging

class OutputGenerator:
   def __init__(self, config: Dict) -> None:
       self.logger = logging.getLogger(__name__)
       self.output_path = Path(config['output']['file_path'])
       self.output_path.mkdir(parents=True, exist_ok=True)

   def write_excel(self, data: List[Dict], filename: str) -> Path:
       """Write processed data to Excel with error handling"""
       try:
           df = pd.DataFrame(data)
           output_file = self.output_path / filename
           df.to_excel(output_file, index=False, engine='openpyxl')
           self.logger.info(f"Successfully wrote data to {output_file}")
           return output_file
       except Exception as e:
           self.logger.error(f"Failed to write Excel file: {str(e)}")
           raise