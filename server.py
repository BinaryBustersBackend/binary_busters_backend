from flask import Flask, request
from flask_cors import CORS
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
CORS(app)

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
    1: "Emily has been struggling with her workload lately. She's been working on a major project that has required a lot of her time and energy. She's been feeling stressed and anxious, and it's starting to affect her performance at work. How would you help her in this situation?",
    2: "Mark is a manager at a software development company. He notices that there is a lack of communication between the developers and the quality assurance (QA) team. This lack of communication is leading to delays and misunderstandings that are affecting the quality of the final product. How can Mark help increase communication between the two teams?",
    3: "Samantha is a team member at a busy marketing agency. She has noticed that there is a lot of negativity and complaining among her colleagues, which is affecting morale and productivity. What can she do to lighten the atmosphere?",
    4: "Karen is a team member at a startup company. She has noticed that one of her colleagues, Tom, often makes offensive jokes and comments that are disrespectful towards women and people of color. Karen finds Tom's behavior offensive and unprofessional, and she knows that other team members feel the same way. How can Karen address the issues she's been noticing?",
    5: "David is a team leader at a software development company. He has noticed that some of his team members have been struggling with stress and burnout due to tight deadlines and heavy workloads. David wants to show his team that he understands the pressure they are under and cares about their well-being. How should David show he's appreciative of their hard work?"
}

OPENAI_PROMPT = "I will be giving you workplace situation questions and I want you to evaluate my response. At the start of the sentence provide me a 1 or 0. 1 as in if my response to the situation was good and 0 if my response to the situation is bad. This is the first question. Situation: "


def random_behavioural_questions() -> int:
      # ID(index) of the the random question and it's content
      return random.randint(0, len(behavioural_questions) - 1)


def openAI_response(user_response, question):
      #system's instruction to OpenAI
      system_instruction = OPENAI_PROMPT + question
      
      #build message that is part of the request to OpenAI's API
      message = [
           {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_response}]
      
      #OpenAI's response
      response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=message)

      #response quality indicates if the user's response is good (0 or 1)
      response_quality = True if response['choices'][0]['message']['content'][0] == "1" else False

      #OpenAI's response in sentence
      response_content = response['choices'][0]['message']['content'][2:]

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