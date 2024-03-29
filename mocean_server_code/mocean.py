version_string = "V3.14 Caprice Edition non troppo"

# added for application code version:
import bottle

from bottle import request, route, run
import json
<<<<<<< Updated upstream
from math import sqrt, exp, sin, cos
import math
from random import randint, random
from time import time


# configure global state values
players, loc, vel, chat, lastloctime = [], [], [], [], []
maxspeed, playerinventory, whalerider, inlostcity = [], [], [], []
torns, torew = 900, 900
startcoord_range_lo = 40
startcoord_range_hi = 200
plankton_bloom = False

hullspeed = 40.
submergedspeed = 5.
whalespeed = 80.
minspeed = 0.33
slowfactor = 0.6
fastfactor = 1.45
veerangle = math.pi/12.
grabradius = 10.
boathookradius = 35.

# vertical parameters
deltadive = 5.

# bathymetry consists of a flat seafloor, one trench and some guassian seamounts
basedepth = 30.
trenchdepth = 50.
nSeamounts = 12
smx0, smx1, smy0, smy1 = 60, torew - 60 - 1, 60, torns - 60 - 1
sigma0, sigma1, amp0, amp1 = 10., 30., 10, 15.
seamounts = [[randint(smx0, smx1), randint(smy0, smy1), sigma0 + random()*sigma1, amp0 + random()*amp1] for i in range(nSeamounts)]
=======
from math import sqrt
from random import randint

# configure global
players, locs, start_dim, torns, torew = [], [], 200, 400, 600

@route('/mocean', method='GET')
def mocean(): 
    msg = "\nbe there swells, let's go a-whalin\n\n")
    msg += "route       key        value            returns:                          \n")
    msg += "=======     =======    =======          ===================               \n")
    msg += "mocean      ----       ----             this usage message                \n")
    msg += "join        name       player's name    name,num_players,x,y,z            \n")
    msg += "quit        name       player's name    goodbye msg                       \n")
    msg += "who         ----       ----             csv list of players               \n")
    msg += "move        name       player's name                                      \n")
    msg += "            heading    north ... west   csv new location x,y,z            \n")
    msg += "dive        name       player's name                                      \n")
    msg += "            direction  up or down       csv new location x,y,z            \n")
    msg += "chat        name       player's name                                      \n")
    msg += "            message    a message        confirm message is on queue       \n")
    msg += "listen      queue      all or player                                      \n")
    msg += "            player     player's name                                      \n")
    return msg
>>>>>>> Stashed changes

# the trench is defined as five contiguous rectangles
tr = []
tr.append([140, 260, 290, 315])
tr.append([260, 266, 290, 360])
tr.append([260, 330, 360, 365])
tr.append([330, 338, 360, 450])
tr.append([330, 410, 450, 455])

<<<<<<< Updated upstream
viewshedbase       = 20.
viewshedbinoculars = 100.

###################
#
# utility functions
#
###################


def calcseamount(i, x, y):
    '''for a given location calculate the height of seamounts[i]'''
    r = sqrt((x - seamounts[i][0])**2 + (y - seamounts[i][1])**2)
    if r > 3.*seamounts[i][2]: return 0.
    return seamounts[i][3]*exp(-.5*(r/seamounts[i][2])**2)

def seamountclosestproximity(id):
    x = loc[id][0]
    y = loc[id][1]
    min_distance = torew * torns
    min_index = -1
    for i in range(len(seamounts)):
        a = x - seamounts[i][0]
        b = y - seamounts[i][1]
        while a > torew/2: a -= torew
        while a < -torew/2: a += torew
        while b > torns/2: b -= torns
        while b < -torns/2: b += torns
        c = sqrt(a**2 + b**2)
        if c < min_distance:
            min_distance = c
            min_index = i
    assert min_index > -1 and min_index < len(seamounts), 'fail in seamountclosestprox()'
    return min_index
   
def intrench(x, y):
    '''bool for whether a location is in the trench or not'''
    for i in range(len(tr)): 
        if x > tr[i][0] and x < tr[i][1] and y > tr[i][2] and y < tr[i][3]: return True
    return False


