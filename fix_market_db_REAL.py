import sqlite3
from pathlib import Path

DB_PATH = Path("/home/CarCollector/mysite/instance/carcollector.sqlite")

def col_exists(cur, table, col):
    cur.execute(f"PRAGMA table_info({table});")
    return any(row[1] == col for row in cur.fetchall())

def table_exists(cur, table):
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table,))
    return cur.fetchone() is not None

def add_col(cur, table, col, ddl):
    if col_exists(cur, table, col):
        print(f"OK {table}.{col}")
        return
    cur.execute(f"ALTER TABLE {table} ADD COLUMN {ddl};")
    print(f"Added {table}.{col}")

def main():
    if not DB_PATH.exists():
        raise SystemExit(f"DB not found: {DB_PATH}")

    con = sqlite3.connect(DB_PATH)
    try:
        cur = con.cursor()

        if not table_exists(cur, "market_listing"):
            raise SystemExit("Table market_listing not found in carcollector.sqlite")

        # Columns your traceback shows the app is SELECTing:
        add_col(cur, "market_listing", "part_variant_key", "part_variant_key TEXT")
        add_col(cur, "market_listing", "part_category", "part_category TEXT")
        add_col(cur, "market_listing", "part_name", "part_name TEXT")
        add_col(cur, "market_listing", "part_mutation_multiplier", "part_mutation_multiplier REAL DEFAULT 1.0")
        add_col(cur, "market_listing", "part_mutation_tags", "part_mutation_tags TEXT")

        con.commit()
        print("Done.")
    finally:
        con.close()

if __name__ == "__main__":
    main()
