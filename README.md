# The ***Mocean*** Python Bytes Team Project 

This project was designed by and for Middle School Python Learners. Most of the code was written
by me. We learn Python motivated by an online game framework. The game is **Mocean**.


* The game **Mocean** is played on an ocean planet
* It supports multiple players: Human beings running Client apps
* There is a single Server on the Internet that knows who is playing and where they are
* The students learn how to build their Client apps based on learning about **routes**.
* Clients talk to the server using the HTTP GET protocol (*communication rules*)


## Steps

There is another built-in game called **Steps** that is simpler. **Steps** and **Mocean** use the same 
*ip address*. Look at the file `StepsClient.py` to see how this simple game works. 


## Using a browser

As a shortcut one can use a browser like Chrome as a Client for Mocean or Steps. For example type into
the browser address bar: **http://52.11.131.9:8080/begin**. That starts the Steps game. To get started
with Mocean use **http://52.11.131.9:8080/mocean**.



## Rob's Notes

### Install `requests`

If you have IDLE installed you can access Python and install packages like `requests` which we need for the **Mocean** project.

- Follow online instructions to install Python 3.9 etcetera; which gives you the IDLE development environment.
- Open a command shell on Windows where you can enter commands. Once you are there:
- Use the `py` command to invoke Python...
- ...and follow this with `-m pip install` to run the **pip** package installer...
- ...and follow this with the name of the package to install: `requests`, as in...

```
py -m pip install requests
```



### Server configuration
- On AWS start a VM (in our case a cloud instance) and ensure...
    - Configuration: += Custom TCP, port 8080, source 0.0.0.0/0
    - Assign an elastic ip
- Login, install miniconda: The single command is...
   

```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh && bash miniconda.sh -b -p $HOME/miniconda && export PATH="$HOME/miniconda/bin:$PATH" && conda config --add channels conda-forge --force
```


- Set up a custom environment for **Mocean** using `conda create`, `conda activate`:
    - Edit `~/.bashrc` and add a line at the end of this file if necessary, then save and run. 

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


### Service Bug

- Wimpy instance: Timeout/restart every five minutes or so. 
- Improved to this from 1 minute by including in `mocean.service`: 

```
TimeoutSec=7200
```

### Python execution 

- The end of the main Python file uses these two lines to engage the bottle web framework
    
```
application = bottle.default_app()
if __name__ == '__main__': run(app=application, host='0.0.0.0', port=8080, reloader=True)
```

- It may be helpful to clear the decks with

```
sudo systemctl daemon-reload
```







