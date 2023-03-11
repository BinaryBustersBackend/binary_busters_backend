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


#list of behavoural_questions

behavioural_questions = []

OPENAI_PROMPT = "I will be giving you workplace situation questions and I want you to evaluate my response. At the start of the sentence provide me a 1 or 0. 1 as in if my response to the situation was good and 0 if my response to the satiation is bad. This is the first question. Situation: "
CURRENT_QUESTION = None

def random_behavioural_questions() -> str:
      return random.choice(behavioural_questions)

def get_user_response() -> str:
      #FIXME: figure out how to get user's response from frontend
      pass

def openAI_response():
      #system's instruction to OpenAI
      system_instruction = OPENAI_PROMPT + CURRENT_QUESTION

      #user's response to question
      user_response = get_user_response()
      
      #build message that is part of the request to OpenAI's API
      message = [{
            "role": "system", "content": system_instruction,
            "role": "user", "content": user_response}]
      
      #OpenAI's response
      response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=message)

      #response quality indicates if the user's response is good (0 or 1)
      response_quality = True if response['choices'][0]['message']['content'][0] == "1" else False

      #OpenAI's response in sentence
      response_content = response['choices'][0]['message']['content'][3::] #double check the slicing

      #retun info as tuple
      return response_quality, response_content
    

      
def controller():
      #control flow of the program
      pass

    

if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=False)
    

    
    