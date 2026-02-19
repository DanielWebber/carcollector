from flask_migrate import Migrate
from app import create_app, db

app = create_app()

# IMPORTANT:
# Do NOT use `import app.models` because it overwrites the name `app`.
# Use one of these safe imports instead:
import app.models as app_models  # noqa: F401

migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run(debug=True)
