#####################Import all Modules ########################################
from urllib import response
from aio_pika import message
from flask import Flask, render_template,request
from rasa.utils.endpoints import EndpointConfig
from rasa.core.agent import Agent
import asyncio
import nest_asyncio
from typing import Text
import tensorflow as tf

################### Declare Application #############################################
app = Flask(__name__)
######################Pre config #################################################


with tf.device("cpu:0"):
    nest_asyncio.apply()
    modelPath=r"C:\Users\luhar\Projects\Covid19-Chatbot\models\20220121-000757-foggy-cube.tar.gz"
    agent = Agent.load(str(modelPath))
    async def parse(text: Text):
        global agent
        response = await agent.handle_text(text)
        return response


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/start", methods=['GET','POST'])
def start():
    ret=""
    msg="Hello"
    if request.method=='POST':
        msg=request.form['fname']

    if agent.is_ready():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(parse(msg))

    if response is not None :
        if type(response) is list:
            ret=response[0].get('text')
        else:
            ret=response
    else:
        ret='The response was not valid'

    return render_template('index.html',message=msg,response=ret)

if __name__=="__main__":
    app.run(debug= True)