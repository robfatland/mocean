<img src="https://raw.githubusercontent.com/robfatland/othermathclub/master/images/misc/duck_and_wolf.png" alt="drawing" width="450"/>

We have been talking about the connection from 'the real world' we live in to the code we write. This project page
is about two such connections. First we have an interesting puzzle to try to solve, about a duck and a wolf. Second 
we have the idea of computers talking to one another across vast distances, like hundreds of miles, in a fraction of 
a second. We have used the **`requests`** Python library to enable this. So read on if you dare! And as always: Let us
know what you think on Slack!


## The Problem


A certain duck can jump into the air and fly away to safety instantly: Provided she is standing on dry land.
But she can not take off from water. Unfortunately she finds herself swimming in a circular pond 
where a wolf (who does not swim) is walking about the perimeter, hungry. The wolf can and does 
run briskly about the pond four times faster than the swimming duck can swim. 
That is: If the duck can swim one meter per second then the wolf can run four meters 
per second. The exact numbers are not important; only the proportion of their speeds.


Is it possible for the Duck to safely swim to the edge of the pond and fly away?


## The Details


Duck begins this puzzle at the center of a circular pond. The pond has a radius of 50 meters.
Wolf is on the East edge of the pond. Duck swims wherever she likes, always at a speed of 
1 meter per second. Wolf runs around the edge or perimeter of the pond, always at 4 meters per second.


Duck wants to fly away but can do so only when she is standing on solid ground.
Wolf always runs as fast as possible to
where Duck would step ashore. Wolf is inimical in this puzzle. 


For game play we will say that Duck's location is given by two numbers, **r** and **a**.

- **`r`** is between 0 and 50: Duck's distance from the center of the pond
- **`a`** is an angle between -180 and 180 degrees: Duck's compass location (again relative to pond-center) 


Zero degrees corresponds to 'East'. 90 degrees is North. -90 degrees is South. 180 degrees is West; so is -180 degrees. 


The Wolf is always at distance 50.0 from the center of the pond because he 
cannot swim. He is on the shore.  Wolf's location is therefore just a direction angle **`b`**. 
Again this is zero degrees when Wolf is East of the center of the pond. 


Now the situation, the location of Duck and the Wolf at any moment, 
is described by three numbers: **`r`**, **`a`**, **`b`**: Duck radius, Duck angle, Wolf angle.


When Duck swims to the edge of the pond (**`r = 50`**): One of two things happen. Either Wolf is 
there also and Wolf gobbles up Duck; or Wolf is *not* there and Duck flies away safely.


## Playing the game part 1: Location

- To play this game use the /duck route: **`http://123.123.123.123:8080/duck`**. 
    - Get the correct ip address from Slack to replace **`123.123.123.123`**. The rest is correct.
- To get the location of the Duck and the Wolf include **`?location`**
    - **`http://123.123.123.123:8080/duck?location`** --> **`0,0,0`**. These are **`r`**, **`a`** and **`b`**.
        - **r** =  0: Duck is at the center of the pond
        - **a** =  0: Duck's direction doesn't really mean anything; but this is 'East'
        - **b** =  0: Wolf direction is 0 degrees also: Wolf is on the East side of the pond.
    - Try this in your browser
- The Server does not remember anything about Duck and Wolf; that is our job
    - To play the game you first tell the Server where Duck and Wolf are
    - You also tell the Server where Duck swims to next
    - Server replies, telling you where Duck is and where Wolf is
    - You do your part using keyword **`location`** and keyword **`destination`** like so:
        - Send **`http://123.123.123.123:8080/duck?location=0,0,0&destination=40,90`**
            - This tells the Server Duck is at the center of the pond
            - It also tells the Server that Wolf is on the East edge of the pond
            - You tell the server Duck swims to **`r = 40, a = 90`** (10 meters from the edge of the pond)
            - The Server replies with **`40, 90, 90`**.
                - This means that Wolf has run around, is waiting for Duck at the North side of the pond.
 - Try this: Pretend to win the game by putting Duck safely at the edge of the pond, away from where you put Wolf
     - This does not count as *actually* winning the game


## Playing the game part 2: Python

Let's suppose you want to try some experiments with Duck to see if you can get her safely to the edge of the pond.
One way to do this is to write a Python program that draws the pond and Duck and Wolf's locations as dots. 
This Python program then asks the player 'Where does Duck swim to next?' The Player responds; and the Python
program has a conversation with the Server, like so:


* Python program to Server: "Duck is at **`r, a`** and Wolf is at **`b`**; and Duck swims to **`new_r, new_a`**
* Server replies to Python: "Duck is now at **`new_r, new_a`** and Wolf is now at **`new_b`**. 


The Python program re-draws everything and asks the Player 'Where does Duck swim to next?'


This is only one possible way of using a Python program as a **ducks** Client, of course.



## Playing the game Part 3: Sitting Duck


How does Duck move? Duck swims in a straight line as fast as possible to her **destination**.


If we wish for Duck to sit still (possibly allowing Wolf to move): Send the Server a **`location`** but not a **`destination`**. 
This will result in Duck sitting still for one second. In this one second Wolf can move up to 4 meters. The Server will of 
course send back Duck's same location and Wolf's (possibly new) location in reply.


## Hints


If you are the sort of person who likes hints (or perhaps you are stuck on this puzzle): Read on!
If you prefer no spoilers, stop here!


Of course it *is* possible for the Duck to escape, just barely! The record for the number of **`requests`** to 
the Server is 212. Is it possible to do better than this? To explain this a little bit further: Someone has
managed to move the Duck 212 times before Duck managed to fly away. Now that is a lot of Duck moves. The 
first challenge is figuring out how to win. The second challenge is to do this with a minimal number of 
Duck moves.


If you are stuck and need help writing Python code to play the Duck game: 
A simple example for a Duck Game Client can be found [at this replit.com page](https://replit.com/@robfatland/duckgameplayer).
