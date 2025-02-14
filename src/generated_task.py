import sqlite3
from pathlib import Path

def calculate_gold_ticket_sales(db_file, output_file):
    DB_FILE = Path(db_file)
    OUTPUT_FILE = Path(output_file)

    if not DB_FILE.exists():
        print("DB file not found")
        return

    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute("SELECT SUM(units * price) FROM tickets WHERE type = 'Gold'")
        total_sales = cursor.fetchone()[0]

        total_sales = total_sales if total_sales is not None else 0

        with OUTPUT_FILE.open("w", encoding="utf-8") as f:
            f.write(str(total_sales) + "\n")

        print(f"Total 'Gold' ticket sales are: {total_sales}")

    except sqlite3.Error as e:
        print(f"Database Error: {e}")
    finally:
        conn.close()

# Run the function
calculate_gold_ticket_sales('./data/ticket-sales.db', './data/sales.txt')