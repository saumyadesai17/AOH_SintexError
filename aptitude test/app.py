import json
import random
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Load the dataset of questions
with open('quiz_data_set.json', 'r') as file:
    all_questions = json.load(file)['result']['quizzes'][0]['questions']

# Select 10 random question IDs
def generate_random_questions(all_questions, k):
    random_question_ids = random.sample(range(len(all_questions)), k)
    selected_questions = [all_questions[i] for i in random_question_ids]
    return selected_questions

@app.route('/')
def index():
    return render_template('index.html', selected_questions=generate_random_questions(all_questions, 20))

@app.route('/get_quiz_data')
def get_quiz_data():
    return jsonify({'result': {'quizzes': [{'questions': generate_random_questions(all_questions, 20)}]}})

if __name__ == '__main__':
    app.run(debug=True, port=5007)
