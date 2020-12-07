# Overview
#   There are two ways to run the Mocean Server: Directly and using the systemd daemon controller.
#     - For normal operation (which will restart the Server if it stops): Use systemd
#       - THIS CURRENTLY HAS A MAJOR BUG AND RESTARTS EVERY 5 MINUTES
#       - sudo systemctl start mocean
#       - After editing mocean.py: sudo systemctl restart mocean 
#       - Clear the decks: sudo systemctl daemon-reload
#       - Debugging info: journalctl -xe 
#     - For development / testing use direct execution
#       - sudo systemctl stop mocean
#         - wait for the process to halt; use sudo systemctl status mocean
#       - check the bottle/mocean environment is available: conda info --envs
#       - conda activate mocean-env 
#       - python mocean.py
#         - notice the 'run' at the end of the file also works for a systemd service
#
# Notes
#   tuples being immutable: this code uses lists for player status
#     A joined player has an index or id that they use to self-identify
#       This certainly permits spoofing :)
#     Data include
#       players[]:  a list of strings. Quit player has namestring set to ''
#       loc[] list of coordinate lists: [x, y, z]
#       vel[] list of velocity lists: [vx, vy]
#       chat[]: a list of strings: chat messages, one per player
#       lastloctime[]: a list of time-of-last-location request
#         ...used to calculate new position according to distance = speed x time
#
# Needed
#   overhead of execution timing: At what point does it impact gameplay? 
#   debugging needs improvement... where do diagnostics go to examine?
#   Mocean Server "on since" would be good once the big bug is fixed
#   Occasionally save status / reload on start?
#   Players expire after one hour?
#


# added for application code version:
import bottle

from bottle import request, route, run
import json
from math import sqrt
import math
from random import randint, random
from time import time

# configure global
players, loc, vel, chat, lastloctime = [], [], [], [], []
torns, torew = 900, 900
startcoord_range_lo = 200
startcoord_range_hi = 500

hullspeed = 30.
minspeed = 0.33
slowfactor = 0.7
fastfactor = 1.25
veerangle = math.pi/12.

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
    
    m  += "  Yarr Swells, lead on!         hullspeed is " + str(hullspeed)           + eol
    m  += "                                                                        " + eol
    m  += "route       key         value                return (string)            " + eol
    m  += "=========   =========   ==================   =====================      " + eol
    m  += "                                                                        " + eol
    m  += "BASIC INTERACTIONS                                                      " + eol
    m  += "mocean      -           -                    this message               " + eol
    m  += "                                                                        " + eol
    m  += "join        name        namestring           id                         " + eol
    m  += "                                                                        " + eol
    m  += "quit        name        namestring           confirm message            " + eol
    m  += "                                                                        " + eol
    m  += "who         -           -                    csv of players             " + eol
    m  += "                                                                        " + eol
#     m  += "look        -           -                    list of nearby itemnames   " + eol
#     m  += "get         id          my id                                           " + eol
#     m  += "            item        itemname             result flag '1' or '0'     " + eol
#     m  += "inventory   id          my id                list what i have           " + eol
#     m  += "use         id          my id                                           " + eol
#     m  += "            item        itemname             result of this action      " + eol
    m  += "                                                                        " + eol
    m  += "COMMUNICATE                                                             " + eol
    m  += "sendchat    id          sender id                                       " + eol
    m  += "            name        name of recipient                               " + eol
    m  += "            message     the message to send  '1' or '0' (success/fail)  " + eol
    m  += "popchat     id          my id                message if there is one    " + eol
    m  += "                                             '0' if there is no message " + eol
    m  += "                                                                        " + eol
    m  += "NAVIGATE                                                                " + eol
    m  += "location    id          my id                x,y,z,f0,f1                " + eol
    m  += "                                               x,y,z = location, depth  " + eol
    m  += "                                               f0 = wrap flag           " + eol
    m  += "                                               f1 = message flag        " + eol
    m  += "                                                                        " + eol
    m  += "velocity    id          my id                vx,vy = velocity           " + eol
    m  += "                                                                        " + eol
    m  += "accel       id          my id                                           " + eol
    m  += "            ctrl        one of: w a s d      x,y,z,vx,vy                " + eol
    m  += "                                                                        " + eol
    m  += "teleport    id          my id                                           " + eol
    m  += "            x           destination x                                   " + eol
    m  += "            y           destination y        x,y,z                      " + eol
    m  += "                                                                        " + eol
    m  += "                                                                        " + eol

    if client_type == 'browser': 
        m += "</PRE>"
        m += "</div>"
        m += "</body>"
        m += "</html>"

    return(m)


@route('/join', method='GET')
def join():
    candidate_name = request.GET.name.strip()
    try :    
        print('possible player name = ', candidate_name)
        if candidate_name in players: return 'join fail on duplicate player name'
        players.append(candidate_name) 
        loc.append([randint(startcoord_range_lo, startcoord_range_hi), 
                    randint(startcoord_range_lo, startcoord_range_hi), 
                    0])
        vel.append([0., 0.])
        lastloctime.append(time())
        chat.append('')
    except ValueError as ve: return("player join fail:" + str(ve))
    return str(players.index(candidate_name))           


@route('/quit', method='GET')
def quit():
    candidate_quit = request.GET.name.strip()
    print("                     quit:", candidate_quit)
    if not candidate_quit in players: 
        return 'quit fail for unlisted player'
    try : 
        player_index = players.index(candidate_quit)
        players[player_index] = ''
    except : return("quit fail")
    return (candidate_quit + " left the toroidal mocean")


