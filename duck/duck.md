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


Duck begins at the center of a circular pond. Duck swims at a speed of 1.
This means in one time unit: Duck moves one distance unit. These could be meters and 
seconds, for example. But this is something that doesn't matter. All that matters is 
that Wolf move four times faster. So while Duck moves a distance 1, Wolf moves a distance
4. This is "Wolf runs fast while Duck swims slow."


Duck wants to fly away but can do so only when she is standing on solid ground.
Wolf always runs as fast as possible to the point on the perimeter of the pond 
where Duck would step out. 


We said that their speeds only matter in a relative sense: Wolf speed = 4 x Duck speed. 
It is also the case that the radius of the pond does not matter. It could be 
radius = ten meters, it could be radius = 240 meters. Why does it not matter?


For game play we will say that the pond has radius 1. Duck's distance from the center of 
the pond while swimming will be some number **r** between 0. and 1.


The other important parameter is which *direction* the Duck is relative to the center
of the pond. We will use a scale of degrees, where East is 0 degrees. North is 90 degrees, 
South is -90 degrees, and West is 180 degrees (or identically -180 degrees). We will
refer to the Duck's direction as an angle **a**.


The Wolf is always at distance 1.0 from the center of the pond because he cannot swim. 


The Wolf's important location parameter is his direction angle **b**. Again this is 0 degrees
when the Wolf is directly East of the center of the pond, and so on. 


Now we can say the state of the pond (the location of the Duck and the Wolf) at any moment 
in time can be described by three numbers: **r**, **a**, **b**. 


If we have Duck swim to the edge of the pond and Wolf gets there first we will have **a** = **b**
and **r = 1**. This is an unfortunate outcome for Duck. 


## Playing the game

r += "To play this game use the /duck route. Send the current location of both Duck   " + lineend
            r += "and wolf; and if you wish: Send a Duck move. There are 3 possible replies:      " + lineend
            r += "                                                                                " + lineend
            r += "1)  'location=r,alpha;wolf=beta'  See below for the explanation                 " + lineend
            r += "2)  'Wolf has lunch'              means the wolf has caught the duck            " + lineend
            r += "3)  'Duck flies away'             means that you have won the game              " + lineend
            r += "                                                                                " + lineend
            r += "Here is how to understand location, two numbers r and alpha:                    " + lineend
            r += "- r is distance from the center of the pond to the Duck. 0 is the center,       " + lineend
            r += "....1 is dry land at the perimeter of the pond. If the Duck reaches r = 1       " + lineend
            r += "....and there is no Wolf there, Duck flies away and you win the game.           " + lineend
            r += "                                                                                " + lineend
            r += "- alpha is a direction angle measured in degrees from East; again relative to   " + lineend
            r += "....the center of the pond. alpha is the Duck's angle, beta is the Wolf's.      " + lineend
            r += "....(The Wolf is always at distance 1 from the center: He can't swim.)          " + lineend
            r += "                                                                                " + lineend
            r += "To move Duck you must send both the Duck's and the Wolf's location.  You also   " + lineend
            r += "..must send directions for Duck to swim: Either to a new distance r' or to a    " + lineend
            r += "..new angle alpha'.                                                             " + lineend
            r += "                                                                                " + lineend
            r += "
