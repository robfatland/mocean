# added for application code version:
import bottle

from bottle import request, route, run
import json
from math import sqrt
import math
from random import randint, random
from time import time

# configure global
players, loc, vel, s0, s1, torew, torns = [], [], [], 200, 500, 1000, 1000

# time of last location call also matches player index
lastloctime = []

vscale = 1.0
clight = 40.
rttwo = sqrt(2.)
piover8 = math.pi/8.
pi3over8 = math.pi*(3./8.)
cosp8 = math.cos(piover8)
sinp8 = math.sin(piover8)
cosp38 = math.cos(pi3over8)
sinp38 = math.sin(pi3over8)

# These are changes to velocity "ice rink" style
#   u is east, 4 north, q west, c south
#   Limited by clight
impulse = {'u': (1., 0.),             \
           '7': (cosp8,sinp8),        \
           '6': (rttwo,rttwo),        \
           '5': (cosp38,sinp38),      \
           '4': (0., 1.),             \
           '3': (-cosp38,sinp38),     \
           '2': (-rttwo,rttwo),       \
           'q': (-cosp8,sinp8),       \
           'a': (-1., 0.),            \
           'z': (-cosp8,-sinp8),      \
           'x': (-rttwo,-rttwo),      \
           'c': (-cosp38,-sinp38),    \
           'v': (0., -1.),            \
           'b': (cosp38,-sinp38),     \
           'n': (rttwo,-rttwo),       \
           'j': (cosp8,-sinp38)} 

# overview
# 
# players, loc and vel are lists of lists (since tuples are immutable)
#   player list is name and (being lazy) player index, an integer
#   the index 'id' never changes. If the player drops out we change status but don't pop the entry 
#    from the state lists. This is intended to speed things up since the id is directly usable as
#    an index. 


@route('/mocean')
def mocean_hello():
    msg   = "          .......................hellow...................                      \n"
    msg  += "                                                                                \n"
    msg  += "route    key         value                returns                               \n"
    msg  += "=====    ===         =====                =======                               \n"
    msg  += "mocean   -           -                    this usage message                    \n"
    msg  += "join     name        a-name               name,id,x,y,z                         \n"
    msg  += "quit     name        a-name               confirm quit                          \n"
    msg  += "who      -           -                    csv of players                        \n"
    msg  += "location id          id from join         x,y,z                                 \n"
    msg  += "velocity id          id from join         vx,vy                                 \n"
    msg  += "accel    id          id from join                                               \n"
    msg  += "         heading     directional char     x,y,z,vx,vy                           \n"
    msg  += "dive     name        a-name                                                     \n"
    msg  += "         direction   u or d               x,y,z                                 \n"
    msg  += "msg      name        all or a-name           ...                                \n"
    msg  += "         message     message                 ... confirm msg on queue           \n"
    msg  += "listen   name        all or a-name        '' or message at top of queue         \n"
    msg  += "                                                                                \n"
    return(msg)

@route('/join', method='GET')
def join():
    name = request.GET.name.strip()
    try :    
        print('player name = ', name)
        if name in players: return 'duplicate player name not allowed to join'
        player_index = len(players)
        players.append([name, player_index]) 
        loc.append([randint(s0, s1), randint(s0, s1), 0])
        vel.append([0., 0.])
        lastloctime.append(time())
    except ValueError as ve: 
        return("player join fail")
    return players[-1][0] + ',' + str(players[-1][1]) + ',' + state(loc[-1][0], loc[-1][1], loc[-1][2])

@route('/quit', method='GET')
def quit():
    msg_string = request.GET.name.strip()
    print("                     quit:", msg_string)
    if not msg_string in players:
        return("quit fail for non-existent player")
    try: 
        player_index = players.index(msg_string)
        # this is where you'd (kilroy) label this player as inactive
    except : return("quit fail")
    return ("you have left the toroidal mocean")

@route('/who', method='GET')
def who(): 
    rmsg = 'players: '
    for name in players: rmsg += name[0] + ' '
    return rmsg

@route('/location', method='GET')
def location(): 
    upbit = 0
    id = int(request.GET.id.strip())
    dt = time() - lastloctime[id]
    lastloctime[id] = time()
    loc[id][0] += vel[id][0] * dt
    loc[id][1] += vel[id][1] * dt
    if loc[id][0] < 0: loc[id][0] += torew ; upbit = 1
    if loc[id][1] < 0: loc[id][1] += torns ; upbit = 1
    if loc[id][0] >= torew: loc[id][0] -= torew ; upbit = 1
    if loc[id][1] >= torns: loc[id][1] -= torns ; upbit = 1
    return state(loc[id][0], loc[id][1], loc[id][2]) + ',' + str(upbit)

@route('/velocity', method='GET')
def velocity(): return 'no velocity yet'

@route('/accel', method='GET')
def accel():
    amplify   = 10.
    id        = int(request.GET.id.strip())
    heading   = request.GET.heading.strip()
    assert len(heading) == 1, 'heading too long: ' + heading
    vel[id][0] += impulse[heading][0] * amplify
    vel[id][1] += impulse[heading][1] * amplify
    return state(loc[id][0], loc[id][1], loc[id][2]) + ',' + str(vel[id][0]) + ',' + str(vel[id][1])

    # speed of light not imposed yet
    # if velx > clight: velx = clight; 
    # if velx < -clight: velx = -clight; 
    # if vely > clight: vely = clight; 
    # if vely < -clight: vely = -clight

    # this does not change location so no location boundary check

    # locx = loc[pidx][0] + vel[pidx][0]; 
    # locy = loc[pidx][1] + vel[pidx][1]
    # if locx < 0.: locx += torew; 
    # if locx >= torew: locx -= torew; 
    # if locy < 0.: locy += torns; 
    # if locy >= torns: locy -= torns
    # loc[pidx][0] = locx; 
    # loc[pidx][1] = locy
    # print(state(loc[pidx]))
    # return(state(loc[pidx]))

@route('/dive', method='GET')
def dive(): return 'no dive yet'

@route('/message', method='GET')
def message(): return 'no message yet'

@route('/listen', method='GET')
def listen(): return 'no listen yet'


def state(x, y, z): return str(int(x)) + ',' + str(int(y)) + ',' + str(int(z))


application = bottle.default_app()
if __name__ == '__main__': run(app=application, host='0.0.0.0', port=8080, reloader=True)
