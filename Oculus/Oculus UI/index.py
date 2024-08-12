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
            return redirect(url_for('logout'))
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

@app.route('/auth', methods=['GET', 'POST'])
def authenticate():
    if request.method=='GET':
        return render_template('auth.html')
    else:
        profile = profiler(request.form.get("userid").upper(),request.form.get("pwd"))
        try:
            session["name"] = profile["student"][0][2]
            session["login"] = "done"
            session["roll"] = request.form.get("userid").upper()
            session["pwd"] = request.form.get("pwd")
            return redirect(url_for("dashboard"))
        except Exception as e:
            session.clear()
            return "Error!"+str(e)

@app.route('/profile-picture')
@login_required
def profile_picture():
    roll_no = session.get("roll")
    pwd = session.get("pwd")
    return profiler(roll_no,pwd).get("image")

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template("dashboard.html", name=session.get("name"))

def main():
    app.run(host='0.0.0.0',debug=True)

if __name__ == '__main__':
    main()
