from flask import Flask, request, abort
from time import time


app = Flask(__name__)
database = []

@app.route("/send", methods=['POST'])
def post_message():
    print('ok')
    message = request.json
    database.append({'name': message['name'],'text': message['text'],'time': time()})
    return {'message sent': True}


@app.route("/messages")
def get_messages():
    try:
        last = float(request.args['last'])
    except:
        return abort(400)

    messages = []

    for message in database:
        if message['time'] > last:
            messages.append(message)

    return {'messages': messages}



if __name__ == '__main__':
    app.run()
