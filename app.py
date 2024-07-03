import resources
from flask import Flask
import views
from extensions import db, security
from create_initial_data import create_data

def create_app():
    app = Flask(__name__)
    
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = "THIS-IS-SOMETHING"
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
    app.config['SECURITY_PASSWORD_SALT'] = "SALT"
    app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = 'Authentication-Token'
    
    
    db.init_app(app)
    
    with app.app_context():
        from models import User, Role
        from flask_security.datastore import SQLAlchemyUserDatastore
        
        user_datastore = SQLAlchemyUserDatastore(db, User, Role)
        
        security.init_app(app, user_datastore)
        
        db.create_all()
        
        create_data(user_datastore)
    
    # disable CSRF protection, form WTForms as well as flask securtiy
    app.config["WTF_CSRF_CHECK_DEFAULT"] = False
    app.config["SECURITY_CSRF_PROTECT_MECHANISMS"] = []
    app.config["SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS"] = True
    
    # Setup the view
    views.create_view(app, user_datastore, db)
    
    # Setup the api
    resources.api.init_app(app)
    
    return app



if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
