from flask.cli import FlaskGroup
from app.wsgi import app

cli = FlaskGroup(app)
if __name__ == "__main__":
    cli()