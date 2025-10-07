from datetime import timedelta

class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres.sggwzzmuagyrpxhdljid:JFU5ZfOEbimX5VbP@aws-1-eu-north-1.pooler.supabase.com:5432/postgres"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "super-secret-key"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
