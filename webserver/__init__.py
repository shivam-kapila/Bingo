import os
from flask import Flask, json
from werkzeug.exceptions import HTTPException


def create_app(config_path=None, debug=None):
    """ Generate a Flask app with all configurations done and connections established.
    In the Flask app returned, blueprints are registered.
    """
    app = Flask(import_name=__name__)

    # Add login manager
    from webserver.login import login_manager
    login_manager.init_app(app)

    # Load configs
    config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'config.py')
    app.config.from_pyfile(config_file)

    if debug is not None:
        app.debug = debug

    # Connect DB
    import db
    db.init_db_connection(app.config['SQLALCHEMY_DATABASE_URI'])

    # Error handing as JSON
    @app.errorhandler(HTTPException)
    def handle_exception(e):
        """Return JSON instead of HTML for HTTP errors."""
        # start with the correct headers and status code from the error
        response = e.get_response()
        # replace the body with JSON
        response.data = json.dumps({
            "code": e.code,
            "name": e.name,
            "description": e.description,
        })
        response.content_type = "application/json"
        return response

    class NoContent(HTTPException):
        code = 204
        description = 'Payment required.'

    # # Static files
    # import webserver.static_manager
    # static_manager.read_manifest()
    # app.context_processor(lambda: dict(get_static_path=static_manager.get_static_path))
    # app.static_folder = '/static'

    _register_blueprints(app)
    return app


def _register_blueprints(app):
    """ Register blueprints for the given Flask app. """
    from webserver.views.index import index_bp
    app.register_blueprint(index_bp)
    from webserver.views.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    from webserver.views.admin import admin_bp
    app.register_blueprint(admin_bp, url_prefix="/admin")
    from webserver.views.lucky_draw import lucky_draw_bp
    app.register_blueprint(lucky_draw_bp, url_prefix="/lucky-draw")
