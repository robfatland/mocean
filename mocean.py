from bottle import request, route, run
import json
from math import sqrt
from random import random

# configure global
players = []
locs = []
start_dim = 200.


@route('/mocean')
def mocean_hello():
    print('                     route mocean hit')
    return ("be there swells, well let's go a-whalin")


################## join ########################


@route('/join', method='GET')
def join():
    print("                  route join hit")
    print("                  len(players) = ", len(players))

    msg_string = request.GET.name.strip()

    print("                               received 'name':", msg_string)
    try :  
        players.append(msg_string)
        locs.append((random()*start_dim,random()*start_dim, 0.))
        # loc.append((1.,2.,3.))
    except : 
        print("adding player failed")
        return("sorry this player join did not work for some reason")
    rmsg = players[-1] + ',' + str(len(players)) + ',' + str(locs[-1][0]) + ',' + str(locs[-1][1]) + ',' + str(locs[-1][2])
    return rmsg


################## quit ########################


@route('/quit', method='GET')
def quit():
    print("                  route quit hit")
    msg_string = request.GET.name.strip()
    print("                               received 'name':", msg_string)
    if not msg_string in players:
        print("non-player quit tried:", msg_string)
        return("you tried to remove a non-existent player")
    try: 
        player_index = players.index(msg_string)
        del players[player_index]
        del locs[player_index]
    except : 
        print("dropping player failed")
        return("sorry this player quit did not work for some reason")
    return ("you have left the toroidal mocean")


@route('/move', method='GET')
def move():
    print("                  route move hit")
    player_name    = request.GET.name.strip()
    move_direction = request.GET.direction.strip()

    print(player_name, move_direction)
    return ("you tried to move")

run(host='0.0.0.0', port=8080, reloader=True)