@route('/who', method='GET')
def who(): 
    lead_msg = 'there are '
    names_msg = ''
    nplayers = 0
    for name in players:           # each name is a 2-element list
      if len(name) > 0:
        nplayers += 1
        names_msg += name + ' '
    if nplayers == 0: return lead_msg + '0 players'
    return lead_msg + str(nplayers) + ' players: ' + names_msg

@route('/look', method='GET')
def look(): return 'look route not implemented yet'

@route('/get', method='GET')
def get(): return 'get route not implemented yet'

@route('/inventory', method='GET')
def inventory(): return 'inventory route not implemented yet'

@route('/use', method='GET')
def use(): return 'use route not implemented yet'


############################
############################
##
## Chat / Broadcast 
##
############################
############################

@route('/sendchat', method='GET')
def sendchat():
    id        = int(request.GET.id.strip())
    recipient = request.GET.name.strip()
    message   = request.GET.message.strip()
    if id < 0: return '0'
    if id >= len(players): return '0'
    if not len(players[id]): return '0'
    if not recipient in players: return '0'
    if not len(message): return '0'
    recip_id = players.index(recipient)
    if len(chat[recip_id]): return '0'
    try : 
        chat[recip_id] = players[id] + ': ' + message
        return '1'
    except : return('0')
    return '0'

@route('/popchat', method='GET')
def popchat():
    id        = int(request.GET.id.strip())
    if id < 0: return '0'
    if id >= len(players): return '0'
    if not len(players[id]): return '0'
    if not len(chat[id]): return '0'
    try : 
        return_message = chat[id]
        chat[id] = ''
        return return_message
    except : return('0')
    return '0'

############################
############################
##
## Spatial / Dynamical
##
############################
############################

def locationstring(id): return str(loc[id][0]) + ',' + str(loc[id][1]) + ',' + str(loc[id][2])
def velocitystring(id): return str(vel[id][0]) + ',' + str(vel[id][1])

@route('/location', method='GET')
def location():
    wrapflag = 0
    id = int(request.GET.id.strip())
    dt = time() - lastloctime[id]
    lastloctime[id] = time()
    loc[id][0] += vel[id][0] * dt
    loc[id][1] += vel[id][1] * dt
    if loc[id][0] < 0:      loc[id][0] += torew ; wrapflag = 1
    if loc[id][1] < 0:      loc[id][1] += torns ; wrapflag = 1
    if loc[id][0] >= torew: loc[id][0] -= torew ; wrapflag = 1
    if loc[id][1] >= torns: loc[id][1] -= torns ; wrapflag = 1
    msgflag = 0 if not len(chat[id]) else 1
    return locationstring(id) + ',' + str(wrapflag) + ',' + str(msgflag)

@route('/velocity', method='GET')
def velocity(): return velocitystring(int(request.GET.id.strip()))

def speed(id):
    vx, vy = vel[id][0], vel[id][1]
    return sqrt(vx*vx + vy*vy)

def tapbreaks(id): 
    if speed(id) < minspeed: vel[id] = [0., 0.]
    vel[id] = [slowfactor * vel[id][0], slowfactor * vel[id][1]]
    return

def gofaster(id): 
    the_speed = speed(id)
    if the_speed > hullspeed: return
    if the_speed == 0.: 
        vel[id] = [1., 0.]
        return
    vel[id] = [fastfactor * vel[id][0], fastfactor * vel[id][1]]
    return 

def veer(id, direction):
    the_speed = speed(id)
    if the_speed == 0.: return
    heading = math.atan2(vel[id][1], vel[id][0])
    if direction == 'left': heading += veerangle
    else:                   heading -= veerangle
    vel[id] = [the_speed*math.cos(heading),the_speed*math.sin(heading)]
    return

@route('/accel', method='GET')
def accel():
    id    = int(request.GET.id.strip())
    ctrl  = request.GET.ctrl.strip()
    assert len(ctrl) == 1, 'control string too long: ' + ctrl
    assert ctrl == 'w' or ctrl == 's' or ctrl == 'a' or ctrl == 'd', 'bad control char'
    if ctrl == 's': tapbreaks(id)
    elif ctrl == 'w': gofaster(id)
    else: veer(id, 'left') if ctrl == 'a' else veer(id, 'right')
    return locationstring(id) + ',' + velocitystring(id)

@route('/teleport', method='GET')
def teleport():
    tic = time()
    id  = int(request.GET.id.strip())
    x   = float(request.GET.x.strip())
    y   = float(request.GET.y.strip())
    if x > 0. and x < torew and y > 0. and y < torns:
        loc[id] = [x, y, 0.]
        dt = time() - tic
        return locationstring(id) + ',' + str(dt*1000.)
    return '0'



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
    except : return('you are on the right route, "begin", but your message is not numerical enough for me!!!')
    v = int(vfloat)
    if v < 0: return('ah good, you are getting warm... i like numbers but this one is a bit negative :( ')
    if v == 0: return("nice message... but it a bit small don't you think?")
    if not float(v) == vfloat: return('actually I need an integer, and ' + str(vfloat) + ' has digits after the decimal point...')
    if not isprime(v): return('your message is positive but not prime enough')
    if v <= 100: return("your message is prime! Make it a bit bigger, like over the century mark, and you're there")
    return "congrats, you solved it!!! A prime greater than 100. The next step: Begin again, this time using the route 'beguine'"

@route('/beguine', method='GET')
def steps_game_part_2():
    msg  = request.GET.message.strip()
    fibo = genfibo(30)
    try :    vfloat = float(msg) 
    except : return('you are on route: "beguine"! Level 2 of the steps game... but this stage requires a number')
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

