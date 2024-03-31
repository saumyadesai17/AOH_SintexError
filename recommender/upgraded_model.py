import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import google.generativeai as palm
from dotenv import load_dotenv
import os

nltk.download('punkt')
nltk.download('stopwords')

df = pd.read_json('Recommender_model_dataset.json')

stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    if isinstance(text, str):
        words = word_tokenize(text)
        clean_words = [word.lower() for word in words if word.lower() not in stop_words]
        return ' '.join(clean_words)
    else:
        return ''

df['Experience'] = df['Projects'].apply(lambda x: preprocess_text(x.get('Experience', '')))
df['Skills'] = df['Skills'].apply(preprocess_text)
df['Domain'] = df['Domain'].apply(preprocess_text)

df['Combined_Text'] = df['Experience'] + ' ' + df['Skills'] + ' ' + df['Domain']

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df['Combined_Text'])

client_resume = "Marketing Manager: Summary: Results-driven marketing manager with over 8 years of experience in developing and executing marketing strategies to drive brand awareness and revenue growth. Skilled in leading cross-functional teams and leveraging data analytics for data-driven decision-making. Proven success in digital marketing, content strategy, and brand management. Skills: - Strategic marketing planning - Digital marketing and social media - Content strategy and creation - Brand development and management - Market research and analysis - Team leadership and collaboration - Budget management Experience: Marketing Manager at ABC Marketing Group, 2017-Present - Developed and executed marketing campaigns that resulted in a 20% increase in brand recognition and a 15% growth in online sales. - Led a team of marketers in creating engaging content for various digital channels, resulting in a 30% increase in website traffic. - Utilized data analytics to monitor and optimize marketing performance, achieving a 10% improvement in conversion rates. Senior Marketing Specialist at XYZ Company, 2014-2017 - Managed the company's social media presence, growing the follower base by 25% and increasing engagement by 20%. - Oversaw the development and implementation of a content marketing strategy that boosted organic website traffic by 40%. - Collaborated with sales teams to align marketing efforts with sales goals, leading to a 15% increase in lead generation. Education: Master of Business Administration, Marketing Concentration, University of Marketing, 2014 - Relevant coursework: Marketing Strategy, Consumer Behavior, MarketResearch"

client_resume = preprocess_text(client_resume)

client_resume_vector = vectorizer.transform([client_resume])

cosine_similarities = cosine_similarity(client_resume_vector, tfidf_matrix)

top_n_projects_indices = cosine_similarities.argsort()[0][-3:][::-1]

recommended_projects = df.loc[top_n_projects_indices, ['Experience', 'Skills', 'Domain']]

def generate_chatbot_response(project_info):

    load_dotenv()
    palm_api_key = os.getenv('PALM_API_KEY')
    palm.configure(api_key=palm_api_key)
    
    response = palm.chat(messages=project_info['Experience'])
    return response.last

for i, (_, project) in enumerate(recommended_projects.iterrows(), start=1):
    project_info = {
        'Experience': project['Experience'],
        'Skills': project['Skills'],
        'Domain': project['Domain']
    }
    chatbot_response = generate_chatbot_response(project_info)
    print(f"Project {i} Details:")
    print(f"Project: {project_info['Experience']}")
    print(f"Skills Required: {project_info['Skills']}")
    print(f"Domain: {project_info['Domain']}")
    print("Chatbot Response:")
    print(chatbot_response)
    print()  
