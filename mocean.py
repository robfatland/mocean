version_message = 'v2 try 5, smaque!'

# Two ways to run Mocean Server: sudo systemctl start mocean and python mocean    
#   - 'restart' after mod mocean.py; clear: daemon-reload; journalctl -xe diagnostics
#   - use 'stop' before switching to option 2, status to verify 
#     - bottle/uwsgi environment is mocean-env: conda info --envs
#     - conda activate mocean-env; and note 'run' at end of mocean.py works both
#
# Lists (not tuples) for state variables (mutable)
#   Joined player has a name and index (spoofing possible!) 
#     players[]:  a list of strings. Quit player has namestring set to ''
#     loc[] list of coordinate lists: [x, y, z]
#     vel[] list of velocity lists: [vx, vy]
#     chat[]: a list of strings: chat messages, one per player
#     lastloctime[]: a list of time-of-last-location request
#         ...used to calculate new position according to distance = speed x time
#

# added for application code version:
import bottle

from bottle import request, route, run
import json
from math import sqrt, exp
import math
from random import randint, random
from time import time

# configure global
players, loc, vel, chat, lastloctime, maxspeed, playerinventory = [], [], [], [], [], [], []
torns, torew = 900, 900
startcoord_range_lo = 40
startcoord_range_hi = 90

hullspeed = 40.
minspeed = 0.33
slowfactor = 0.6
fastfactor = 1.45
veerangle = math.pi/12.
grabradius = 30.

# vertical parameters
deltadive = 5.

# bathymetry consists of a flat seafloor, one trench and some guassian seamounts
basedepth = 30.
trenchdepth = 50.
nSeamounts = 12
smx0, smx1, smy0, smy1 = 60, torew - 60 - 1, 60, torns - 60 - 1
sigma0, sigma1, amp0, amp1 = 10., 30., 10, 15.
seamounts = [[randint(smx0, smx1), randint(smy0, smy1), sigma0 + random()*sigma1, amp0 + random()*amp1] for i in range(nSeamounts)]

# trench defined as five contiguous rectangles
tr = []
tr.append([140, 260, 290, 315])
tr.append([260, 266, 290, 360])
tr.append([260, 330, 360, 365])
tr.append([330, 338, 360, 450])
tr.append([330, 410, 450, 455])

viewshedbase = 50.
nWhales = 17
nTreasures = nSeamounts

def calcseamount(i, x, y):
    r = sqrt((x - seamounts[i][0])**2 + (y - seamounts[i][1])**2)
    if r > 3.*seamounts[i][2]: return 0.
    return seamounts[i][3]*exp(-.5*(r/seamounts[i][2])**2)

def intrench(x, y):
    for i in range(len(tr)): 
        if x > tr[i][0] and x < tr[i][1] and y > tr[i][2] and y < tr[i][3]: return True
    return False

def bathymetry(x, y): 
    if intrench(x, y): depth = trenchdepth
    else: 
        depth = basedepth
        for i in range(len(seamounts)):
            depth -= calcseamount(i, x, y)
            if depth < 0.:
              depth = 0. 
              break
    return depth
    

whales    = [[randint(0, torew - 1), randint(0, torns - 1), 0] for i in range(nWhales)]
treasures = [[seamounts[i][0], seamounts[i][1], bathymetry(seamounts[i][0], seamounts[i][1])] for i in range(len(seamounts))]

treasures[0].append('palantir')                      # see whales and players
treasures[1].append('spare air')                     # stay down longer
treasures[2].append('iron dust')                     # plankton bloom
treasures[3].append('sharp knife')                   # cut away ocean garbage from whale
treasures[4].append('map')                           # see bathymetry and treasure
treasures[5].append('bathysphere ALVIN')             # dive into trench
treasures[6].append('bathysphere JASON')             # dive into trench
treasures[7].append('bathysphere ROPOS')             # dive into trench
treasures[8].append('bag of donuts')                 # snack
treasures[9].append('800 pieces of eight')
treasures[10].append('8800 pieces of eight')
treasures[11].append('88000 pieces of eight')

