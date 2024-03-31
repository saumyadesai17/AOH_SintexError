from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from langchain_google_genai import ChatGoogleGenerativeAI
import markdown2
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# Set up language model
google_api_key = os.getenv('GOOGLE_API_KEY')
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=google_api_key)

# Load recommender model data
df = pd.read_json('Recommender_model_dataset.json')

# Preprocess data
nltk.download('punkt')
nltk.download('stopwords')
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

# Set up TF-IDF vectorizer
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df['Combined_Text'])

# Home route to render the HTML form
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', message='No file part')
        
        file = request.files['file']
        
        if file.filename == '':
            return render_template('index.html', message='No selected file')

        if file:
            client_resume = preprocess_binary(file)
            client_resume_vector = vectorizer.transform([client_resume])
            cosine_similarities = cosine_similarity(client_resume_vector, tfidf_matrix)

            top_n_projects_indices = cosine_similarities.argsort()[0][-3:][::-1]
            recommended_projects = df.loc[top_n_projects_indices, ['Experience', 'Skills', 'Domain']]

            project_details = []
            for _, project in recommended_projects.iterrows():
                project_info = {
                    'Experience': project['Experience'],
                    'Skills': project['Skills'],
                    'Domain': project['Domain']
                }
                chatbot_response = generate_approach(project_info)
                # Convert the chatbot response to Markdown format
                markdown_response = markdown2.markdown(chatbot_response)
                project_details.append((project_info, markdown_response))
            
            return render_template('recommend.html', project_details=project_details)

    return render_template('index.html')

def preprocess_binary(file):
    try:
        # Read the binary content of the file
        file_contents = file.read()
        
        # Decode the binary content using UTF-8
        decoded_content = file_contents.decode('utf-8')
    except UnicodeDecodeError:
        # If decoding as UTF-8 fails, try decoding using a different encoding
        decoded_content = file_contents.decode('latin-1')  # or 'ISO-8859-1'
    
    # Perform any necessary preprocessing on the decoded content
    # For example, tokenization, removing stop words, etc.
    # preprocessed_content = preprocess_text(decoded_content)
    
    # Return the preprocessed content
    return decoded_content

# Function to generate approach using language model
def generate_approach(project_info):
    prompt = f"I want you to suggest me building a Specific projects based on this info:\"{project_info}\" and also give me Approach on how to build that project specifically and how it will benefit in boosting my resume."
    result = llm.invoke(prompt)
    return result.content

if __name__ == '__main__':
    app.run(debug=True,port=5002)
