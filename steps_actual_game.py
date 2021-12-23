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
def steps_win():
    global lineend
    msg = request.GET.solution.split()
    return_msg  = 'You have moved on to the puzzle phase of the steps game.' + lineend + lineend
    if not len(msg):
        return_msg += 'Now I will ask you the puzzle. If you think the solution is the ' + lineend
        return_msg += 'word "flapjacks" then you can tell me like this:                ' + lineend + lineend
        return_msg += '        http://52.34.243.66:8080/puzzle?solution=flapjacks      ' + lineend + lineend
    else:
        if msg[0] == 'leaf':
            return_msg += 'Correct, the answer is "leaf". Go on to the next part!' + lineend + lineend
            return_msg += '        http://52.34.243.66:8080/problem                    ' + lineend + lineend
        else:
            return_msg += 'Incorrect.                                              ' + lineend + lineend
    return_msg += 'I better remind you what the puzzle is. Here we go...          '     + lineend + lineend
    return_msg += 'Simplest way to get out of a deciduous forest?' + lineend + lineend
    return return_msg

application = default_app()
if __name__ == '__main__': run(host='0.0.0.0', port=8080, reloader=True)
