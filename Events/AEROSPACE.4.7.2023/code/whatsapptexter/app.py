from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from time import sleep

import pyautogui

import chromedriver_binary
import jinja2, json

# with open("../reg.json") as f:
#     people = json.load(f)
#     mypeople = []
#     rolls = []
#     tableau = [["#", "Name", "Roll Number", "Email", "Phone Number", "Signature"]]
#     c=0
#     for i in sorted(people, key=lambda d: d['roll_no']):
#         c+=1
#         if i["roll_no"].upper() not in rolls:
#             rolls.append(i["roll_no"].upper())
#             mypeople.append({"#":c,
#                              "name":i["name"],
#                              "roll_no":i["roll_no"],
#                              "phone_no":i["phone_no"]})
#     people = mypeople


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
    txt = f'''Good Afternoon, {person['name']}!

We're thrilled to remind you about today's highly anticipated event, "Aerovision 2023 - Aerospace Cyber Security," happening at the *_GRD Laboratory, E Block, 1st Floor_*. The wait is over, and we're excited to welcome you today to share this remarkable experience.

Your Event Ticket:
Just a quick reminder, please have your event ticket ready for entry. Whether you've got a printed version or a digital copy on your phone, make sure to keep it handy – it's your pass to an unforgettable adventure.

Event Details:
Date: Today - August 22 at *_4:30PM_*
Duration: A day of aviation and cybersecurity excellence

We have an exciting lineup of workshops, a challenging hackathon, and the captivating AvCon presentation conference waiting for you. Don't miss out on this opportunity to immerse yourself in the world of aerospace cybersecurity, connect with industry experts, and fuel your passion for innovation.

Remember to bring your laptops if you can, as they'll come in handy during the interactive sessions.

Get ready for an extraordinary day as we embark on this incredible journey together!

Best regards,
The Eye, CSEA
PSG College of Technology
Please do not reply to this message, as this is an automated notification.'''

    # sendmail("21Z202@psgtech.ac.in",
    #      f"{person['roll_no']}@psgtech.ac.in",
    #      "smtp.gmail.com",
    #      "pmEc68SzMM1W5jSYdpyk",
    #      txt.replace("%0A","\n"),
    #      txt.replace("%0A","<br/>"),
    #      "[The Eye] Briefing and Planning '23")

    driver.get(f"https://web.whatsapp.com/send/?phone=91{person['phone_no']}&type=phone_number&app_absent=0")


    WebDriverWait(driver, 500).until(EC.presence_of_element_located((By.XPATH, "//*[@aria-label='Attach']")))

    attach_btn = driver.find_element(By.XPATH,
                                "//*[@aria-label='Attach']"
        )
    attach_btn.click()
    docu_btn = driver.find_element(By.XPATH,
                                "//*[@class='erpdyial tviruh8d gfz4du6o r7fjleex lhj4utae le5p0ye3']"
        )
    docu_btn.click()

    sleep(0.75)

    pyautogui.typewrite(f"C:\\Users\\aaditya\\Desktop\\BE-CSE\\THE_EYE_CSEA\\Events\\AEROSPACE.4.7.2023\\code\\ticket-generation\\ticket-pdfs\\{person['roll'].upper()}.pdf")
    sleep(0.75)
    pyautogui.press('enter')

    WebDriverWait(driver, 500).until(EC.presence_of_element_located((By.XPATH, "//*[@data-testid='send']")))

    sleep(0.25)

    lines = txt.split('\n')
    for line in lines:
        if "ENTER" in line:
            parts = line.split("ENTER")
            pyautogui.typewrite(parts[0])
            pyautogui.press('enter')
            pyautogui.typewrite(parts[-1])
        else:
            pyautogui.typewrite(line)
        pyautogui.hotkey('shift', 'enter')
    sleep(0.75)
    pyautogui.press('enter')

    

    try:
        alert = driver.switch_to.alert()
        alert.accept()
    except:
        pass
    sleep(3)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

driver.quit()