import pickle

from flask import Flask
from flask import request
from flask import jsonify

import numpy as np
import pandas as pd


def prepare_data(df, test=False):
    df.rename(columns={'Hipertension':'Hypertension'}, inplace=True)
    df['ScheduledDay'] = pd.to_datetime(df['ScheduledDay'])
    df['AppointmentDay'] = pd.to_datetime(df['AppointmentDay'])
    
    # Make the column names lower-case and uniform
    df.columns = df.columns.str.lower().str.replace('-', '_')

    # Make the string values of categorical columns lower-case and uniform
    categorical_columns = df.dtypes[df.dtypes == 'object'].index.tolist()
    for col in categorical_columns:
        df[col] = df[col].str.lower().str.replace(' ', '_')

    # Make the target variable boolean
    if test==False:
        df.no_show = (df.no_show == 'yes').astype(int)       

    return df

def feature_engineering(df):
    # Credit: https://github.com/fastai/fastai/blob/master/fastai/tabular/core.py#L26

    attr = ['Year', 'Month', 'Week', 'Day', 
            'Dayofweek', 'Dayofyear', 
            'Is_month_end', 'Is_month_start', 
            'Is_quarter_end', 'Is_quarter_start',  
            'Hour', 'Minute', 'Second']

    for field_name in ['scheduledday', 'appointmentday']:

        field = df[field_name]
        prefix = field_name
        
        week = field.dt.isocalendar().week.astype(field.dt.day.dtype) if hasattr(field.dt, 'isocalendar') else field.dt.week
        for n in attr: df[prefix + n] = getattr(field.dt, n.lower()) if n != 'Week' else week   

        df.drop(field_name, axis=1, inplace=True)

    return df

def prepare_test(test_appointment):
    df_test = pd.DataFrame(test_appointment, index=[0])
    df_test = prepare_data(df_test, test=True)
    df_test = feature_engineering(df_test)
    df_test = df_test[numerical + categorical]

    X_test_num = scaler.transform(df_test[numerical])
    X_test_cat = ohe.transform(df_test[categorical])
    X_test = np.column_stack([X_test_num, X_test_cat])

    return X_test

numerical = [
        'patientid',
        'age',
        'scheduleddayWeek',
        'scheduleddayDay',
        'scheduleddayDayofyear',
        'scheduleddayHour',
        'scheduleddayMinute',
        'scheduleddaySecond',
        'appointmentdayDay',
        'appointmentdayDayofyear'
        ]

categorical = [
            'gender',
            'scholarship',
            'hypertension',
            'diabetes',
            'alcoholism',
            'handcap',
            'sms_received',
            'scheduleddayYear',
            'scheduleddayMonth',
            'scheduleddayDayofweek',
            'scheduleddayIs_month_end',
            'scheduleddayIs_month_start',
            'scheduleddayIs_quarter_end',
            'scheduleddayIs_quarter_start',
            'appointmentdayMonth',
            'appointmentdayWeek',
            'appointmentdayDayofweek',
            'appointmentdayIs_month_end',
            'appointmentdayIs_month_start',
            'neighbourhood'
        ]

model_file = '../models/LGBMClassifier_tranformers_final.bin'

with open(model_file, 'rb') as f_in:
    scaler, ohe, model = pickle.load(f_in)

app = Flask('noshow')

@app.route('/predict', methods=['POST'])
def predict():
    test_appointment = request.get_json()

    X_test = prepare_test(test_appointment)
    
    y_pred = model.predict_proba(X_test)[0,1]
    
    no_show = y_pred >= 0.5

    result = {
        'no_show_probability': float(y_pred),
        'no_show': bool(no_show)
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)