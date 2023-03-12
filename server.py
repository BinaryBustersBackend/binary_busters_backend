from flask import Flask, request
from dotenv import load_dotenv
import os
import openai
import random
import itertools

# Load .env that contains API key
load_dotenv(".venv/.env")

# Set the API key
openai.api_key = os.getenv('OPEN_API_KEY')


app = Flask(__name__)

@app.route("/")
def home():
    create_code_dict()
    print(code_dict)
    # print(len(behavioural_questions))
    return "Hello, we are Binary Busters!"

#code questions bank
code_dict = {}

#dict of behavoural_questions
behavioural_questions = {
    1: "Tell me about a time when you were not able to meet a time commitment. What prevented you from meeting it? What was the outcome and what did you learn from it?",
    2: "Describe a long-term project that you managed. How did you keep everything moving along in a timely manner?",
    3: "Give me an example of a time when you set a goal and were able to meet or achieve it.",
    4: "Tell me about a time you had to quickly adjust your work priorities to meet changing demands.",
    5: "Tell me about the toughest decision you've had to make in the past six months",
    6: "What did you do when you needed to motivate a group of individuals?", 
    7: "Tell me about a time you stepped up into a leadership role.",
    8: "Describe a situation when you negotiated with others in your organization to reach agreement.",
    9: "We've all had to work with people that don't like us. How do you deal with someone that doesn't like you?",
    10: "We all make mistakes we wish we could take back. Tell me about a time you wish you would handled a situation differently with a colleague.",
    11: "Tell me about a time when you received negative feedback from your manager. How did you respond?",
    12: "Tell me about a time when you missed an obvious solution to a problem.",
    13: "Tell me about a time when you faced a problem that had multiple possible solutions.",
    14: "Tell me about a time when you came up with a new approach to a problem.", 
    15: "Describe a situation in which you found a creative way to overcome an obstacle.",
    16: "How have you leveraged data to develop a strategy?", 
    17: "Tell me about a time when you were 75 percent through a project, and you had to pivot strategy", 
    18: "Tell me about a time when you had to choose between technologies for a project", 
    19: "Tell me about a time you had to deal with ambiguity", 
    20: "Describe a time when you sacrificed short term goals for long term success",
    21: "Provide an example of when you personally demonstrate ownership.", 
    22: "What's your greatest strength?", 
    23: "What's your greatest weakness?", 
    24: "Tell me about a time you recovered from a difficult situation.", 
    25: "How do you handle multiple tasks at a limited time?", 
    26: "Describe a time when you had to work under pressure. How did you handle the stress, and what was the outcome?", 
    27: "Tell me about a time when you had to make a decision with limited information. What factors did you consider, and what was the outcome?", 
    28: "Describe a time when you had to work with a team member who was not pulling their weight. How did you handle the situation, and what was the outcome?",
    29: "Describe a time when you had to work with a difficult manager. How did you handle the situation, and what was the outcome?",
    30: "Tell me about a time when you had to overcome a communication barrier. What steps did you take to address the barrier, and what was the outcome?",
    31: "Describe a time when you had to work with a team to develop a new process. What steps did you take, and what was the outcome?",
    32: "Tell me about a time when you had to work with a team to improve the efficiency of a process. What steps did you take, and what was the outcome?"
}

OPENAI_PROMPT = "I will be giving you workplace situation questions and I want you to evaluate my response. At the start of the sentence provide me a 1 or 0. 1 as in if my response to the situation was good and 0 if my response to the situation is bad. This is the first question. Situation: "


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
      response_content = response['choices'][0]['message']['content'][2::]

      #retun info as dict
      return {"response_quality": response_quality, "response_content": response_content}
    

@app.route('/getQuestion', methods=["GET"])
def send_question():
      #sending the random question from the question back to the frontend
      limit = int(request.args.get('limit', len(behavioural_questions)))
      
      questions = dict(itertools.islice(behavioural_questions.items(), limit))

      return questions

    #   current_question_ID = random_behavioural_questions()

    #   return {
    #         "questionId": current_question_ID,
    #         "question": behavioural_questions[current_question_ID]
    #         }

@app.route("/getOpenAIResponse", methods=["POST", "GET"], strict_slashes=False)
def receive_user_behavioural_response():
      #questionID on display on the frontend
      questionID = request.json["questionId"]
      #getting the user response from the prompt
      userResponse = request.json["userResponse"]
      #finding the question in our question back that matches the displayed question
      question = behavioural_questions[questionID]
      return openAI_response(userResponse, question)

def create_code_dict():
    for i in range(1, 11):
        
        file_path = os.path.join("./python_buggy_code/" + str(i) + ".txt")
        with open(file_path, "r") as f:
            answer = f.readline().rstrip().split(',')  # Store first line as answer
            modify_answer = list(map(lambda x: int(x), answer))
            question = f.read() # Store second line as question
            code_dict[i] = [question, modify_answer] # Store question and answer in a list

@app.route('/getCodeQuestion', methods=["GET"])
def send_code_questions():
     create_code_dict()
     limit = int(request.args.get('limit', len(code_dict)))
     questions = dict(itertools.islice(code_dict.items(), limit))
     return questions