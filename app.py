#####################Import all Modules ########################################
from flask import Flask, render_template,request,session
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
    modelPath="./static/20220123-135605-allegro-ridge.tar.gz"
    agent = Agent.load(str(modelPath))
    async def parse(text: Text):
        global agent
        response = await agent.handle_text(text)
        return response

message_hist={}

@app.route("/",methods=['GET','POST'])
def home():
    

    ret=""
    msg=""

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
                
            message_hist[msg]=ret
            print(message_hist)
        else:
            ret='The response was not valid'

        return render_template('index.html',message_hist=message_hist)

    else:
        
        return render_template('index.html')


if __name__=="__main__":
    app.run(debug= True)
    session.clear()