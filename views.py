from flask import render_template_string, render_template, Flask, request, jsonify
from flask_security import current_user, SQLAlchemySessionUserDatastore
from flask_security.decorators import auth_required, roles_required
from flask_security.utils import hash_password


def create_view(app : Flask, user_datastore : SQLAlchemySessionUserDatastore, db ):

    # homepage

    @app.route('/')
    def home():
        return render_template_string(
            """
                <h1> This is homepage </h1>
                <div><a href="/login"> login </a></div>
                <a href="/profile"> Profile page </a>
            """
        )
    
    # profile 
    @app.route('/profile')
    @auth_required('session', 'token')
    def profile():
        return render_template_string(
            """
                <h1> This is profile page </h1>
                <p> Welcome, {{current_user.email}}
                <p> Role : {{current_user.roles[0].description}}</p>
                <a href="/logout">logout</a>

            """
        )
        
    # Register
    @app.route('/register', methods=['POST'])
    def register():
        data = request.get_json()
        
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')
        
        if not email or not password or not role:
            return jsonify({'message': 'email, password and role are required'}), 403
        if user_datastore.find_user(email = email):
            return jsonify({'message' : 'User already exists'}), 400
        if role == 'inst':
            user_datastore.create_user(email=email, password=hash_password(password), roles=['inst'], active = False )
            db.session.commit()
            return jsonify({'message': 'Instructor registered successfully, waiting for admin approval'}), 201
        elif role == 'stud':
            try:
                user_datastore.create_user(email=email, password=hash_password(password), roles=['stud'], active = True )
                db.session.commit()
            except:
                return jsonify({'message': 'Error in registering student'}), 400
            return jsonify({'message': 'Student registered successfully'}), 201
        return jsonify({'message' : 'invalid role'}), 400
        
    
    @app.route('/inst-dashboard')
    @roles_required('inst')
    def inst_dashboard():
        return render_template_string(
            """
                <h1> Instructor profile </h1>
                <p> it should only be visible to instructor</p>
            """
        )
    
    @app.route('/stud-dashboard')
    @roles_required('stud')
    def stud_dashboard():
        return render_template_string(
            """
                <h1> Student profile </h1>
                <p> it should only be visible to student</p>
            """
        )