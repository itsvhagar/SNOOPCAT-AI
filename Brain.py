import random
import os
from flask import jsonify
from openai import OpenAI
import PyPDF2


def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        text = ''
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text



class Brain(object):
    def __init__(self, name, model, openai_key):
        self.name = name
        self.model = model
        self.knowledge_base = [{'role':'system', 'content':'Your name is Snoop Cat AI. You are a helpful assistant. The first prompt will be a long text,'
                                        'and any messages that you get be regarding that. Please answer any '
                                        'questions and requests having in mind the first prompt. '
                                        'If user asks for other information, just answer them'}]
        self.client = OpenAI(api_key=openai_key)
        self.chatSessions = []
        self.brain_id = random.randint(100000,999999)
        self.ip_pool = []

    def add_knowledge_base(self, content):
        # Check file type
        if ".txt" in content:
            content = read_file(content)
        elif ".pdf" in content:
            content = read_pdf(content)
        self.knowledge_base.append({'role': 'system', 'content': content})
        print("Current KnowledgeBases: " + str(len(self.knowledge_base)))
        return self.knowledge_base.index({'role': 'system', 'content': content})

    def remove_knowledge_base(self, content_id):
        self.knowledge_base.remove(self.knowledge_base[content_id])
        return True

    def new_chat_session(self, ip):
        self.ip_pool.append(ip)
        knowledge_base = []
        for item in self.knowledge_base:
            knowledge_base.append(item)
        chat_session = {
            "id": ip,
            "knowledgeBase": knowledge_base
        }
        self.chatSessions.append(chat_session)
        return chat_session['id']

    def ask_question(self, question, chat_session_id = None):
        if not chat_session_id in self.ip_pool:
            chat_session_id = self.new_chat_session(chat_session_id)
        for chat_session in self.chatSessions:
            if chat_session['id'] == chat_session_id:
                chat_session['knowledgeBase'].append({'role': 'user', 'content': question})
                response = self.client.chat.completions.create(
                    model = self.model,
                    messages = chat_session['knowledgeBase']
                )
                chat_session['knowledgeBase'].append({'role': 'system', 'content': response.choices[0].message.content})
                print(chat_session['knowledgeBase'])
                return response.choices[0].message.content, chat_session_id

    def load_chat(self, chat_session_id):
        if not chat_session_id in self.ip_pool:
            response = {
                "status": "No chat found",
                "data": {'role': 'system', 'content': "What's up!"}
            }
            return jsonify(response)
        else:
            for chat_session in self.chatSessions:
                if chat_session['id'] == chat_session_id:
                    response = {
                        "status": "Chat found",
                        "data": chat_session['knowledgeBase']
                    }
                    return jsonify(response)



