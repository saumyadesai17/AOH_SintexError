import streamlit as st
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

palm_api_key = os.getenv('PALM_API_KEY')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'gen-lang-client-0318117254-964dda6da97b.json'

nltk.download('punkt')
nltk.download('stopwords')

model = load_model('trained_model.h5') 
with open('carrier_enhancement.json', 'r') as file:
    data = json.load(file)

df = pd.DataFrame(data)

stop_words = set(stopwords.words('english'))
vectorizer = TfidfVectorizer(stop_words=list(stop_words)) 

df['resume_text'] = df['projects'].apply(lambda x: ' '.join([p['description'] for p in x]))

tfidf_matrix = vectorizer.fit_transform(df['resume_text'])

def extract_text_from_pdf(uploaded_file):
    text = ""
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
    return text


def suggest_careers(user_resume_text):
    user_resume_vector = vectorizer.transform([user_resume_text])

    cosine_similarities = cosine_similarity(user_resume_vector, tfidf_matrix)

    top_career_indices = cosine_similarities.argsort()[0][-3:][::-1]
    top_careers = df.loc[top_career_indices, 'career']

    return list(set(top_careers))

def main():
    st.title("Resume Analyzer")

    uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

    if uploaded_file is not None:
        resume_text = extract_text_from_pdf(uploaded_file)
        suggestions = suggest_careers(resume_text)
        st.write("Suggested Careers:")
        for i, career in enumerate(suggestions, start=1):
            st.write(f"{i}) {career}")
        
        st.write("Suggested Domains:")
        for career in suggestions:
            response = palm.chat(messages=career+"suggest two more domains similar to the one earlier mentioned that have even better Future Scope and how could i switch into that domain when i have skills for the domain that i have mentioned earlier")
            st.write(response.last)

if __name__ == "__main__":
    main()
