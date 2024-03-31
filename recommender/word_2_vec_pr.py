import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity
import google.generativeai as palm
from dotenv import load_dotenv
import os

nltk.download('punkt')
nltk.download('stopwords')

# Load the dataset
df = pd.read_json('Recommender_model_dataset.json')

# Preprocess text data
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    if isinstance(text, str):
        words = word_tokenize(text)
        clean_words = [word.lower() for word in words if word.lower() not in stop_words]
        return clean_words
    else:
        return []

df['Experience'] = df['Projects'].apply(lambda x: preprocess_text(x.get('Experience', '')))
df['Skills'] = df['Skills'].apply(preprocess_text)
df['Domain'] = df['Domain'].apply(preprocess_text)

# Train Word2Vec model
all_words = df['Experience'].sum() + df['Skills'].sum() + df['Domain'].sum()
word2vec_model = Word2Vec(sentences=all_words, vector_size=100, window=5, min_count=1, workers=4)

# Function to convert text to Word2Vec embeddings
def text_to_embeddings(text):
    embeddings = []
    for word in text:
        if word in word2vec_model.wv:
            embeddings.append(word2vec_model.wv[word])
    return embeddings

df['Experience_Embeddings'] = df['Experience'].apply(text_to_embeddings)
df['Skills_Embeddings'] = df['Skills'].apply(text_to_embeddings)
df['Domain_Embeddings'] = df['Domain'].apply(text_to_embeddings)

# Define client resume and convert to Word2Vec embeddings
client_resume = """
Ravirajsingh Sodha https://www.linkedin.com/in/ravirajsingh-sodha-345b1a28a https://github.com/raviraj-441 ravirajsinghsodha441@gmail.com — +91-7666761944 — Mumbai, India Objective Motivated B.Tech student with a passion for data science and programming, seeking opportunities to apply and enhance skills in impactful projects. Education B.Tech Computer Science and Engineering (Data Science) Dwarkadas Jivanlal Sanghvi College of Engineering, Mumbai, India Expected Graduation: May 2026 Current CGPA: 8.83 MHT-CET (PCM): 96.77 Percentile HSC(12th Grade) A.A.V.Patel Junior College, Mumbai, India Board Percentage: 70% Skills SSC (10th Grade) SMTR.N.Sheth Vidyamandir, Mumbai, India Board Percentage: 85.20% • Programming: C, C++, Java, Python • WebTechnologies: HTML, CSS, JavaScript, Node.js • Tools: Canva, AutoCAD • Data Science: Machine Learning, Deep Learning, Data Analysis, Web Scraping, SQL, Open CV • NLP(Natural Language Processing), Cosine Similarity, TFIDF Vectorizer • Blockchain Technologies : Solidity, Smart Contracts, Consensus Algorithm, Golang, Cryptography, Data Structures Soft Skills Communication Projects Team Collaboration Problem Solving Time Management Adaptability Chatbot with Google Generative AI: Developed a chatbot using Google Generative AI API, implementing real-time chat functionality and natural language processing. Integrated an exit command for seamless termination, enhancing user interaction. GitHub: https://github.com/raviraj-441 Healthcare Predictive Modeling: Developed a machine learning model to predict the likelihood of diabetes based on patient data. Engineered relevant features, focusing on ’Glucose’, ’BMI’, and ’Age’ to enhance model performance. Utilized Random Forest and Gradient Boosting models, achieving a testing accuracy of 74.7%. GitHub: https://github.com/raviraj-441 Credit Card Fraud Detection: Implemented a machine learning model for detecting fraudulent activities in credit card transactions. Engineered features to improve model performance, including the creation of a new ’Hour’ feature representing the hour of the day for each transaction. Addressed class imbalance using the Synthetic Minority Over-sampling Technique (SMOTE) during model training. GitHub: https://github.com/raviraj-441 Stock Price Prediction with LSTM: Implemented a stock price prediction model using Long Short-Term Memory (LSTM) neural networks. The model was trained on historical stock data obtained from Yahoo Finance. Utilized evaluation metrics such as Mean Squared Error (MSE) and Mean Absolute Error (MAE) to assess model performance. GitHub: https://github.com/raviraj-44 Hackathons & Competitions DATAHACK2.0, S4DSDJSCECollege Community: Secured 5th rank among participants. Developed an innovative project for Automatic Project Recognition and Recommendation using machine learning techniques. Implemented natural language processing (NLP) and cosine similarity for accurate project recommendations. Secured 3rd Price at VCET Hackathon: Developed an innovative platform that connects students studying the same subjects, offering a virtual collaborative space. The platform provides features like shared study materials, virtual study rooms, and AI-powered study groups tailored to individual learning styles and preferences, fostering effective and engaging learning. WonBestDomain(ML)Prize at CODEISSANCE: Created a project on phishing site prediction in a 24-hour hackathon organized by Thadomal Sahani College of Engineering. Languages English (Proficient) Hobbies Marathi Hindi Gujarati (Native)
"""
client_resume_tokens = preprocess_text(client_resume)
client_resume_embeddings = text_to_embeddings(client_resume_tokens)

# Compare client resume embeddings with project embeddings using cosine similarity
def calculate_similarity(project_embeddings):
    similarity = 0
    count = 0
    for project_embedding in project_embeddings:
        for client_resume_embedding in client_resume_embeddings:
            similarity += cosine_similarity([client_resume_embedding], [project_embedding])[0][0]
            count += 1
    if count > 0:
        return similarity / count
    else:
        return 0

df['Similarity'] = df.apply(lambda row: calculate_similarity(row['Experience_Embeddings'] + row['Skills_Embeddings'] + row['Domain_Embeddings']), axis=1)

# Get top 3 recommended projects based on similarity
recommended_projects = df.nlargest(3, 'Similarity')

# Chatbot integration
load_dotenv()
palm_api_key = os.getenv('PALM_API_KEY')
palm.configure(api_key=palm_api_key)

print("Welcome to the Project Recommender!")

for i, (_, project) in enumerate(recommended_projects.iterrows(), start=1):
    project_info = {
        'Experience': ' '.join(project['Experience']),
        'Skills': ' '.join(project['Skills']),
        'Domain': ' '.join(project['Domain'])
    }
    chatbot_prompt = f"Generate specific projects and approaches for a project related to:\nExperience: {project_info['Experience']}\nSkills: {project_info['Skills']}\nDomain: {project_info['Domain']}\n"
    
    response = palm.chat(messages=chatbot_prompt)
    print(f"Assistant: {response.last}")
    print()

