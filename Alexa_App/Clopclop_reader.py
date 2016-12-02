from flask import Flask
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode 

app = Flask(__name__)
ask = Ask(app, "/Clopclop_reader")


def get_headlines():
    user_pass_dict = {'user': 'AlexaAppThrowaway',
                      'passwd': 'password',
                      'api_type': 'json'}
    sess = requests.Session()
    sess.headers.update({'User-Agent': 'I am testing Alexa: AlexaAppThrowaway'})
    sess.post('https://www.reddit.com/api/login', data = user_pass_dict)
    time.sleep(1)
    url = 'https://reddit.com/r/clopclop/top/.json?limit=10'
    html = sess.get(url)
    data = json.loads(html.content.decode('utf-8'))
    titles = [unidecode.unidecode(listing['data']['title']) for listing in data['data']['children']]
    titles = '... '.join([i for i in titles])
    return titles


@app.route('/')
def homepage():
    return "Hi there, how ya doin?"

if __name__ == '__main__':
    app.run(debug=True)

@ask.launch
def start_skill():
    welcome_message = 'Hello there, would you like to hear the top 10 Clop Clop articles?'
    return question(welcome_message)

@ask.intest("YesIntent")
def share_headlines():
    headlines = get_headlines()
    headline_msg = 'The current Clop Clop headlines are {}'.format(headlines)
    return statement(headline_msg)

@ask.intent("NoIntent")
def no_intent():
    bye_text = 'I am not sure why you asked me to run then Nitish, but okay... ... bye forever'
    return statement(bye_text)

