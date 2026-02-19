# fix_market_db.py
import os, sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "instance", "car_collector.db")

def get_cols(cur, table):
    cur.execute(f"PRAGMA table_info({table})")
    return {row[1] for row in cur.fetchall()}

def add_col(cur, table, col_name, col_def_sql):
    cols = get_cols(cur, table)
    if col_name in cols:
        print(f"OK {table}.{col_name}")
        return
    cur.execute(f"ALTER TABLE {table} ADD COLUMN {col_def_sql}")
    print(f"Added {table}.{col_name}")

def main():
    if not os.path.exists(DB_PATH):
        raise SystemExit(f"DB not found: {DB_PATH}")

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    # make sure table exists
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='market_listing'")
    if not cur.fetchone():
        raise SystemExit("Table market_listing not found in this DB.")

    add_col(cur, "market_listing", "part_variant_key", "part_variant_key TEXT")
    add_col(cur, "market_listing", "part_category", "part_category TEXT")
    add_col(cur, "market_listing", "part_name", "part_name TEXT")
    add_col(cur, "market_listing", "part_mutation_multiplier", "part_mutation_multiplier REAL DEFAULT 1.0")
    add_col(cur, "market_listing", "part_mutation_tags", "part_mutation_tags TEXT DEFAULT ''")

    con.commit()
    con.close()
    print("Done.")

if __name__ == "__main__":
    main()
