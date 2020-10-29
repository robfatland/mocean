# mocean

There are two games here. 

1. A simple test game called the *Steps Game* that has five consecutive puzzles, each one on a different route. 
2. The game **mocean** which will coordinate players and a game space for interactive play




## Client for Steps game

Start with `http://<ip>:8080/begin?message=<some_message>`. This uses route `begin` and key `message`. Once the player solves
this first puzzle they are directed to a new route. So change the route and start over guessing the new puzzle. The game has 
five routes. This Client code makes it fairly easy to change the route; and you can also quit playing. 


If a sensible result doesn't come back in under a second it is 99.99999% likely the Server code isn't running. 

```
import requests, time
urlbase, route = 'http://54.69.30.193:8080/', 'begin'
while True:
    msg = input('msg to send to route ' + route + ':')
    if msg == 'exit' or msg == 'quit':  break
    if msg == 'route': route = input("enter a new route:")
    else: 
        tic = time.time()
        answer_back = requests.get(urlbase + route + '?' + 'message=' + msg).text
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
