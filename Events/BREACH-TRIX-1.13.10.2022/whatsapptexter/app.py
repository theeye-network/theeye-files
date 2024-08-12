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

for person in people[19:]:
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    txt = f'''Good Evening, {person['name']}!%0A
%0A
We wish to heartily thank you for continuing as a member of the Cybersecurity-Focus Club The Eye, CSEA.%0A
%0A
You are invited to attend the Briefing and Planning Meet for 2023 at G403 at 4.30PM on Wednesday, 8 February 2023.%0A
Hoping to actively work with you in our future endeavors!%0A
%0A
You can find our social media below - to keep in the loop:%0A
*Instagram:* https://www.instagram.com/welcometotheeye/%0A
*LinkedIn:* https://www.linkedin.com/company/visio-protectoris/%0A
*Medium:* https://medium.com/@welcometotheeye%0A
%0A
For any queries, please contact *Aaditya Rengarajan (+91 94445 11430)*. Do *not* respond to this message, as this is an automated message.'''

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