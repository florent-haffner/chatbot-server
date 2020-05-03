from flask import Flask, request
from src.chatbot import chat

app = Flask(__name__)

# Handle the Heroku server status to return to webapp
@app.route( '/', methods=['GET'] )
def getStatus():
    return { 'online_status': True }

# Handle the message flow I/O chatbot and api response
@app.route( '/message', methods=['POST'] )
def postMessageToChatbot():
    request_body = request.json['messageRequested']
    response = chat(request_body)
    return response
