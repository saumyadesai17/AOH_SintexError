import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('punkt')
nltk.download('stopwords')


df = pd.read_json('project-recommendation-model\PY_data.json')


stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    if isinstance(text, str):

        words = word_tokenize(text)

        clean_words = [word.lower() for word in words if word.isalpha() and word.lower() not in stop_words]
        return ' '.join(clean_words)
    else:
        return ''


df['Experience'] = df['Projects'].apply(lambda x: preprocess_text(x.get('Experience', '')))


df['Skills'] = df['Skills'].apply(preprocess_text)
df['Domain'] = df['Domain'].apply(preprocess_text)


vectorizer = TfidfVectorizer()


tfidf_matrix = vectorizer.fit_transform(df['Experience'] + ' ' + df['Skills'] + ' ' + df['Domain'])

# This is sample resume content used for testing Replace it the clients resume according to the use case
client_resume = "Marketing Manager: Summary: Results-driven marketing manager with over 8 years of experience in developing and executing marketing strategies to drive brand awareness and revenue growth. Skilled in leading cross-functional teams and leveraging data analytics for data-driven decision-making. Proven success in digital marketing, content strategy, and brand management. Skills: - Strategic marketing planning - Digital marketing and social media - Content strategy and creation - Brand development and management - Market research and analysis - Team leadership and collaboration - Budget management Experience: Marketing Manager at ABC Marketing Group, 2017-Present - Developed and executed marketing campaigns that resulted in a 20% increase in brand recognition and a 15% growth in online sales. - Led a team of marketers in creating engaging content for various digital channels, resulting in a 30% increase in website traffic. - Utilized data analytics to monitor and optimize marketing performance, achieving a 10% improvement in conversion rates. Senior Marketing Specialist at XYZ Company, 2014-2017 - Managed the company's social media presence, growing the follower base by 25% and increasing engagement by 20%. - Oversaw the development and implementation of a content marketing strategy that boosted organic website traffic by 40%. - Collaborated with sales teams to align marketing efforts with sales goals, leading to a 15% increase in lead generation. Education: Master of Business Administration, Marketing Concentration, University of Marketing, 2014 - Relevant coursework: Marketing Strategy, Consumer Behavior,MarketResearch" 


client_resume = preprocess_text(client_resume)


client_resume_vector = vectorizer.transform([client_resume])


cosine_similarities = cosine_similarity(client_resume_vector, tfidf_matrix)


top_n_projects_indices = cosine_similarities.argsort()[0][::-1][:3]


recommended_projects = df.loc[top_n_projects_indices, ['Experience', 'Skills', 'Domain']]


pd.set_option('display.max_colwidth', None)


for index, row in recommended_projects.iterrows():
    print(f"Project: {row['Experience']}\nSkills Required: {row['Skills']}\nDomain: {row['Domain']}\n")


