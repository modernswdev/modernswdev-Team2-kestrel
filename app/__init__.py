from flask import Flask, render_template, send_from_directory

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route("/sw.js")
    def service_worker():
        return send_from_directory(app.static_folder, "sw.js",
                                   mimetype="application/javascript")

    return app