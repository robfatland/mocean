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

- Make sure the Python script imports `bottle`
- Make sure the Python script concludes with the "correct" `run()` statements
- Install `miniconda` on the Server
- Create a Python environment
- Configure a `.service` file 
    - Add to this file proper automated restart lines
        - See [this website](https://ma.ttias.be/auto-restart-crashed-service-systemd/)
- Use the appropriate `systemctl` commands to start and monitor the service
- Test the service

### Python Server code outline

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
