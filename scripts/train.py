# # Project: Predicting no-shows in medical appointments

# ## Dependencies

# %%
import pandas as pd
import numpy as np

from sklearn.model_selection import GridSearchCV
from sklearn.metrics import roc_auc_score, accuracy_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder


import lightgbm as lgb
import pickle

#----------------------------------------------------------------------------------------
# # Data Loading
# The Kaggle dataset for this project can be downloaded from: https://www.kaggle.com/datasets/joniarroba/noshowappointments/data
# Details of the dataset, including description of columns and associated datatypes, can be found [here](../data/README.md).
#----------------------------------------------------------------------------------------
print('...loading data')
data_loc = '../data/KaggleV2-May-2016.csv'

df = pd.read_csv(data_loc, 
                 parse_dates=['ScheduledDay', 'AppointmentDay'],
                 dtype={
                            'Scholarship':'bool',
                            'Hipertension':'bool',
                            'Diabetes':'bool',
                            'Alcoholism':'bool',
                            'SMS_received':'bool'
                     }
              )

#----------------------------------------------------------------------------------------
# # Data cleaning and preparation
# * Correct typos
# * Make the column names lower-case and uniform
# * Make the string values of categorical columns lower-case and uniform
# * Impute/Handle missing values [there are no missing values in this dataset]
# * Make the target variable boolean
#----------------------------------------------------------------------------------------
print('...cleaning and preparing data for modelling')
def prepare_data(df, test=False):
    df.rename(columns={'Hipertension':'Hypertension'}, inplace=True)
    
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

df = prepare_data(df)

#----------------------------------------------------------------------------------------
# # Feature Engineering
# * Construct datetime-related features out of 'scheduledday' and 'appointmentday' which can be treated as numerical or categorical data, instead of datetime data
# * Drop columns 'scheduledday' and 'appointmentday'
# * Drop any column which has only 1 unique value
# Credit: https://github.com/fastai/fastai/blob/master/fastai/tabular/core.py#L26
#----------------------------------------------------------------------------------------
print('...engineering features')
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

df = feature_engineering(df)

#----------------------------------------------------------------------------------------
# # Setting up the validation framework 
# * Perform the train/validation/test split with Scikit-Learn
#----------------------------------------------------------------------------------------
print('...separating input features and target variable')
y_train = df.no_show.values

del df['no_show']

#----------------------------------------------------------------------------------------
# # Categorical/Numerical Features
#----------------------------------------------------------------------------------------
print('...separating categorical and numerical features')
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

df = df[numerical + categorical]
#df.head()

#----------------------------------------------------------------------------------------
# # Data Preparation-II: Feature Scaling + OHE
# ### Training set: Feature Scaling
#----------------------------------------------------------------------------------------
print('...encoding/scaling features')
X_train_num = df[numerical]

scaler = StandardScaler()
#scaler = MinMaxScaler()

X_train_num = scaler.fit_transform(X_train_num)

ohe = OneHotEncoder(sparse=False, handle_unknown='ignore')
X_train_cat = ohe.fit_transform(df[categorical])

X_train = np.column_stack([X_train_num, X_train_cat])
features = [feature for feature in np.append(scaler.get_feature_names_out(),ohe.get_feature_names_out())]

#----------------------------------------------------------------------------------------
# # Modelling
# ## LightGBM
#----------------------------------------------------------------------------------------
print('...training using best model')
lgbm_best = lgb.LGBMClassifier(boosting_type='dart',
                                learning_rate=0.1,
                                max_depth=12,
                                n_estimators=500)

lgbm_best.fit(X_train, y_train)

# fitting to training set
print('...evaluation of fit')
y_fit = lgbm_best.predict_proba(X_train)[:, 1]
print('Accuracy:', accuracy_score(y_train, y_fit >= 0.5))
print('AUC ROC:', roc_auc_score(y_train, y_fit))

#----------------------------------------------------------------------------------------
# # Saving model
#----------------------------------------------------------------------------------------
print('...saving model')
model_name = "LGBMClassifier_tranformers_final"

with open(f'../models/{model_name}.bin', 'wb') as f_out: # 'wb' means write-binary
    pickle.dump((scaler, ohe, lgbm_best), f_out)