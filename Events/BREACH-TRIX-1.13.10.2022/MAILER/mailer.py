from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl, smtplib


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
        print(f"tried sending [{receiver} , {subject} , {text}]; failed due to error : {e}.")

email_msg = f'''Good Morning MF!

Thank you so much for signing up with The Eye for the BREACH'22 workshop 2022. This is a friendly reminder to join the workshop today and tomorrow at 4:30PM.

Venue : GRD Computer Laboratory
Time : 4:30PM

Please bring your own personal laptop if possible. If you cannot do so, it's no problem!

Hope to see you there!

For any queries, please contact Aaditya Rengarajan (21Z202@psgtech.ac.in | +91 94445 11430).'''
sendmail("21Z202@psgtech.ac.in",
         f"aadityarenga@gmail.com",
         "smtp.gmail.com",
         "pmEc68SzMM1W5jSYdpyk",
         email_msg,
         email_msg.replace("\n","<br/>"),
         "[The Eye] Welcomeasdf to BREACH'22!")