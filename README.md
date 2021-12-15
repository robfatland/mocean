# The ***Mocean*** project 

This project was designed around a club for Middle School Python Learners (fans of the game *Among Us*). 
There are two "games" involved, one called **Steps** and one called **Mocean**. 
**Steps** is a simple interactive text game.
**Mocean** is a more complicated Server~Client online game that supports multiple players exploring
a 'world' in competition with one another. The idea is for the students to build their own
Client applications to play this game. 


This project has a lot in common with creating data services
for research. 


We proceed as follows:


- Create a minimal service on a local machine: A very simple dialog, precursor to the **steps** game
- Create the same service on a cloud VM
- Extend the functionality a bit further to complete the **steps** game
- Build a variant of this, the multi-player online game **mocean** 
- Build out a data service


## First **Steps**

This creates and runs the **steps** server on your own computer. It is very simple because we simply run
a single Python file to create the local Server. Then we use our browser as a local Client of this Server.
In later versions of **steps** we will complicate things by using the Linux system daemon as a 
sort of *minder* that runs (and re-starts) the Python program. For the moment, however, we can
see what is going on as 'a running Python program that listens and responds' (the Server) and a
separate program, a web browser, i.e. a Client, that pokes the Server with a simple message and
receives a reply. 


* Install Python 3 and the `requests` and `bottle` packages

```
python -m pip install requests
python -m pip install bottle
```

* Create a file `steps.py` like this:

```
import json
from bottle import request, route, run, default_app

# '@route' is a decorator that assigns the 'steps' a function 'steps_game()'

@route('/steps', method='GET')
def steps_game():
    msg = request.GET.message.strip()
    print("          Server received message:", msg)
    try :                      True
    except :                   return('This message will never be printed')
    return 'welcome! You sent the steps game the message: ' + msg

application = default_app()
if __name__ == '__main__': run(host='0.0.0.0', port=8080, reloader=True)
```

The last two lines of this file are key to operating correctly both here and
in the expanded context of a cloud-based Server VM.


* Run `steps.py`


```
python steps.py
```


This provides a run-time response like:


```
Bottle v0.12.19 server starting up (using WSGIRefServer())...
Listening on http://0.0.0.0:8080/
Hit Ctrl-C to quit.
```

### How to play **steps**


- Open a browser and in the address bar type in `http://localhost:8080/steps`
    - This should produce text output `welcome to the rudimentary steps game`
- You can include additional information by typing in `http://localhost:8080/steps?message=hello fellow sentients`


## Cloud steps


### Server setup

