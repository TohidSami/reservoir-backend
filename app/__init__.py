from flask import Flask
def create_app():
    app=Flask(__name__)

    from app.routes.well_routes import well_bp
    from app.routes.prod_routes import prod_bp
    from app.routes.plot_routes import plot_bp

    app.register_blueprint(well_bp)
    app.register_blueprint(prod_bp)
    app.register_blueprint(plot_bp)

    return app