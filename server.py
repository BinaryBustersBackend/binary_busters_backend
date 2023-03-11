from flask import Flask, request
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
    # print(len(behavioural_questions))
    return "Hello, Flask!"

#code questions bank
code_list = []

#list of behavoural_questions
behavioural_questions = ["Tell me about a time when you were not able to meet a time commitment. What prevented you from meeting it? What was the outcome and what did you learn from it?",
                         "Describe a long-term project that you managed. How did you keep everything moving along in a timely manner?",
                         "Give me an example of a time when you set a goal and were able to meet or achieve it",
                         "Tell me about a time you had to quickly adjust your work priorities to meet changing demands.",
                         "Give me an example of a time you faced a conflict while working on a team. How did you handle that?"
                         ]

OPENAI_PROMPT = "I will be giving you workplace situation questions and I want you to evaluate my response. At the start of the sentence provide me a 1 or 0. 1 as in if my response to the situation was good and 0 if my response to the satiation is bad. This is the first question. Situation: "


def random_behavioural_questions() -> int:
      # ID(index) of the the random question and it's content
      return random.randint(0, len(behavioural_questions) - 1)


def openAI_response(user_response, question):
      #system's instruction to OpenAI
      system_instruction = OPENAI_PROMPT + question
      
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

      #retun info as dict
      return {"response_quality": response_quality, "response_content": response_content}
    

@app.route('/getQuestion')
def send_question():
      #sending the random question from the question back to the frontend
      current_question_ID = random_behavioural_questions()
      return {
            "questionId": current_question_ID,
            "question": behavioural_questions[current_question_ID]
            }

@app.route("/getOpenAIResponse", methods=["POST"], strict_slashes=False)
def receive_user_behavioural_response():
      #questionID on display on the frontend
      questionID = request.json["questionId"]
      #getting the user response from the prompt
      userResponse = request.json["userResponse"]
      #finding the question in our question back that matches the displayed question
      question = behavioural_questions[questionID]
      return openAI_response(userResponse, question)


def read_files():
    for i in range(1, 11):
        with open(str(i) + ".txt", "r") as e:
            code_list.append(e.read())




if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=False)
