# Test Clients


These are Jupyter cells built in development. They are not `mocean` Clients. 


## Useful route changer / play the **steps** game Client

### code


```
import requests, time
urlbase, route = 'http://AAA.BBB.CCC.DDD:PPPP/', 'begin'
while True:
    msg = input("msg to send to route '" + route + "':")
    if msg == 'exit' or msg == 'quit':  break
    if msg == 'route': route = input("enter a new route:")
    else: 
        tic = time.time()
        answer_back = requests.get(urlbase + route + '?' + 'message=' + msg).text
        toc = time.time()
        print('\nServer response: \n\n' + answer_back + '\n\n' + str(round((toc - tic)*1000., 1)) \
              + ' milliseconds, URL = ' + urlbase + route + '?' + 'message=' + msg + '\n\n') 
```


### writeup


# The Steps Game

You play this game by running the little program given below. 
The purpose of the program is to talk to a Server. 
In order for it to work you must have the `requests` library installed on your computer. 


Each time you send a message to the Server you are trying to guess what it wants to hear.
When you guess correctly (hopefully the Server will give you hints) you move on to the next puzzle.


## Putting your message together

A guess message is a Python *string* with six pieces glued together. 
The work is done by the program; so you only have to worry about what to say for your actual *guess*.
Here is what those six pieces are, if you are interested:


- the string `http://` means the message is going out onto the internet
- the ip address `AAA.BBB.CCC.DDD` is the Server's internet address
- the addition of `:PPPP` uses the designated port number. The Server listens on that port.
- the addition of `/begin` is the first puzzle game **route**. Each puzzle has an associated route.
- the addition of `?message=` is a key. This tells the Server to get ready for your guess.
- the addition of your guess (as a string) is the value that goes with the key

This is a lot of detail. The point is that this structure gives us a lot of flexibility in how we 
communicate between two computers. You can also imagine it is a bit like casting a magic spell: 
It is all necessary for the spell to work... even if the precise details are unclear.


## Running the program

When you run this code the `input()` statement will prompt you for a message to send the Server
on the `begin` route. Once you solve this first puzzle you will be given the next route. To 
change your route just type in `route` and then enter the new route name. From there you can 
start working on the second puzzle. 


To stop playing just type in `exit` or `quit`. 

## Installing `requests`

If you do not have the `requests` module installed you will get an error:


`no module named 'requests'`


To install it on a PC:

- Open the `command` window 
- Type in the command `python -m pip install requests`
- Try the program again to see if `requests` is now ok



## Simple one ping


```
import requests, time
urlbase, route = 'http://54.69.30.193:8080/', 'begin'

msg = 'hello' 
tic = time.time()
answer_back = requests.get(urlbase + route + '?' + 'message=' + msg).text
toc = time.time()
print('\nServer response: \n\n' + answer_back + '\n\n' + str(round((toc - tic)*1000., 1)) + ' milliseconds, URL = ' + urlbase + route + '?' + 'message=' + msg + '\n\n') 
```


## Very simple test: Server adds 37 to a number


```
import requests
import time

def apicall(x): return requests.get('http://AAA.BBB.CCC.DDD:PPPP/exchange?task=' + str(x)).text

tic = time.time(); check_42 = apicall(5); toc = time.time()

print(check_42)
print(1000.*(toc-tic))
```
