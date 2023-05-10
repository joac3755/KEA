from datetime import datetime
import sqlite3
import smtplib, ssl
import requests


from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def getTodaysDate():
    current_dateTime = datetime.now()
    today_date = "{}/{}/{}".format(current_dateTime.day, current_dateTime.month, current_dateTime.year)
    return today_date


def requestDailyBookings(todays_date, ip):
    url = 'http://{}/api/1337/GetDailyBookings'.format(ip)
    headers = {"Content-Type": "application/json"}
    response = requests.post(url,headers = headers, json=todays_date)
    
    return response



def requestBookingPermission(userEmail,ip):
    url = 'http://{}/api/1337/Get_email_verification'.format(ip)
    headers = {"Content-Type": "application/json"}
    response = requests.post(url,headers = headers, json=userEmail)

    return response



def requestNewBooking(BookingInfo, ip):
    url = 'http://{}/api/1337/Set_new_booking'.format(ip)
    headers = {"Content-Type": "application/json"}
    response = requests.post(url,headers = headers, json=BookingInfo)

    return response






def setBookingAvailiability(daylibookings, timeslots):
    Booking_status = []
    for i in range(0,len(timeslots)):
        tmpBookingStatus = []
        for booking in daylibookings:
            if timeslots[i] == booking[2]:
                tmpBookingStatus.append("Optaget")
                
            else:
                tmpBookingStatus.append("Ledig")
        if "Optaget" in tmpBookingStatus:
            Booking_status.append("Optaget")
        else:
            Booking_status.append("Ledig")
    return Booking_status



def sendhtmlemail(receiver, subject, msg):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "KEAbeitS22@gmail.com"  # Enter your address
    receiver_email = receiver #"KEAbeitS22@gmail.com"  # Enter receiver address
    password = "XXXXXXXXXXXXXXXXXXXXXXXX"



    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails
    body = msg

    message.attach(MIMEText(body, "html"))
    text = message.as_string()


    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
    #print("test")
    pass















