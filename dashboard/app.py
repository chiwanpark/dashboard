from flask import Flask


def create_app():
    app = Flask(__name__.split('.')[0])
    register_blueprint(app)

    @app.route('/')
    def index():
        return 'Hello World!'

    return app


def register_blueprint(app):
    pass