def bathymetry(x, y): 
    '''for a location return the seafloor depth as floating point positive meters'''
    if intrench(x, y): depth = trenchdepth
    else: 
        depth = basedepth
        for i in range(len(seamounts)):
            depth -= calcseamount(i, x, y)
            if depth < 0.:
                depth = 0. 
                break
    return depth


def idok(id):
    '''boolean integer id value corresponds to a player'''
    if id < 0 or id >= len(players) or len(players[id]) == 0: return False
    return True

def itemindex(id, item):
    '''if item in p[id]'s inventory list (match sub-list[1]): Return the index of that item, else -1'''
    for inventoryitem in playerinventory[id]:
        if item == inventoryitem[1]: 
            return playerinventory[id].index(inventoryitem)
    return -1

def viewshed(id):
    '''determine how far a player can see'''
    if itemindex(id, 'binoculars') >= 0: return viewshedbinoculars
    retval = viewshedbase - loc[id][2]
    if retval < 5.: retval = 5.
    return retval


def proximity(x, y, z, u, v, w): 
    '''determine distance between two 3D points using coordinates'''
    return sqrt((x-u)**2 + (y-v)**2 + (z-w)**2)


def myproximity(id, thing): 
    '''determine distance between a player (from id) and a thing'''
    return proximity(loc[id][0], loc[id][1], loc[id][2], thing[0], thing[1], thing[2])

def myplayerproximity(name1, name2): 
    '''determine distance between a player (from id) and a thing'''
    i1 = players.index(name1)
    i2 = players.index(name2)
    return proximity(loc[i1][0], loc[i1][1], loc[i1][2], loc[i2][0], loc[i2][1], loc[i2][2])


def locationstring(id):    
    '''convert a player x y z location to a comma-separated string'''
    return str(loc[id][0]) + ',' + str(loc[id][1]) + ',' + str(loc[id][2])


def velocitystring(id):    
    '''convert a player vx vy velocity to a comma-separated string'''
    return str(vel[id][0]) + ',' + str(vel[id][1]) + ',' + str(vel[id][2])

def playerheading(id):       
    '''return player heading in radians as a floating point value'''
    return math.atan2(vel[id][1], vel[id][0])

def playerspeed(id):       
    '''return player speed as a floating point value'''
    return sqrt(vel[id][0]**2 + vel[id][1]**2)

def playerspeedstring(id): 
    '''return player speed as a string'''
    return str(playerspeed(id))


def ctrlok(ctrl):
    '''boolean: accel control is valid'''
    if ctrl == 'w' or ctrl == 's' or ctrl == 'a' or ctrl == 'd': return True
    return False


def tapbreaks(id): 
    '''slow down the player (or if they are slow already: stop them)'''
    if playerspeed(id) < minspeed: 
        vel[id][0], vel[id][1] = 0., 0.
        return True
    vel[id][0], vel[id][1] = slowfactor * vel[id][0], slowfactor * vel[id][1]
    return True


def gofaster(id): 
    '''speed the player up by fastfactor, up to the players maximum speed'''
    the_speed = playerspeed(id)
    if the_speed > maxspeed[id]: return True
    if the_speed == 0.: 
        vel[id][0], vel[id][1] = cos(vel[id][2]), sin(vel[id][2])
        return True
    vel[id][0], vel[id][1] = fastfactor * vel[id][0], fastfactor * vel[id][1]
    return True

def veer(id, direction):
    '''veer off left or right corresponding to a / d controls'''
    s = playerspeed(id)
    heading = vel[id][2]
    if direction == 'left': heading += veerangle
    else:                   heading -= veerangle
    vel[id][0], vel[id][1], vel[id][2] = s*cos(heading), s*sin(heading), heading
    return True

##########
#
# functions for Steps game
#
##########

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

###################
#
# set up the "things" (whales and treasures) in the world
#
###################

nWhales = 17
nTreasures = nSeamounts

whales    = [[randint(0, torew - 1), randint(0, torns - 1), 0] for i in range(nWhales)]

