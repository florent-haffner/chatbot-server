from flask import Flask, request
from chatbot import chat
app = Flask(__name__)

# Handle the status to return to webapp
@app.route( '/status', methods=['GET'] )
def getStatus():
    return { 'chatbot_status': 'online' }

# Handle the message flow I/O chatbot and api response
@app.route( '/message', methods=['POST'] )
def postMessageToChatbot():
    request_body = request.json['message']
    response = chat(request_body)
    return response
