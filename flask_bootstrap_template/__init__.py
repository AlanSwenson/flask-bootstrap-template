import os
import click

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin.contrib.sqla import ModelView
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, logout_user, login_user, login_required
from flask_admin import Admin, AdminIndexView, expose, helpers
from flask_assets import Environment, Bundle


from flask_bootstrap_template.config import DevelopmentConfig

# db = SQLAlchemy()
# migrate = Migrate()
# bcrypt = Bcrypt()
# admin = Admin()
# login = LoginManager()
assets = Environment()


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__, static_url_path="/static")
    app.config.from_object(config_class)

    with app.app_context():
        import flask_bootstrap_template.models as models

        initialize_extensions(app)

        bundle_assets(app)
        # add_admin_views()

    @app.route("/", methods=["POST", "GET"])
    def index():

        return render_template("index.html", title="Flask Bootstrap Template")

    @app.cli.command("create-user")
    @click.argument("email")
    def create_user(email):

        pw = input("Password: ")
        user = models.User(email=email, password=pw)
        db.session.add(user)
        db.session.commit()
        print("User Created")

    return app


def initialize_extensions(app):
    # db.init_app(app)
    # for admin backend
    # admin.init_app(app, index_view=models.RestaurantAdminIndexView())
    # migrate.init_app(app, db)
    # bcrypt.init_app(app)
    # login.init_app(app)
    assets.init_app(app)


# def add_admin_views():
#     admin.add_view(models.MyModelView(models.MenuItem, db.session))


def bundle_assets(app):
    assets.url = app.static_url_path
    js = Bundle("js/custom.js", output="gen/packed.js",)
    css = Bundle("css/custom.css", output="gen/packed.css",)
    less = Bundle(
        "css/custom.less", filters="less,cssmin", output="gen/packed_less.css"
    )

    assets.register("js_all", js)
    assets.register("less_all", less)
    assets.register("css_all", css)
