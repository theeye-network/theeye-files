import uvicorn, os
from fastapi import FastAPI, Depends, HTTPException, Header
from enum import Enum
from pydantic import BaseModel
from fastapi.responses import FileResponse
from typing import Dict

from flask import Flask, flash, redirect, render_template, request, session

from datetime import datetime, timedelta

from extensions import mongo
from bson.objectid import ObjectId
from bson.binary import Binary
import uuid, json, io

from prettytable import PrettyTable

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl, smtplib

import dns.resolver

dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']


app = FastAPI()

class LinksType(str, Enum):
    sec='sec'
    white='white'
    research = 'research'
    quart = 'quart'
    intel = 'intel'
    osint = 'osint'

class incidentForm(BaseModel):
    date: str # Date
    contact: str # Contact
    info: str # Information regarding System/Network/User
    symptoms: str # Symptoms Observed/Background
    tech: str # Technical Information
    non_tech: str # Non-Technical Information

    def as_dict(self):
        return {
            "Date": self.date,
            "Contact": self.contact,
            "Information regarding System/Network/User": self.info,
            "Symptoms Observed/Background": self.symptoms,
            "Technical Information": self.tech,
            "Non-Technical Information": self.non_tech 
        }

class vulnerabilityForm(BaseModel):
    contact: str # Contact
    products: str # Affected Products
    symptoms: str # Versions/Models Affected
    vendor: str # Vendor Details
    vuln: str # Vulnerability Description
    impact: str # Impact

    def as_dict(self):
        return {
            "Contact": self.contact,
            "Affected Products": self.products,
            "Versions/Models Affected": self.symptoms,
            "Vendor Details": self.vendor,
            "Vulnerability Description": self.vuln,
            "Impact": self.impact
        }

flaskapp = Flask(__name__)

flaskapp.secret_key = "KrrrzPPghtfgSKbtJEQCTA"

flaskapp.config['MONGO_URI'] = "mongodb+srv://flaskapp:qwertyuiop@webpage.st9wxca.mongodb.net/webpage?retryWrites=true&w=majority"
mongo.init_app(flaskapp)

print("[MONGODB] CONNECTED")

a = mongo.db.webpage.find()

print("[MONGODB] INITIALIZED")

def load_configuration():
    with open("config.json") as f:
        return json.load(f)

def sendmail(receiver,subject,text,link=None):
        # try:
        mailid = load_configuration()['email']
        mailps = load_configuration()['email_pass']
        sender_email = mailid
        receiver_email = receiver
        password = mailps
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = receiver_email
        part1 = MIMEText(text, 'plain')

        with flaskapp.test_request_context():

            html = render_template("email.html",
                                   text = text,
                                   subject = subject,
                                   hackathon = load_configuration(),
                                   link = link)
        part2 = MIMEText(html, 'html')

        message.attach(part1)
        message.attach(part2)

        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(mailid,password)
        server.sendmail(mailid, receiver_email, message.as_string())
        server.quit()
        # except Exception as e:
        #     print(e)


@app.get("/home")
def home():
    hallOfFame = []
    for i in mongo.db.webpage.find({"type":"HOF"}):
        hallOfFame.append(f'{str(i.get("name"))} [{str(i.get("roll"))}]')
    if len(hallOfFame)<=1:
        HOF = []
    else:
        hof = []
        for i in hallOfFame:
            if i not in hof:
                hof.append(i)
        HOF = {"names":hof}
    announcements = []
    for i in mongo.db.webpage.find({"type":"announcement"}):
        announcements.append(f'{str(i.get("details"))}')

    return {"HOF": HOF, "announcements": announcements}


@app.get("/listOfLinks/{theType}")
def listOfLinks(theType: LinksType):

    typeTyper = {
                    "sec": "Security Guidelines",
                    "white": "White Papers",
                    "research": "Research Papers",
                    "quart": "Quarterly Reports",
                    "intel": "Intelligence Tools",
                    "osint": "OSINT Tools"
                }

    try:
        rel = mongo.db.webpage.find_one({"listOfLinks":typeTyper[theType]}).get("list")
    except:
        rel = []

    return {"type": typeTyper[theType], "list": rel}

@app.get("/blog")
def blog():

    rel = mongo.db.webpage.find({"type":"blog_post"})
    rell = []
    for i in rel:
        i["id"] = str(i["_id"])
        del i["_id"]
        i["content"] = i["content"][:65] + "..."
        rell.append(i)
    return {"posts": rell}


@app.get("/blog/{post_id}")
def blogPost(post_id: str):

    rel = mongo.db.webpage.find_one({"_id":ObjectId(post_id)})
    del rel["_id"]

    return {"post": rel}

@app.post("/increp")
def increp(incidentFrm: incidentForm):
    thedic = incidentFrm.as_dict()
    x = PrettyTable()
    for (i,j) in thedic.items():
        x.add_row([i,j])
    for i in load_configuration()['cert_team']:
        sendmail(i,"[THE EYE] New Incident Reported",f'''
Hey,
A new incident has been reported using the form on the website.
Here are the details\n<pre>\n{x}</pre>\nPlease revert ASAP.''')
    return {"message": "Recieved"}

@app.post("/vulnrep")
def vulnrep(vulnFrm: vulnerabilityForm):
    thedic = vulnFrm.as_dict()
    x = PrettyTable()
    for (i,j) in thedic.items():
        x.add_row([i,j])
    for i in load_configuration()['cert_team']:
        sendmail(i,"[THE EYE] New Vulnerability Reported",f'''
Hey,
A new vulnerability has been reported using the form on the website.
Here are the details\n<pre>\n{x}</pre>\nPlease revert ASAP.''')
    return {"message": "Recieved"}

if __name__=="__main__":
	uvicorn.run(app, host='0.0.0.0', port=56789)