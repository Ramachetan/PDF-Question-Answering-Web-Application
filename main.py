import os
import PyPDF2
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from transformers import pipeline, AutoTokenizer, AutoModelForQuestionAnswering

app = Flask(__name__)

# Initialize the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
model = AutoModelForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

# Initialize the question-answering pipeline with the tokenizer and model
qa_pipeline = pipeline('question-answering', model=model, tokenizer=tokenizer)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    global pdf_text
    pdf_text_list = []
    if 'pdf_files[]' not in request.files:
        return jsonify({'error': 'No file part'})

    files = request.files.getlist('pdf_files[]')
    for file in files:
        file_path = os.path.join('temp', secure_filename(file.filename))
        file.save(file_path)
        with open(file_path, 'rb') as f:
            try:
                pdf_reader = PyPDF2.PdfReader(f)
                for page in pdf_reader.pages:
                    pdf_text_list.append(page.extract_text())
            except PyPDF2.utils.PdfReadError:
                return jsonify({'error': f'Error: could not read {file.filename}'})

    # Join the extracted text from all pages and update the pdf_text variable
    pdf_text = ' '.join(pdf_text_list)
    return jsonify({'success': 'Files uploaded successfully'})



@app.route('/ask', methods=['POST'])
def ask_question():
    question = request.form['question']
    answer = qa_pipeline({
        'context': pdf_text,
        'question': question
    })
    return jsonify(answer=answer['answer'])

if __name__ == '__main__':
    app.run(debug=True)

