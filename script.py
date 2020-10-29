from bottle import request, route, run
import json
from math import sqrt


########
#
# Here is the main part of this Server program...
#     '@route' is a decorator that assigns the 'begin' route the function 'steps_game_part_1'
#
########

@route('/begin', method='GET')
def steps_game_part_1():
    msg = request.GET.message.strip()
    print("                               Server received message:", msg)
    try :    vfloat = float(msg) 
    except :                   return('you are on the right route: "begin", hurray! but your message is not numerical enough for me!!!')
    v = int(vfloat)
    if v < 0:                  return('ah good, you are getting warm... i like numbers but this one is a bit negative :( ')
    if v == 0:                 return("nice message... but it a bit small don't you think?")
    if not float(v) == vfloat: return('actually I need an integer, and ' + str(vfloat) + ' has digits after the decimal point...')
    if not isprime(v):         return('your message is positive but not prime enough')
    if v <= 100:               return("your message is prime! Make it a bit bigger, like over the century mark, and you're there")
    return "congrats, you solved it!!! A prime greater than 100. The next step: Begin again, this time using the route 'beguine'"



# This is a utility function to check whether the Player entered a prime number

def isprime(n):
    if n == 2: return True
    if n < 2 or not n % 2: return False
    for i in range(3, int(sqrt(n))+1, 2): if not n % i: return False
    return True
       



# This line of code starts the Server using the Bottle web framework
 
run(host='0.0.0.0', port=8080, reloader=True)
