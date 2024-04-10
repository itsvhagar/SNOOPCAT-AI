from flask import Flask, render_template, request, jsonify
import openai
import PyPDF2
from Brain import Brain
from argparse import ArgumentParser

app = Flask(__name__)



def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        text = ''
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text


# Define the default route to return the index.html file
@app.route("/")
def index():
    return render_template("index.html")

# Define the /api route to handle POST requests
@app.route("/ask", methods=["POST"])
def api():
    ip = request.json.get("ip")
    if ip == "":
        ip = request.remote_addr
    # Get the message from the POST request
    message = request.json.get("message")
    # Send the message to OpenAI's API and receive the response
    response = brain.ask_question(message, chat_session_id=ip)
    res = {
        "status": "ok",
        "data": response
    }
    return jsonify(res)

@app.route("/load_chat", methods=["GET"])
def load_chat():
    ip = request.remote_addr
    # Get the message from the POST request
    message = request.json.get("message")
    # Send the message to OpenAI's API and receive the response
    response = brain.load_chat(chat_session_id=ip)
    return response
    

if __name__=='__main__':
    parser = ArgumentParser()
    parser.add_argument('-key', '--openai_key', default="", type=str, help='OpenAI API Key')
    args = parser.parse_args()
    brain = Brain(name="Brain", model='gpt-3.5-turbo', openai_key=args.openai_key)
    brain.add_knowledge_base('whitepaper.pdf')
    cert = 'certificate.crt'
    key = 'private_key.key'
    app.run(host='0.0.0.0', debug=False, port=443, ssl_context=(cert, key))