@route('/mocean', method='GET')
def mocean_hello():

    m = ""
    client_type = request.GET.client.strip()

    if client_type == 'browser': 
        eol = '<br>'
        m += "<!DOCTYPE HTML>"
        m += "<html>"
        m += "<head>"
        m += "<title>Welcome to the Toroidal Mocean!</title>"
        m += "</head>"
        m += "<body>"
        m += "<div>"
        m += "<tt>"
        m += "<PRE>"

    else:
        eol = '\n'
    
    m  += version_message + eol
    m  += "                             hullspeed " + str(hullspeed)                        + eol
    m  += "    Unless noted: failed routes return 0, successful routes return 1              " + eol
    m  += "                                                                                  " + eol
    m  += "route            key         value                     return string              " + eol
    m  += "=========        =========   ==================        =====================      " + eol
    m  += "                                                                                  " + eol
    m  += "BASIC ACTIONS                                                                     " + eol
    m  += "mocean           -           -                         this message               " + eol
    m  += "                                                         (from a browser: add on  " + eol
    m  += "                                                          '?client=browser' for   " + eol
    m  += "                                                          a better printout)      " + eol
    m  += "                                                                                  " + eol
    m  += "join             name        namestring                id                         " + eol
    m  += "                                                                                  " + eol
    m  += "quit             name        namestring                                           " + eol
    m  += "                                                                                  " + eol
    m  += "who              -           -                         lists players in game      " + eol
    m  += "                                                                                  " + eol
    m  += "name             id          my id                     gives the name from the id " + eol
    m  += "                                                                                  " + eol
    m  += "id               name        namestring                gives the id from the name " + eol
    m  += "                                                                                  " + eol
    m  += "look             id          my id                     list of nearby things:     " + eol
    m  += "                                                         thing,x,y,z,             " + eol
    m  += "                                                                                  " + eol
    m  += "get              id          my id                     grabs a nearby treasure    " + eol
    m  += "                                                         use inventory to see     " + eol
    m  += "                                                                                  " + eol
    m  += "inventory        id          my id                     list of what i have        " + eol
    m  += "                                                                                  " + eol
    m  += "COMMUNICATE                                                                       " + eol
    m  += "sendchat         id          sender id                                            " + eol
    m  += "                 name        name of recipient                                    " + eol
    m  += "                 message     the message to send       also sets speed to zero    " + eol
    m  += "                                                                                  " + eol
    m  += "popchat          id          my id                     message if there is one    " + eol
    m  += "                                                       '0' if no message          " + eol
    m  += "                                                                                  " + eol
    m  += "NAVIGATE                                                                          " + eol
    m  += "location         id          my id                     x,y,z,f0,f1,f2             " + eol
    m  += "                                                         x,y,z = location, depth  " + eol
    m  += "                                                         f0 = wrap flag           " + eol
    m  += "                                                         f1 = message flag        " + eol
    m  += "                                                         f2 = nearby flag         " + eol
    m  += "                                                                                  " + eol
    m  += "velocity         id          my id                     vx,vy = velocity           " + eol
    m  += "                                                                                  " + eol
    m  += "accel            id          my id                                                " + eol
    m  += "                 ctrl        one of: w a s d           x,y,z,vx,vy (loc, vel)     " + eol
    m  += "                                                                                  " + eol
    m  += "dive             id          my id                                                " + eol
    m  += "                 ctrl        one of: r f               r = rise, f = down         " + eol
    m  += "                                                       x,y,z,vx,vy (loc, vel)     " + eol
    m  += "                                                                                  " + eol
    m  += "teleport         id          my id                                                " + eol
    m  += "                 x           destination x                                        " + eol
    m  += "                 y           destination y             x,y,z (location)           " + eol
    m  += "                                                                                  " + eol
    m  += "ping             id          my id                     depth in +meters to bottom " + eol
    m  += "                                                                                  " + eol
    m  += "                                                                                  " + eol

    if client_type == 'browser': 
        m += "</PRE>"
        m += "</div>"
        m += "</body>"
        m += "</html>"

    return(m)

####################
# 
# utility functions
# 
####################

def idok(id):
    if id < 0 or id >= len(players) or len(players[id]) == 0: return False
    return True

def viewshed(id):
    retval = viewshedbase - loc[id][2]
    if retval < 5: retval = 5
    return retval

def proximity(x, y, z, u, v, w): return sqrt((x-u)**2 + (y-v)**2 + (z-w)**2)

def myproximity(id, thing): 
    return proximity(loc[id][0], loc[id][1], loc[id][2], thing[0], thing[1], thing[2])


####################
#
# routes: basic
#
####################

