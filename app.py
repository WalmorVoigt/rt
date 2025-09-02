from flask import Flask, render_template
from extensions import db

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://rt_user:rt_password@localhost/rt_blog"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        from models import User, Post
        db.create_all()

    import routes
    app.register_blueprint(routes.bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0")


