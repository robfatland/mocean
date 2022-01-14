import json
from bottle import request, route, run, default_app

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


application = default_app()
if __name__ == '__main__': run(host='0.0.0.0', port=8080, reloader=True)
