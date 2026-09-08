import logging
import os
import sqlite3
import pandas as pd
from flask import Flask, jsonify, request

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("DataPipeline")

# Absolute path configuration (prevents SQLite file path mismatches)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "transactions.db")
CSV_NAME = os.path.join(BASE_DIR, "data.csv")


def ensure_database():
    """Generates dataset if missing and populates transactions table directly."""
    if not os.path.exists(CSV_NAME):
        sample_df = pd.DataFrame({
            "transaction_id": [101, 102, 103, 104, 105],
            "transaction_date": ["2026-01-01", "2026-01-02", "2026-01-03", "2026-01-04", "2026-01-05"],
            "amount": [150.50, 299.99, 45.00, 1200.00, 89.90],
            "category": ["Electronics", "Clothing", "Groceries", "Electronics", "Home"]
        })
        sample_df.to_csv(CSV_NAME, index=False)
    
    df = pd.read_csv(CSV_NAME)
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    
    conn = sqlite3.connect(DB_NAME)
    df.to_sql("transactions", conn, if_exists="replace", index=False)
    conn.close()
    logger.info(f"Database successfully loaded at '{DB_NAME}' with {len(df)} records.")


# Initialize database automatically on startup
ensure_database()

app = Flask(__name__)


def execute_query(query: str, params: tuple = ()):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description] if cursor.description else []
    conn.close()
    return [dict(zip(columns, row)) for row in rows]


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "service": "transaction-pipeline-api"}), 200


@app.route("/api/kpis", methods=["GET"])
def get_kpis():
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
        logger.error(f"KPI Query Error: {e}")
        return jsonify({"error": "Failed to calculate KPIs", "details": str(e)}), 500


@app.route("/api/transactions", methods=["GET"])
def get_transactions():
    limit = request.args.get("limit", default=10, type=int)
    try:
        query = "SELECT * FROM transactions LIMIT ?"
        result = execute_query(query, (limit,))
        return jsonify({"count": len(result), "data": result}), 200
    except Exception as e:
        logger.error(f"Transactions Fetch Error: {e}")
        return jsonify({"error": "Failed to fetch transactions", "details": str(e)}), 500


if __name__ == "__main__":
    logger.info("Starting REST API application...")
    app.run(host="0.0.0.0", port=5000, debug=True)