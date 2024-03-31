
import pandas as pd
import json
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from keras.models import load_model

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

def suggest_careers(user_resume_text):
  
    user_resume_vector = vectorizer.transform([user_resume_text])

    cosine_similarities = cosine_similarity(user_resume_vector, tfidf_matrix)

    top_career_indices = cosine_similarities.argsort()[0][-3:][::-1]
    top_careers = df.loc[top_career_indices, 'career']


    percentages = cosine_similarities[0, top_career_indices] * 100

    return list(zip(top_careers, percentages))


user_resume_text = """Marketing Manager: Summary: Results-driven marketing manager with over 8 years of experience in developing and executing marketing strategies to drive brand awareness and revenue growth. Skilled in leading cross-functional teams and leveraging data analytics for data-driven decision-making. Proven success in digital marketing, content strategy, and brand management. Skills: - Strategic marketing planning - Digital marketing and social media - Content strategy and creation - Brand development and management - Market research and analysis - Team leadership and collaboration - Budget management Experience: Marketing Manager at ABC Marketing Group, 2017-Present - Developed and executed marketing campaigns that resulted in a 20% increase in brand recognition and a 15% growth in online sales. - Led a team of marketers in creating engaging content for various digital channels, resulting in a 30% increase in website traffic. - Utilized data analytics to monitor and optimize marketing performance, achieving a 10% improvement in conversion rates. Senior Marketing Specialist at XYZ Company, 2014-2017 - Managed the company's social media presence, growing the follower base by 25% and increasing engagement by 20%. - Oversaw the development and implementation of a content marketing strategy that boosted organic website traffic by 40%. - Collaborated with sales teams to align marketing efforts with sales goals, leading to a 15% increase in lead generation. Education: Master of Business Administration, Marketing Concentration, University of Marketing, 2014 - Relevant coursework: Marketing Strategy, Consumer Behavior,MarketResearch"""

suggestions = suggest_careers(user_resume_text)


for i, (career, percentage) in enumerate(suggestions, start=1):
    print(f"{i}) {career}: {percentage:.2f}%")
