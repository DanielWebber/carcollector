from sqlalchemy import text
from app import create_app, db

app = create_app()

def ensure_inventory_columns():
    cols = [r[1] for r in db.session.execute(text("PRAGMA table_info(inventory)")).fetchall()]

    if "variant_key" not in cols:
        db.session.execute(text("ALTER TABLE inventory ADD COLUMN variant_key TEXT"))
    if "mutation_multiplier" not in cols:
        db.session.execute(text("ALTER TABLE inventory ADD COLUMN mutation_multiplier REAL NOT NULL DEFAULT 1.0"))
    if "mutation_tags" not in cols:
        db.session.execute(text("ALTER TABLE inventory ADD COLUMN mutation_tags TEXT NOT NULL DEFAULT ''"))

    # Backfill existing rows safely
    db.session.execute(text("UPDATE inventory SET variant_key = COALESCE(variant_key, 'base')"))
    db.session.execute(text("UPDATE inventory SET mutation_multiplier = COALESCE(mutation_multiplier, 1.0)"))
    db.session.execute(text("UPDATE inventory SET mutation_tags = COALESCE(mutation_tags, '')"))

    # Helpful index for stacking lookups
    db.session.execute(text(
        "CREATE INDEX IF NOT EXISTS ix_inventory_stack ON inventory(user_id, part_category, part_name, variant_key)"
    ))

    db.session.commit()
    print("Inventory schema updated successfully.")
    print("Columns now:", [r[1] for r in db.session.execute(text("PRAGMA table_info(inventory)")).fetchall()])

if __name__ == "__main__":
    with app.app_context():
        ensure_inventory_columns()
