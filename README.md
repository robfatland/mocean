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

- In what follows I use `PPPP` for the port number. Replace this with 8080.
- Start up a Server (in our case a cloud instance) and ensure...
    - It has the proper ports available on the Internet
        - On AWS console this means += Custom TCP, port PPPP, source 0.0.0.0/0
    - It may use a fixed ip address (on AWS "Elastic ip"); otherwise it will be a bit of a moving target.
- Make sure the Python script imports `bottle`, concludes with proper `run()` statements
- Install `miniconda` on the Server
- Create a Python environment (I used `mocean-dev`)
    - See section below on creating this environment
- Configure a `.service` file 
    - Be sure to include the proper automated restart entries
        - See [this website](https://ma.ttias.be/auto-restart-crashed-service-systemd/)
- Use the appropriate `systemctl` commands to start and monitor the service
    - `systemctl start`
    - `systemctl stop`
    - `systemctl restart` after modifying the server code does a refresh
    - `systemctl status mocean` 

### Python Server code sketch

***Notice this fails without you fix the port number!!***

See file `mocean.py`.

### install miniconda, ... and subsequent configuration steps ...

```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh && bash miniconda.sh -b -p $HOME/miniconda && export PATH="$HOME/miniconda/bin:$PATH" && conda config --add channels conda-forge --force
```

We are on a trajectory to use `systemd` as a manager for the service daemon. 

Edit `~/.bashrc` and add a line at the end of this file if necessary: 

```
export PATH="$HOME/miniconda/bin:$PATH"
```

Save this file and run it:

```
source ~/.bashrc
```

Check that `python` is indicating a path that includes *miniconda*.

```
which python
```

should produce something like `/home/ubuntu/minconda/bin/conda`. 


Create an environment that includes the `uwsgi` gateway interface and the bottle web framework: 

```
conda create -n mocean-env --yes bottle uwsgi
```

Activate this environment; we have two methods: 

```
conda activate mocean-env
```

or

```
source activate mocean-env
```

Test:

```
which uwsgi
```

should produce something like

```
/home/ubuntu/miniconda/envs/mocean-env/bin/uwsgi
```

Now create a `.service` file. This will reside in `/lib/systemd/system/`. Since the game is called "mocean" the file will
be `mocean.service`. Here are the contents but ***notice this fails without you fix the port number!!*** 

The service file is `mocean.service` in this repo. Do not clobber the existing service file with a 
modification as it could break the VM. Rather use `systemctl stop` and then make the switch before
restarting.


In more detail: Edit the new `mocean.service` in a user directory, then stop the service, then copy using `sudo`:

```
sudo cp /home/ubuntu/mocean/mocean.service /lib/systemd/system/mocean.service
```

That is for Ubuntu. Then restart the service.

### Service file parameters


#### Bug

I currently experience timeout/restarts every five minutes or so. It was worse but I include this line in the `[Service]` 
segment of the `.service` file: 

```
TimeoutSec=7200
```

This does not give me 2 hours of operation... just five minutes up from one minute. So an open problem to resolve.

#### Service file further notes

The `Restart` and `RestartSec` entries in this file allow the `systemd` manager to notice the service is not working and restart it.
The ExecStart fires up the Python code to run. In this case the Python code parses HTTP GET traffic. Notice that 
the Python file `mocean.py` is the operative code; it does the interesting stuff. It concludes as shown above with these lines: 

```
application = bottle.default_app()
if __name__ == '__main__': run(app=application, host='0.0.0.0', port=PPPP, reloader=True)
```

When building this on the cloud: Note that the cloud vendor can provide a fixed ip address that you map to 
the Server so its address never changes for the duration of a project.


Start the service using

```
sudo systemctl start mocean
```

This may not return; you can try ctrl-z and `bg` to place it in the background. Check the status using 

```
sudo systemctl status mocean.service
```

If the process failed to start: It may be helpful to clear the decks before another attempt. Use

```
sudo systemctl daemon-reload
```


To test the service directly enter the command

```
uwsgi --http :PPPP --wsgi-file /home/ubuntu/mocean/mocean.py --master
```







