# The ***Mocean*** project 

This project is about creating an online Service and using that Service from a Python program.
It was originally built for a Middle School Python club; so it begins with games. 
In fact there are two games involved, one called **Steps** and one called **Mocean**. 
**Steps** is a simple interactive text game.
**Mocean** is a more complicated Server~Client online game in the spirit of **Among Us**.
It supports multiple players exploring
an alien world in parallel. The idea is the students build their own
Client applications to play this game. 


This project has a lot in common with creating data services
for research. For this reason this document extends beyond installing 
the games to include a data service example. It also touches on related/supporting
technologies:

- use of the **`bottle`** web framework and the underlying **`uwsgi`** hosting service framework
- notes on debugging 
- (miniconda) python installation plus packages and environments
- on-demand EC2 instances (virtual machines) on AWS; including making and using AMIs
- using both a browser and Python code as a Client of a web Service
- transferring a service from a cheap VM ($0.30/hour) to a ***very*** cheap VM ($0.01/hour) to save money


Development sequence:


- Create a minimal 'simple dialog' service on a local machine (this document)
- Create the same service on a cloud VM (this document)
- Extend the functionality a bit further to complete the **steps** game
- Build a variant, the multi-player online game **mocean** 
- Build out a data service


## First **Steps**


The task is to run a **steps** server on one's own computer from a single Python file.


The subsequent version of **steps** is built on a cloud VM. This will use the Linux system daemon 
to run the same code (the Python program) as a service. As the VM is on the internet we can reach
it through its ip address.  


We have two means of connecting with **steps**: First through a browser address bar, and 
then from a Python *Client* program. 


### Procedure: Build the local version of **steps**


* Install Python 3 and the `requests` and `bottle` packages

```
python -m pip install requests
python -m pip install bottle
```

* Create `steps.py`:

```
import json
from bottle import request, route, run, default_app

# '@route' is a decorator that assigns the 'steps' route a function 'steps_game()'

@route('/steps', method='GET')
def steps_game():
    msg = request.GET.message.strip()
    print("          Server received message:", msg)
    try :                      True
    except :                   return('This message will never be printed')
    return 'welcome! You sent a message: ' + msg

application = default_app()
if __name__ == '__main__': run(host='0.0.0.0', port=8080, reloader=True)
```


* Run `steps.py`


```
python steps.py
```


Run-time response should be:


```
Bottle v0.12.19 server starting up (using WSGIRefServer())...
Listening on http://0.0.0.0:8080/
Hit Ctrl-C to quit.
```

### Play **steps**

#### ...using a browser


- Open a browser and in the address bar type in `http://localhost:8080/steps`
    - This should produce text output `welcome! You sent the steps game the message: '
- You can include additional information by typing in `http://localhost:8080/steps?message=hello fellow sentients`
    - This should produce text output `welcome! You sent the steps game the message: hello fellow sentients'


#### ...using Python code


Create `steps_client.py`:


```
import requests
print(requests.get('http://localhost:8080/steps?message=What is your favorite color?').content.decode('utf-8'))
```


Run this program


```
python local_steps_client.py
```


This should a short message that echoes `What is your favorite color?`. 


## Cloud steps


### Procedure: Build the cloud VM version of **steps**


Our goal here is to set up a cloud virtual machine that does just what the above version of **`steps`** does. 
It will use the [Linux system daemon](https://en.wikipedia.org/wiki/Systemd), 
and a specialized [Python environment](https://towardsdatascience.com/virtual-environments-104c62d48c54), 
in addition to the
[`bottle` Python web framework](https://bottlepy.org/docs/dev/) used above. 


Explaining these is outside the scope of this cookbook but there is
a wealth of information online such as 
[this digital ocean article](https://www.digitalocean.com/community/tutorials/how-to-use-systemctl-to-manage-systemd-services-and-units)
that describes Linux system service management in some detail.


- On the cloud start a Virtual Machine
    - On AWS
        - Include a Custom TCP with port = 8080 and source = 0.0.0.0/0
            - If this was not done during initialization of the VM you can do it later 
                - Method: Add an inbound rule to the instance's Security Group
                    - Use the same three parameters: Custom TCP, port 8080, source 0.0.0.0/0
        - Associate an elastic ip with the VM to give it a stable URL
        - For notes on AWS EC2 launch see [this link](https://github.com/cloudbank-project/burnop/blob/main/aws-ec2-start-stop.md)
- Log in to your VM and install miniconda by copying and pasting this text:
   

```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh && bash miniconda.sh -b -p $HOME/miniconda && export PATH="$HOME/miniconda/bin:$PATH" && conda config --add channels conda-forge --force
```



- Edit `~/.bashrc` and add a line at the end of this file: 


```
export PATH="$HOME/miniconda/bin:$PATH"
```


Save and run:

```
source ~/.bashrc
```

Check that `python` and `conda` execute from the *miniconda* installation:


```
prompt> which python
/home/ubuntu/miniconda/bin/python
prompt> which conda
/home/ubuntu/miniconda/bin/conda
```


- Install `requests` and `bottle` on the VM


```
prompt> pip install requests
prompt> pip install bottle
```

> ***Warning: Do not install these libraries inside the environment you create below. There they can get wires
> crossed with the bottle/uwsgi message handling, causing the service we are building to not run.


- Use the `conda` package manager to create an environment that includes the `uwsgi` gateway interface and the `bottle` web framework


```
conda create -n steps-env --yes bottle uwsgi
```


> ***Supposing you accidentally create an *environment* that you decide you want to remove. Remove it not using the `conda` 
> utility but rather with the related `conda-env` (conda environment) utility. To learn more issue 
> `conda-env -h`. An environment must be deactivated before it can be deleted. The command is `conda-env remove -n steps-env`. 
> List conda environments with `conda-env list`. List packages installed therein with `conda list -n steps-env`.***


Activate this environment; two methods for this are: 


```
prompt> conda activate steps-env
```


or


```
prompt> source activate steps-env
```


> ***If `activate` of `steps-env`*** 


```
ubuntu@ip-172-31-46-86:~$ conda activate steps-env

