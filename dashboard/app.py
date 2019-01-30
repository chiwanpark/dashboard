from flask import Flask


def create_app():
    app = Flask(__name__.split('.')[0])
    register_blueprint(app)

    @app.route('/')
    def index():
        return 'Hello World!'

    return app


def register_blueprint(app):
    from dashboard.metric import blueprint as metric_blueprint
    app.register_blueprint(metric_blueprint)