@route('/join', method='GET')
def join():
    candidate_name = request.GET.name.strip()
    try :    
        print('possible player name = ', candidate_name)
        if candidate_name in players: return '0'
        players.append(candidate_name) 
        loc.append([randint(startcoord_range_lo, startcoord_range_hi), 
                    randint(startcoord_range_lo, startcoord_range_hi), 
                    0])
        vel.append([0., 0.])
        lastloctime.append(time())
        maxspeed.append(hullspeed)
        chat.append('')
        playerinventory.append(['air tank', 1.])           
    except ValueError as ve: return '0'
    return str(players.index(candidate_name))           


@route('/quit', method='GET')
def quit():
    candidate_quit = request.GET.name.strip()
    print("                     quit:", candidate_quit)
    if not candidate_quit in players: 
        return '0'
    try : 
        player_index = players.index(candidate_quit)
        players[player_index] = ''
    except : return '0'
    return '1'


@route('/who', method='GET')
def who(): 
    lead_msg = 'there are '
    names_msg = ''
    nplayers = 0
    for name in players:           # each name is a 2-element list
      if len(name) > 0:
        nplayers += 1
        names_msg += name + ' '
    return lead_msg + str(nplayers) + ' players: ' + names_msg

@route('/name', method='GET')
def name(): 
    id = int(request.GET.id.strip())
    if not idok(id): return '0'
    if len(players[id]): return players[id]
    return '0'

@route('/id', method='GET')
def id(): 
    name = int(request.GET.name.strip())
    if name in players: return str(players.index(name))           
    return '0'


@route('/look', method='GET')
def look(): 
    id = int(request.GET.id.strip())
    if not idok(id): return '0'
    nearbystring = ''
    theviewshed = viewshed(id)
    for whale in whales:
        if myproximity(id, whale) < theviewshed:
            nearbystring += 'whale,'
            nearbystring += str(whale[0]) + ','
            nearbystring += str(whale[1]) + ','
            nearbystring += str(whale[2]) + ','
    for treasure in treasures:
        if myproximity(id, treasure) < theviewshed:
            nearbystring += 'treasure,'
            nearbystring += str(treasure[0]) + ','
            nearbystring += str(treasure[1]) + ','
            nearbystring += str(treasure[2]) + ','
    return nearbystring

@route('/get', method='GET')
def get(): 
    id = int(request.GET.id.strip())
    if not idok(id): return '0'
    for treasure in treasures:
        if myproximity(id, treasure) < grabradius:
            treasure_index = treasures.index(treasure)
            playerinventory[id].append(treasure[3])
            del(treasures[treasure_index])
            print('diag: treasures = ' + str(treasures))
            print('diag: player got treasure, their inv = ' + str(playerinventory[id]))
    return 

@route('/inventory', method='GET')
def inventory(): 
    id = int(request.GET.id.strip())
    if not idok(id): return '0'
    return str(playerinventory[id])

@route('/use', method='GET')
def give(): 
  return 'use not implemented yet'


############################
#
# routes: chat, broadcast
#
############################

@route('/sendchat', method='GET')
def sendchat():
    id = int(request.GET.id.strip())
    if not idok(id): return '0'
    vel[id] = [0., 0.]                        # sendchat stops the player
                                              # this freezes you while you type out the message
                                              # and it runs whether or not you include the other args
    recipient = request.GET.name.strip()
    if not recipient in players: return '0'
    message   = request.GET.message.strip()
    if not len(message): return '0'

    recip_id = players.index(recipient)
    if len(chat[recip_id]): return '0'
    try : 
        chat[recip_id] = players[id] + ': ' + message
        return '1'
    except : return '0' 
    return '0'

@route('/popchat', method='GET')
def popchat():
    id        = int(request.GET.id.strip())
    if not idok(id): return '0'
    if not len(chat[id]): return '0'
    try : 
        return_message = chat[id]
        chat[id] = ''
        return return_message
    except : return '0' 
    return '0'

############################
#
# Spatial / Dynamical
#
############################

def locationstring(id):    return str(loc[id][0]) + ',' + str(loc[id][1]) + ',' + str(loc[id][2])
def velocitystring(id):    return str(vel[id][0]) + ',' + str(vel[id][1])
def playerspeed(id):       return sqrt(vel[id][0]**2 + vel[id][1]**2)
def playerspeedstring(id): return str(playerspeed(id))

###############
#
# acceleration controls
#
###############

def ctrlok(ctrl):
    if ctrl == 'w' or ctrl == 's' or ctrl == 'a' or ctrl == 'd': return True
    return False

