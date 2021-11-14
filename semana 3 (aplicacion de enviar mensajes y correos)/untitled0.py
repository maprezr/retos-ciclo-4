# -*- coding: utf-8 -*-
"""
Created on Sat Nov  6 11:01:57 2021

@author: maper
"""

from flask import Flask
import os
from twilio.rest import Client
from flask import request
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)

@app.route("/")

def inicio ():
    test = os.environ.get("Test")
    return test

@app.route ("/sms")
def sms():
    try:  
        # Find your Account SID and Auth Token at twilio.com/console
        # and set the environment variables. See http://twil.io/secure
        account_sid = os.environ['TWILIO_ACCOUNT_SID']
        auth_token = os.environ['TWILIO_AUTH_TOKEN']
        client = Client(account_sid, auth_token)
        contenido = request.args.get("mensaje")
        destino = request.args.get("telefono")
        message = client.messages.create(
                                      body= contenido,
                                      from_='+19284370241',
                                      to= "+57" + destino
                                 )
        
        print(message.sid)
        return "enviado correctamente"
    except Exception as e:
        return "Error enviando mensaje"

@app.route("/envio-correo")
def email():
    destino = request.args.get("correo-destino")
    asunto = request.args.get("asunto")
    contenido = request.args.get("contenido")
    
    message = Mail(
    from_email='maperez.r@hotmail.com',
    to_emails= destino,
    subject=asunto,
    html_content = contenido)
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        return "enviado correctamente"
    except Exception as e:
        print(e.message)
        return  " no se pudo enviar el mensaje"
    


if __name__ == '__main__':
    app.run()
    