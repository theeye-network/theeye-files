from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from time import sleep

import chromedriver_binary

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl, smtplib
import jinja2, json

def sendmail(from_mail,to_mail,thesmtp,pwd,content,html,subject):
    # creating the MIME as plain text and HTML
    sender_email = from_mail
    receiver_email = to_mail
    password = pwd
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email
    part1 = MIMEText(content, 'plain')
    part2 = MIMEText(html, 'html')
    message.attach(part1)
    message.attach(part2)
    # starting an SSL context to send an e-mail
    try:
      context = ssl.create_default_context()
      with smtplib.SMTP_SSL(thesmtp, 465, context=context) as server:
          server.login(sender_email, password)
          server.sendmail(
              sender_email, receiver_email, message.as_string()
          )
      return 'Succesfuly Sent'
    except Exception as e:
        print(f"tried sending [{to_mail} , {subject} , {content}]; failed due to error : {e}.")

with open("../reg.json") as f:
    people = json.load(f)
    mypeople = []
    rolls = []
    tableau = [["#", "Name", "Roll Number", "Email", "Phone Number", "Signature"]]
    c=0
    for i in sorted(people, key=lambda d: d['roll_no']):
        c+=1
        if i["roll_no"].upper() not in rolls:
            rolls.append(i["roll_no"].upper())
            mypeople.append({"#":c,
                             "name":i["name"],
                             "roll_no":i["roll_no"],
                             "phone_no":i["phone_no"]})
    people = mypeople

print(json.dumps(people,indent=4))

opns = Options()
opns.binary_location='C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe'
opns.add_argument('--no-sandbox')
opns.add_argument("--disable-popup-blocking")
opns.add_argument("profile-directory=Profile 1")
opns.add_argument('ignore-certificate-errors')
opns.add_argument('--disable-dev-shm-usage')
opns.add_argument("--disable-notifications")
opns.set_capability('unhandledPromptBehavior', 'dismiss')
opns.set_capability('UnexpectedAlertBehaviour', 'dismiss')
driver = webdriver.Chrome(executable_path='C:\\chromedriver.exe', options = opns)
driver.get("https://web.whatsapp.com")
print("Scan QR Code, And then Enter")
input()
print("Logged In")
body = driver.find_element(By.CSS_SELECTOR, "body")
body.send_keys(Keys.CONTROL + 't')
body.send_keys(Keys.CONTROL + Keys.TAB)
body.send_keys(Keys.CONTROL + 'w')

c=0

for person in people:
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    txt = f'''Good Morning, {person['name']}!%0A
%0A
Welcome to Iris 2023. Please fill in the Google Form at https://forms.gle/hwE6RTzh4c67ztTL7 and join the WhatsApp Group at https://chat.whatsapp.com/LrfhY9WR1JgBanuFn2WIgT for updates.%0A
%0A
The problems for the Coding Stream will be released by 12PM Saturday (March 4), and the CTF for the Hacking Stream will kickoff at 12AM Sunday (March 5). The Hacking Competition will last for 1 day while the Coding Competition will last for 1.5 days.%0A
Please raise any queries in the WhatsApp Group.%0A
Do *not* respond to this message, as this is an automated message.'''

    # sendmail("21Z202@psgtech.ac.in",
    #      f"{person['roll_no']}@psgtech.ac.in",
    #      "smtp.gmail.com",
    #      "pmEc68SzMM1W5jSYdpyk",
    #      txt.replace("%0A","\n"),
    #      txt.replace("%0A","<br/>"),
    #      "[The Eye] Briefing and Planning '23")

    driver.get(f"https://web.whatsapp.com/send/?phone=91{person['phone_no']}&text={txt}&type=phone_number&app_absent=0")
    send_xpath = '//button[@data-testid="compose-btn-send"]'
    WebDriverWait(driver, 500).until(EC.presence_of_element_located((By.XPATH, send_xpath)))

    send_button = driver.find_element(By.XPATH, send_xpath)
    send_button.click()
    try:
        alert = driver.switch_to.alert()
        alert.accept()
    except:
        pass
    sleep(5)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

driver.quit()