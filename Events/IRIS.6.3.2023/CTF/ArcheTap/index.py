from flask import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/graminBankurrrr')
def download():
    return send_file('ExploitMe.class')

if __name__ == '__main__':
    app.run()
