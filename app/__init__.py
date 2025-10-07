from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, unset_jwt_cookies
from flask_cors import CORS
from .config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    from .models import Member

    @app.route("/")
    def home():
        return "<h2>Flask connected to Supabase with Register/Login/Logout</h2>"

    @app.route("/register", methods=["POST"])
    def register():
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        if not name or not email or not password:
            return jsonify({"error": "All fields are required"}), 400

        exists = Member.query.filter_by(email=email).first()
        if exists:
            return jsonify({"error": "Email already registered"}), 400

        hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")
        new_member = Member(name=name, email=email, password=hashed_pw)
        db.session.add(new_member)
        db.session.commit()

        return jsonify({"message": "Registration successful!", "member": {"id": new_member.id, "name": new_member.name}}), 201

    @app.route("/login", methods=["POST"])
    def login():
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Email and password required"}), 400

        member = Member.query.filter_by(email=email).first()
        if not member or not bcrypt.check_password_hash(member.password, password):
            return jsonify({"error": "Invalid email or password"}), 401

        access_token = create_access_token(identity={"id": member.id, "name": member.name})
        return jsonify({"message": "Login successful", "token": access_token, "name": member.name}), 200

    @app.route("/logout", methods=["POST"])
    @jwt_required()
    def logout():
        response = jsonify({"message": "Logout successful"})
        unset_jwt_cookies(response)
        return response, 200

    with app.app_context():
        db.create_all()

    return app
