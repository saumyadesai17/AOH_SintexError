from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
import textwrap
from IPython.display import Markdown, display
import markdown2

app = Flask(__name__)


# Load environment variables
load_dotenv()
def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

# Initialize LangChain model
google_api_key = os.getenv('GOOGLE_API_KEY')
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=google_api_key)

# Helper function to format text as Markdown
def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/code_editor', methods=['GET', 'POST'])
def code_editor():
    if request.method == 'POST':
        # Get the user's code and question from the form
        user_code = request.form.get('code')
        question = request.form.get('question')
        
        # Evaluate the user's code and generate the solution
        if user_code:
            ai_solution = evaluate_user_code(user_code, question)
            return render_template('question.html', question=question, ai_solution=ai_solution)
        else:
            # Handle the case when user_code is empty
            return render_template('question.html', question=question, ai_solution="No solution generated")

  

# Helper function to format text as Markdown
def to_markdown(text):
    return Markdown(text)

@app.route('/generate_question', methods=['POST'])
def generate_question():
    # Get the selected DSA topic and difficulty level from the form
    topic = request.form.get('topic')
    difficulty_level = request.form.get('level')
    # Generate a DSA question based on the selected topic and difficulty level
    question = generate_dsa_question(topic, difficulty_level)
    # Render the question page with the generated question
    solution=generate_dsa_questions_solution(question)
    content=markdown2.markdown(question)
    return render_template('question.html', question=content)



def generate_dsa_question(topic, difficulty_level):
    prompt = f"Generate a DSA coding question on {topic} for {difficulty_level} level."
    result = llm.invoke(prompt)
    return result.content

def evaluate_user_code(user_code, question):
    prompt = f"Evaluate the following code for this question {question}and tell if it is correct or not and test it for 3 extreme use cases and if the code is not correct please give the corrected code and explain the logic behind it and Tell the time complexity of both the codes:\n\n{user_code}\n\n"
    result = llm.invoke(prompt)
    return markdown2.markdown(result.content)

def generate_dsa_questions_solution(question):
    prompt = f"Generate only correct Code for this question:{question},in this language only C++"
    result = llm.invoke(prompt)
    return markdown2.markdown(result.content)



    

if __name__ == '__main__':
    app.run(debug=True,port=5004)
