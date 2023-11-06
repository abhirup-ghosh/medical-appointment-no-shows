## Setting up your EC2 instance

Pre-requisites:
* [Opening an AWS account](https://mlbookcamp.com/article/aws)
* [Launching an EC2 instance](https://mlbookcamp.com/article/aws-ec2)

EC2 is a fancy name for an Linux machine. Since this was my first time working with an EC2 instance, I put down some basic instructions of setting up my environment on the Ubuntu EC2 instance.

SSH into AWS EC2 instance:
```
ssh -i "jupyter.pem" ubuntu@<${Public_IPv4_DNS}>.compute.amazonaws.com # jupyter.pem: key-pair file
```

and create a basic directory structure:
```
ubuntu@ip-172-31-26-0:~$ mkdir Documents Downloads
```

## Installing Conda



Download the installer:
```
ubuntu@ip-172-31-26-0:~$ cd Downloads/
ubuntu@ip-172-31-26-0:~/Downloads$ wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
```
Verify your installer hashes.
```
ubuntu@ip-172-31-26-0:~/Downloads$ shasum -a 256 Miniconda3-latest-Linux-x86_64.sh 
43651393236cb8bb4219dcd429b3803a60f318e5507d8d84ca00dafa0c69f1bb  Miniconda3-latest-Linux-x86_64.sh
```

Install Miniconda:
```
ubuntu@ip-172-31-26-0:~$ bash Miniconda3-latest-Linux-x86_64.sh

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
```

## Launch Jupyter notebook

On EC2:

```
>>> conda activate ml-zoomcamp
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