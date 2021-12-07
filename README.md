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


**http://52.11.131.9:8080/begin** will start **Steps**. Notice this is just a URL, not Python code. 
This is our first clue that Python is acting like a browser.  Similarly you can see if the **Mocean** 
game is running or not using **http://52.11.131.9:8080/mocean**.



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

***Students: From here down you are free to read but you may ignore the rest!***


## Server setup

- On the cloud start a Virtual Machine
    - Config on AWS: += Custom TCP, port 8080, source 0.0.0.0/0
        - If not done during init: Add an inbound rule to the instance's security group with these parameters
    - Use an elastic ip
- Login, install miniconda
   

```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh && bash miniconda.sh -b -p $HOME/miniconda && export PATH="$HOME/miniconda/bin:$PATH" && conda config --add channels conda-forge --force
```


This sequence of concatenated commands should install miniconda in one paste.


Next we set up a custom environment for **Mocean** using `conda create` and `conda activate`. However: The steps are elaborated below so don't just thrash about here...


First: Edit `~/.bashrc` and add a line at the end of this file if necessary, then save and run. 

```
export PATH="$HOME/miniconda/bin:$PATH"
source ~/.bashrc
```

- Check that `python` is indicating a path that includes *miniconda*.

```
which python
```

- Should produce something like `/home/ubuntu/minconda/bin/conda`. 
- Create an environment that includes the `uwsgi` gateway interface and the bottle web framework: 

```
conda create -n mocean-env --yes bottle uwsgi
```

- Activate this environment; two methods for this are: 

```
conda activate mocean-env
source activate mocean-env
```

- Test that uwsgi is executing from the correct (miniconda/bin) location:

```
which uwsgi
```

- Needed: Rationale for the environments, for the explicit path in `.service` and...
- ...for why the `.service` file does not actually invoke the mocean-env environment
- Create `~/.bash_aliases` file using a leading `m` to connect these shortcuts with `mocean`:

```
alias mstart='sudo systemctl start mocean'
alias mstop='sudo systemctl stop mocean'
alias mrestart='sudo systemctl restart mocean'
alias mstatus='sudo systemctl status mocean'
alias mdaemon='sudo systemctl daemon-reload'
alias mjournal='journalctl -xe'
alias mps='ps -ef | grep mocean'
alias mkill='sudo kill -9 '
```

- It is considered bad form to interrupt the `systemd` daemon using `kill`...
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
- Improved to this from 1 minute by including in `mocean.service`: 

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