def tapbreaks(id): 
    if playerspeed(id) < minspeed: 
        vel[id] = [0., 0.]
        return True
    vel[id] = [slowfactor * vel[id][0], slowfactor * vel[id][1]]
    return True

def gofaster(id): 
    the_speed = playerspeed(id)
    if the_speed > maxspeed[id]: return True
    if the_speed == 0.: 
        vel[id] = [1., 0.]
        return True
    vel[id] = [fastfactor * vel[id][0], fastfactor * vel[id][1]]
    return True

def veer(id, direction):
    the_speed = playerspeed(id)
    if the_speed == 0.: return True
    heading = math.atan2(vel[id][1], vel[id][0])
    if direction == 'left': heading += veerangle
    else:                   heading -= veerangle
    vel[id] = [the_speed*math.cos(heading),the_speed*math.sin(heading)]
    return True

@route('/location', method='GET')
def location():
    id = int(request.GET.id.strip())
    if not idok(id): return '0'
    wrapflag = 0
    dt = time() - lastloctime[id]
    lastloctime[id] = time()
    loc[id][0] += vel[id][0] * dt
    loc[id][1] += vel[id][1] * dt
    if loc[id][0] < 0:      loc[id][0] += torew ; wrapflag = 1
    if loc[id][1] < 0:      loc[id][1] += torns ; wrapflag = 1
    if loc[id][0] >= torew: loc[id][0] -= torew ; wrapflag = 1
    if loc[id][1] >= torns: loc[id][1] -= torns ; wrapflag = 1

    # access the message with the popchat route
    msgflag = 0 if not len(chat[id]) else 1

    # nearbyflag is intended to reduce the number of 'look' routes
    nearbyflag = 0 
    theviewshed = viewshed(id)
    for treasure in treasures:
        if myproximity(id, treasure) < theviewshed: 
            nearbyflag = 1
            break
    if not nearbyflag: 
        for whale in whales:
            if myproximity(id, whale) < theviewshed: 
                nearbyflag = 1
                break

    return locationstring(id) + ',' + str(wrapflag) + ',' + str(msgflag) + ',' + str(nearbyflag)

@route('/velocity', method='GET')
def velocity(): 
    id = int(request.GET.id.strip())
    if not idok(id): return '0'
    return velocitystring(id)

@route('/accel', method='GET')
def command():
    id = int(request.GET.id.strip())
    if not idok(id): return '0'
    ctrl = request.GET.ctrl.strip()
    if not ctrlok(ctrl): return '0'
    if   ctrl == 'w': gofaster(id)
    elif ctrl == 's': tapbreaks(id)
    else: 
        veerdirection = 'left' if ctrl == 'a' else 'right'
        veer(id, veerdirection)
    return locationstring(id) + ',' + velocitystring(id)

@route('/teleport', method='GET')
def teleport():
    id  = int(request.GET.id.strip())
    if not idok(id): return '0'
    tic = time()
    x   = float(request.GET.x.strip())
    y   = float(request.GET.y.strip())
    if x >= 0. and x < torew and y >= 0. and y < torns:
        loc[id] = [x, y, 0.]
        dt = time() - tic
        return locationstring(id) + ',' + str(dt*1000.)
    return '0'

@route('/dive', method='GET')
def dive():
    id  = int(request.GET.id.strip())
    if not idok(id): return '0'
    ctrl = request.GET.ctrl.strip()
    if ctrl != 'r' and ctrl != 'f': return '0'
    if playerspeed(id) > 0: return '0'
    mydepth = loc[id][2]
    if ctrl == 'r':
        mydepth -= deltadive
        if mydepth < 0.: mydepth = 0.
    else:
        seafloordepth = bathymetry(loc[id][0], loc[id][1])
        mydepth += deltadive
        if mydepth > seafloordepth: mydepth = seafloordepth
    loc[id][2] = mydepth
    return locationstring(id)

@route('/ping', method='GET')
def ping():
    id  = int(request.GET.id.strip())
    if not idok(id): return '0'
    # funny idea
    # if playerspeed(id) > hullspeed/2: return str(200 + randint(1,500))
    thisdepth = bathymetry(loc[id][0], loc[id][1])
    # print(loc[id][0], loc[id][1], thisdepth)
    return str(thisdepth)


#####################################################
#####################################################
####
####   STEPS game and related utilities
####
#####################################################
#####################################################


@route('/hello')
def hello(): return 'be a swell and have some 3.14'


################## begin ########################

