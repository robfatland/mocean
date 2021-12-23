import json
from bottle import request, route, run, default_app

# '@route' is a decorator that assigns the 'steps' route the function 'steps_game()'

@route('/steps', method='GET')
def steps_game():
    lineend = '<br>'
    msg = request.GET.message.strip()
    print("          Server steps route received message:", msg)
    try :                      True 
    except :                   return('This message will never be printed')
    return_msg = 'Hi! Congratulations, you are halfway done!' + lineend + lineend
    if len(msg): return_msg += '  you sent: ' + msg + lineend + lineend
    return_msg += 'To finish the game: Paste the following in your browser:' + lineend + lineend
    return_msg += '  http://52.34.243.66:8080/win?code=hurray for Python!!!' + lineend + lineend
    return return_msg

@route('/win', method='GET')
def steps_win():
    lineend = '<br>'
    msg = request.GET.code.strip()
    print("          Server win route received message:", msg)
    try :                      True 
    except :                   return('This message will never be printed')
    return_msg  = 'You have won the steps game, well done!' + lineend + lineend
    return_msg += '    Collect one million dollars from a Monopoly game.' + lineend + lineend
    if len(msg) > 0: 
        return_msg += '       I notice you sent code: ' + msg + lineend + lineend
        return_msg += '       (What if you send a different code???)' + lineend + lineend
    return_msg += 'Please treat yourself to some bubble tea now' + lineend + lineend
    return return_msg

application = default_app()
if __name__ == '__main__': run(host='0.0.0.0', port=8080, reloader=True)
