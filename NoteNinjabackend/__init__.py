from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from sqlalchemy.engine import Engine
from sqlalchemy import event
from flask_login import LoginManager


db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'kjdnfvpiubfpiv'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Document

    with app.app_context(): 
        create_database()
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.go'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database():
    if not path.exists('../var/NoteNinjabackend-instance/' + DB_NAME):
        db.create_all()
        print('Created Database')

@event.listens_for(Engine, "connect") #sqlite for some reason does NOT support foreign keys by default. This makes it so that foreign keys are enabled
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()