import json
from bottle import request, route, run, default_app

lineend = '<br>'

@route('/steps', method='GET')
def steps_game():
    global lineend
    msg = request.GET.message.split()
#     return_msg = 'yip ' + msg
#     print("          Server steps route received message:", msg)
#     return_msg = 'Congratulations, that was step one!' + lineend + lineend
#     if len(msg): 
#         return_msg += 'You sent a message! It was: ' + msg + lineend + lineend
#         if return_msg == 'passport':
#             return_msg += '"passport" is correct. You can move on to the next route.' + lineend
#             return_msg += 'The next route is called "puzzle". Enter into your browser' + lineend
#             return_msg += 'the URL http://52.34.243.66:8080/puzzle' + lineend + lineend
#             return_msg += 'Good Luck!' + lineend + lineend
#         else:
#             return_msg += 'To move on: Try sending the message "passport".' + lineend + lineend
#     else: 
#         return_msg += 'Now try sending me a message. Maybe your message is "pancakes"' + lineend
#         return_msg += 'in which case you would type in this:               ' + lineend + lineend
#         return_msg += '        http://52.34.243.66:8080/steps?message=pancakes' + lineend + lineend
    return 'i say: ' + msg

# @route('/puzzle', method='GET')
# def steps_win():
#     global lineend
#     msg = request.GET.solution.text
#     return_msg  = 'You have moved on to the puzzle phase of the steps game.'
#     return return_msg

application = default_app()
if __name__ == '__main__': run(host='0.0.0.0', port=8080, reloader=True)
