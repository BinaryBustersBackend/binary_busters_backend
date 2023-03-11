from flask import Flask
from dotenv import load_dotenv
import os
import openai
import random


# Load .env that contains API key
load_dotenv(".venv/.env")

# Set the API key
openai.api_key = os.getenv('OPEN_API_KEY')


app = Flask(__name__)

@app.route("/")
def home():
	return "Hello, Flask!"


if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=False)
    