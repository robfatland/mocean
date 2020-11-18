# added for application code version:
import bottle

from bottle import request, route, run
import json
from math import sqrt
import math
from random import randint, random

# configure global
players, loc, vel, start_dim, torns, torew = [], [], [], 600, 600, 800

vscale = 1.0
clight = 40.
rttwo = sqrt(2.)
piover8 = math.pi/8.
pi3over8 = math.pi*(3./8.)
cosp8 = math.cos(piover8)
sinp8 = math.sin(piover8)
cosp38 = math.cos(pi3over8)
sinp38 = math.sin(pi3over8)

impulse = [(1., 0.),             \
           (cosp8,sinp8),        \
           (rttwo,rttwo),        \
           (cosp38,sinp38),      \
           (0., 1.),             \
           (-cosp38,sinp38),     \
           (-rttwo,rttwo),       \
           (-cosp8,sinp8),       \
           (-1., 0.),            \
           (-cosp8,-sinp8),      \
           (-rttwo,-rttwo),      \
           (-cosp38,-sinp38),    \
           (0., -1.),            \
           (cosp38,-sinp38),     \
           (rttwo,-rttwo),       \
           (cosp8,-sinp38)] 


impulse_dictionary = { 'u': 0, '7': 1, '6': 2, '5': 3, '4': 4, '3': 5, '2': 6, 'q': 7, \
                       'a': 8, 'z': 9, 'x': 10, 'c': 11, 'v': 12, 'b': 13, 'n': 14, 'j': 15 }


@route('/mocean')
def mocean_hello():
    msg   = "be there swells, let's go a-whalin                                              \n"
    msg  += "                                                                                \n"
    msg  += "route    key         value                returns                               \n"
    msg  += "=====    ===         =====                =======                               \n"
    msg  += "mocean   -           -                    this usage message                    \n"
    msg  += "join     name        a-name               x,y,z                                 \n"
    msg  += "quit     name        a-name               confirm quit                          \n"
    msg  += "who      -           -                    csv of players                        \n"
    msg  += "location name        a-name               x,y,z                                 \n"
    msg  += "velocity name        a-name               vx,vy                                 \n"
    msg  += "move     name        a-name                                                     \n"
    msg  += "         heading     n, s, e or w         x,y,z                                 \n"
    msg  += "dive     name        a-name                                                     \n"
    msg  += "         direction   u or d               x,y,z                                 \n"
    msg  += "msg      name        all or a-name           ...                                \n"
    msg  += "         message     message                 ... confirm msg on queue           \n"
    msg  += "listen   name        all or a-name        '' or message at top of queue         \n"
    msg  += "                                                                                \n"
    return(msg)

@route('/join', method='GET')
def join():
    msg = request.GET.name.strip()
    try :    
        if msg in players: return 'duplicate player name not allowed to join'
        players.append(msg) 
        loc.append((random()*start_dim, random*start_dim, 0))
        vel.append((0., 0.))
    except ValueError as ve: 
        return("player join fail")
    return players[-1] + ',' + state(loc[-1][0], loc[-1][1], loc[-1][2])

@route('/quit', method='GET')
def quit():
    msg_string = request.GET.name.strip()
    print("                     quit:", msg_string)
    if not msg_string in players:
        return("quit fail for non-existent player")
    try: 
        player_index = players.index(msg_string)
        del players[player_index]; del loc[player_index]
    except : return("quit fail")
    return ("you have left the toroidal mocean")

@route('/who', method='GET')
def who(): 
    rmsg = 'players: '
    for name in players: rmsg += name + ' '
    return rmsg

@route('/location', method='GET')
def location(): return 'no location yet'

@route('/velocity', method='GET')
def velocity(): return 'no velocity yet'

@route('/move', method='GET')
def move():
    name      = request.GET.name.strip()
    heading   = request.GET.heading.strip()
    if not name in players: return 'move fail for unrecognized player'
    pidx = players.index(name)
    iidx = impulse[heading]

    impx  = impulse[iidx][0]; 
    impy  = impulse[iidx][1]
    velx += impx;             
    vely += impy
    if velx > clight: velx = clight; 
    if velx < -clight: velx = -clight; 
    if vely > clight: vely = clight; 
    if vely < -clight: vely = -clight

    vel[pidx][0] = velx; 
    vel[pidx][1] = vely
    locx = loc[pidx][0] + vel[pidx][0]; 
    locy = loc[pidx][1] + vel[pidx][1]
    if locx < 0.: locx += torew; 
    if locx >= torew: locx -= torew; 
    if locy < 0.: locy += torns; 
    if locy >= torns: locy -= torns
    loc[pidx][0] = locx; 
    loc[pidx][1] = locy
    print(state(loc[pidx]))
    return(state(loc[pidx]))

@route('/dive', method='GET')
def dive(): return 'no dive yet'

@route('/message', method='GET')
def message(): return 'no message yet'

@route('/listen', method='GET')
def listen(): return 'no listen yet'


def state(x, y, z): return str(int(x)) + ',' + str(int(y)) + ',' + str(int(z))








#####################################################
#####################################################
####
####   STEPS game and utilities
####
#####################################################
#####################################################


@route('/hello')
def hello(): return 'be swell and have two or three 3.14is'


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


application = bottle.defaut_app()

if __name__ == '__main__':
    run(app=application, host='0.0.0.0', port=8080, reloader=True)

