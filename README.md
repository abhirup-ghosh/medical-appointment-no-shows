# Predicting no-shows in medical appointments

## Table of Contents
- [Project Overview](#project-overview)
- [Datasets](#datasets)
- [Dependencies](#dependencies)
- [Getting Started](#getting-started)
- [Directory structure](#dirctory-structure)
- [Models](#models)
- [Contributors](#contributors)
- [License](#license)
- [Acknowledgments](#acknowledgments)
- [Contributions and Feedback](#contributions-and-feedback)

---

## [Project Overview](#project-overview)

Predicting whether a patient will show up for their scheduled medical appointment is a critical task for healthcare providers as it can help optimize resource allocation and improve overall patient care. This machine learning project focuses on addressing the issue of patient no-shows in medical appointments. By harnessing the power of data and machine learning, we aim to develop a predictive model that can assist healthcare facilities in identifying patients at higher risk of no-shows. 


Starting with a Kaggle data of medical appointment no-shows by [Joni Hoppen](https://www.linkedin.com/in/jonihoppen/) and [Aquarela Analytics](https://www.linkedin.com/company/aquare-la/), we evaluate the performances of four different classification algorithms (Logistic Regression, Decision Trees, Random Forests, XGBoost, and LightGBM) and settle on an `LGBMClassifier` model as our final model. Using the trained model we make predictions on whether a future appointment would lead to a no-show or not. Finally, we containerise this application and deploy it on the cloud.

![Title Image](./data/no-show-patients.jpg)

Credit: Austrian Medical Association (ÖÄK)

## [Datasets](#datasets)

This project uses a Kaggle dataset of over 100,000 medical appointments characterised by 14 associated variables, including temporal details, patient information and the ultimate outcome (and the **target variable** of our classification task) of the appointment -- whether the patient showed up for the appointment or not. The dataset was created by [Joni Hoppen](https://www.linkedin.com/in/jonihoppen/) and [Aquarela Analytics](https://www.linkedin.com/company/aquare-la/), and can be downloaded from:
```
https://www.kaggle.com/datasets/joniarroba/noshowappointments/data
```

Further details of the datasets used can be found [here](./data/README.md).

## [Dependencies](#dependencies)

The project requires the following dependencies to be installed:

```
Conda
Docker
```

## [Getting Started](#getting-started)

To run this project locally, follow these steps:

### 1. Clone the repository: 


```
git clone https://github.com/abhirup-ghosh/medical-appointment-no-shows.git
```


### 2. **Setting up the environment:**

The easiest way to set up the environment is to use [Anaconda](https://www.anaconda.com/download). I used the standard Machine Learning Zoomcamp conda environment `ml-zoomcamp`, which you can create, activate, and install the relevant libraries in, using the following commands in your terminal:

```
conda create -n ml-zoomcamp python=3.9
conda activate ml-zoomcamp
conda install numpy pandas scikit-learn seaborn jupyter xgboost pipenv flask gunicorn lightgbm
```

Alternatively, I have also provided a conda `environment.yml` file that can be directly used to create the environment:

```
conda env create -f opt/environment.yml
```

In case, you are working in a python virtual environment, I provide a list of dependencies that can be pip installed using:
```
pip install -r opt/optional_requirements.txt
```

### 3. Running `notebooks/notebook.ipynb`

This notebook outlines the entire investigation and consists of the following steps [🚨 Skip this step, if you want to directly want to use the final configuration for training and/or final model for predictions]:

- Data loading
- Data cleaning and preparation
- Exploratory data analysis
- Feature Engineering
- Feature importance
- Setting up a validation framwork
- Model evaluation [and hyper-parameter tuning]
- Saving the best model and encoders [in the [models](../models) directory]
- Preparation of the test data
- Making predictions using the saved model
- Testing Flask framework

### 4. Training model

We encode our best model (LGBMClassifier) inside the `scripts/train.py` file which can be run using:
```
cd scripts
python train.py
```

The output of this script, which includes the model and the encoder/scaler transforms, can be found in: `models/LGBMClassifier_tranformers_final.bin`. It have an accuracy of **0.807** and an ROC AUC = **0.797**. This is the model we use to make predictions in the next steps.

### 5. Making predictions

We have written a Flask code for serving the model by exposing the port:9696, which can be run using:

```
cd scripts
python predict.py
```
or `gunicorn` as:
```
cd scripts
gunicorn --bind 0.0.0.0:9696 predict:app
```

We can use this to make an example prediction on the appointment:

```
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
```

using the command:

```
cd scripts
python predict-test.py
# {'no_show': False, 'no_show_probability': 0.2880257379453167}
```

This gives us a `no_show` class [0 or 1] as well as a probability.

🚨 Always remember to `conda activate ml-zoomcamp` whenever opening a new terminal/tab.

### 6. Model Deployment

Run the `Dockerfile` using [make sure that the docker daemon is running?] to build the image `no-show-prediction`:

```
docker build -t no-show-prediction .
```

We can access the docker container via the terminal using:
```
docker run -it --rm --entrypoint=bash no-show-prediction
```

Once the image is built, we need to expose the container port (9696) to the localhost port (9696) using:

```
docker run -it --rm -p 9696:9696 no-show-prediction
```

We can now make a request in exactly the same way as Step 5:

```
cd scripts
python predict-test.py
# {'no_show': False, 'no_show_probability': 0.2880257379453167}
```

## [Models](#models)

We evaluated the performances of four different models. Their accuracies and ROC AUC are listed in the table below:

|Model                          | Accuracy 	| ROC_AUC 	|
|-----                          | -------- 	| ------- 	|
|LogisticRegression             | 0.792 	| 0.686 	|
|DecisionTreeClassifier         | 0.793 	| 0.725 	|
|RandomForestClassifier         | 0.793 	| 0.682 	|
|XGBClassifier                  | 0.796 	| 0.749 	|
|LGBMClassifier ✅              | 0.796   | 0.752   |

Our final model, LGBMClassifier, produced a score of **0.807** and an ROC AUC = **0.797**.

## [Directory structure](#dirctory-structure)

```bash
./medical-appointment-no-shows
├── scripts
│   ├── train.py
│   ├── predict.py
│   ├── predict-test.py
│   ├── constants.py
│   └── __pycache__
├── opt
│   ├── optional_requirement.txt
│   └── environment.yml
├── notebooks
│   └── notebook.ipynb
├── models
│   ├── XGBClassifier_tranformers_final.bin
│   ├── XGBClassifier_final.bin
│   ├── XGBClassifier.bin
│   ├── RandomForestClassifier.bin
│   ├── LogisticRegression.bin
│   ├── LGBMClassifier_tranformers_final.bin
│   ├── LGBMClassifier.bin
│   └── DecisionTreeClassifier.bin
├── data
│   ├── README.md
│   └── KaggleV2-May-2016.csv
├── README.md
├── LICENSE
└── Dockerfile
```

## [Contributors](#contributors)
Abhirup Ghosh, <abhirup.ghosh.184098@gmail.com>

## [License](#license)
This project is licensed under the [MIT License](./LICENSE).

## [Acknowledgments](#acknowledgments)
* [Alexey Grigorev](https://github.com/alexeygrigorev)
* [DataTalks.Club](https://datatalks.club/)
* [Joni Hoppen](https://www.linkedin.com/in/jonihoppen/)/[Aquarela Analytics](https://www.linkedin.com/company/aquare-la/)

<!---
## Follow-ups/Next steps
* Fix: target variable and input features
  * how is a defender judged
  * where can we feel the most impact
  * multi-target variable prediction: find a way to predict each attribute depending on it's own set of features
  * target variables can be derived, advanced metrics regarding each attribute.
* Move onto feature selection/engineering: Advanced defensive metrics
-->

## [Contributions and Feedback](#contributions-and-feedback)

We welcome contributions from the community and feedback from healthcare professionals and data scientists. Together, we can refine our model and enhance its utility in real-world healthcare settings. Feel free to explore the project, contribute, or reach out with any questions or suggestions. Together, we can work towards a healthcare system that is more efficient, patient-centered, and cost-effective.


