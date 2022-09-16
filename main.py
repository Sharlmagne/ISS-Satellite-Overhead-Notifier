import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 00.000000
MY_LONG = 00.000000
MY_EMAIL = "sending_email@email.com"
APP_PASSWORD = "**************"
RECEIVING_EMAIL = "receiving_email@email.com"


# Check if the ISS Satellite is above current location
def is_iss_above():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG:
        return True
    else:
        return False


# Check for nighttime
def is_dark():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()

    time_now = int(datetime.now().time().hour)
    sunset = int(data["results"]["sunset"][11:13]) - 5
    sunrise = int(data["results"]["sunrise"][11:13])

    print("sunset:", sunset)
    print("sunrise:", sunrise)
    print("time now:", time_now)

    if sunset <= time_now <= sunrise - 5:
        return True
    else:
        return False


# Send email
def send_email(subject, body, email_address):
    with smtplib.SMTP('64.233.184.108', port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=APP_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=email_address,
            msg=f"Subject:{subject}\n\n{body}"
        )


while True:
    if is_iss_above() and is_dark():
        time.sleep(60)
        send_email("Lookup!", "The ISS is currently above your location.", RECEIVING_EMAIL)


