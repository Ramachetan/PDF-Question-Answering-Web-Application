import os
import PyPDF2
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from transformers import pipeline, AutoTokenizer, AutoModelForQuestionAnswering, AutoModelForSequenceClassification

app = Flask(__name__)

# Initialize the tokenizer and model for BERT
bert_tokenizer = AutoTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
bert_model = AutoModelForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

# Initialize the tokenizer and model for DistilBert
distilbert_tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased')
distilbert_model = AutoModelForSequenceClassification.from_pretrained('distilbert-base-uncased')

# Initialize the question-answering pipeline with the BERT tokenizer and model
qa_pipeline = pipeline('question-answering', model=bert_model, tokenizer=bert_tokenizer)

# Initialize the selection classifier pipeline with the DistilBert tokenizer and model
selection_pipeline = pipeline('text-classification', model=distilbert_model, tokenizer=distilbert_tokenizer)

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

    # First, use the DistilBert selection classifier to find relevant text passages
    relevant_passages = []
    for passage in pdf_text.split('\n'):  # Assuming passages are separated by newlines
        classification = selection_pipeline(passage)
        if classification[0]['label'] == 'LABEL_1':  # Adjust this depending on how your classifier is set up
            relevant_passages.append(passage)

    # Next, use the BERT fine-tuned model for question answering on the relevant passages
    relevant_context = ' '.join(relevant_passages)
    answer = qa_pipeline({
        'context': relevant_context,
        'question': question
    })

    return jsonify(answer=answer['answer'])

if __name__ == '__main__':
    app.run(debug=True)
