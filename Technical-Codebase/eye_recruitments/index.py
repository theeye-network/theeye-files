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

@app.route('/finalogin', methods=['GET', 'POST'])
@login_required
def final_login():
    '''
    session["name"]
    session["login"]
    session["roll"]
    session["pwd"]
    session["programme"]
    session["semester"]'''
    sem_to_year = {
        "1": "1st",
        "2": "1st",
        "3": "2nd",
        "4": "2nd",
        "5": "3rd",
        "6": "3rd",
        "7": "4th",
        "8": "4th"
    }
    name = session["name"].replace(" ","+")
    if "BE COMPUTER SCIENCE & ENGINEERING" in session['programme']:
        if "ARTIFICIAL INTELLIGENCE" in session['programme']:
            dept = "CSE+(AI+%26+ML)"
        else:
            dept = "CSE"
        return redirect(str(f'''https://docs.google.com/forms/d/e/1FAIpQLSeIz1McO80nVW-LCEKpDY40mnmNtyg8NRNu1SH4asXwhWfa7Q/
        viewform?usp=pp_url&
        entry.1515980368={name}&
        entry.448363363={session['roll']}&
        entry.617036074={session['phone']}&
        entry.786955649={session['roll']}@psgtech.ac.in&
        entry.1619461677={sem_to_year[str(session['semester'])]}&
        entry.1141893820={dept}'''.replace("\n","").replace(" ","")))
    return "This is only for CSE Students."

def main():
    app.run(host='0.0.0.0',
        port=5000,
        debug=True)

if __name__ == '__main__':
    main()