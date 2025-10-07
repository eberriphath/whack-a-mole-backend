# Whack-a-Mole Backend

This repository contains the backend for the Whack-a-Mole game, including:

1. **User Authentication App** (Flask, PostgreSQL via Supabase)
   - Features: Register, Login, Logout
   - Modular structure using Flask factory (`app/__init__.py`)
   - Runs on **port 5640**

2. **Score Submission App** (Flask, PostgreSQL via Supabase)
   - Features: Submit scores for players
   - Single-file Flask app (`Score.py`)
   - Runs on **port 5540**

---

## Project Structure

whack-a-mole-backend/
├─ app/
│ ├─ init.py # Flask factory, routes for auth
│ ├─ config.py # Config for database and JWT
│ └─ models.py # Database models (Member)
├─ requirements.txt
├─ run.py # Entry point for user/auth app
└─ Score.py # Entry point for score submission


---

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd whack-a-mole-backend


### 2. Create a virtual environment
python3 -m venv venv
source venv/bin/activate   # Linux / Mac
# .\venv\Scripts\activate  # Windows PowerShell

### 3. Install dependencies
pip install -r requirements.txt
