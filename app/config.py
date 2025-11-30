import os
from dotenv import load_dotenv
load_dotenv()

token_capacity = int(os.getenv("TOKEN_CAPACITY", 100))
time_interval = int(os.getenv("TIME_INTERVAL", 60))

redis_host = os.getenv("REDIS_HOST")
redis_port = int(os.getenv("REDIS_PORT"))
redis_password = os.getenv("REDIS_PASSWORD")

app_base_url = os.getenv("APP_BASE_URL")