# this is of course a hardcode
whales[0].append('Anisha')
whales[1].append('Stephen Jay Gould')
whales[2].append('Debbie Kelley')
whales[3].append('Herman Melville')
whales[4].append('Ishmael')
whales[5].append('Charles Darwin')
whales[6].append('William Wang')
whales[7].append('Paul Erdos')
whales[8].append('George Of The Jungle')
whales[9].append('Simone de Beauvoir')
whales[10].append('Alex Honnold')
whales[11].append('Marvin Gaye')
whales[12].append('Bill Watterson')
whales[13].append('James Earl Jones')
whales[14].append('Richard Alley')
whales[15].append('Naomi Oreskes')
whales[16].append('Yayoi Kusama')

treasures = [[seamounts[i][0], seamounts[i][1], bathymetry(seamounts[i][0], seamounts[i][1])] for i in range(len(seamounts))]

# this is of course a hardcode
treasures[0].append('fishing net')
treasures[1].append('crash alert')
treasures[2].append('JSON ROV')
treasures[3].append('ALVIN submarine')
treasures[4].append('imaging sonar')
treasures[5].append('teleport crystal')
treasures[6].append('chrono-synclastic infundibulum')
treasures[7].append('binoculars')
treasures[8].append('ham and cheese sandwich')
treasures[9].append('boat hook')
treasures[10].append('iron dust')
treasures[11].append('iron dust')

# this is of course a hardcode
seamounts[0].append('Mount Crumpet')                 
seamounts[1].append('Axial Seamount')                     
seamounts[2].append('Meru Prastarah')                     
seamounts[3].append('Krakatoa')                       
seamounts[4].append('Atlantis')                           
seamounts[5].append('Euler Seamount')             
seamounts[6].append('Ridhi Seamount')             
seamounts[7].append('Aiden Seamount')             
seamounts[8].append('Loihi Seamount')                 
seamounts[9].append("Kick 'em Jenny")
seamounts[10].append('West Mata')
seamounts[11].append('Vema Seamount')

#####################
#
# The mocean usage route
#
#####################

version_message = version_string + '   browser? add client=browser. brief? add usage=brief'
world_message   = 'our ocean is ' + str(torew) + ' by ' + str(torns) + '. hullspeed is ' + str(hullspeed)

@route('/mocean', method='GET')
def mocean():

    m = ""
    client_type = request.GET.client.strip()
    usage_type  = request.GET.usage.strip()

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
    m  += world_message + eol

    if usage_type == 'brief':

        m  += "mocean                 --> this message (this is the brief version)      " + eol
        m  += "join         name      --> id string '0', '1', '2', etcetera             " + eol
        m  += "quit         name      --> '1' on success and '0' on fail                " + eol
        m  += "who                    --> there are 2 players: fred wilma               " + eol
        m  += "name         id        --> name of player with this id                   " + eol
        m  += "id           name      --> id of player with this name                   " + eol
        m  += "look         id        --> what you see, where it is: thing,x,y,z        " + eol
        m  += "get          id, item  --> did i manage to grab something nearby         " + eol
        m  += "inventory    id        --> list of what i have                           " + eol
        m  += "sendchat     id, name, message                                           " + eol
        m  += "popchat      id        --> the message for me if there is one (or '0')   " + eol
        m  += "location     id        --> x, y, z, wrap flag, message flag, nearby flag " + eol
        m  += "velocity     id        --> vx, vy, heading in radians                    " + eol
        m  += "accel        id, ctrl: use w faster s slower a left d right              " + eol
        m  += "stop         id        --> stop swimming (velocity goes to 0, 0)         " + eol
        m  += "dive         id, ctrl: use r to rise and f to go deeper                  " + eol
        m  += "teleport     id, x, y: teleport to new location                          " + eol
        m  += "ping         id        --> depth in +meters to sea floor where i am      " + eol

    else: 
        m  += "    Unless noted: a FAIL returns string 0, SUCCESS returns 1                      " + eol
        m  += "                                                                                  " + eol
        m  += "route            key         value                     return string              " + eol
        m  += "=========        =========   ==================        =====================      " + eol
        m  += "                                                                                  " + eol
        m  += "BASIC ACTIONS                                                                     " + eol
        m  += "mocean           -           -                         this message (long version)" + eol
        m  += "                                                         client=browser --> HTML  " + eol
        m  += "                                                         usage=brief --> brief    " + eol
        m  += "                                                                                  " + eol
        m  += "join             name        must be alphanumeric      id string                  " + eol
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
        m  += "get              id          my id                                                " + eol
        m  += "                 item        item name                 try to get something       " + eol
        m  += "                                                                                  " + eol
        m  += "inventory        id          my id                     list items i have          " + eol
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
        m  += "velocity         id          my id                     vx,vy,heading in radians   " + eol
        m  += "                                                                                  " + eol
        m  += "accel            id          my id                                                " + eol
        m  += "                 ctrl        one of: w a s d           x,y,z,vx,vy,heading        " + eol
        m  += "                                                                                  " + eol
        m  += "stop             id          my id                     sets player velocity to 0  " + eol
        m  += "                                                                                  " + eol
        m  += "dive             id          my id                                                " + eol
        m  += "                 ctrl        one of: r f               r = rise, f = down         " + eol
        m  += "                                                       x,y,z,vx,vy,heading        " + eol
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
# routes: basic
#
####################

