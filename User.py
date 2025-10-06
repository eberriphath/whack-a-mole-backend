from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, unset_jwt_cookies
from datetime import timedelta

app = Flask(__name__)
CORS(app)


app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql+psycopg2://postgres.sggwzzmuagyrpxhdljid:JFU5ZfOEbimX5VbP@aws-1-eu-north-1.pooler.supabase.com:5432/postgres"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "super-secret-key" 


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())


with app.app_context():
    db.create_all()


@app.route("/", methods=["GET"])
def home():
    return "<h2> Flask connected to Supabase with Register/Login/Logout</h2>"


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

    access_token = create_access_token(
        identity={"id": member.id, "name": member.name},
        expires_delta=timedelta(hours=1)
    )

    return jsonify({"message": "Login successful", "token": access_token, "name": member.name}), 200


@app.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    response = jsonify({"message": "Logout successful"})
    unset_jwt_cookies(response)
    return response, 200

# ----------------------------------------------

if __name__ == "__main__":
    app.run(debug=True, port=5640)
