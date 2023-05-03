
from flask import Flask, render_template, request, redirect, url_for, abort, jsonify, send_file
from datetime import datetime
from Functions import *


app = Flask(__name__)

ip="192.168.1.104:23336" #### ændre ip-adressen så den passer med hvor topdesk kører




@app.route('/', methods=['GET', 'POST'])
def booking():
    timeslot = ["8:00-9:00", "9:00-10:00", "10:00-11:00", "11:00-12:00", "12:00-13:00", "13:00-14:00", "14:00-15:00", "15:00-16:00", "16:00-17:00"]
    today_date = getTodaysDate()
    #lav funktion til at sende request
    #og returner datapakken
    mydict = {
     "msg": today_date
    }
    answer = requestDailyBookings(mydict, ip).json()
    print("topdesk message: {}".format(answer["answer"]))
    dailyBookings = answer["bookings"]
    print(dailyBookings)

    # lav funktion der samler information om hvad der er optaget på dags dato
    # feed it to template og make jinja - DONE
    booking_availiability = setBookingAvailiability(dailyBookings, timeslot)
    print(booking_availiability)

   
    if request.method == 'POST':
        reserved_timeslot = request.form.getlist('checkbox')
        if len(reserved_timeslot) == 0:
            errorMsg = "Du skal vælge et tidsrum!"
            return render_template('podcastbooking.html', timeslots = timeslot, bookingstatus=booking_availiability, numberOfTimeslots = len(timeslot), error = errorMsg)
        else:
            reservation_email = request.form['Email']
            print(reserved_timeslot)
            print(reservation_email)
            current_dateTime = datetime.now()
            reservation_date = "{}/{}/{}".format(current_dateTime.day, current_dateTime.month, current_dateTime.year)
            print(reservation_date)
            ### lav funktion der sender email i request og får permission status retur - DONE
            mydict = {
                    "msg": reservation_email
                    }
            answer = requestBookingPermission(mydict,ip).json()
            print("topdesk message: {}".format(answer["answer"]))
            permission = answer["answer"]


            # To-DO! lav if-statement der returner template med error msg  om ugyldig email - Done
            if permission == "Nope":
                errorMsg = "Email kunne ikke genkendes!"
                return render_template('podcastbooking.html', timeslots = timeslot, bookingstatus=booking_availiability, numberOfTimeslots = len(timeslot), error = errorMsg) 
            else:
                #retuner primary key på email match
                userID = answer["UserID"]
                print(userID)

                #vi skal skrive funktion der sender bookinginformation til topdesk
                mydict = {
                    "msg": "ny Booking",
                    "UserID": userID,
                    "date": reservation_date,
                    "timeslots": reserved_timeslot
                    }
                answer = requestNewBooking(mydict,ip).json()
                print("topdesk message: {}".format(answer["answer"]))


                if answer["answer"] == "Fail":
                    errorMsg = "Der opstod en fejl!"
                    return render_template('podcastbooking.html', timeslots = timeslot, bookingstatus=booking_availiability, numberOfTimeslots = len(timeslot), error = errorMsg) 
                else:

            # To-DO! skriv funktion til at sende email notifikation om booking til angivne email
                    receiver = reservation_email
                    subject = "Podcast Studio Booking Notifikation"
                    msg = '''
                            <html>
                                <body>
                                    <h1> Goddag!
                                    <br>
                                    <p> Du har i dag {} booket podcast studiet
                                    <br>
                                    <p> i følgende tidsrum {}.
                                <body>
                            <html>
                    
                            '''.format(reservation_date, reserved_timeslot)
                    sendhtmlemail(receiver, subject, msg) 
                    print("email has been sent to {}".format(reservation_email))


                    return redirect('/')


        
    return render_template('podcastbooking.html', timeslots = timeslot, bookingstatus=booking_availiability, numberOfTimeslots = len(timeslot)) 
    






if __name__ == '__main__':
    app.run(debug=True)






# to-Do: lav pæn email - designer inde over 
