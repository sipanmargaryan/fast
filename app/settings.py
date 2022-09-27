import os

from dotenv import load_dotenv

load_dotenv()

ENV = os.getenv("ENV", "dev")
HASURA_URL = os.getenv("HASURA_URL", "")
HASURA_TOKEN = os.getenv("HASURA_TOKEN", "")