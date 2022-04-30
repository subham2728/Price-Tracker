import requests
from bs4 import BeautifulSoup
import smtplib
import os
from dotenv import load_dotenv
from email.message import EmailMessage
import time
from datetime import datetime

flipkart_price=0
amazon_price=0

load_dotenv()
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
PASSWORD = os.environ.get("PASSWORD")
PORT_NUMBER = os.environ.get("PORT_NUMBER")
RECEIVER_EMAIL = os.environ.get("RECEIVER_EMAIL")
URL_FLIPKART = os.environ.get("URL_FLIPKART")
URL_AMAZON = os.environ.get("URL_AMAZON")
user_agent = {"User-Agent" : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}


def flipkart():
    req = requests.get(URL_FLIPKART, headers=user_agent)
    htmlContent = req.content
    soup = BeautifulSoup(htmlContent, 'html.parser')
    new_flipkart_price = (soup.find("div", class_="_30jeq3 _16Jk6d")).get_text()
    if(flipkart_price==0):
        flipkart_price=new_flipkart_price
    elif(flipkart_price!=new_flipkart_price):
        content=("Hey Subham, \n Price has been changed in Flipkart \n OLD PRICE = {} \n NEW PRICE = {} ".format(flipkart_price,new_flipkart_price))
        send_email(content)
        flipkart_price=new_flipkart_price

def amazon():
    req = requests.get(URL_AMAZON, headers=user_agent)
    htmlContent = req.content
    soup = BeautifulSoup(htmlContent, 'html.parser')
    new_amazon_price = (soup.find("span", class_="a-offscreen")).get_text()

    if(amazon_price==0):
        amazon_price=new_amazon_price

    elif(amazon_price!=new_amazon_price):
        content=("Hey Subham, \n Price has been changed in Amazon \n OLD PRICE = {} \n NEW PRICE = {} ".format(amazon_price,new_amazon_price))
        send_email(content)
        amazon_price=new_amazon_price

def send_email(content):
    server=smtplib.SMTP('smtp.gmail.com',PORT_NUMBER)
    msg = EmailMessage()
    msg.set_content(content)
    msg['Subject'] = 'PRICE CHANGED'
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL

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
    while True:
        now = datetime.now()
        time = now.strftime("%I:%M")
        if(time=="12:00" or time=="06:00"):
            flipkart()
            amazon()
