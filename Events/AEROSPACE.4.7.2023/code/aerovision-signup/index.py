from flask import *

import requests, json, datetime, math
from bs4 import BeautifulSoup

app = Flask(__name__)

FILE_UPLOAD_PATH = "secureUploads/" 
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = "KrrrzPPghtfgSKbtJEQCTA"

app.PROPAGATE_EXCEPTIONS = True


from functools import wraps

def login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        try:
            session.get("roll")
            return func(*args, **kwargs)
        except Exception as e:
            return str(e)
    return decorated_view

def organizer_login(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        try:
            with open("organizers.json") as orgF:
                orgArr = json.load(orgF)
            if session.get("roll").upper() not in orgArr:
                return {"message":"403 Forbidden"}
            return func(*args, **kwargs)
        except Exception as e:
            return {"message":"403 Forbidden"}
    return decorated_view

def profiler(username,pwd):

    session = requests.Session()
    r = session.get('https://ecampus.psgtech.ac.in/studzone2/')
    loginpage = session.get(r.url)
    soup = BeautifulSoup(loginpage.text,"html.parser")

    viewstate = soup.select("#__VIEWSTATE")[0]['value']
    eventvalidation = soup.select("#__EVENTVALIDATION")[0]['value']
    viewstategen = soup.select("#__VIEWSTATEGENERATOR")[0]['value']

    item_request_body  = {
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__LASTFOCUS': '',
        '__VIEWSTATE': viewstate,
        '__VIEWSTATEGENERATOR': viewstategen,
        '__EVENTVALIDATION': eventvalidation,
        'rdolst': 'S',
        'txtusercheck': username,
        'txtpwdcheck': pwd,
        'abcd3': 'Login',
    }

    
    response = session.post(url=r.url, data=item_request_body, headers={"Referer": r.url})
    val = response.url

    if response.status_code == 200:

        defaultpage = 'https://ecampus.psgtech.ac.in/studzone2/AttWfStudProfile.aspx'
    
        page = session.get(defaultpage)
        soup = BeautifulSoup(page.text,"html.parser")

        image_url = "https://ecampus.psgtech.ac.in/studzone2/WfAttStudPhoto.aspx"
        response = session.get(image_url)

        # Return the image data as a response
        image_data = Response(response.content, mimetype='image/jpeg')

        data = []
        column = []
    
        try:

            table = soup.find('table', attrs={'id':'ItStud'})

            rows = table.find_all('tr')
            for index,row in enumerate(rows):
                
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                data.append([ele for ele in cols if ele]) # Get rid of empty val

            table = soup.find('table', attrs={'id':'DlsAddr'})
            addr = []

            rows = table.find_all('tr')
            for index,row in enumerate(rows):
                
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                addr.append([ele for ele in cols if ele]) # Get rid of empty val

            return {"student":data, "address":addr, "image":image_data}

        except Exception as e:
            
            return str(e)
    else:
        return item_request_body

def test_timetable(req_info): 

    username = req_info.get("roll")
    pwd = req_info.get("pass")
    

    session = requests.Session()
    r = session.get('https://ecampus.psgtech.ac.in/studzone2/')
    loginpage = session.get(r.url)
    soup = BeautifulSoup(loginpage.text,"html.parser")

    viewstate = soup.select("#__VIEWSTATE")[0]['value']
    eventvalidation = soup.select("#__EVENTVALIDATION")[0]['value']
    viewstategen = soup.select("#__VIEWSTATEGENERATOR")[0]['value']

    item_request_body  = {
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__LASTFOCUS': '',
        '__VIEWSTATE': viewstate,
        '__VIEWSTATEGENERATOR': viewstategen,
        '__EVENTVALIDATION': eventvalidation,
        'rdolst': 'S',
        'txtusercheck': username,
        'txtpwdcheck': pwd,
        'abcd3': 'Login',
    }

    
    response = session.post(url=r.url, data=item_request_body, headers={"Referer": r.url})
    val = response.url

    if response.status_code == 200:

        defaultpage = 'https://ecampus.psgtech.ac.in/studzone2/FrmEpsTestTimetable.aspx'
    
        page = session.get(defaultpage)
        soup = BeautifulSoup(page.text,"html.parser")

        data = []
        column = []
    
        try:

            table = soup.find('table', attrs={'id':'DgResult'})

            rows = table.find_all('tr')
            for index,row in enumerate(rows):
                
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                data.append([ele for ele in cols if ele]) # Get rid of empty val

            table = soup.find_all('table', attrs={'width':'85%', 'align':'center'})[-1]
            slots = []
            rows = table.find_all('tr')
            for index,row in enumerate(rows):
                
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                slots.append([ele for ele in cols if ele]) # Get rid of empty val

            return {"slots":slots, "timetable":data}

        except Exception as e:
            
            return "Invalid password"
    else:
        return item_request_body



@app.route('/')
def slash():
    if session.get("roll"):
        return redirect(url_for("final_login"))
    else:
        session.clear()
        return redirect(url_for("authenticate"))

def find_student_by_roll(rollNumber):
    with open('details.json', 'r') as f:
        students_data = json.load(f)
    index = 0
    for student in students_data:
        print(student.get("Roll #"), rollNumber, student.get("Roll #") == rollNumber)
        if student.get("Roll #") == rollNumber:
            return student, index
        index += 1
    return None

@app.route('/add_attendance/<string:rollNumber>', methods=['GET'])
def add_attendance(rollNumber):
    student, idx = find_student_by_roll(rollNumber)
    
    if student:

        with open('details.json', 'r') as f:
            students_data = json.load(f)

        student = students_data[idx]

        today_date = datetime.datetime.today().strftime('%d-%m-%Y')
        
        if 'attended' not in student:
            student['attended'] = [today_date]
        else:
            student['attended'].append(today_date)

        student['attended'] = list(set(student['attended']))

        # Save the updated JSON data
        with open('details.json', 'w') as f:
            json.dump(students_data, f, indent=4)

        return jsonify({"message": f"Attendance added for {rollNumber} on {today_date}"}), 200
    else:
        return jsonify({"error": "Roll number not found"}), 404

@app.route('/get_attendance/<string:rollNumber>', methods=['GET'])
def get_attendance(rollNumber):
    student, idx = find_student_by_roll(rollNumber)
    
    if student and 'attended' in student:
        attendance = student['attended']
        return jsonify({"attended": attendance}), 200
    else:
        return jsonify({"attended": []}), 200


@app.route('/auth', methods=['GET', 'POST'])
def authenticate():
    if request.method=='GET':
        return render_template('signup.html', err=False)
    else:
        profile = profiler(request.form.get("userid").upper(),request.form.get("pwd"))
        try:
            session["name"] = (str(profile["student"][0][2])).title()
            session["login"] = "done"
            session["roll"] = request.form.get("userid").upper()
            session["pwd"] = request.form.get("pwd")
            session["programme"] = profile["student"][1][2]
            session["semester"] = profile["student"][1][2]
            try:
                tests = test_timetable({"roll":request.form.get("userid").upper(), "pass":request.form.get("pwd")})
                time_table = []

                for i in tests["timetable"][1:]:
                    time_table.append({
                        "sem": i[0],
                        "course": i[1],
                        "title": " ".join([j.capitalize() for j in i[2].split(" ")]),
                        "date": f"{i[3]}",
                        "slot": f"{i[4]}"
                        })
                session["semester"] = time_table[0].get("sem")
                session["phone"] = str(profile.get("address")[0][-1]).split("Student Mobile:")[-1].split(" ")[0].strip()
            except:
                pass
            return redirect(url_for("final_login"))
        except Exception as e:
            session.clear()
            return render_template("signup.html", err=True)


@app.route('/clear')
def clear_sesh():
    session.clear()
    return redirect(url_for("slash"))

@app.route('/profile-picture')
def profile_picture():
    roll_no = session.get("roll")
    pwd = session.get("pwd")
    return profiler(roll_no,pwd).get("image")

@app.route('/finalogin', methods=['GET', 'POST'])
@login_required
def final_login():
    if request.method=='GET':
        with open("details.json") as jsonf:
            data = json.load(jsonf)
        myStream = "Coding"
        for i in data:
            if i.get("Roll #").upper() == dict(session).get("roll").upper():
                myStream = i.get("Interest")
                break
        return render_template("finalform.html", details = dict(session), myStream = myStream)
    else:
        session.clear()
        with open("details.json") as jsonf:
            data = json.load(jsonf)
        rollNo = request.form.get("roll").upper()
        index = 0
        for i in data:
            if i.get("Roll #").upper() == rollNo:
                data.pop(index)
                break
            index+=1
        data.insert(index,
            {
            "Name": request.form.get("name"),
            "Roll #": request.form.get("roll").upper(),
            "Semester": request.form.get("semester"),
            "Programme": request.form.get("programme").upper(),
            "Interest": request.form.get("stream"),
            "Phone #": request.form.get("phno"),
            "WhatsApp #": request.form.get("whatsapp")
            })
        with open("details.json", "w") as jsonf:
            json.dump(data, jsonf, indent=4)
        return render_template("success.html", name=request.form.get("name"))

@app.route('/number')
def give_numbers():
    with open("details.json") as jsonf:
        deets = json.load(jsonf)
    return {"number":len(deets), "participants": deets}

@app.route('/check_in')
@organizer_login
def orgAdder():
    return render_template("attendance.html")

def main():
    app.run(host='0.0.0.0',
        port=5000,
        debug=True)

if __name__ == '__main__':
    main()