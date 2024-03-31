from flask import Flask, render_template, request
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)

# Load JSON data into DataFrame
df = pd.read_json('PY_data.json')

# Define preprocessing function
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    if isinstance(text, str):
        words = word_tokenize(text)
        clean_words = [word.lower() for word in words if word.isalpha() and word.lower() not in stop_words]
        return ' '.join(clean_words)
    else:
        return ''

# Apply preprocessing to relevant columns
df['Experience'] = df['Projects'].apply(lambda x: preprocess_text(x.get('Experience', '')))
df['Skills'] = df['Skills'].apply(preprocess_text)
df['Domain'] = df['Domain'].apply(preprocess_text)

# Vectorize text data
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df.apply(lambda x: x['Projects']['Experience'] + ' ' + x['Skills'] + ' ' + x['Domain'], axis=1))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    client_resume = request.form['resume']
    client_resume = preprocess_text(client_resume)
    client_resume_vector = vectorizer.transform([client_resume])
    cosine_similarities = cosine_similarity(client_resume_vector, tfidf_matrix)
    top_n_projects_indices = cosine_similarities.argsort()[0][::-1][:3]
    recommended_projects = df.loc[top_n_projects_indices, ['Projects', 'Skills', 'Domain']]
    
    # Extracting experiences from the recommended projects
    recommended_experience = [df.iloc[index]['Projects']['Experience'] for index in top_n_projects_indices]
    
    return render_template('recommend.html', recommended_projects=recommended_projects, recommended_experience=recommended_experience)

if __name__ == '__main__':
    app.run(debug=True,port=5002)
    
