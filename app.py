from flask import Flask, request
from chatbot import chat
app = Flask(__name__)

@app.route( '/status', methods=['GET'] )
def getStatus():
    return { 'chatbot_status': 'online' }

@app.route( '/message', methods=['POST'] )
def postMessageToChatbot():
    request_body = request.json
    response = chat(request_body['message'])
    return { 'response': response }

