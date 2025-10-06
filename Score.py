from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow React frontend to communicate

# Supabase Postgres connection string (replace with your credentials)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql+psycopg2://postgres.sggwzzmuagyrpxhdljid:JFU5ZfOEbimX5VbP@aws-1-eu-north-1.pooler.supabase.com:5432/postgres"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the Scores table
class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_name = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, nullable=False)

# Create the table in Supabase
with app.app_context():
    db.create_all()

# Root route for testing
@app.route("/", methods=["GET"])
def home():
    return "<h1>Flask connected to Supabase Postgres ✅</h1>"

# Route to submit all scores
@app.route("/submit-scores", methods=["POST"])
def submit_scores():
    data = request.json
    player_name = data.get("playerName")
    scores = data.get("scores")  # Expect an array

    if not player_name or not scores:
        return jsonify({"error": "playerName and scores array are required"}), 400

    try:
        for s in scores:
            db.session.add(Score(player_name=player_name, score=s))
        db.session.commit()
        return jsonify({"message": "All scores submitted successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5540)
