import json
import re
from bottle import request, route, run, default_app
from math import sqrt, cos, sin, pi

lineend = '<br>'

@route('/steps', method='GET')
def steps_game():
    global lineend
    msg = request.GET.message.split()
    print("          Server steps route received message:", msg)
    return_msg = 'Congratulations, that was step one!' + lineend + lineend
    if len(msg): 
        return_msg += 'You sent a message! It was: ' + msg[0] + lineend + lineend
        if msg[0] == 'passport':
            return_msg += '"passport" is correct. You can move on to the next route.' + lineend
            return_msg += 'The next route is called "puzzle". Enter into your browser' + lineend
            return_msg += 'the URL http://52.34.243.66:8080/puzzle' + lineend + lineend
            return_msg += 'Good Luck!' + lineend + lineend
        else:
            return_msg += 'To move on: Try sending the message "passport".' + lineend + lineend
    else: 
        return_msg += 'Now try sending me a message. Maybe your message is "pancakes"' + lineend
        return_msg += 'in which case you would type in this:               ' + lineend + lineend
        return_msg += '        http://52.34.243.66:8080/steps?message=pancakes' + lineend + lineend
    return return_msg

@route('/puzzle', method='GET')
def steps_puzzle():
    global lineend
    msg = request.GET.solution.split()
    return_msg  = 'You are in the puzzle part of steps.' + lineend + lineend
    if not len(msg):
        return_msg += 'Puzzle: What is the simplest way to escape a deciduous forest?' + lineend + lineend
        return_msg += 'The solution is just a single word. If you think the solution ' + lineend
        return_msg += '  is the word "flapjacks" then tell me so like this:          ' + lineend + lineend
        return_msg += '        http://52.34.243.66:8080/puzzle?solution=flapjacks    ' + lineend + lineend
    else:
        if msg[0] == 'leaf':
            return_msg += 'Correct, the answer is "leaf". Continue to the next route,' + lineend
            return_msg += '  a problem you must solve. As you might guess, use:      ' + lineend + lineend
            return_msg += '        http://52.34.243.66:8080/problem                  ' + lineend + lineend
        else:
            return_msg += 'Your guess "' + msg[0] + '" is not correct.               ' + lineend + lineend
            return_msg += 'The simplest way to escape a deciduous forest is ???  '     + lineend + lineend
    return return_msg

@route('/problem', method='GET')
def steps_problem():
    global lineend
    msg = request.GET.solution.split()
    return_msg  = 'Steps problem...                    ' + lineend + lineend
    if not len(msg):
        return_msg += 'You have five unique stuffed animals. How many ways are there ' + lineend
        return_msg += '  to choose a subset of them? A subset can contain 0, 1, 2, 3,' + lineend
        return_msg += '  4, or 5 stuffed animals. If you think the answer is 6 then  ' + lineend
        return_msg += '  tell me so by typing in this:                               ' + lineend + lineend
        return_msg += '        http://52.34.243.66:8080/problem?solution=6           ' + lineend + lineend
    else:
        try: 
            solution = int(msg[0])
            if solution == 32:
                return_msg += 'Correct, there are two raised to the fifth power subsets. ' + lineend
                return_msg += '  (or as you say: 32)                                     ' + lineend
                return_msg += 'Now you can move on to the Python route. Use              ' + lineend + lineend
                return_msg += '        http://52.34.243.66:8080/python                   ' + lineend + lineend
            elif solution > 32:
                return_msg += 'Your solution "' + str(solution) + '" is too big.         ' + lineend + lineend
                return_msg += 'The number of subsets of five stuffed animals is ???      ' + lineend
            else: 
                return_msg += 'Your solution "' + str(solution) + '" is too small.       ' + lineend + lineend
                return_msg += 'The number of subsets of five stuffed animals is ???      ' + lineend
        except:
            return_msg += 'Since we are counting, your solution should be a positive integer.' + lineend + lineend
            return_msg += 'The number of subsets of five stuffed animals is ???              ' + lineend
    return return_msg

