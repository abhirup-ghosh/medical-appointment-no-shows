# Dataset: Medical Appointment No Shows

This is a Kaggle dataset of over 100,000 medical appointments characterised by 14 associated variables, including temporal details, patient information and the ultimate outcome (and the **target variable** of our classification task) of the appointment -- whether the patient showed up for the appointment or not.

## Source

This is a Kaggle dataset, which can be downloaded from:

```
https://www.kaggle.com/datasets/joniarroba/noshowappointments/data
```


## Dataset details



* Rows: 110,527 [each corresponding to a medical appointment]
* Input features: 14
* Target variable: **"No Show"** column

## Data Dictionary

| Index| Column Name | Description | Datatype |
|--|--|--|--|
|01 | PatientId | Identification of a patient | int |
|02 | AppointmentID | Identification of each appointment | int |
|03 | Gender | Male or Female | string |
|04 | ScheduledDay | The day of the actual appointment, when they have to visit the doctor | datetime |
|05 | AppointmentDay | The day someone called or registered the appointment | datetime |
|06 | Age | How old is the patient | int |
|07 | Neighbourhood | Where the appointment takes place | string |
|08 | Scholarship | Reference: https://en.wikipedia.org/wiki/Bolsa_Fam%C3%ADlia | bool |
|09 | Hypertension | Whether the patient has Hypertension | bool |
|10 | Diabetes | Whether the patient has Diabetes | bool |
|11 | Alcoholism | Whether the patient has been diagnosed with alcoholism | bool |
|12 | Handcap | Number of desabilites a patient has [(explanation provided by creator of dataset)](https://www.kaggle.com/datasets/joniarroba/noshowappointments/discussion/29699#229356) | int |
|13 | SMS_received | 1 or more messages sent to the patient | bool |
|14 | No-show | Whether the patient showed up for the appointment | string |

## Acknowledgement

* [Joni Hoppen](https://www.linkedin.com/in/jonihoppen/)
* [Aquarela Analytics](https://www.linkedin.com/company/aquare-la/)