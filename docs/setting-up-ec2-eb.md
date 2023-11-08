# Setting up your EC2 instance

Pre-requisites:
* [Opening an AWS account](https://mlbookcamp.com/article/aws)
* [Launching an EC2 instance](https://mlbookcamp.com/article/aws-ec2)

EC2 is a fancy name for an Linux machine. Since this was my first time working with an EC2 instance, I put down some basic instructions of setting up my environment on the Ubuntu EC2 instance.

## Access instance and basic setup

SSH into AWS EC2 instance:
```
>>> ssh -i "jupyter.pem" ubuntu@<${Public_IPv4_DNS}>.compute.amazonaws.com # jupyter.pem: key-pair file
```

and create a basic directory structure:
```
>>> mkdir Documents Downloads
```

## Clone project repository

```
>>> mkdir -p Documents/projects
>>> cd Documents/projects
>>> git clone https://github.com/abhirup-ghosh/medical-appointment-no-shows.git
```

## Install Conda and create course environment

Download the installer:
```
>>> cd Downloads/
>>> wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
```
Verify your installer hashes.
```
>>> shasum -a 256 Miniconda3-latest-Linux-x86_64.sh 
43651393236cb8bb4219dcd429b3803a60f318e5507d8d84ca00dafa0c69f1bb  Miniconda3-latest-Linux-x86_64.sh
```

Install Miniconda:
```
>>> bash Miniconda3-latest-Linux-x86_64.sh

In order to continue the installation process, please review the license
agreement.
Please, press ENTER to continue
>>> 

Do you accept the license terms? [yes|no]
[no] >>> yes

Miniconda3 will now be installed into this location:
/home/ubuntu/miniconda3

  - Press ENTER to confirm the location
  - Press CTRL-C to abort the installation
  - Or specify a different location below

[/home/ubuntu/miniconda3] >>> 
PREFIX=/home/ubuntu/miniconda3


You can undo this by running `conda init --reverse $SHELL`? [yes|no]
[no] >>> yes
```

Install course conda environment [optional]:

```
>>> conda create -n ml-zoomcamp python=3.9
>>> conda activate ml-zoomcamp
>>> conda install numpy pandas scikit-learn seaborn jupyter
```

## Launch Jupyter notebook

On EC2:

```
>>> conda activate ml-zoomcamp
>>> cd cd Documents/projects/medical-appointment-no-shows
>>> jupyter notebook --ip=0.0.0.0 --no-browser --port 8888
.
.
.
    To access the notebook, open this file in a browser:
        file:///home/ubuntu/.local/share/jupyter/runtime/nbserver-3029-open.html
    Or copy and paste one of these URLs:
        http://ip-172-31-26-0:8888/?token=<TOKEN>
     or http://127.0.0.1:8888/?token=<TOKEN>
```

On local machine:

```
>>> ssh -L 8888:localhost:8888 -i "jupyter.pem" ubuntu@ubuntu@<${Public_IPv4_DNS}>.compute.amazonaws.com
```

On local machine browser:

```
http://localhost:8888
```

This will prompt a token input. Provide `<TOKEN>` from the above step.


## Install, Start and Test Docker

Updating package index: Before installing Docker, you should update the package index:

```
>>> sudo apt-get update
```

Installing docker: To install Docker on Ubuntu, you can use the following command:


```
>>> sudo apt-get install docker.io -y
```

Starting the Docker service: After installing Docker, you will need to start the Docker service:

```
>>> sudo systemctl start docker
```

At this point, it is worth exploring running docker without sudo privileges. You could follow the instructions in this page:
https://stackoverflow.com/questions/48957195/how-to-fix-docker-got-permission-denied-issue


```
>>> # Create the docker group if it does not exist
>>> sudo groupadd docker

>>> # Add your user to the docker group.
>>> sudo usermod -aG docker $USER

>>> # Log in to the new docker group (to avoid having to log out / log in again; but if not enough, try to reboot):
>>> newgrp docker
```
Verifying the installation: Once you have started the Docker service, you can verify that it is running by running the following command in your terminal:

```
>>> docker run hello-world
```

## Setting up Elastic Beanstalk application

Install `pipenv` using `pip`: 
```
>>> pip install pipenv
```

Using `pipenv` install relevant packages including `awsebcli`
```
>>> pipenv install gunicorn flask pandas scikit-learn lightgbm awsebcli
```

Run a command inside the virtualenv with `pipenv run`. Alternatively, to activate this project's virtualenv, run:

```
>>> pipenv shell
```

Initialise the elastic beanstalk repository:

```
>>> eb init -p "Docker running on 64bit Amazon Linux 2" -r eu-north-1 no-show-predictor
You have not yet set up your credentials or your credentials are incorrect 
You must provide your credentials.
(aws-access-id): AKIA****
(aws-secret-key): ****
```

There are a few important points here:
* `-p docker` did not work for me and instead had to be replaced by a more detailed `-p "Docker running on 64bit Amazon Linux 2"`
* It prompted my aws-access-id and key which had to be generated using `Security Credentials`


This creates the repository under `.elasticbeanstalk` with a config file:

```
>>> cat .elasticbeanstalk/config.yml                                                                                                                                                                                                           
branch-defaults:                                                                                                                                                                                                                                                                                                              
  main:                                                                                                                                                                                                                                                                                                                       
    environment: null                                                                                                                                                                                                                                                                                                         
global:                                                                                                                                                                                                                                                                                                                         application_name: no-show-predictor
  branch: null
  default_ec2_keyname: null
  default_platform: Docker running on 64bit Amazon Linux 2
  default_region: eu-north-1
  include_git_submodules: true
  instance_profile: null
  platform_name: null
  platform_version: null
  profile: eb-cli
  repository: null
  sc: git
  workspace_type: Application
```

Run the elastic beanstalk repository using:
```
>>> eb local run --port 9696
```

This automatically launches the `gunicorn` bind, which can then be accessed from another tab using:

```
>>> python scripts/predict-test.py
# {'no_show': False, 'no_show_probability': 0.2880257379453167}  
```

## Creating the application environment

```
# In case you are not already in the pipenv environment
>>> pipenv shell
```

Create the environment using:

```
>>> eb create no-show-predictor-env
Creating application version archive "app-23d6-231108_160635019599".
Uploading no-show-predictor/app-23d6-231108_160635019599.zip to S3. This may take a while.
Upload Complete.
Environment details for: no-show-predictor-env
  Application name: no-show-predictor
  Region: eu-north-1
  Deployed Version: ****
  Environment ID: ****
  Platform: arn:aws:elasticbeanstalk:eu-north-1::platform/Docker running on 64bit Amazon Linux 2/3.6.3
  Tier: WebServer-Standard-1.0
  CNAME: UNKNOWN
  Updated: 2023-11-08 16:06:39.154000+00:00
Printing Status:
2023-11-08 16:06:37    INFO    createEnvironment is starting.
2023-11-08 16:06:39    INFO    Using elasticbeanstalk-eu-north-1-166783209982 as Amazon S3 storage bucket for environment data.
2023-11-08 16:06:59    INFO    Created security group named: ****
2023-11-08 16:07:14    INFO    Created security group named: ****
2023-11-08 16:07:14    INFO    Created target group named: ****
2023-11-08 16:07:14    INFO    Created Auto Scaling launch configuration named: ****
2023-11-08 16:07:45    INFO    Created Auto Scaling group named: ****
2023-11-08 16:07:45    INFO    Waiting for EC2 instances to launch. This may take a few minutes.
2023-11-08 16:07:45    INFO    Created Auto Scaling group policy named: ****
2023-11-08 16:07:45    INFO    Created Auto Scaling group policy named: ****
2023-11-08 16:07:45    INFO    Created CloudWatch alarm named: ****
2023-11-08 16:07:45    INFO    Created CloudWatch alarm named: ****
2023-11-08 16:09:05    INFO    Created load balancer named: ****
2023-11-08 16:09:05    INFO    Created Load Balancer listener named: ****
2023-11-08 16:10:37    INFO    Instance deployment completed successfully.
2023-11-08 16:10:50    INFO    Application available at no-show-predictor-env.eba-hpbyckm2.eu-north-1.elasticbeanstalk.com.
2023-11-08 16:10:51    INFO    Successfully launched environment: no-show-predictor-env
```

Thus we created an AWS Elastic Beanstalk environment for the "no-show-predictor" application. It includes steps such as uploading the application archive to Amazon S3, setting up various resources like security groups and load balancers, and ensuring the application is successfully deployed and accessible at a specific URL.