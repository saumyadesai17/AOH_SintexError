from flask import Flask, render_template, request, make_response
from flask import redirect, url_for,flash

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import InputRequired, URL
from bs4 import BeautifulSoup
import requests
import textwrap
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
import markdown2
import pdfkit

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

google_api_key = os.getenv('GOOGLE_API_KEY')
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=google_api_key)

class JobForm(FlaskForm):
    input_level = SelectField('Input Level', choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('hard', 'Hard')], validators=[InputRequired()])
    job_link = StringField('Job Link', validators=[InputRequired(), URL()])
    submit = SubmitField('Generate Roadmap')

def generate_pdf_from_html(html_content):
    try:
        # Set the path to wkhtmltopdf executable
        config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
        pdf = pdfkit.from_string(html_content, 'MyPDF.pdf', configuration=config)
        return pdf
    except Exception as e:
        # Log the error or handle it as needed
        print(f"Error generating PDF: {e}")
        return None

def scrape_job_details(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        div_element = soup.find('div', class_='internship_details')

        if div_element:
            job_title = soup.find('div', class_='heading_4_5 profile').text.strip()
            company_name = soup.find('div', class_='heading_6 company_name').text.strip()
            experience = soup.find('div', class_='job-experience-item').text.strip()
            skills = [tag.text for tag in soup.find_all('span', class_='round_tabs')]
            key_responsibilities = soup.find('div', class_='text-container').text.strip()
            company_description = soup.find('div', class_='about_company_text_container').text.strip()
        else:
            return "Job details not found on the page."
    except requests.exceptions.RequestException as e:
        return f"Failed to retrieve the web page: {e}"

    prompt = f"You have to create a complete in detail roadmap on how to prepare for this job role: {job_title}, for Company: {company_name}, which requires Experience of: 3 {experience}, SKills: {skills}, Key Responsibilites/Requirements: {key_responsibilities}, Company Description: {company_description} and be more specific and try to give more descriptive answer and elaborate each point in detail as much as possible"
    result = llm.invoke(prompt)
    return result.content

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    roadmap_html = request.form.get('roadmap_html')

    # Generate PDF from HTML content
    pdf = generate_pdf_from_html(roadmap_html)

    if pdf:
        # Create response with PDF data
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=roadmap.pdf'
        return response
    else:
        # Handle case where PDF generation failed
        flash("Failed to generate PDF. Please try again later.", "error")
        return redirect(url_for('index'))

    

@app.route('/', methods=['GET', 'POST'])
def index():
    form = JobForm()
    roadmap = None
    if form.validate_on_submit():
        job_link = form.job_link.data
        roadmap = markdown2.markdown(scrape_job_details(job_link))
        return render_template('result.html', roadmap=roadmap)
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run( debug=True,port=5011)
