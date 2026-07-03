from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.services.supabase_service import init_supabase
from app.utils.helpers import error_response

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable Cross-Origin Resource Sharing (CORS)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Validate configurations
    Config.validate()
    
    # Init Supabase
    init_supabase()
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.donor import donor_bp
    from app.routes.search import search_bp
    from app.routes.request import request_bp
    from app.routes.admin import admin_bp
    
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(donor_bp, url_prefix="/api/donors")
    app.register_blueprint(search_bp, url_prefix="/api/search")
    app.register_blueprint(request_bp, url_prefix="/api/requests")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    
    @app.route("/", methods=["GET"])
    def index():
        return {
            "message": "Welcome to the Blood Donor Management System API",
            "documentation": "Visit /health for system status, or use the /api/ prefix to access modules.",
            "modules": {
                "auth": "/api/auth",
                "donors": "/api/donors",
                "search": "/api/search",
                "requests": "/api/requests",
                "admin": "/api/admin"
            }
        }, 200

    @app.route("/health", methods=["GET"])
    def health_check():
        from app.services.supabase_service import get_supabase
        supabase_ok = get_supabase() is not None
        return {
            "status": "healthy",
            "supabase_connected": supabase_ok
        }, 200

    # Custom Error Handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return error_response("Resource not found.", code=404)

    @app.errorhandler(500)
    def internal_server_error(error):
        return error_response("Internal server error.", code=500)
        
    return app
