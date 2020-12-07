# This files 'locean.py' is a very simple example of Server code.
# 
# It contains only one route called 'locean'. This route listens for two possible key values:
#   key 'help' prints a help message
#   key 'tempo' tries to set the tempo of a song

import bottle
from bottle import request, route, run
import json
from time import time

@route('/locean', method='GET')
def locean_response():
    msg = 'locean protocol'
    key_choice = request.GET.
    return(msg)


@route('/accel', method='GET')
def accel():
    amplify   = 10.
    id        = int(request.GET.id.strip())
    heading   = request.GET.heading.strip()
    assert len(heading) == 1, 'heading too long: ' + heading
    vel[id][0] += impulse[heading][0] * amplify
    vel[id][1] += impulse[heading][1] * amplify
    return state(loc[id][0], loc[id][1], loc[id][2]) + ',' + str(vel[id][0]) + ',' + str(vel[id][1])



application = bottle.default_app()
if __name__ == '__main__': run(app=application, host='0.0.0.0', port=8080, reloader=True)
