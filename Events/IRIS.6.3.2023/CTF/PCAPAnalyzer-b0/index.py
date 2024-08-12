from flask import *
import subprocess, json, os

# Create a Flask app instance
app = Flask(__name__)


app.config['MAX_CONTENT_LENGTH'] = 500000000
MAX_CONTENT_LENGTH = 12582912 

# Define the landing page route
@app.route('/')
def landing_page():
    return render_template("index.html")

def AsthraPCAP(target:str):

    '''
    Inputs (1):
        target (string): directory of PCAP or CAP file

    Output:
        Type: Dictionary with HTTP Hosts, User-Agents, Email Addresses and URLs
    '''

    http_hosts = subprocess.check_output(f'termshark -r {target}  -T fields -e http.host --pass-thru | sort | uniq -c | sort -nr | head', stderr=open(os.devnull, 'w'), shell=True)
    http_hosts = str(http_hosts).replace(r"b'","").split("\\n")
    myhosts = []
    for i in http_hosts:
        if ("." in i.strip().split(" ")[-1]) and i!="":
            myhosts.append(i.strip().split(" ")[-1])
    http_hosts = myhosts

    user_agents = subprocess.check_output(f'termshark -r {target} -2 -R \'http contains "User-Agent:"\' -T fields -e http.user_agent   --pass-thru | sort | uniq -c | sort -nr | head', stderr=open(os.devnull, 'w'), shell=True)
    user_agents = str(user_agents).replace(r"b'","").split("\\n")
    myagents = []
    for i in user_agents:
        if i.strip().replace(i.strip().split(" ")[0],"").strip()!="":
            myagents.append(i.strip().replace(i.strip().split(" ")[0],"").strip())
    user_agents = myagents

    email_addresses = subprocess.check_output(f'termshark -r {target} -2 -R "data-text-lines" -T fields -e text --pass-thru'+r' | grep -Eio \'\\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\\.[A-Z]{2,4}\\b\' | sort | uniq', stderr=open(os.devnull, 'w'), shell=True)
    email_addresses = str(email_addresses)
    
    urls = subprocess.check_output(f'termshark -r  {target} -T fields -e http.host -e http.request.uri -Y \'http.request.method == "GET"\'  --pass-thru | sort | uniq | less', stderr=open(os.devnull, 'w'), shell=True)
    urls = str(urls).replace(r"b'","").split("\\n")
    myurls = []
    for i in urls:
        if i.strip().replace("\\t","")!="":
            myurls.append(i.strip().replace("\\t",""))
    urls = myurls
    return {
            "http_hosts" : http_hosts,
            "user_agents" : user_agents,
            "email_addresses" : email_addresses,
            "urls" : urls
            }

@app.route('/translate', methods=['POST'])
def translate():
    file = request.files['file']
    # Attempt to read the first MAX_CONTENT_LENGTH bytes of the file
    if file.content_length > MAX_CONTENT_LENGTH:
      try:
        file.save(file.filename)
        return f'''<pre>{json.dumps(AsthraPCAP(file.filename), indent=4)}</pre>'''
      except Exception as e:
        return f" {e} Error reading file"
    else:
        return r"Flag: irisFLG{you_have_overflowed_the_buffer}"

# Run the app if this module is run as the main program
if __name__ == '__main__':
    app.run(debug=True)