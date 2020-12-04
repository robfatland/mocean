# Step 0: import some libraries...
#   'requests' lets us talk to the internet (the Server)
import requests
import time
from random import randint
from sys import exit

# Step 2: Where the Server lives on the Internet
server = 'http://54.69.30.193:8080/'


# Step 3: Create Client functions for some routes
#   Routes we are interested in are:
#     mocean
#     join
#     quit
#     who
#     sendchat
#     popchat


def mymocean():
  return requests.get(server + 'mocean').text


def myjoin(name):
  '''join the mocean game as a player'''
  msg = server + 'join?name=' + name
  return int(requests.get(msg).text)


def myquit(name):
  '''quit the mocean game'''
  msg = server + 'quit?name=' + name
  return requests.get(msg).text


def mywho(): 
  '''get a list of who() is playing mocean'''
  return requests.get(server + 'who').text


def mysendchat(id, recipient, message):
  '''send a message to another player'''
  full_url = server + 'sendchat?'
  full_url += 'id=' + str(id) + '&'
  full_url += 'name=' + recipient + '&'
  full_url += 'message=' + message
  print('\n\nmysendchat url: \n\n' + full_url + '\n')
  return requests.get(full_url).text


def mypopchat(id):
  '''read a message sent to me'''
  full_url = server + 'popchat?'
  full_url += 'id=' + str(id)
  return requests.get(full_url).text


# Step 4: STORY TIME!!!!!
# =======================

mymocean_result = mymocean()
print('here is what route=mocean got:\n\n' + mymocean_result + '\n\n')

some_players = ['rob', 'fob', 'hob', 'grob', 'shelob', 'phil']

who_reply = mywho()
print()
print('Here is the list of words in the Server reply to "who?":\n')
who_split = who_reply.split()
print(who_split)
print()

players_in_game = int(who_split[2])

if players_in_game == 0:
  print('no players at the moment... better add them to the game! \n\n')
  for player_name in some_players: 
    player_id = myjoin(player_name)
    print('player ' + player_name + ' has id = ' + str(player_id))
else: 
  print('there are players already in the game; no joining needed. \n\n')


who_reply = mywho()
who_split = who_reply.split()
players_in_game = int(who_split[2])

assert players_in_game > 0, print('oops wrong number of players')

if players_in_game == 5: 
  print()
  print('only five players... maybe phil got left out, let us join him in...')
  print()
  phil_player_id = myjoin('phil')

print('ok we have some players. We check this a couple of times...\n\n')

for i in range(2):
    time.sleep(2)
    print(mywho())

# phil should be one of the players. Let's have him quit. 

print()
print('make phil quit... the result is:')
print()
print(myquit('phil'))
print()
print()

time.sleep(1)
print(mywho())
time.sleep(1)

print()
print('Now we will send a message from grob (id = 3) to shelob')
chat_reply = mysendchat(3, 'shelob', 'hey come over here i found some treasure')
print('if this worked we should see a one here: ' + chat_reply)
print()
print()

time.sleep(2)
print(mywho())
print()
print()
time.sleep(2)

print('now shelob will check her messages (her player id is 4)')
print()
print()
popchat_reply = mypopchat(4)
print('Here is the message that shelob received:\n\n' + popchat_reply)
print()
print()

time.sleep(1)
popchat_reply = mypopchat(3)
print('popchat for player id 3: ' + popchat_reply + '      (...zero means no messages for poor grob)\n')
