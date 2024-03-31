from flask import Flask, render_template, request, make_response
import json
import pdfkit
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


from io import BytesIO


app = Flask(__name__)

# Load JSON data
with open('interview_question_dataset.json', 'r') as file:
    questions_data = json.load(file)

# Homepage route
@app.route('/')
def index():
    return render_template('index.html', questions=None)

@app.route('/questions', methods=['POST'])
def get_questions():
    selected_profession = request.form['profession']
    selected_difficulty = request.form['difficulty']

    # Filter questions based on selected criteria
    filtered_questions = [question for question in questions_data if question['job_role'] == selected_profession and question['difficulty_level'] == selected_difficulty]

    return render_template('questions.html', questions=filtered_questions)

# Route to handle form submission and PDF download
# Route to handle PDF download
@app.route('/download_pdf', methods=['POST'])
def download_pdf():
    selected_questions = request.form.getlist('selected_questions')

    # Filter questions based on selected criteria
    filtered_questions = [question for question in questions_data if str(question.get('id', '')) in selected_questions]

    # Generate PDF
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(100, 750, "Filtered Questions")
    y_position = 730
    for idx, question in enumerate(filtered_questions, start=1):
        y_position -= 20
        c.drawString(100, y_position, f"{idx}. {question['question']}")
        y_position -= 15
        c.drawString(120, y_position, f"Difficulty: {question['difficulty_level']}")
        y_position -= 15
        c.drawString(120, y_position, f"Answer: {question['answer']}")
        y_position -= 15
        c.drawString(120, y_position, f"Reference: {question['reference']}")
        y_position -= 15
        c.drawString(120, y_position, f"Tags: {', '.join(question['tags'])}")
        y_position -= 25
    c.save()

    buffer.seek(0)

    # Prepare PDF download
    return app.response_class(
        buffer,
        mimetype='application/pdf',
        headers={'Content-Disposition': 'attachment;filename=filtered_questions.pdf'}
    )

if __name__ == '__main__':
    app.run(debug=True,port=5006)
