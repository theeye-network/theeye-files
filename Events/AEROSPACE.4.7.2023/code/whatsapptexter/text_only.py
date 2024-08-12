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
import pyautogui


opns = Options()
opns.binary_location='chromedriver.exe'
opns.add_argument('--no-sandbox')
opns.add_argument("--disable-popup-blocking")
opns.add_argument("profile-directory=Profile 1")
opns.add_argument('ignore-certificate-errors')
opns.add_argument('--disable-dev-shm-usage')
opns.add_argument("--disable-notifications")
driver = webdriver.Chrome( options = opns)
driver.get("https://web.whatsapp.com")
print("Scan QR Code, And then Enter")
input()
print("Logged In")
body = driver.find_element(By.CSS_SELECTOR, "body")
body.send_keys(Keys.CONTROL + 't')
body.send_keys(Keys.CONTROL + Keys.TAB)
body.send_keys(Keys.CONTROL + 'w')


c=0


with open("details.json") as f:
    people = json.load(f)


for person in people:
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    txt = f'''Hello {person['name']}%0A
We hope you're ready for an exciting day ahead. Today, on August 24th, we have a special treat for the coding stream participants – a coding MCQ challenge!%0A
%0A
To make sure everything goes smoothly, we kindly request *all* participants (all streams: coding/hacking) to fill out the Excel Sheet provided at the following link: https://docs.google.com/spreadsheets/d/1pws9FmdsOT-jlIVZMezNwvx9Qe6qKF1HvlnMduf2J3g/edit?usp=sharing. Your timely responses will greatly assist us in preparing for the event.%0A
%0A
Additionally, we have set up a dedicated WhatsApp group to facilitate communication and updates. Join the group using the following link: https://chat.whatsapp.com/BTb5PSWzfz0FsKmY8LtZZF%0A
%0A
Please note that the MCQ challenge is exclusive to the coding stream participants. We invite all participants to fill out the Excel Sheet and join the WhatsApp group, but only those in the coding stream will be participating in the MCQs.%0A
%0A
Get your coding hats on and be ready for an engaging and intellectually stimulating experience. If you have any last-minute questions, feel free to reach out to us.%0A
%0A
Looking forward to seeing you all shine in the hackathon!%0A
%0A
Best regards,%0A
%0AThe Eye, CSEA
%0APSG College of Technology
%0APlease do not reply to this message, as this is an automated notification.'''

    # sendmail("21Z202@psgtech.ac.in",
    #      f"{person['roll_no']}@psgtech.ac.in",
    #      "smtp.gmail.com",
    #      "pmEc68SzMM1W5jSYdpyk",
    #      txt.replace("%0A","\n"),
    #      txt.replace("%0A","<br/>"),
    #      "[The Eye] Briefing and Planning '23")

    driver.get(f"https://web.whatsapp.com/send/?phone=91{person['phone_no']}&text={txt}&type=phone_number&app_absent=0")

    WebDriverWait(driver, 500).until(EC.presence_of_element_located((By.XPATH, "//*[@aria-label='Attach']")))
    
    send_xpath = '//button[@aria-label="Send"]'
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, send_xpath)))

    send_button = driver.find_element(By.XPATH, send_xpath)
    send_button.click()
    # pyautogui.press('enter')
    try:
        alert = driver.switch_to.alert()
        alert.accept()
    except:
        pass
    sleep(0.75)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

driver.quit()