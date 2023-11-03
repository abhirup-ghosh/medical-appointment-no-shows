# Predicting no-shows in medical appointments

## Table of Contents
- [Project Overview](#project-overview)
- [Datasets](#datasets)
- [Directory structure](#dirctory-structure)
- [Dependencies](#dependencies)
- [Workflow](#workflow)
  - [Modelling workflow](#modelling-workflow)
  - [Deployment workflow](#deployment-workflow)

---

## [Project Overview](#project-overview)

This machine learning project focuses on addressing the issue of patient no-shows in medical appointments. Predicting whether a patient will show up for their scheduled medical appointment is a critical task for healthcare providers as it can help optimize resource allocation and improve overall patient care. By harnessing the power of data and machine learning, we aim to develop a predictive model that can assist healthcare facilities in identifying patients at higher risk of no-shows.

## [Datasets](#datasets)

This project uses a Kaggle dataset of over 100,000 medical appointments characterised by 14 associated variables, including temporal details, patient information and the ultimate outcome (and the **target variable** of our classification task) of the appointment -- whether the patient showed up for the appointment or not. The dataset was created by * [Joni Hoppen](https://www.linkedin.com/in/jonihoppen/) and [Aquarela Analytics](https://www.linkedin.com/company/aquare-la/), and can be downloaded from:
```
https://www.kaggle.com/datasets/joniarroba/noshowappointments/data
```

Further details of the datasets used can be found [here](./data/README.md).

## [Project Structure](#project-structure)

The project consists of the following components [Long-form details [here](./docs/DataScienceWorkflow_CheatSheet.pdf)]:

- **Data Wrangling and Preprocessing:** This step involves loading the datasets, examining their contents, and performing necessary data cleaning, integration, transformation, reduction and formatting. Finally we save the preprocessed dataset and split it into training, validation and test sets. Details are provided in [this notebook](./notebooks/data-wrangling-preprocessing.ipynb).

- **Data Exploration:** After data wrangling, the dataset is explored to gain insights and understand the distribution and relationships between variables. Descriptive statistics and visualizations are used to analyze the data. Details are provided in [this notebook](./notebooks/data-exploration.ipynb).

- **Feature Selection and Engineering:** Feature selection techniques are applied to identify the most relevant features for predicting individual defensive performance. Additionally, feature engineering is performed to create new informative features that can enhance the model's predictive capabilities.

- Model Development and Evaluation: Various machine learning algorithms are trained and evaluated using appropriate evaluation metrics. The models are fine-tuned using techniques such as cross-validation and hyperparameter optimization to improve their performance.

- Handling Imbalanced Data: If the dataset exhibits class imbalance (e.g., uneven distribution of defensive performance classes), techniques for handling imbalanced data, such as oversampling or undersampling, are applied to address this issue.

- Model Deployment: Once a satisfactory model is obtained, it can be deployed for practical use. This step involves saving the trained model, setting up the necessary infrastructure (e.g., hosting platform), and creating an interface (e.g., API) for making predictions.


## [Dependencies](#dependencies) [**WIP**]

The project requires the following dependencies to be installed:

```
Docker
Terraform
Docker Compose
```

## Getting Started/Workflow [**WIP**]

To run this project locally, follow these steps:

1. Clone the repository: `git clone https://github.com/your/repository.git`
2. Install the required dependencies: `pip install -r opt/requirements.txt`
3. Download the datasets and place it in the appropriate directory.
4. Run the project scripts in the order specified in the project structure section.


## [Directory structure](#dirctory-structure) [**WIP**]

```bash
football-advanced-performance-metrics/
|-- data/                           # raw and processed data used in the project.
|   |-- raw/                        # the original data files, such as credit_data.csv.
|   |   |-- dataset.csv             
|   |   |-- template.csv            
|   |-- predictions/                # the predictions of the model.
|   |   |-- test_predictions.csv            
|-- models/                         # models built.
|   |-- model.joblib
|-- docs/                           # documentation for the project, such as project requirements, design documents, and user guides.
|-- notebooks/                      # Jupyter notebooks for each stage of the workflow.
|   |-- exploration/                # notebooks related to data exploration.
|   |   |-- data_exploration.ipynb  # the code for exploring and visualizing the data.
|   |-- modelling/                  # notebooks related to data modelling.
|   |   |-- data_modelling.ipynb    # the code for modelling.
|-- opt/                            # optional code for the project
|   |-- requirements.txt            # pre-requisite pip-installable packages
|-- src/                            # source code for the project.
|   |-- train.py                    # the code for the final model.
|   |-- constants.py                # the code for the features.
|   |-- server.py                   # the code query the REST API.
|   |-- __init__.py                 # a file that makes the src directory a Python package.
|-- tests/                          # code for testing the project.
|   |-- __init__.py                 # a file that makes the tests directory a Python package.
|   |-- make_predictions_with_api.py # a file to make predictions using the API.
|   |-- send_valid_request.sh       # a file that makes sure that API works (sends to localhost:5001).
|-- README.md                       # title-page: a brief description of the project.
|-- LICENSE                         # the license under which the project is distributed: MIT License
|-- Dockerfile                      # Dockerfile [created image ~2GB]
|-- docker-compose.yaml
```

## Contributors
Abhirup Ghosh, <abhirup.ghosh.184098@gmail.com>



## License
This project is licensed under the [MIT License](./LICENSE).

## Acknowledgments
Acknowledgment 1
Acknowledgment 2

## Follow-ups/Next steps
* Fix: target variable and input features
  * how is a defender judged
  * where can we feel the most impact
  * multi-target variable prediction: find a way to predict each attribute depending on it's own set of features
  * target variables can be derived, advanced metrics regarding each attribute.
* Move onto feature selection/engineering: Advanced defensive metrics

## Contributions and Feedback:

We welcome contributions from the community and feedback from healthcare professionals and data scientists. Together, we can refine our model and enhance its utility in real-world healthcare settings.

Feel free to explore the project, contribute, or reach out with any questions or suggestions. Together, we can work towards a healthcare system that is more efficient, patient-centered, and cost-effective.


