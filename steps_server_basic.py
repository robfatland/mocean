import json
from bottle import request, route, run, default_app

# '@route' is a decorator that assigns the 'steps' route the function 'steps_game()'

@route('/steps', method='GET')
def steps_game():
    msg = request.GET.message.strip()
    print("          Server received message:", msg)
    try :                      True 
    except :                   return('This message will never be printed')
    return 'welcome! Your message to the steps game was: ' + msg


application = default_app()
if __name__ == '__main__': run(host='0.0.0.0', port=8080, reloader=True)
