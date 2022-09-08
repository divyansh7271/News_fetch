import datetime
import requests
from bs4 import BeautifulSoup
import redis


class Scraper:
    def __init__(self):
        self.markup = requests.get('https://ndtv.com/').text
        # self.keywords = keywords

    def parse(self):
        soup = BeautifulSoup(self.markup,'html.parser')
        links = soup.findAll("a",{"class": "item-title"})
        # print(links)
        self.saved_links = []
        for link in links:
            self.saved_links.append(link)
  

    def store(self):
        r = redis.Redis(host='localhost', port=6379, db=0)
        count = 0
        for link in self.saved_links:
            if count<=10:
                r.set(link.text, str(link))
                count = count + 1

    def email(self):
        r = redis.Redis(host='localhost', port=6379, db=0)
        links = [str(r.get(k)) for k in r.keys()]


        # email
        import smtplib

        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText

        me = "codevoldemort@gmail.com"
        you = "divyansh7271yt@gmail.com"

        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Link"
        msg['From'] = me
        msg['To'] = you
        password = ""

        # Create the body of the message (a plain-text and an HTML version).
        html = """
            <h4> %s links you might find interesting today:</h4>

            %s

        """ %(len(links), '<br></br>'.join(links))

        mime = MIMEText(html, 'html')
        msg.attach(mime)

        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.ehlo()
        mail.starttls()
        mail.login(me,password)
        mail.sendmail(me, you, msg.as_string())
        mail.quit()
        print('Email Sent')

        r.flushdb()        


s = Scraper()
s.parse()
s.store()
s.email()
# if datetime.datetime.now().hour == 10:
#     s.email()
