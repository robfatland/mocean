# Server: A computer somewhere that is an expert
# Client: A program I write



# READ ME FIRST
# =============
#
# This code is called a Client. It talks to a Server over the internet. Think about that!
#   Just a couple lines of Python code and you can talk to other computers anywhere on earth!
#
# The way this Client works is it builds a string called 'package' which contains several
#   pieces of information (including a guess for a puzzle game). You will be able to change
#   your guesses and other parts of 'package' as you go. 
#
# Nobody has won the game yet. If you win: Let me know!
#
# 'package' has six parts glued together.
#   - an ip address stored in the variable urlbase. This does not change.
#   - a route. This short string changes as you play the game
#   - a question mark character: This does not change
#   - a key: This short string changes as you play the game
#   - an equals sign character: This does not change
#   - a value: This is your guess for what the right answer is. 
#       - This string changes each time you make a guess.
#
# Notice that the second part of the 'package' string is called the *route*.
# The route starts out as the string 'begin'. Think of this route as "what part of the game I am in".
# So you stay with the 'begin' route as you make guesses. It is a bit like the Adventure Game
#   but with no background story.
# 
# Each time you input a new guess it is sent to the 'begin' route. But you can also change
# the route once you get the first guess right. The reply that comes back tells you what 
# the next route is called. So for your input type the word 'route' and then enter the new
# route. So then you will be sending messages to the new route.
# 
# The key string is 'message'. That never changes in the Steps game. Then the value is your guess.  
#

import requests, time

urlbase, route, key = 'http://AAA.BBB.CCC.DDD:PPPP/', 'begin', 'message'

while True:
    print("\nUse 'route' to change the game; or 'quit' to quit...")
    myguess = input("\nMy next guess: ")
    if   myguess == 'exit' or myguess == 'quit':  
      break
    elif myguess == 'route': 
      route = input("ok, enter a new route: ")
    else: # try a guess
        package = urlbase + route + '?' + key + '=' + myguess
        tic = time.time()
        server_response = requests.get(package).text
        toc = time.time()
        echo_time = str(round((toc - tic)*1000., 1))

        print()
        print('what the Server said was:')
        print()
        print(server_response)
        print()
        print()
        print('This is what we sent to the Server:')
        print()
        print(package)
        print()
        print()
        print('the time it took: ', echo_time)
        print()
        print()
