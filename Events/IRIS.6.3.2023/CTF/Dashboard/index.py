from flask import *
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
        team = request.form.get("team-name")
        teams = getTeams()
        myTeam = None
        for i in teams:
            if i["team-name"] == team:
                myTeam = i
                session["login"] = json.dumps(myTeam)
                return redirect(url_for('dashboard'))
    session.clear()
    return render_template('login.html')

@app.route('/dash')
def dashboard():
    if session.get('login')==None:
        return redirect(url_for('login'))
    else:
        teams = getTeams()
        myTeam = None
        for i in teams:
            if i["team-name"] == json.loads(session.get("login")).get("team-name"):
                myTeam = i

        sorted_teams = sorted(teams, key=lambda team: team['points'], reverse=True)

        prevalues = list("" for i in range(9))

        if "EFJACZEBYQEB" in myTeam["solved"]:
            prevalues[0] = "EFJACZEBYQEB\" disabled style=\"background-color:#D2FDD6;border-radius: 25px;pading:25px;width: 50%;"
        if "blahblah" in myTeam["solved"]:
            prevalues[1] = "blahblah\" disabled style=\"background-color:#D2FDD6;border-radius: 25px;pading:25px;width: 50%;"
        if "you_have_overflowed_the_buffer" in myTeam["solved"]:
            prevalues[2] = "you_have_overflowed_the_buffer\" disabled style=\"background-color:#D2FDD6;border-radius: 25px;pading:25px;width: 50%;"
        if "XXXXXX" in myTeam["solved"]:
            prevalues[3] = "XXXXXX\" disabled style=\"background-color:#D2FDD6;border-radius: 25px;pading:25px;width: 50%;"
        if "IaMsUrEyOuDiDnOtBrUtEfOrCeMe" in myTeam["solved"]:
            prevalues[4] = "IaMsUrEyOuDiDnOtBrUtEfOrCeMe\" disabled style=\"background-color:#D2FDD6;border-radius: 25px;pading:25px;width: 50%;"
        if "B@tmaN150ffth3R@1ls" in myTeam["solved"]:
            prevalues[5] = "B@tmaN150ffth3R@1ls\" disabled style=\"background-color:#D2FDD6;border-radius: 25px;pading:25px;width: 50%;"
        if "thAt5W#@tS#3S@1d" in myTeam["solved"]:
            prevalues[6] = "thAt5W#@tS#3S@1d\" disabled style=\"background-color:#D2FDD6;border-radius: 25px;pading:25px;width: 50%;"
        if "PayMe5z1ll10n@ndIwontExposeYou" in myTeam["solved"]:
            prevalues[7] = "PayMe5z1ll10n@ndIwontExposeYou\" disabled style=\"background-color:#D2FDD6;border-radius: 25px;pading:25px;width: 50%;"
        if "T#is15@sEcr3tF1l3" in myTeam["solved"]:
            prevalues[8] = "T#is15@sEcr3tF1l3\" disabled style=\"background-color:#D2FDD6;border-radius: 25px;pading:25px;width: 50%;"
        return render_template("dashboard.html", team=myTeam, prevalues=prevalues, topTeams = sorted_teams)


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
            print("updatedFile")
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