Our goal here is to set up a cloud virtual machine that does just what the above version of **`steps`** does. It will
include additional elements: The [Linux system daemon](https://en.wikipedia.org/wiki/Systemd), 
a specialized [Python environment](https://towardsdatascience.com/virtual-environments-104c62d48c54), 
and more extensive use of the
[`bottle` Python web framework](https://bottlepy.org/docs/dev/). 
Explaining how these work is outside the scope of this cookbook approach but there is
a wealth of information online.


- On the cloud start a Virtual Machine
    - On AWS
        - += Custom TCP, port 8080, source 0.0.0.0/0
            - If this is not done during initialization of the instance: 
                - Add an inbound rule to the instance's Security Group
                    - Use the same three parameters: Custom TCP, port 8080, source 0.0.0.0/0
            - Use an elastic ip to ensure your server will always appear at the same URL
        - For detailed notes on AWS EC2 launch see [this link](https://github.com/cloudbank-project/burnop/blob/main/aws-ec2-start-stop.md)
- Log in to your VM and install miniconda by copying and pasting this text:
   

```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh && bash miniconda.sh -b -p $HOME/miniconda && export PATH="$HOME/miniconda/bin:$PATH" && conda config --add channels conda-forge --force
```


This sequence of concatenated commands should install miniconda in one go. The next step ensures that `miniconda` will
have precedence in finding various executables (`python`, `conda` etc).


- Edit `~/.bashrc` and add a line at the end of this file: 


```
export PATH="$HOME/miniconda/bin:$PATH"
```


Save and run:

```
source ~/.bashrc
```

Check that `python` executes from a path that includes *miniconda*.

```
which python
```

This should produce `/home/ubuntu/minconda/bin/conda`. If not: Debug!


- Install `requests` and `bottle`


```
pip install requests
pip install bottle
```

> ***Warning: Do not install these libraries inside the environment you create below. There they can get wires
> crossed with the bottle/uwsgi message handling, causing the service we are building to not run.


- Use the `conda` package manager to create an environment that includes the `uwsgi` gateway interface and the bottle web framework


```
conda create -n steps-env --yes bottle uwsgi
```


> ***Supposing you accidentally create an *environment* that you decide you want to remove. You do this not using the `conda` 
> command but rather with the related `conda-env` (conda environment) command. To find out what it does you can issue 
> `conda-env -h`. The environment must be deactivated before it can be deleted. The the command is `conda-env remove -n steps-env`. 
> List the conda environments with `conda-env list`. List packages installed therein with `conda list -n steps-env`.***


Activate this environment; two methods for this are: 


```
conda activate steps-env
```


or


```
source activate steps-env
```

> ***Possible Fail Point: Error on `activate` of `steps-env`*** 


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
conda init bash
```


Note that once a Python environment is activated this is reflected in the cursor prompt.


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


#### Debugging


The Linux VM maintains a journal of events recorded by the system daemon. Read this journal by issuing the command 

```
journalctl -xe
```

Here, after the steps game has been played, we should find diagnostic printouts from the `steps.py` program.
Below in the section **How to play cloud steps** is a description of how to verify that inbound Client requests 
align with journal entries printed by the steps game.



***What is needed in the operational procedure is a way of debugging server halts: Why do they happen?***


***What is needed in the code is a state file that can be reloaded on restart to pick up where the game left off***







- Create a `steps` environment within Python

```
conda create -n steps-env --yes bottle uwsgi
```







### How to play **cloud steps**


#### Version 1: Playing **steps** using your browser


In your browser address bar type **`http://52.34.243.66:8080/steps`**.


To verify your browser URL against the system daemon journal, add a key-value
to your browser URL: **`http://52.34.243.66:8080/steps?message=hello wurlde`**.
Now in the bash shell of the cloud VM issue


```
journalctl -xe
```


The output should include a line **`Server received message: hello wurlde`**. This is a means of determining whether 
the Client inbound message to the Server is arriving as intended.



#### Version 2: Playing **steps** using Python


- As noted above you must have both Python 3 and the `requests` library installed.


## Advanced cloud steps


### How to play advanced **cloud steps**


## Mocean


The game **Mocean** is set on an ocean planet in the shape of a torus. 
It supports multiple players. You join the game and begin exploring.
The Server keeps track of where you are on the ocean planet.
You will need to build your own game Client. It will talk to the Server
using various **routes** as commands. 
All of this relies on a communication protocol (rulebook) called **`HTTP GET`**.





To make certain steps easier create a clone of this repo on your server:


```
cd ~
git clone https://github.com/robfatland/mocean.git
```

You should have a **`mocean`** directory with all these contents therein: In your home directory.
Copy the file `mocean.py` to your home directory and make sure it is executable.


```
cd ~
cp mocean/mocean.py .
chmod a+rx mocean.py
```


That Python code `mocean.py` is intended to be run on this EC2 instance as a service, using the ***system daemon***. More on this in a bit. 


Next we set up a custom environment for **mocean** using `conda create` and `conda activate`. The steps are elaborated at length here; please follow methodically!


First: 


Create a new file called `~/.bash_aliases` consisting of the aliases shown below. The alias names
are a bit labored but the idea is to create a little custom vocabulary consistent with the 'mocean'
frame of mind.


```
alias mocean_activate='conda activate mocean-env'
alias mocean_start='sudo systemctl start mocean'
alias mocean_stop='sudo systemctl stop mocean'
alias mocean_restart='sudo systemctl restart mocean'
alias mocean_status='sudo systemctl status mocean'
alias mocean_daemon='sudo systemctl daemon-reload'
alias mocean_journal='journalctl -xe'
alias mocean_ps='ps -ef | grep mocean'
alias mocean_kill='sudo kill -9 '
```

When I execute `source .bashrc` this strangely de-activates the `mocean-env` environment. 
Once I reactivate the `mocean-env` environment
these aliases exist; so hopefully they work as desired.


### **`systemd`** service creation


We now want to follow some sort of directions ([example site](https://www.shubhamdipt.com/blog/how-to-create-a-systemd-service-in-linux/))
to create a service that runs automatically on startup and re-starts itself should it halt for some reason. 


In the home directory edit a file called `mocean.service`.


```
cd /etc/systemd/system
```





### Closing notes


- It is bad form to interrupt the `systemd` daemon using `kill`...
    - ...however I resort to this at times...
    - ...as some `systemctl` tasks don't work smoothly. (they tend to just hang)
- Take advantage of the `systemd` by creating a `mocean.service` file 
    - This and other files referred to are in this repository
    - Include proper automated restart entries
    - See [this website](https://ma.ttias.be/auto-restart-crashed-service-systemd/)
    - This file goes into `/lib/systemd/system/`. 
    - Since the game is called "mocean" the file will be `mocean.service`. 
    - An example is in this repository
    - Stop the service (e.g. `mstop` with `mps` and `mkill` together...) before swapping in a new version


## Service Bug

- Wimpy instance: Timeout/restart every five minutes or so. 
- Improved from 1 minute by including in `mocean.service`: 

```
TimeoutSec=7200
```

## Python execution 

- The end of the main Python file uses these two lines to engage the bottle web framework
    
```
application = bottle.default_app()
if __name__ == '__main__': run(app=application, host='0.0.0.0', port=8080, reloader=True)
```

- It may be helpful to clear the decks with

```
sudo systemctl daemon-reload
```







