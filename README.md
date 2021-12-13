# The ***Mocean*** Python Bytes Project 

This project was designed by and for Middle School Python Learners (who as we know are fans of the game *Among Us*). 
**Mocean** is a Server~Client online game which depends upon the players building their own Client applications.
This is a bit like building your own airplane before you fly it. First we write a Client that can taxi on a 
runway; and only later do we add wings and a tail...


* The game **Mocean** is set on an ocean planet in the shape of a torus 
* It supports multiple players; so you simply connect and say "join" to join the game
    * A Server living on the Internet knows who is playing and where they are located
* Students learn how to build their Client by learning about **routes**
    * A route is equivalent for our purposes to a command
* Student Clients talk to the server using the HTTP GET protocol
    * A protocol is a *rule for how to communicate*


## Steps


To get started we have a simpler game running on the same server. This simpler game is called **Steps**.
You play **Steps** by sending in guesses and reading the Server's response. The Server is giving you hints
about what to say; so it is a guessing game.


## Using a browser


**http://52.34.243.66:8080/steps** will start the **steps** game. This is a URL, not Python code. 
Python will eventually be substituted for the browser address bar.



## For Python: You must install `requests`

If you have IDLE installed you can access Python and install packages like `requests` which we need to play **Mocean**.

- Follow online instructions to install Python 3.9 etcetera; which gives you the IDLE development environment.
- Open a command shell on Windows where you can enter commands. Once you are there:
- Use the `py` command to invoke Python...
- ...and follow this with `-m pip install` to run the **pip** package installer...
- ...and follow this with the name of the package to install: `requests`, as in...

```
py -m pip install requests
```


## Server setup

- On the cloud start a Virtual Machine
    - Config on AWS: += Custom TCP, port 8080, source 0.0.0.0/0
        - If not done during init: Add an inbound rule to the instance's security group with these parameters
    - Use an elastic ip
- Login, install miniconda by copying and pasting the following command...
   

```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh && bash miniconda.sh -b -p $HOME/miniconda && export PATH="$HOME/miniconda/bin:$PATH" && conda config --add channels conda-forge --force
```


This sequence of concatenated commands should install miniconda in one go.


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


First: Edit `~/.bashrc` and add a line at the end of this file: 

```
export PATH="$HOME/miniconda/bin:$PATH"
```

Save the file and run it: 

```
source ~/.bashrc
```

Check that `python` executes from a path that includes *miniconda*.

```
which python
```

This should produce something like `/home/ubuntu/minconda/bin/conda`. If not you will need to debug the situation: Why is `conda` running from
a *non-miniconda* location?


Next: Using the `conda` package manager command we create an environment that includes the `uwsgi` gateway interface and the bottle web framework: 

```
conda create -n mocean-env --yes bottle uwsgi
```

Supposing you accidentally create an *environment* that you decide you want to remove. You do this not using the `conda` command but rather 
with the related `conda-env` (conda environment) command. To find out what it does you can issue `conda-env -h`. The environment must be 
deactivated before it can be deleted. The the command is `conda-env remove -n environment_i_do_not_want`.


Activate this environment; two methods for this are: 

```
conda activate mocean-env
```


or

```
source activate mocean-env
```


### Wait! That Did Not Work

I did the **activate** command and received an error: 

```
ubuntu@ip-172-31-46-86:~$ conda activate mocean-env

CommandNotFoundError: Your shell has not been properly configured to use 'conda activate'.
To initialize your shell, run

    $ conda init <SHELL_NAME>

Currently supported shells are:
  - bash
  ...etcetera...
```

So I ran 

```
conda init bash
```

and without complaint the system informed me that this modified the `.bashrc` file. So I retried `conda activate mocean-env` and this time it worked.
My cursor changed to reflect that I was *inside* the `mocean-env` environment. 


### That sorted, we continue


When the environment is active the cursor should change (default behavior) to reflect the active environment. 
We are now operating in a sort of sub-reality (the *mocean-env* environment).
Actions taken within this environment do not affect the generic bash environment.


Next step: Test that uwsgi is executing from the correct (miniconda/bin) location:

```
which uwsgi
```


Notice this shows a path that includes not only `miniconda` but also the `mocean-env` subdirectory.
The sub-directory corresponds to the `mocean-env` environment.


***In what follows we are setting up a server; including an ability for it to re-start itself
should it halt. In this process a file called `.service` is referenced. What is needed here is a
brief explanation; including a 'path' rationale and how the .service file invokes the 
special mocean-env environment.***


***What is needed in the operational procedure is a way of debugging server halts: Why do they happen?***


***What is needed in the code is a state file that can be reloaded on restart to pick up where the game left off***


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







