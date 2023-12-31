from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TOKEN", "NONE")

WEBHOOK_HOST = "https://07b4-178-88-127-165.ngrok-free.app"
WEBHOOK_PATH = "/webhook/" + TOKEN
WEBHOOK_URL = WEBHOOK_HOST + WEBHOOK_PATH
WEBAPP_HOST = "localhost"
WEBAPP_PORT = 8000
