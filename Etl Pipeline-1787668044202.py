import logging
import os
from typing import Dict, Any
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("pipeline_debug.log"), logging.StreamHandler()]
)

class ScalableETLPipeline:
    def __init__(self, config: Dict[str, Any]):
        self.input_path = config.get("input_path")
        self.output_path = config.get("output_path")

    def extract(self) -> pd.DataFrame:
        """Extracts raw dataset with validation."""
        try:
            if not os.path.exists(self.input_path):
                raise FileNotFoundError(f"Source file missing: {self.input_path}")
            df = pd.read_csv(self.input_path)
            logging.info(f"Successfully ingested {len(df)} rows from {self.input_path}")
            return df
        except Exception as e:
            logging.error(f"Extraction Failure: {str(e)}")
            raise

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Applies vectorized Pandas operations and handles bad records."""
        try:
            # 1. Structured Debugging & Data Validation
            initial_rows = len(df)
            df = df.dropna(subset=["transaction_id", "user_id"])
            logging.info(f"Filtered out {initial_rows - len(df)} corrupt/null records.")

            # 2. Vectorized Optimization for Speed
            df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0.0)
            df["processed_timestamp"] = pd.Timestamp.now(tz="UTC")
            df["tax_amount"] = df["amount"] * 0.08  # Vectorized calculation

            logging.info("Transformations successfully executed.")
            return df
        except Exception as e:
            logging.error(f"Transformation Failure: {str(e)}")
            raise

    def load(self, df: pd.DataFrame) -> None:
        """Loads clean output into high-performance Parquet format."""
        try:
            os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
            df.to_parquet(self.output_path, index=False)
            logging.info(f"Pipeline complete. Clean data saved to {self.output_path}")
        except Exception as e:
            logging.error(f"Load Failure: {str(e)}")
            raise

if __name__ == "__main__":
    pipeline_config = {
        "input_path": "data/raw_transactions.csv",
        "output_path": "data/processed/clean_transactions.parquet"
    }
    etl = ScalableETLPipeline(pipeline_config)
    
    # Execution sequence
    raw_data = etl.extract()
    clean_data = etl.transform(raw_data)
    etl.load(clean_data)