# Spoiler Warning

Do not read this code if you are working on the Duck-Wolf problem.



```
import requests
from time import time, sleep
from math import sin, cos, pi, sqrt

def AngleJustify(alpha):
    while alpha <= -180.: alpha += 360.
    while alpha > 180.: alpha -= 360.
    return alpha

dtr = pi/180.
pond_radius = 50.
r, a, b = 0., 0., 0.         # Duck is at radius r, angle a. Wolf is at angle b.
cr = 12.3                    # circling radius for Duck
angle_fraction = 9999/10000  # how ambitious Duck is while circling
toc = time()
url = 'http://52.34.243.66:8080/duck?'
msg = url  + 'location=0,0,0&destination=' + str(cr) + ',180'     # swim out to cr away from Wolf
reply = requests.get(msg).text.replace("<br>", "\n").split(',')
tic = time()
etime = int((tic - toc)*1000)
print("Duck game start...")
print(etime, "ms elapsed (first request timer)\n" + "~"*40 + "\n")
# print(reply)

r, a, b = float(reply[0]), float(reply[1]), float(reply[2])
ab_angle = AngleJustify(a - b)
call_counter = 1

while True:
    call_counter += 1
    print(str(call_counter) + ': r, a, b, delta =    ' + str(round(r,2)) + '   ' + \
          str(round(a,2)) + '   ' + str(round(b,2)) + '   ' + str(round(ab_angle,2)))
    msg  = url + 'location=' + str(r) + ',' + str(a) + ',' + str(b) + '&destination='
    msg += str(cr) + ',' + str(a + abs(ab_angle-180)*angle_fraction)
    reply = requests.get(msg).text.replace("<br>", "\n").split(',')
    r, a, b = float(reply[0]), float(reply[1]), float(reply[2])
    ab_angle = a - b
    while ab_angle <= -180.: ab_angle += 360.
    while ab_angle > 180.: ab_angle -= 360.
    if abs(abs(ab_angle)-180.) < 1.:
        print('\n\n\n       Duck is nearly 180 degrees opposite Wolf.')
        break

print('\n\nDuck makes a dash for the shore. Will she make it???\n\n\n')
sleep(3.0)
msg  = url + 'location='
msg += str(r) + ',' + str(a) + ',' + str(b) 
msg += '&destination='
msg += str(pond_radius) + ',' + str(a)
reply = requests.get(msg).text.replace("<br>", "\n").split(',')
# print(reply)
r, a, b = float(reply[0]), float(reply[1]), float(reply[2].split('\n')[0])
dx = pond_radius*(cos(dtr*a) - cos(dtr*b))
dy = pond_radius*(sin(dtr*a) - sin(dtr*b))
wolf_distance = sqrt(dx*dx + dy*dy)

if a == b: print('Nope, sorry. But Wolf has a nice lunch.')
else: 
    print('Duck flies away!')
    print('And: When Duck took off, Wolf was ' + str(round(wolf_distance,1)) + ' meters away')
    print('And: This took ' + str(call_counter + 1) + ' requests.\n\n')

```
