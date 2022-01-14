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


## Playing the game part 1: Location

- To play this game use the /duck route: **`http://123.123.123.123:8080/duck`**. 
    - I prefer not to publish the location of the game here
    - Get the correct ip address from Slack, to replace **`123.123.123.123`**. The rest is correct.
- To get the location of the Duck and the Wolf include **`?location`**
    - Test this out; the result should always be **`0,0,90`**. These are the values for **r**, **a** and **b**
        - **r** =  0: Duck is at the center of the pond
        - **a** =  0: Duck's direction doesn't really mean anything since she is at the center of the pond
        - **b** = 90: Wolf direction is 90 degrees: Wolf is on the North side of the pond.
    - You can do this at the start of the game to be sure everything is working ok
- The Server does not remember who you are or where the Duck is or where the Wolf is...
    - To play the game you must tell the Server where they are by providing **r**, **a** and **b**
    - You do this using the same keyword **`location`** but you add in the location information
        - Suppose the Duck is at distance 40, direction -90. Suppose Wolf is at direction 0.
        - You would send the Server: **`http://123.123.123.123:8080/duck?location=40.21,-90.00,12.43`**
        - Telling the Server where the Duck and Wolf are will make more sense below in Part 2
 - You can pretend to win the game by putting Duck safely at the edge of the pond away from Wolf
     - This does not count as *actually* winning the game


## Playing the game part 2: Moving the Duck

- You move Duck by adding another keyword **destination**. It is separated from **location** by an ampersand character **`&`**.
- Suppose Duck is at distance **r** = 40. and angle **a** = -90 and you want her to be at **r** = 40 and **a** = -100. Here is what you send:
    - **`http://123.123.123.123:8080/duck?location=40,-90,12.43&destination=40,-100`**
    - Let's break this down into parts:
        - **`http://`** signals we are using the http protocol (rules of communication)
        - **`123.123.123.123`** is the internet address of the Server for our game
        - **`:8080`** is the port number on the Server for our game
        - **`/duck`** is the route. This tells the Server we want to work on the Duck and Wolf puzzle.
        - **`?`** is a separator. Everything after this separator will be keys and values
        - **`location=40,-90,12.43`** is the `location` key followed by three values: **r**, **a** and **b** for Duck and Wolf locations
        - **`&`** is a separator between key/value pairs
        - **`destination=40,-100`** is the `destination` key followed by three values: **new r** and **new a**. That is where Duck will go next. 
    - Notice that we are allowed to say where the Duck goes (using `destination`) but we do not get to say where Wolf goes
        - Wolf's new location is determined by the Server
        - The Server will reply with `location=40.00,-100.00,-47.22`
            - Notice Duck has arrived at `destination`: Distance r = 40.00 and angle a = -100.00
            - Notice Wolf has run around the edge of the pond to get closer to Duck. Wolf is now at angle b = -47.22


How does Duck move? Duck swims in a straight line as fast as possible to **destination**.