@route('/python', method='GET')
def steps_python():

    global lineend

    r  = 'This is the last part of the steps game: Login to replit.com and          ' + lineend
    r += 'create a Python program like the one below. Then predict what it will     ' + lineend
    r += 'do. Then run it. Then report on slack what it did. Good luck.             ' + lineend
    r += '                                                                          ' + lineend
    r += '                                                                          ' + lineend
    r += '   (...and if you would like another challenge: try the /duck route...)   ' + lineend
    r += '                                                                          ' + lineend
    r += '                                                                          ' + lineend
    r += '                                                                          ' + lineend
    r += 'import requests                                                           ' + lineend
    r += 'from time import time                                                     ' + lineend
    r += '                                                                          ' + lineend
    r += 'url = "http://52.34.243.66:8080/"                                         ' + lineend
    r += 'route = "puzzle"                                                          ' + lineend
    r += 'msg = url + route                                                         ' + lineend
    r += '                                                                          ' + lineend
    r += 'toc = time()                                                              ' + lineend
    r += 'reply = requests.get(msg).text.replace("&ltbr&gt", "\\n")                 ' + lineend
    r += 'tic = time()                                                              ' + lineend
    r += '                                                                          ' + lineend
    r += 'etime = int((tic - toc)*1000)                                             ' + lineend
    r += '                                                                          ' + lineend
    r += 'print(etime, "milliseconds elapsed")                                      ' + lineend
    r += 'print("The reply from the Server was:\\n" + "~"*40 + "\\n")               ' + lineend
    r += 'print(reply)                                                              ' + lineend
    r += '                                                                          ' + lineend
    return r

def ParseLocation(locstring):

    loclist = re.split(',|,\s|;|;\s', locstring)   # \s is regex whitespace

    try: 
        r = float(loclist[0])
        a = float(loclist[1])
        b = float(loclist[2])
    except:
        r, a, b = 0., 0., 0.

    if r <  0.: r = 0.

    while a <= -180.: a += 360.
    while a  >  180.: a -= 360.
    while b <= -180.: b += 360.
    while b  >  180.: b -= 360.

    return r, a, b,

def ParseDestination(dststring):

    dstlist = re.split(',|,\s|;|;\s', dststring)   # \s is regex whitespace
    try: 
        rd = float(dstlist[0])
        ad = float(dstlist[1])
    except:
        rd, ad = 0., 0.
    if rd <  0.: rd = 0.
    while ad <= -180.: ad += 360.
    while ad  >  180.: ad -= 360.

    return rd, ad

@route('/duck', method='GET')
def steps_duck():

    global lineend

    dtr         = pi/180.
    rtd         = 180./pi
    duck_speed  = 1.
    wolf_speed  = 4.
    pond_radius = 50.

    location_msg    = request.GET.location
    destination_msg = request.GET.destination
    len_loc         = len(re.split(',|,\s|;|;\s', location_msg))
    len_dst         = len(re.split(',|,\s|;|;\s', destination_msg))

    if len_loc == 0 and len_dst == 0: 
        msg  = 'location=0,0,0' + lineend + lineend + 'Duck is at the center of the pond' + lineend + lineend
        msg += 'To read about this game please visit:' + lineend + lineend
        msg += '        https://github.com/robfatland/mocean/blob/main/duck/duck.md' + lineend + lineend
    else:
        if len_loc == 3:
            r,   a,  b  = ParseLocation(location_msg)
            if not len_dst == 2: 
                rd = r
                ad = a
                dt = 1.
            else: 
                rd, ad         = ParseDestination(destination_msg)
                a_rad, b_rad   = a*dtr, b*dtr
                ad_rad         = ad*dtr
                x0, y0, x1, y1 = r * cos(a_rad), r * sin(a_rad), rd * cos(ad_rad), rd * sin(ad_rad)
                dt             = sqrt((x0 - x1)**2 + (y0 - y1)**2)/duck_speed

            # distance along perimeter wolf can go
            wolf_max   = dt*wolf_speed
            arc        = ad - b                   # arc is angle gap from wolf now to where wolf wants to go
            while arc <= -180.: arc += 360.
            while arc >   180.: arc -= 360.       # arc will be in its minimal form

            distance_to_ad = abs(arc*dtr*pond_radius)
            if distance_to_ad <= wolf_max: bd = ad
            else: 
                wolf_angle = (wolf_max / pond_radius) * rtd 
                if arc < 0.: wolf_angle = -wolf_angle 
                bd = b + wolf_angle

            msg = str(round(rd,2)) + ',' + str(round(ad,2)) + ',' + str(round(bd,2))

            if rd >= pond_radius:
                if ad == bd: 
                    msg += lineend + lineend + 'Wolf has lunch' + lineend + lineend
                else:
                    msg += lineend + lineend + 'Duck flies away! (you win)' + lineend + lineend

        else: msg = 'something went wrong'

    return msg


application = default_app()
if __name__ == '__main__': run(host='0.0.0.0', port=8080, reloader=True)
