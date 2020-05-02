import requests
import re

def build_request_to_server(message_from_bot):

    email = re.match('[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}', message_from_bot)
    message = message_from_bot

    body = {
        'email': email, 'message': message
    }
    api_request = requests.post('http://localhost:8080/sendEmail', data=body)

    print(api_request.status_code)
    print(api_request.headers)

    if api_request.status_code == 200:
        print('text')
        print(api_request.text)
        print('json')
        print(api_request.json())


build_request_to_server("Ok, truc@email.com. I need help to build my application !")
