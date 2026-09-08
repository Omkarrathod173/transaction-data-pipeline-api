import logging
import os
import sqlite3
import pandas as pd
from flask import Flask, jsonify, request

# Configure structured console logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("DataPipeline")

DB_NAME = "transactions.db"

# ==========================================
# 1. ETL PIPELINE MODULE
# ==========================================

def extract_data(file_path: str) -> pd.DataFrame:
    """Extract raw transaction dataset."""
    logger.info(f"Extracting data from: {file_path}")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Source file not found at path: {file_path}")
    return pd.read_csv(file_path)


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean, validate, and transform raw transaction records."""
    logger.info("Transforming raw data...")

    # Remove duplicate records
    df = df.drop_duplicates()

    # Clean column headers
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # Type coercion and null cleaning
    if "transaction_date" in df.columns:
        df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors="coerce")

    if "amount" in df.columns:
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0.0)

    if "transaction_id" in df.columns:
        df = df.dropna(subset=["transaction_id"])

    logger.info(f"Transformation complete. Clean record count: {len(df)}")
    return df


def load_data(df: pd.DataFrame, db_name: str = DB_NAME, table_name: str = "transactions"):
    """Load cleaned records into SQLite database."""
    logger.info(f"Loading data into SQLite table '{table_name}'...")
    conn = sqlite3.connect(db_name)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()
    logger.info("Data successfully loaded to database.")


def run_etl(file_path: str):
    """Orchestrates the ETL execution sequence."""
    try:
        raw_df = extract_data(file_path)
        clean_df = transform_data(raw_df)
        load_data(clean_df)
    except Exception as e:
        logger.error(f"ETL pipeline execution failed: {e}")


# ==========================================
# 2. REST API MODULE
# ==========================================

app = Flask(__name__)


def execute_query(query: str, params: tuple = ()):
    """Helper method to run SQL queries and return dictionary records."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description] if cursor.description else []
    conn.close()
    return [dict(zip(columns, row)) for row in rows]


@app.route("/health", methods=["GET"])
def health_check():
    """Service health check endpoint."""
    return jsonify({"status": "healthy", "service": "transaction-pipeline-api"}), 200


@app.route("/api/kpis", methods=["GET"])
def get_kpis():
    """Returns top-level KPI summary metrics."""
    try:
        query = """
        SELECT 
            COUNT(*) AS total_transactions,
            ROUND(SUM(amount), 2) AS total_revenue,
            ROUND(AVG(amount), 2) AS avg_transaction_value
        FROM transactions
        """
        result = execute_query(query)
        return jsonify(result[0] if result else {}), 200
    except Exception as e:
        logger.error(f"API KPI Error: {e}")
        return jsonify({"error": "Failed to calculate KPIs", "details": str(e)}), 500


@app.route("/api/transactions", methods=["GET"])
def get_transactions():
    """Returns paginated/limited transaction records."""
    limit = request.args.get("limit", default=10, type=int)
    try:
        query = "SELECT * FROM transactions LIMIT ?"
        result = execute_query(query, (limit,))
        return jsonify({"count": len(result), "data": result}), 200
    except Exception as e:
        logger.error(f"API Fetch Error: {e}")
        return jsonify({"error": "Failed to fetch transactions", "details": str(e)}), 500


if __name__ == "__main__":
    # Run ETL process if source CSV exists locally
    if os.path.exists("data.csv"):
        run_etl("data.csv")

    logger.info("Starting REST API application...")
    app.run(host="0.0.0.0", port=5000, debug=True)