@route('/join', method='GET')
def join():
    name = request.GET.name.strip()
    if not name.isalnum(): return '-1'
    try :    
        if name in players: 
            return str(players.index(name))
        players.append(name) 
        loc.append([randint(startcoord_range_lo, startcoord_range_hi), 
                    randint(startcoord_range_lo, startcoord_range_hi), 
                    0.])
        vel.append([0., 0., random()*2.*math.pi])
        lastloctime.append(time())
        maxspeed.append(hullspeed)
        chat.append('')
        playerinventory.append([['air tank', 'air tank', 1.]])           
        whalerider.append(False)
        inlostcity.append(False)
    except ValueError as ve: return 'failed to join player into the game'
    return str(players.index(name))           


@route('/quit', method='GET')
def quit():
    name = request.GET.name.strip()
    if not name in players: 
        return 'quit failed: name not found in the active players list'
    try : 
        player_index = players.index(name)
        players[player_index] = ''
    except : return 'exception trying to remove player from active players list'
    return 'player ' + name + ' removed from the game'


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
    if not idok(id): return 'bad player id; try debugging using the id route'
    if len(players[id]): return players[id]
    return '0'


@route('/id', method='GET')
def id(): 
    name = request.GET.name.strip()
    if name in players: 
        return str(players.index(name))           
    return '-1'


@route('/look', method='GET')
def look(): 
    id = int(request.GET.id.strip())
    if not idok(id): return 'bad player id; try debugging using the id route'
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
    try : 
        id = int(request.GET.id.strip())
        if not idok(id): return 'bad player id; try debugging using the id route'
    except : 
        return 'id exception in get route'
    try : 
        item = request.GET.item.strip()
    except: 
        return 'item exception in get route'

    # the operational radius of a get depends on whether the player has the boathook treasure
    # to do this is a ridiculous way of checking whether the player has a boat hook
    radius = boathookradius if not itemindex(id, 'boat hook') < 0 else grabradius

    if item == 'treasure':
        for treasure in treasures:
            if myproximity(id, treasure) < radius:
                playerinventory[id].append(['treasure', treasure[3]])
                treasure_index = treasures.index(treasure)
 
                # an infinite supply of iron dust: it is not deleted from treasures[]
                #   to do also a large pile of abandoned 'crash alert' devices
                if not treasures[treasure_index][1] == 'iron dust':
                    del(treasures[treasure_index])
                got_treasure_msg = 'treasure recovered! '
                return got_treasure_msg            # to do: Expand this for esach treasure
                                                   # 
                                                   # fishing net... 
                                                   # crash alert
                                                   # JSON ROV
                                                   # ALVIN submarine
                                                   # imaging sonar
                                                   # teleport crystal
                                                   # (c-s i) 
                                                   # binoculars
                                                   # ham and cheese sandwich
                                                   # boat hook
                                                   # iron dust     'iron dust (from a large pile)'
                                                   # iron dust 
        return 'there is no treasure within your grasp at the moment'

    elif item == 'whale':
        if whalerider[id]: return 'you are already riding a whale'
        if not plankton_bloom: return 'all the whales are too hungry to help you'
        for whale in whales:
            if myproximity(id, whale) < radius:
                whale_index = whales.index(whale)
                whale_name = whale[3]
                playerinventory[id].append(['whale', whale_name])
                del(whales[whale_index])
                whalerider[id] = True
                maxspeed[id] = whalespeed
                return 'congratulations, you are now riding a whale'
        return 'there are no whales within your reach at the moment'
    return 'Did you specify the item you want to get? If so: That item is not available'

