from flask import Flask, render_template, send_from_directory
import os

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'pawlink.sqlite'),
    )

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route("/sw.js")
    def service_worker():
        return send_from_directory(app.static_folder, "sw.js",
                                   mimetype="application/javascript")
                                   
    if test_config is not None:
        app.config.from_mapping(test_config)
    
    os.makedirs(app.instance_path, exist_ok=True)

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    return app