CommandNotFoundError: Your shell has not been properly configured to use 'conda activate'.
To initialize your shell, run

    $ conda init <SHELL_NAME>

Currently supported shells are:
  - bash
  ...etcetera...
```

> ***Solution***


Run this command:


```
prompt> conda init bash
(steps-env) prompt>
```


Once a Python environment is activated, it is reflected in the cursor prompt.


- From within the `steps-env` environment: Test that uwsgi is executing from the correct (miniconda/bin) location:


```
which uwsgi

/home/ubuntu/miniconda/envs/steps-env/bin/uwsgi
```


- Edit a file called `steps.service` in the ubuntu home directory to read as follows:


```
[Unit]
Description=Operate steps game

[Service]
Type=simple
Restart=on-failure
RestartSec=5s
TimeoutSec=7200
User=ubuntu
WorkingDirectory=/home/ubuntu/
ExecStart=/bin/bash -c '/home/ubuntu/miniconda/envs/steps-env/bin/uwsgi --http :8080 --wsgi-file /home/ubuntu/steps.py --master'

[Install]
WantedBy=multi-user.target
```

> An earlier version of this file set `Type=forking`. This seems to work but the `start` command never returns.
> [This stack overflow exchange](https://unix.stackexchange.com/questions/308311/systemd-service-runs-without-exiting)
> recommends `Type=simple`.


- Copy this file to the directory `/etc/systemd/system`


```
sudo cp steps.service /etc/systemd/system
```


- Ensure that the `steps.py` program above is present and executable in the home directory of the `ubuntu` user


#### Auto-start


Once you are satisfied that the service is working properly you can configure it to auto-start whenever the
VM reboots. The command for this is:


```
sudo systemctl enable steps.service
```


To undo this: 


```
sudo systemctl disable steps.service
```


#### Debugging


The Linux VM maintains a journal of events recorded by the system daemon. Read this journal by issuing the command 

```
journalctl -xe
```

Here, after the steps game has been played, we should find the results of diagnostic print statements 
from the `steps.py` program.
Below in the section **How to play cloud steps** is a description of how to verify that inbound Client requests 
align with journal entries printed by the steps game.



If the steps service is not working, test it locally by running a Python script. Here is the example code 
given above in this walk-through: 


```
import requests
print(requests.get('http://localhost:8080/steps?message=1.12 fred johnson').content.decode('utf-8'))
```


Use `journalctl -xe` to verify that the service ran. If it did not: There is a problem with the system daemon
running the Python program `steps.py`. Use `ps -ef | grep steps` to be sure that the service is running. There
are typically three `uwsgi` processes running.


If the **steps** service is running and responding on the cloud VM, the next step is to verify that the
service is working over the internet as well. Use the browser method described below under **cloud steps > browser**.


Once the browser approach is verified, try the Python approach described below, **cloud steps > Python**.



### How to play **cloud steps**


#### **cloud steps > browser**


In your browser address bar type **`http://52.34.243.66:8080/steps`**.


To verify your browser URL against the system daemon journal, add a key-value
to your browser URL: **`http://52.34.243.66:8080/steps?message=hello wurlde`**.
Now in the bash shell of the cloud VM issue


```
journalctl -xe
```


The output should include a line **`Server received message: hello wurlde`**. This is a means of determining whether 
the Client inbound message to the Server is arriving as intended.



