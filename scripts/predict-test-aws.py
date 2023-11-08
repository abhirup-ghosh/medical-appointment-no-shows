import requests
import pandas as pd

host = "no-show-predictor-env.eba-hpbyckm2.eu-north-1.elasticbeanstalk.com"
url = f"http://{host}/predict"

test_appointment = {
                    'PatientId': 377511518121127.0,
                    'AppointmentID': 5629448,
                    'Gender': 'F',
                    'ScheduledDay': '2016-04-27 13:30:56+0000',
                    'AppointmentDay': '2016-06-07 00:00:00+0000',
                    'Age': 54,
                    'Neighbourhood': 'MARIA ORTIZ',
                    'Scholarship': False,
                    'Hipertension': False,
                    'Diabetes': False,
                    'Alcoholism': False,
                    'Handcap': 0,
                    'SMS_received': True
                    }

response = requests.post(url, json=test_appointment).json()
print(response)