@route('/backdoor', method='GET')
def backdoor(): 
    id = int(request.GET.id.strip())
    if not idok(id): return 'bad player id; try debugging using the id route'
    for treasure in treasures: playerinventory[id].append(['treasure', treasure[3]])
    return 'ok'

@route('/bonanza', method='GET')
def bonanza(): 
    id = int(request.GET.id.strip())
    if not idok(id): return 'bad player id; try debugging using the id route'
    for treasure in treasures: playerinventory[id].append(['treasure', treasure[3]])
    return 'ok'

@route('/whalename', method='GET')
def whalename(): 
    id = int(request.GET.id.strip())
    if not idok(id): return 'bad player id; try debugging using the id route'
    if not whalerider[id]: return 'this player has no whale and hence no whale name'
    for inventoryitem in playerinventory[id]:
        if inventoryitem[0] == 'whale': return inventoryitem[1]
    return 'something is amiss; you are riding a whale but i could not find its name...'

@route('/treasurename', method='GET')
def treasurename():
    id = int(request.GET.id.strip())
    if not idok(id): return 'bad player id; try debugging using the id route'
    msg = 'treasures held by ' + players[id] + ': '
    for inventoryitem in playerinventory[id]:
        if inventoryitem[0] == 'treasure':
            msg += inventoryitem[1] + ' '
    return msg

@route('/seamountname', method='GET')
def seamountname():
    '''yields the name of the nearest seamount to player id-string'''
    # to do: Technically this is not published but available. The official way of 
    #   getting seamount names is by use applied to treasure crash alert. 
    id = int(request.GET.id.strip())
    if not idok(id): return 'bad player id; try debugging using the id route'
    nearest_index = seamountclosestproximity(id)
    msg = 'the nearest seamount to you is called ' + seamounts[nearest_index][4]
    return msg


@route('/inventory', method='GET')
def inventory(): 
    id = int(request.GET.id.strip())
    if not idok(id): return 'bad player id; try debugging using the id route'
    return str(playerinventory[id])


@route('/use', method='GET')
def use(): 
    global plankton_bloom
    id = int(request.GET.id.strip())
    if not idok(id): return 'bad player id; try debugging using the id route'
    item = request.GET.item.strip()

    thisindex = itemindex(id, item)
    if thisindex == -1: return 'player does not have requested item to use; be sure to spell it as listed in your inventory!'

    if item == 'iron dust':
        plankton_bloom = True
        del(playerinventory[id][thisindex])
        msg  = 'you sprinkle the iron dust on the surface of the ocean...\n'
        msg += '...the iron is a nutrient needed by plankton... \n'
        msg += '...so with all this iron the plankton begin to bloom...\n'
        msg += '...filling the ocean with miniscule copepods...\n'
        msg += '...which is what whales love to eat...\n'
        msg += '...so the whales enjoy a plankton feast...'
        return msg
    elif item == 'crash alert':
        closest_index = seamountclosestproximity(id)
        msg  = 'you look at your crash alert device...\n' 
        msg  = '...it seems to know about the names of undersea mountains that you are close to...\n'
        msg += '  it says: Closest seamount to your current location is: \n'
        msg += '  ' + seamounts[closest_index][4] + '\n'
        return msg
    elif item == 'fishing net':
        return 'catch fish! ...but this treasure is not yet active in the game'
    elif item == 'boat hook':
        return 'the boat hook automatically extends your reach for getting things...'
    elif item == 'JSON ROV':
        return 'you can send the ROV down to explore...  but this treasure is not yet active in the game'
    elif item == 'ALVIN submarine':
        return 'with ALVIN you are able to explore deep trenches... but this treasure is not yet active in the game'
    elif item == 'map':
        return 'this treasure is not yet active in the game...'
    elif item == 'teleport crystal':
        return 'the teleport crystal helps you teleport to anywhere in the mocean'
    elif item == 'chrono-synclastic infundibulum':
        return 'as you dissolve into wave-like form you realize you can go anywhere, more or less'
    elif item == 'binoculars':
        return 'these binoculars are used automatically: They give you the ability to see further off into the distance.'
    elif item == 'ham and cheese sandwich':
        return 'ah that was delicious. You feel not so hungry and ready for more action!'
    else:
        return 'there is no way to make use of that item right now'
    return "this item is not in your inventory; be sure to use exact spelling"