#### **cloud steps > Python**


- As noted above you must have both Python 3 and the `requests` library installed.
- The idea is for this code to run from your local machine 
    - Let's suppose the elastic IP address is 123.123.123.123

```
import requests
print(requests.get('http://123.123.123.123:8080/steps?message=from Python to cloud steps').content.decode('utf-8'))
```


Here is a slightly more involved Python program that tests the steps game and provides the time of
execution in milliseconds.


```
import requests
import time

def stepscaller(s): 
    return requests.get('http://52.34.243.66:8080/steps?message=' + str(s)).text

toc = time.time()
steps_response = stepscaller(16)
tic = time.time()

print(steps_response)
print('milliseconds:', 1000.*(tic-toc))
```



## Advanced cloud steps


### How to play advanced **cloud steps**


## Mocean

(placeholder)

## Data Service

(placeholder)


## Supporting Concepts and Procedures

### Create an AMI


If the VM is expensive and not doing very much: It would be ideal to reduce it in capacity to match its load. 
On the AWS console go to the EC2 dashboard and select the (stopped) instance. Under the Actions drop down
follow the path to **Create Image**. This is a simple one-page wizard that will create an image of the 
instance in a matter of ten minutes or so. On AWS this image is called an **AMI** for **Amazon Machine Image**.
It can be used to launch new instances ***that do not have to be the same machine type***. This is how one
can reduce the daily cost of running the service: Use an AMI to migrate the service to a cheaper, lower-power
VM.




- Go to the AWS console: Compute Services: EC2 dashboard: Launch instance
- The wizard page 1 presents four image pool options on the left sidebar: Choose **My AMIs**
    - This should show the AMI you created. Check the selected Regions if an AMI is not apparent.
- Go through the rest of the launch procedure as usual
    - Choose a (possibly cheaper) instance on page two of the wizard
    - Notice that the root volume size will match that of the saved AMI
    - Notice that tab 6 **Configure Security Group** is an opportunity to set up the communication port
        - See the section above on building a cloud VM version of **steps**
        - The specific details: Using the **Add rule** button: Include a Custom TCP with port = 8080 and source = 0.0.0.0/0 



### New VM Security Issue


Upon creating the AMI: Start a new VM from it. Test the new VM to verify it behaves properly. This will
include checking the service (using a browser or Python, for example, as described above). It will also
include logging in to the new VM. The new VM inherits its access keypair from the AMI, which of course is
an image of the original / previous VM. Now: At this point we encournter a 'good' problem: There
is a security alert that arises on your local bash shell when you first attempt to connect to the new VM.
That is: You may well receive a warning like the one below since the new VM
has an identity different from the one your bash shell recorded for the original VM. 


```
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (man-in-the-middle attack)!
It is also possible that a host key has just been changed.
The fingerprint for the ECDSA key sent by the remote host is
[longfingerprintstringhere]
Please contact your system administrator.
Add correct host key in /home/[localdirectory]/.ssh/known_hosts to get rid of this message.
Offending ECDSA key in /home/[localdirectory]/.ssh/known_hosts:33
  remove with:
  ssh-keygen -f "/home/[localdirectory]/.ssh/known_hosts" -R "123.123.123.123"
ECDSA host key for 123.123.123.123 has changed and you have requested strict checking.
Host key verification failed.
```


### Finishing new VM set-up

- Once the instance is tested out there are two details to modify
    - The original instance had an elastic ip associated; so either re-associate or get a new elastic ip for this instance
    - The original instance ID was saved in the start / stop Lambda function environment variables
        - Since there are two Lambda functions: Both must have their environment variables modified to reflect the new instance
- If you have moved to the new instance on a permanent basis and have no further use for the original
    - The original is a candidate for termination once you are absolutely certain that this is a safe step
        - Terminate the instance
        - Delete any residual associated resources (Security Group, Internet Gateway, EBS volumes)


# Residual notes


- What is **`HTTP GET`**? What are service **`routes`**?
- Need a complete list of all the ripples from an EC2
- Ideal to describe various interrupt / restart mechanisms (`systemctl` and so on)
- Aliases for frequently used commands
- GitHub clone and commit recipes, push on a regular basis (`git clone https://github.com/robfatland/mocean.git`)
- [using `systemd`](https://www.shubhamdipt.com/blog/how-to-create-a-systemd-service-in-linux/)
- [restarting notes](https://ma.ttias.be/auto-restart-crashed-service-systemd/)
- Explain what the last two lines of the Client Python programs are doing:ss
    
```
application = bottle.default_app()
if __name__ == '__main__': run(app=application, host='0.0.0.0', port=8080, reloader=True)
```







