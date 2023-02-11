from envparse import Env

env = Env()
REAL_DATABASE_URL = env.str(
    "REAL_DATABASE_URL",
    default="postgresql+asyncpg://postgres:1234@0.0.0.0:5432/postgres"
) # connect string for the database