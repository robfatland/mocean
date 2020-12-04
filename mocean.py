# Left off with the PC Client not able to do popchat/sendchat
#
# Overview
#   To debug directly use `conda activate mocean-dev` to make the miniconda install of bottle 
#     available. Use sudo systemctl restart mocean to restart the service.
#
#   tuples being immutable I will stay dynamic by using lists
#     players[] is a list of strings. The index matches loc[] and vel[]
#     loc[] is [x, y, z]
#     vel[] is [vx, vy]
# 
# ideas
#   Server Operation
#   time out is a major issue; it resets the game every minute or two...
#     although maybe not for the Python Client
#   where print statements and other diagnostics go... is another big deal
#   it would be helpful to notice a start time; 
#     create a route called uptime returning 'since...'
# 
#   Players
#   expire after one hour?
#   who: lists only active players (not dead spots) 
#   quit: name collapses to '' and that is the only indication
#
#   Chat routes
#   Only two routes to begin with
#   Only one message held at a time
#   route popchat returns string 'sender: msg'
#   route sendchat returns string '1' or '0' 
# 
#   Broadcast routes
#   broadcast route
#
#   State
#   Create a state file that can be reloaded and then rewritten; and periodically updated
#   Clients can periodically check 'am  I in the game?' 
#     If not: There could be an assert route to reintroduce them 
#       This is a bad fix to the timeout issue


# added for application code version:
import bottle

from bottle import request, route, run
import json
from math import sqrt
import math
from random import randint, random
from time import time

# configure global
players, loc, vel, s0, s1, torns, torew = [], [], [], 200, 500, 1000, 1000

# for DMs
chat = []

# time of last location call also matching to player index
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

# ice-rink-style velocity changes
#   u is east, 4 = north, q west, c south
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


@route('/mocean', method='GET')
def mocean_hello():

    client_type = request.GET.client.strip()
    if client_type == 'browser': closeout = '<br>'
    else:                        closeout = '\n'
    
    msg   = "if thar be swells, lead on MacDuff                                   " + closeout
    msg  += "                                                                     " + closeout
    msg  += "route    key         value                returns                    " + closeout
    msg  += "=====    ===         =====                =======                    " + closeout
    msg  += "mocean   -           -                    this message               " + closeout
    msg  += "join     name        namestring           id                         " + closeout
    msg  += "quit     name        namestring           confirm message            " + closeout
    msg  += "who      -           -                    csv of players             " + closeout
    msg  += "sendchat id          sender id                                       " + closeout
    msg  += "         name        name of recipient                               " + closeout
    msg  += "         message     the message to send  '1' or '0' (success/fail)  " + closeout
    msg  += "popchat  id          my id                message if there is one    " + closeout
    msg  += "                                          '0' if there is no message " + closeout
    msg  += "                                                                     " + closeout

    return(msg)


@route('/join', method='GET')
def join():
    candidate_name = request.GET.name.strip()
    try :    
        print('possible player name = ', candidate_name)
        if candidate_name in players: return 'join fail on duplicate player name'
        players.append(candidate_name) 
        loc.append([randint(s0, s1), randint(s0, s1), 0])
        vel.append([0., 0.])
        lastloctime.append(time())
        chat.append('')
    except ValueError as ve: 
        return("player join fail")
    return str(players.index(candidate_name))           # will be this players id


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


#####################################################
#####################################################
####
####   STEPS game and utilities
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

