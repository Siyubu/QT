from flask import Flask,Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS,cross_origin

import logging
DB_NAME = "qtexam.db"

app = Flask(__name__)
db = SQLAlchemy()
cors = CORS(app, resources={r"*": {"origins": "*"}})

logging.getLogger('flask_cors').level = logging.DEBUG


def create_app():
    app.config['SECRET_KEY'] = "this qt exam "
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
    CORS(app)
    db.init_app(app)

    from server.auth import auth
    from server.view import view
    app.register_blueprint(auth)
    app.register_blueprint(view)

#Assignee,TasksAssignee
    from server.model import User,Project,Task,TaskProject,Assignee,TasksAssignee
    from server import create_database
    create_database(app)
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

if __name__ =="__main__":
    app = create_app()
    app.run(debug = True)