# to do make these treasures give sensible get responses...
# treasures[4].append('imaging sonar')
# treasures[6].append('chrono-synclastic infundibulum')


############################
#
# communication routes
#
############################

@route('/sendchat', method='GET')
def sendchat():
    id = int(request.GET.id.strip())
    if not idok(id): return 'bad player id; try debugging using the id route'

    vel[id][0], vel[id][1] = 0., 0.           # sendchat stops the player
                                              # this freezes you while you type out the message
                                              # and it runs whether or not you include the other args
    recipient = request.GET.name.strip()
    if not recipient in players: return 'player for chat message does not seem to be in the game'
    message   = request.GET.message.strip()
    if not len(message): return 'the message was not send: seems to be too short'

    recip_id = players.index(recipient)
    if len(chat[recip_id]): return 'player has an unread message blocking your message'
    try : 
        chat[recip_id] = 'player ' + players[id] + ' tells you: ' + message
    except : return 'sendchat failed for an unknown reason'
    return 'your message is in your recipients inbox waiting to be read'


@route('/popchat', method='GET')
def popchat():
    id        = int(request.GET.id.strip())
    if not idok(id): return 'bad player id; try debugging using the id route'
    if not len(chat[id]): return 'no message in your inbox'
    try : 
        return_message = chat[id]
        chat[id] = ''
    except : return 'popchat() experienced an unknown error' 
    return return_message


############################
#
# spatial routes
#
############################


@route('/location', method='GET')
def location():
    id = int(request.GET.id.strip())
    if not idok(id): return 'bad player id; try debugging using the id route'

    wrapflag = 0
    thisnow = time()
    dt = thisnow - lastloctime[id]
    lastloctime[id] = thisnow
    loc[id][0] += vel[id][0] * dt
    loc[id][1] += vel[id][1] * dt
    if loc[id][0] < 0:      loc[id][0] += torew ; wrapflag = 1
    if loc[id][1] < 0:      loc[id][1] += torns ; wrapflag = 1
    if loc[id][0] >= torew: loc[id][0] -= torew ; wrapflag = 1
    if loc[id][1] >= torns: loc[id][1] -= torns ; wrapflag = 1

    # if submerged adjust maxspeed and change depth if the sea floor rises
    if loc[id][2] > 0.:
        if not whalerider[id]: maxspeed[id] = submergedspeed
        depth = bathymetry(loc[id][0], loc[id][1])
        if depth < loc[id][2]:
            loc[id][2] = depth
            # when forced to surface return max speed to hull speed
            if depth == 0. and not whalerider[id]: maxspeed[id] = hullspeed

    # access the message with the popchat route
    msgflag = 0 if not len(chat[id]) else 1

    # nearbyflag reduces 'look' calls... arguably not really useful
    #   check treasures, whales and other players
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
    if not nearbyflag:
        for name in players: 
            if name != players[id] and len(name) > 0 and myplayerproximity(players[id], name) < theviewshed:
                nearbyflag = 1
                break

    return locationstring(id) + ',' + str(wrapflag) + ',' + str(msgflag) + ',' + str(nearbyflag)

@route('/velocity', method='GET')
def velocity(): 
    id = int(request.GET.id.strip())
    if not idok(id): return 'bad player id; try debugging using the id route'
    return velocitystring(id)

