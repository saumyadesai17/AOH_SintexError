from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import google.generativeai as palm
from dotenv import load_dotenv
import os
import pandas as pd
import json
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from keras.models import load_model
import PyPDF2

nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)

model = load_model('trained_model.h5') 
with open('carrier_enhancement.json', 'r') as file:
    data = json.load(file)

df = pd.DataFrame(data)

stop_words = set(stopwords.words('english'))
vectorizer = TfidfVectorizer(stop_words=list(stop_words)) 

df['resume_text'] = df['projects'].apply(lambda x: ' '.join([p['description'] for p in x]))

tfidf_matrix = vectorizer.fit_transform(df['resume_text'])

def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text

def suggest_careers(user_resume_text):
    user_resume_vector = vectorizer.transform([user_resume_text])

    cosine_similarities = cosine_similarity(user_resume_vector, tfidf_matrix)

    top_career_indices = cosine_similarities.argsort()[0][-3:][::-1]
    top_careers = df.loc[top_career_indices, 'career']

    return list(set(top_careers))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_resume():
    if request.method == 'POST':
        resume = request.files['resume']
        if resume.filename.endswith('.pdf'):
            filename = secure_filename(resume.filename)
            resume_text = extract_text_from_pdf(resume)
            suggestions = suggest_careers(resume_text)
            return redirect(url_for('result', suggestions=suggestions))
        else:
            return "Please upload a PDF file."

@app.route('/result')
def result():
    suggestions = request.args.get('suggestions').split(',')
    domains = []
    for career in suggestions:
        response = palm.chat(messages=career+"suggest two more domains similar to the one earlier mentioned that have even better Future Scope and how could i switch into that domain when i have skills for the domain that i have mentioned earlier")
        domains.append(response.last)
    return render_template('result.html', suggestions=suggestions, domains=domains)

if __name__ == '__main__':
    load_dotenv()
    palm_api_key = os.getenv('PALM_API_KEY')
    palm.configure(api_key=palm_api_key)
    app.run(debug=True)
