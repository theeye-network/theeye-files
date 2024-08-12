from flask import *
from modules import xlink
import json

app = Flask(__name__)
app.config["SECRET_KEY"] = "CXHUIDE8HWQ78UY9483HD9WEUH79Y"

def getTeams():
    with open("data/teams.json") as f:
        data = json.load(f)
    return data

def writeTeam(team):
    with open("data/teams.json") as f:
        data = json.load(f)
    newData = []
    for i in data:
        if i["team-name"] != team["team-name"]:
            newData.append(i)

    newData.append(team)
    with open("data/teams.json", "w") as f:
        json.dump(newData, f, indent=4)

@app.route('/')
def redirector():
    if session.get("login")!=None:
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':

        student = xlink.profiler(request.form.get("roll-no"),
                      request.form.get("password"))

        if student.get("message")  == "valid":

            try:

                session["login"] = json.dumps(next(team for team in getTeams() if any(member["roll"] == request.form.get("roll-no") for member in team["team-members"])))
                return redirect(url_for("dashboard"))
                
            except:

                return {"message": "404 Team Not Found"}

        else:
            return {"message": "401 Incorrect Credentials"}

    session.clear()
    return render_template('login.html')

@app.route('/dash')
def dashboard():
    if session.get('login')==None:
        return redirect(url_for('login'))
    else:
        teams = getTeams()

        myTeam = json.loads(session.get("login"))

        sorted_teams = sorted(teams, key=lambda team: team['points'], reverse=True)

        with open("data/challenges.json") as f:
            myData = json.load(f)

        return render_template("dashboard.html", team=myTeam, topTeams = sorted_teams, challenges = myData)


@app.route('/verify-flag', methods=['GET','POST'])
def verify_flag():
    if session.get('login')==None:
        return redirect(url_for('login'))
    else:
        flagFound = 'false'
        data = request.json
        with open("data/challenges.json") as f:
            myData = json.load(f)
        for i in myData:
            if i["name"] == data["challengeName"]:
                if data["flag"] in i["flags"]:
                    flagFound = 'true'
                    myPoints = i["points"]/len(i["flags"])

        if flagFound=='true':
            teams = getTeams()
            for i in teams:
                if i["team-name"] == json.loads(session.get("login")).get("team-name"):
                    myTeam = i

            # prevent doublesolve
            if data["flag"] in myTeam["solved"]:
                return jsonify({'result': flagFound})

            solved = myTeam["solved"]
            solved.append(data["flag"])
            points = myTeam["points"]
            points += myPoints
            myTeam.update({"solved":solved,"points":points})
            writeTeam(myTeam)
            session["login"] = json.dumps(myTeam)

        return str(flagFound)


@app.route('/get-points', methods=['GET','POST'])
def get_points():
    if session.get('login')==None:
        return redirect(url_for('login'))
    else:
        return str(int(json.loads(session.get('login')).get('points')))


@app.route('/easypoints')
def easypoints():
    if session.get('login')==None:
        return redirect(url_for('login'))
    else:
        teams = getTeams()
        myTeam = None
        for i in teams:
            if i["team-name"] == json.loads(session.get("login")).get("team-name"):
                myTeam = i

        return render_template("easypoints.html", team=myTeam)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('redirector'))

if __name__ == '__main__':
    app.run()