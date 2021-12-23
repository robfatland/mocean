from turtle import Turtle, Screen
import requests, time

urlbase, route, key, repeats = 'http://54.69.30.193:8080/', 'move', 'name', 1

screenwidth = 800
screenheight = 600
screen = Screen()
screen.setup(screenwidth + 4, screenheight + 8)
screen.setworldcoordinates(0, 0, screenwidth, screenheight)

t = Turtle()
t.hideturtle()
t.up()

while True:
    msg = input('msg to send to route ' + route + ', key ' + key + ': ')
    if   msg == 'exit' or msg == 'quit':  break
    if   msg == 'route':   route = input("enter a new route:")
    elif msg == 'key':     key   = input("enter a new key:")
    elif msg == 'repeats': repeats = int(input("enter number of repetitions:"))
    else:
        for repetitions in range(repeats):
            tic = time.time()
            answer_back = requests.get(urlbase + route + '?' + key + '=' + msg).text
            toc = time.time()
            print('\nServer response: \n\n' + answer_back + '\n\n' + str(round((toc - tic)*1000., 1)) \
                  + ' milliseconds, URL = ' + urlbase + route + '?' + key + '=' + msg + '\n\n')
            if route == 'join' and key == 'name':
                newloc = answer_back.split(',')
                t.goto(int(newloc[1]), int(newloc[2]))
            if route == 'move' and key == 'name':
                newloc = answer_back.split(',')
                t.goto(int(newloc[0]), int(newloc[1]))
                t.dot()
