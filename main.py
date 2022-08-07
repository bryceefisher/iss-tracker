import requests
from datetime import datetime
import time
import math
import smtplib

MY_LAT = 44.085450  # Your latitude
MY_LONG = -123.063350  # Your longitude
MY_EMAIL = ""  # Your email
PASSWORD = ""  # Your password

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

# Your position is within +5 or -5 degrees of the ISS position.


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("http://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.now()

look_for_iss = True

while look_for_iss:
    if time_now.hour > 21 or time_now.hour < 6:
        if math.isclose(MY_LAT, iss_latitude, rel_tol=5) and math.isclose(MY_LONG, iss_longitude, rel_tol=5):
            with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
                connection.starttls()
                connection.login(user=MY_EMAIL, password=PASSWORD)
                connection.sendmail(from_addr=MY_EMAIL,
                                    to_addrs="bryce.e.fisher@gmail.com",
                                    msg="Subject:ISS Notifier\n\nHey Bryce,\nLook Up!")
    time.sleep(60)