@route('/begin', method='GET')
def steps_game_part_1():
    msg = request.GET.message.strip()
    try :  vfloat = float(msg) 
    except : return 'you are on the right route, "begin", but your message is not numerical enough for me!!!'
    v = int(vfloat)
    if v < 0: return 'ah good, you are getting warm... i like numbers but this one is a bit negative :( '
    if v == 0: return "nice message... but it a bit small don't you think?" 
    if not float(v) == vfloat: return 'actually I need an integer, and ' + str(vfloat) + ' has digits after the decimal point...' 
    if not isprime(v): return 'your message is positive but not prime enough' 
    if v <= 100: return "your message is prime! Make it a bit bigger, like over the century mark, and you're there"
    return "congrats, you solved it!!! A prime greater than 100. The next step: Begin again, this time using the route 'beguine'"

@route('/beguine', method='GET')
def steps_game_part_2():
    msg  = request.GET.message.strip()
    fibo = genfibo(30)
    try :    vfloat = float(msg) 
    except : return 'you are on route: "beguine"! Level 2 of the steps game... but this stage requires a number' 
    v = int(vfloat)
    if not float(v) == vfloat: return('...actually I am looking for an integer; but ' + str(vfloat) + ' has digits after the decimal point...')
    if v < 0: return('ah good, an integer, you are getting close. But stay with non-negative integers for this one')
    if v == 0: return("very nice... the first Fibonacci number! you are warm!")
    if v == 1: return("very nice... the second (and third) Fibonacci number! not quite there yet but heating up!")
    if v == 2: return("very nice... the fourth Fibonacci number! getting warmer")
    if v in fibo:
        this_index = fibo.index(v)
        if this_index == 16: return("   Congratulations! You solved the beguine route...       \n\n" + \
                                    "       (5000 Bonus Points if you calculated 987 using Python code...) \n\n" + \
                                    "           Continue the game on the 'sirduke' route...                      \n")
        return('you tried Fibonacci number ' + str(this_index + 1) + ' (which is ' + str(v) + '); right track but I am a huge fan of the *seventeenth* one...')
    return("your guess is in the right neighborhood... try making a left on Fibonacci street...")

@route('/sirduke', method='GET')
def steps_game_part_3():
    msg = request.GET.message.strip()
    if not msg == 'wigs':  return("This time I need the fourth word of the song 'Satin Doll'...")
    return("Well done! You're nobody's fool... Move on to route 'euler' now!")

@route('/euler', method='GET')
def steps_game_part_4():
    msg = request.GET.message.strip()
    try :    vfloat = float(msg) 
    except : return('you are on route "euler", level 4 of the Steps game.  This stage requires a number.')
    v = int(vfloat)
    if not float(v) == vfloat: return('...actually I am looking for an integer; whereas ' + str(vfloat) + ' has digits after the decimal point...')
    if v < 0: return('ah good, an integer, thank you, you are getting close. This integer will be positive.')
    if v < 3: return("very nice... but this integer is the sum of some other positive integers!")
    this_solution = 5000 * 10001
    if not v == this_solution: return("I need to know the sum of 1 + 2 + 3 + 4 + 5 + ... + 10000")
    return("very nice, Euler would be pleased. On to the final route, called 'meruprastarah'")

@route('/meruprastarah', method='GET')
def steps_game_part_5():
    msg = request.GET.message.strip()
    the_list = msg.split(',')
    if not len(the_list) == 6: return("I would like the 6th row of Pascale's triangle, comma-separate: 1, ....")
    try:    il = [int(the_list[i].strip()) for i in range(6)]
    except: return("you sent a list of six items, far as I can tell, but they must all be integers.")
    sl = [1, 5, 10, 10, 5, 1]
    if not il == sl: return ("Six items is correct; but I need the six numbers in row six of the Pascale triangle, separated by commas.")
    return('Well done!! You have completed the Steps game. Tell Rob this on Slack!!!')

def genfibo(n):
    if n < 3: n = 3
    if n > 30: n = 30
    fibo = [0, 1]
    for i in range(2, n): fibo.append(fibo[-1] + fibo[-2])
    return fibo
    
def isprime(n):
    if n == 2: return True
    if n < 2 or not n % 2: return False
    for i in range(3, int(sqrt(n))+1, 2): 
        if not n % i: return False
    return True
       
# How to run it in casual mode...
# run(host='0.0.0.0', port=8080, reloader=True)


application = bottle.default_app()
if __name__ == '__main__': run(app=application, host='0.0.0.0', port=8080, reloader=True)

