from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")

assert DATABASE_URL, "DATABASE_URL not configured in .env (follow the .env.example)"
assert SECRET_KEY, "SECRET_KEY not configured in .env (follow the .env.example)"