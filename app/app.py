from flask import Flask
from flask_cors import CORS
from app.config.config import Config
from app.config.database import init_db
from app.config.logger import setup_logger
from app.middlewares.logging_middleware import LoggingMiddleware
from app.middlewares.error_handler import register_error_handlers


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, resources={r'/api/*': {'origins': '*'}})

    init_db(app)

    setup_logger(app)

    app.wsgi_app = LoggingMiddleware(app.wsgi_app)

    register_error_handlers(app)

    from app.routes.auth_routes import auth_bp
    from app.routes.employee_routes import employee_bp
    from app.routes.category_routes import category_bp
    from app.routes.device_routes import device_bp
    from app.routes.dashboard_routes import dashboard_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(employee_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(device_bp)
    app.register_blueprint(dashboard_bp)

    @app.route('/api/health')
    def health():
        return {'success': True, 'message': 'ok'}

    return app
