# mocean

There are two games: **steps** and **mocean**. They use the same *ip address*. Play a game by formatting a URL to include
the ip address, port, route, key and value. (possibly more than one of the latter two). Can use a browser but the project 
concept is to use a Python Client. 

## Client for steps game

Start with `http://<ip>:8080/begin?message=<some_message>`. The route is `begin` and the key is `message`. 
Iterate based on responses. Upon solving this puzzle the User is directed to a new route. Change the route and do the
next challenge. There are five of these. Here is example Client code.

```
import requests, time

urlbase, route, key = 'http://AAA.BBB.CCC.DDD:PPPP/', 'begin', 'message'

while True:
    msg = input('msg to send to route `' + route + '`, key `' + key + '`: ')
    if   msg == 'exit' or msg == 'quit':  break
    elif msg == 'route': route = input("enter a new route: ")
    elif msg ==   'key':   key = input("enter a new key: ")
    else:
        full_message = urlbase + route + '?' + key + '=' + msg
        tic = time.time()
        answer_back = requests.get(full_message).text
        toc = time.time()
        print('\nServer response: \n\n' + answer_back + '\n\n' + str(round((toc - tic)*1000., 1)) \
              + ' milliseconds, URL = ' + urlbase + route + '?' + 'message=' + msg + '\n\n') 
```

## mocean ideas

- Server maintains the state but the Client exchanges are stateless
- torus 600 x 800 with depth
- locations are integers
- routes: join, quit, who, chat, move, dive, grab 
- issues: different latencies would give players an unfair advantage
- message queue between players / broadcast

## Server configuration

### Outline

- Start up a Server (in our case a cloud instance) and ensure...
    - It has the proper ports available on the Internet
        - On AWS this means += Custom TCP, port PPPP, source 0.0.0.0/0
- Make sure the Python script imports `bottle`, concludes with proper `run()` statements
- Install `miniconda` on the Server
- Create a Python environment
- Configure a `.service` file 
    - Add to this file proper automated restart lines
        - See [this website](https://ma.ttias.be/auto-restart-crashed-service-systemd/)
- Use the appropriate `systemctl` commands to start and monitor the service
- Test the service

### Python Server code sketch

```
import bottle
from bottle import request, route, run
import json
# more imports here...

# using a decorator to match a route to a callback. This one has no key-value requirement
@route('/mocean')
def mocean_hello():
    msg   = "be there swells, let's go a-whalin"
    return(msg)

# A more involved route + callback
@route('/begin', method='GET')
def steps_game_part_1():
    msg = request.GET.message.strip()
    try :  vfloat = float(msg) 
    except : return('you are on the right route, "begin", but your message is not numerical enough for me!!!')
    v = int(vfloat)
    if v < 0: return('ah good, you are getting warm... i like numbers but this one is a bit negative :( ')
    if v == 0: return("nice message... but it a bit small don't you think?")
    if not float(v) == vfloat: return('actually I need an integer, and ' + str(vfloat) + ' has digits after the decimal point...')
    if not isprime(v): return('your message is positive but not prime enough')
    if v <= 100: return("your message is prime! Make it a bit bigger, like over the century mark, and you're there")
    return "congrats, you solved it!!! A prime greater than 100. The next step: Begin again, this time using the route 'beguine'"

def isprime(n):
    if n == 2: return True
    if n < 2 or not n % 2: return False
    for i in range(3, int(sqrt(n))+1, 2): 
        if not n % i: return False
    return True
       
# to test/run in a casual mode use: run(host='0.0.0.0', port=8080, reloader=True)
# to run in more robust systemd mode:
application = bottle.default_app()
if __name__ == '__main__':
    run(app=application, host='0.0.0.0', port=8080, reloader=True)
```

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
be `mocean.service`. Here are the contents: 


```
[Unit]
Description=Job to run the Python mocean.py Server code, in turn to parse HTTP GET API calls
[Service]
Type=forking
Restart=on-failure
RestartSec=5s
ExecStart=/bin/bash -c '/home/ubuntu/miniconda/envs/mocean-env/bin/uwsgi --http :PPPP --wsgi-file /home/ubuntu/mocean/mocean.py --master'
[Install]
WantedBy=multi-user.target
```

Usually this is edited in a user directory and then copied using `sudo` to the destination, as in 

```
sudo cp /home/ubuntu/mocean/mocean.service /lib/systemd/system/mocean.service
```

The `Restart` and `RestartSec` entries in this file allow the `systemd` manager to notice the service is not working a restart it.
The ExecStart fires up the Python code to run. In this case the Python code parses HTTP GET traffic. Notice that 
the Python file `mocean.py` is the operative code; it does the interesting stuff. It concludes as shown above with these lines: 

```
application = bottle.default_app()
if __name__ == '__main__': run(app=application, host='0.0.0.0', port=PPPP, reloader=True)
```

Notice I am using `PPPP` for the port number (use a real number) and I use `AAA.BBB.CCC.DDD` for the ip address (use a real
ip address). When building this on the cloud: Note that the cloud vendor can provide a fixed ip address that you map to 
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







