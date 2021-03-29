import os
from flask import Flask
from flask_login import LoginManager


def create_app(config_path=None, debug=None):
    """ Generate a Flask app with all configurations done and connections established.
    In the Flask app returned, blueprints are registered.
    """
    app = Flask(import_name=__name__)

    # Load configs
    config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'config.py')
    app.config.from_pyfile(config_file)

    if debug is not None:
        app.debug = debug

    # Connect DB
    import db
    db.init_db_connection(app.config['SQLALCHEMY_DATABASE_URI'])

    # # Static files
    # import webserver.static_manager
    # static_manager.read_manifest()
    # app.context_processor(lambda: dict(get_static_path=static_manager.get_static_path))
    # app.static_folder = '/static'

    return app
