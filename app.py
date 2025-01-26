# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_migrate import Migrate
from flask_login import current_user, login_required
from flask_sqlalchemy import SQLAlchemy
from model import db, User, Invitation
from config import Config
from werkzeug.security import generate_password_hash, check_password_hash
import string
import random

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate = Migrate(app, db)
    @app.route('/')
    def home():
        return redirect(url_for('login'))


    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password_hash, password):
                # Here you would typically set up a session
                flash('Successfully logged in!', 'success')
                return render_template('dashboard.html')
            else:
                flash('Invalid username or password', 'error')

        return render_template('login.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            invitation_code = request.form.get('invitation_code')

            # Check if username already exists
            if User.query.filter_by(username=username).first():
                flash('Username already exists', 'error')
                return render_template('register.html')
            if User.query.filter_by(email=email).first():
                flash('Email already exists', 'error')
                return render_template('register.html')
            # Validate that both passwords match
            if password != confirm_password:
                flash('Passwords do not match', 'error')
                return render_template('register.html')

            check_invitation = Invitation.query.filter_by(invitation_code=invitation_code).first()
            if check_invitation is None:
                flash('Invitation code is invalid', 'error')
                return render_template('register.html')
            else:
                db.session.delete(check_invitation)
                db.session.commit()
            # Generate hashed password and create a new user
            password_hash = generate_password_hash(password)
            new_user = User(username=username, password_hash=password_hash,
                            email=email)
            try:
                db.session.add(new_user)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"Database error: {e}")
                flash('An error occurred while registering', 'error')
                return render_template('register.html')

            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))

        return render_template('register.html')

    @app.route('/dashboard')
    def dashboard():
        # Render the home page
        return render_template('dashboard.html')

    @app.route('/profile')
    def profile():
        return render_template('profile.html')


    @app.route('/generate-invitation-code', methods=['POST'])
    def generate_invitation_code():
        def generate_code():
            # Generate the random six-character alphanumeric code
            return ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        max_attempts = 1000
        for _ in range(max_attempts):
            code = generate_code()
            existing_code = Invitation.query.filter_by(invitation_code=code).first()
            if not existing_code:
                new_code = Invitation(invitation_code=code, created_user=current_user.id)
                db.session.add(new_code)
                db.session.commit()
                return jsonify({'invitation_code': code})
        return jsonify({'error': 'Could not generate an unique invitation code'}), 500  # Return JSON with the code

    @app.route('/my-invitation-codes', methods=['GET'])
    @login_required
    def my_invitation_codes():
        # Retrieve all invitation codes created by the current user
        codes = Invitation.query.filter_by(created_user=current_user.id).all()
        return jsonify({'codes': [code.code for code in codes]})

    @app.route('/friends')
    def friends():
        return render_template('friends.html')

    # test


    @app.route('/chat')
    def chat():
        return render_template('chat.html')


    @app.route('/notifications')
    def notifications():
        return render_template('notifications.html')

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)