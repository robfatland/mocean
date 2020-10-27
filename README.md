# mocean
my take on a simple interactive Server-driven game


## Client for route game

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

## todo

- class
- routes
    - join
    - quit
    - move
    - dive

## ideas

- torus 600 x 800
- lottery circles: enter them and you are transported from the game
- server hands out positions; client only sends in impulses
- depth level down to 16, photic zone is the top 6: 1.0, 0.83, 0.67, 0.50, 0.33, 0.17, 0.00 so range of vision drops
- return: all features within a view radius
