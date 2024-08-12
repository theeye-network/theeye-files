from flask import *
import uuid, json, io
from tabulate import tabulate

app = Flask(__name__)
app.secret_key = "KrrrzPPghtfgSKbtJEQCTA"

app.PROPAGATE_EXCEPTIONS = True

def reg():
    with open("reg.json") as file:
        data = json.load(file)
    return data

@app.route('/')
def home_page():
    if len(reg())>60:
        full="true"
    else:
        full="false"
    return render_template("index.html",
                            full=full)

@app.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
    if request.method=='GET':
        return render_template("signup.html")
    if request.method=='POST':
        with open("reg.json") as file:
            data = json.load(file)
        data.append(dict(request.form))
        with open("reg.json", "w") as file:
            json.dump(data, file, indent=4)
        return render_template("welcome.html",
                                name = request.form.get("name"))

@app.route('/attendance')
def attendance():
    rolls = []
    tableau = [["#", "Name", "Roll Number", "Email", "Phone Number", "Signature"]]
    c=0
    for i in sorted(reg(), key=lambda d: d['roll_no']):
        c+=1
        if i["roll_no"].upper() not in rolls:
            rolls.append(i["roll_no"].upper())
            tableau.append([str(c),i["name"],i["roll_no"].upper(),f'{i["roll_no"].upper()}@psgtech.ac.in',i['phone_no'],'Sign Below:\n\n\n\n__________'])
    table = tabulate(tableau,
                     headers="firstrow",
                     tablefmt="grid")
    a = table.replace("\n","<br/>")
    return f'<pre>{a}</pre>'

def main():
  app.run(debug=True,
          host='0.0.0.0',
          port=56789)

if __name__ == '__main__':
  main()