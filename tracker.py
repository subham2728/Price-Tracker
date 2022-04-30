import requests
from bs4 import BeautifulSoup
import smtplib
import os
from dotenv import load_dotenv
from email.message import EmailMessage
import GithubAutoRepo

flipkart_price=0
amazon_price=0

load_dotenv()
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
PASSWORD = os.environ.get("PASSWORD")
PORT_NUMBER = os.environ.get("PORT_NUMBER")
RECEIVER_EMAIL = os.environ.get("RECEIVER_EMAIL")
URL_FLIPKART = os.environ.get("URL_FLIPKART")
URL_AMAZON = os.environ.get("URL_AMAZON")
GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REPO_PATH = os.getcwd()

GithubAutoRepo.autoRepo(REPO_PATH,GITHUB_TOKEN,GITHUB_USERNAME)

def flipkart():
    r = requests.get(URL_FLIPKART)
    htmlContent = r.content
    soup = BeautifulSoup(htmlContent, 'html.parser')
    flipkart_price = str(soup.find_all("div", class_="_30jeq3 _16Jk6d")).replace('[<div class="_30jeq3 _16Jk6d">','').replace('</div>]','')
    print(flipkart_price)

def amazon():
    r = requests.get(URL_AMAZON)
    htmlContent = r.content
    soup = BeautifulSoup(htmlContent, 'html.parser')
    amazon_price = (soup.find_all("span", class_="a-offscreen"))
    print(amazon_price)

def send_email():
    server=smtplib.SMTP('smtp.gmail.com',PORT_NUMBER)
    msg = EmailMessage()
    msg.set_content(check)
    msg['Subject'] = 'PRICE CHANGED'
    msg['From'] = SENDER_EMAIL
    msg['To'] =RECEIVER_EMAIL

    server.starttls()
    try:
        server.login(SENDER_EMAIL,PASSWORD)
        print("Login success")

        try:
          server.send_message(msg)
          print("Mail sent")
          time.sleep(1)
          print("Mail sent to : \n",RECEIVER_EMAIL)
          server.quit()
        except:
          print("Failed to sent")
    except:
        print("Login Fail")


if __name__=="__main__":
    flipkart()
    amazon()