@route('/accel', method='GET')
def accel():
    id = int(request.GET.id.strip())
    if not idok(id): return 'bad player id; try debugging using the id route'
    ctrl = request.GET.ctrl.strip()
    if not ctrlok(ctrl): return 'accel route fail, possibly bad ctrl (should be one of: w a s d)'
    if   ctrl == 'w': gofaster(id)
    elif ctrl == 's': tapbreaks(id)
    else: 
        veerdirection = 'left' if ctrl == 'a' else 'right'
        veer(id, veerdirection)
    return locationstring(id) + ',' + velocitystring(id)

@route('/stop', method='GET')
def stop():
    id = int(request.GET.id.strip())
    if not idok(id): return 'bad player id; try debugging using the id route'
    vel[id][0], vel[id][1] = 0., 0.        # retains memory of heading ([2])
    return locationstring(id) + ',' + velocitystring(id)

@route('/teleport', method='GET')
def teleport():
    '''teleport to x, y provided you have a teleport crystal in your inventory'''
    id  = int(request.GET.id.strip())
    if not idok(id): return 'bad player id; try debugging using the id route'
    if itemindex(id, 'teleport crystal') < 0: return 'you need to find a particular treasure to teleport'
    x   = float(request.GET.x.strip())
    y   = float(request.GET.y.strip())
    if x >= 0. and x < torew and y >= 0. and y < torns:
        loc[id] = [x, y, 0.]
        vel[id][0], vel[id][1] = 0., 0.
        return locationstring(id)
    return 'teleport failed, possibly bad x, y coordinates?'

@route('/dive', method='GET')
def dive():
    id  = int(request.GET.id.strip())
    if not idok(id): return 'bad player id; try debugging using the id route'
    ctrl = request.GET.ctrl.strip()
    if ctrl != 'r' and ctrl != 'f': return '-1'
    vel[id][0], vel[id][1] = 0., 0.
    mydepth = loc[id][2]
    if ctrl == 'r':
        mydepth -= deltadive
        if mydepth < 0.: mydepth = 0.
        if mydepth == 0. and not whalerider[id]: maxspeed[id] = hullspeed
    else:
        seafloordepth = bathymetry(loc[id][0], loc[id][1])
        mydepth += deltadive
        if mydepth > seafloordepth: mydepth = seafloordepth
    loc[id][2] = mydepth
    return locationstring(id)

@route('/ping', method='GET')
def ping():
    id  = int(request.GET.id.strip())
    if not idok(id): return 'bad player id; try debugging using the id route'
    thisdepth = bathymetry(loc[id][0], loc[id][1])
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

# How to run it in casual mode...
# run(host='0.0.0.0', port=8080, reloader=True)


application = bottle.default_app()
if __name__ == '__main__': run(app=application, host='0.0.0.0', port=8080, reloader=True)
=======
@route('/join', method='GET')
def join():

    msg = request.GET.name.strip()
    if len(msg) == 0: return('player name has zero characters; join failed')
    try :  players.append(msg); locs.append((randint()*start_dim,randint()*start_dim, 0))
    except : return("player join fail for some reason")
    rmsg = players[-1] + ',' + str(len(players)) + ',' + str(locs[-1][0]) + ',' + str(locs[-1][1]) + ',' + str(locs[-1][2])
    print("                  len(players) = ", len(players))
    return rmsg

@route('/quit', method='GET')
def quit():
    msg = request.GET.name.strip()
    if not msg in players: return("failed to remove a non-existent player")
    try: player_index = players.index(msg); del players[player_index]; del locs[player_index]
    except : return("sorry this player quit did not work for some reason")
    return ("you have left the toroidal mocean")

@route('/move', method='GET')
def move():
    name    = request.GET.name.strip()
    heading = request.GET.heading.strip()
    if not name in players: return('fail to move as player name not recognized')
    player_index = players.index(name)
    torx, tory, torz = locs[player_index]
    if   heading == 'north': tory = (tory + 1) % torns
    elif heading == 'south': tory = (tory - 1) % torns 
    elif heading == 'east' : torx = (torx + 1) % torew
    elif heading == 'west' : torx = (torx - 1) % torew 
    locs[player_index] = (torx, tory, torz)
    return state(torx, tory, torz)

def state(x, y, z): return str(x) + ',' + str(y) + ',' + str(z)
>>>>>>> Stashed changes

