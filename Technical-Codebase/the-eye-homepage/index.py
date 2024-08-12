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


app = Flask(__name__)

app.secret_key = "KrrrzPPghtfgSKbtJEQCTA"
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.permanent_session_lifetime = timedelta(minutes=5)

app.config['MONGO_URI'] = "mongodb+srv://flaskapp:qwertyuiop@webpage.st9wxca.mongodb.net/webpage?retryWrites=true&w=majority"
mongo.init_app(app)

print("[MONGODB] CONNECTED")

a = mongo.db.webpage.find()

print("[MONGODB] INITIALIZED")

def load_configuration():
    with open("config.json") as f:
        return json.load(f)

def sendmail(receiver,subject,text,link=None):
    try:
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
    except Exception as e:
        print(e)


@app.route("/", methods=["GET"])
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

    return render_template("home.html", HOF=HOF, announcements=announcements)


@app.route("/about", methods=["GET", "POST"])
def about():
    return render_template("about.html")


@app.route("/<type>", methods=["GET"])
def listOfLinks(type):

    typeTyper = {
                    "sec": "Security Guidelines",
                    "white": "White Papers",
                    "research": "Research Papers",
                    "quart": "Quarterly Reports",
                    "intel": "Intelligence Tools",
                    "osint": "OSINT Tools"
                }

    try:
        rel = mongo.db.webpage.find_one({"listOfLinks":typeTyper[type]}).get("list")
    except:
        rel = []

    return render_template("listOfLinks.html", type=typeTyper[type], relist=rel)


@app.route("/blog", methods=["GET", "POST"])
def blog():

    rel = mongo.db.webpage.find({"type":"blog_post"})

    return render_template("theBlog.html", relist=rel)


@app.route("/blog/<post_id>", methods=["GET", "POST"])
def blogPost(post_id):

    rel = mongo.db.webpage.find_one({"_id":ObjectId(post_id)})

    return render_template("blogPost.html", rel=rel)

@app.route("/increp", methods=["GET", "POST"])
def increp():
    if request.method=='POST':
        thedic = dict(request.form)
        x = PrettyTable()
        for (i,j) in thedic.items():
            x.add_row([i,j])
        for i in load_configuration()['cert_team']:
            sendmail(i,"[THE EYE] New Incident Reported",f'''
Hey,
A new incident has been reported using the form on the website.
Here are the details\n<pre>\n{x}</pre>\nPlease revert ASAP.''')
        return render_template("recieved.html")
    return render_template("incident.html")

@app.route("/vulnrep", methods=["GET", "POST"])
def vulnrep():
    if request.method=='POST':
        thedic = dict(request.form)
        x = PrettyTable()
        for (i,j) in thedic.items():
            x.add_row([i,j])
        for i in load_configuration()['cert_team']:
            sendmail(i,"[THE EYE] New Vulnerability Reported",f'''
Hey,
A new vulnerability has been reported using the form on the website.
Here are the details\n<pre>\n{x}</pre>\nPlease revert ASAP.''')
        return render_template("recieved.html")

    return render_template("vulnerability.html")

if __name__=="__main__":
	app.run(host='0.0.0.0', port=56789)