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


################### beguine #######################

@route('/beguine', method='GET')
def steps_game_part_2():

    print("                  route beguine hit")
    msg_string = request.GET.message.strip()
    print("                                   sent:", msg_string)

    fibo = genfibo(30)

    try :    vfloat = float(msg_string) 
    except : return('you are on route: "beguine"! Level 2 of the steps game... but this stage requires a number')

    v = int(vfloat)
    if not float(v) == vfloat: return('...actually I am looking for an integer; but ' + str(vfloat) + ' has digits after the decimal point...')

    if v < 0: return('ah good, an integer, you are getting close. But stay with non-negative integers for this one')

    if v == 0: return("very nice... the first Fibonacci number! you are warm!")
    if v == 1: return("very nice... the second (and third) Fibonacci number! not quite there yet but heating up!")
    if v == 2: return("very nice... the fourth Fibonacci number! getting warmer")

    if v in fibo:
        this_index = fibo.index(v)
        if this_index == 16: return("   CONGRATULATIONS!!!!!!!! You solved the beguine route!!!!!!!!!!\n\n" + \
                                    "       (((You get 5000 Bonus Points if you calculated 987 using Python))) \n\n" + \
                                    "           The game continues on the sirduke route...                      \n" + \
                                    "             ...or you can start designing your own route puzzles if you like!")
        return('you tried Fibonacci number ' + str(this_index + 1) + ' (which is ' + str(v) + '); right track but I am a huge fan of the *seventeenth* one...')

    return("your guess is in the right neighborhood... try making a left on F-street...")


################### sirduke #######################

@route('/sirduke', method='GET')
def steps_game_part_3():
    print("                  route sirduke hit")
    msg_string = request.GET.message.strip()
    print("                                   sent:", msg_string)
    if not msg_string == 'wigs':  return("This time I need the fourth word of the song 'Satin Doll'...")
    return("Well done! You're nobody's fool... Move on to route 'euler' now!")



################### euler #######################

@route('/euler', method='GET')
def steps_game_part_4():

    print("                  route euler hit")
    msg_string = request.GET.message.strip()
    print("                                   sent:", msg_string)

    try :    vfloat = float(msg_string) 
    except : return('you are on route "euler" and that is level 4 of the steps game.  This stage requires a number.')

    v = int(vfloat)
    if not float(v) == vfloat: return('...actually I am looking for an integer; but ' + str(vfloat) + ' has digits after the decimal point...')

    if v < 0: return('ah good, an integer, thank you, you are getting close. This integer will be positive.')
    if v < 3: return("very nice... but this integer is the sum of some positive integers!")
    this_solution = 5000 * 10001
    if not v == this_solution: return("I need to know the sum of 1 + 2 + 3 + 4 + 5 + ... + 10000")
    return("very nice, Euler would be pleased. On to the final route, called 'meruprastarah'")



################### meruprastarah #######################

@route('/meruprastarah', method='GET')
def steps_game_part_5():

    print("                  route meruprastarah hit")
    msg_string = request.GET.message.strip()
    print("                                   sent:", msg_string)

    the_list = msg_string.split(',')
    if not len(the_list) == 6: return('The solution is the numbers in row 6 of the Pascale triangle, separated by commas.')
    
    try: il = [int(the_list[i].strip()) for i in range(6)]
    except: return("you sent a list of six items, far as I can tell, but they must all be integers.")

    sl = [1, 5, 10, 10, 5, 1]

    if not il == sl: return ("You have sent a list of six numbers (correct) but they are not the ones in row six of the Pascal triangle separated by commas.")
  
    return('Well done; you have completed the Steps game. Tell Rob on Slack!')



################### utility functions #####################

def genfibo(n):
    if n < 3: n = 3
    if n > 30: n = 30
    fibo = [0, 1]
    for i in range(2, n): fibo.append(fibo[-1] + fibo[-2])
    return fibo
    


# This is a utility function to check whether the Player entered a prime number

def isprime(n):
    if n == 2: return True
    if n < 2 or not n % 2: return False
    for i in range(3, int(sqrt(n))+1, 2): if not n % i: return False
    return True
       



# This line of code starts the Server using the Bottle web framework
 
run(host='0.0.0.0', port=8080, reloader=True)


