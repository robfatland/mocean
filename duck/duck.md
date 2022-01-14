<img src="https://raw.githubusercontent.com/robfatland/othermathclub/master/images/misc/duck_and_wolf.png" alt="drawing" width="450"/>


## The Problem

A certain duck can jump into the air and fly away to safety instantly: Provided she is standing on dry land.
But she can not take off from water. Unfortunately she finds herself swimming in a circular pond 
where a wolf (who does not swim) is walking about the perimeter, hungry. The wolf can and does 
run briskly about the pond four times faster than the swimming duck can swim. 
That is: If the duck can swim one meter per second then the wolf can run four meters 
per second. The exact numbers are not important; only the proportion of their speeds.


Is it possible for the Duck to safely swim to the edge of the pond and fly away?


## The Details


Duck begins at the center of a circular pond. The pond has a radius of 50 meters.
Duck swims at a speed of 1 meter per second. Wolf runs at 4 meters per second.


Duck wants to fly away but can do so only when she is standing on solid ground.
Wolf always runs as fast as possible to the point on the perimeter of the pond 
where Duck would step out. 


For game play we will say that Duck's location is given by two numbers:
**r** between 0 and 50 and **a** between -180 and 180. **r** is Duck's 
distance from the center of the pond in meters. **a** is the direction
angle. When **a** is 0 degrees that corresponds to East. 
North is 90 degrees, 
South is -90 degrees, and West is 180 degrees (or -180 degrees). 


The Wolf is always at distance 50.0 from the center of the pond because he 
cannot swim. He is on the shore.  Wolf's location is therefore given
by just his direction angle **b**. Again this is 0 degrees
when the Wolf is directly East of the center of the pond, and so on. 


Now we say the situation, the location of both Duck and the Wolf at any moment 
in time, can be described by three numbers: **r**, **a**, **b**. 


If we have Duck swim to the edge of the pond and Wolf gets there first we will have **a** = **b**
and **r = 50**. They are at the same location. This is an unfortunate outcome for Duck. 


## Playing the game

- To play this game use the /duck route: **`http://123.123.123.123:8080/duck`**. 
    - I prefer not to publish the location of the game here
    - Get the correct ip address from Slack, to replace **`123.123.123.123`**. The rest is correct.
- To get the location of the Duck and the Wolf include **`?location`**
    - Test this out; the result should always be 0,0,0. These are the values for **r**, **a** and **b**
    - You can do this at the start of the game to be sure everything is working ok
- The Server does not remember who you are or where the Duck is or where the Wolf is
    - To play the game you must tell the Server where they are
    - You do this using the same keyword **`location`** but you add in the location information
        - Suppose the Duck is at distance 40 from the center of the pond, at direction -90
        - Suppose the Wolf is at direction 0
        - You would send the Server: **`http://123.123.123.123:8080/duck?location=40,-90,0`**

