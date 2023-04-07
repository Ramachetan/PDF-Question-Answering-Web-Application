# PDF Question Answering Web Application

The PDF Question Answering Web Application is a tool that allows users to upload PDF files and ask questions about their contents. The application uses a BERT-based question-answering pipeline to provide accurate answers to user questions. The front-end interface is designed using HTML, CSS, and JavaScript, and the Flask server handles file uploads and question-answering requests.

## Getting Started

To use the application, you will need to have Python 3.x and the following packages installed:

- Flask
- PyPDF2
- transformers

To install the packages, run the following command:

pip install flask PyPDF2 transformers

To start the Flask server, navigate to the project directory and run the following command:


You can then access the front-end interface by opening a web browser and navigating to `http://localhost:5000`.

## Usage

To use the application, follow these steps:

1. Upload one or more PDF files using the form provided.
2. Ask a question about the contents of the PDF files using the input field provided.
3. Click the "Ask" button to submit the question.
4. The application will generate an answer to the question and display it in the chat container.

## Demo

You can see a demo of the application in action at this link: https://youtu.be/JDE-V4IBvHQ.

## Future Work

In the future, the application could be expanded to support more file formats and question-answering models.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


