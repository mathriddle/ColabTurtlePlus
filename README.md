# ColabTurtlePlus

An extension of the original ColabTurtle by Tolga Atam (tolgaatam) using classes (so multiple turtle are possible). Also includes some code from jaronma ColabTurtle_2 repo.

This is a module for drawing classic Turtle figures on Google Colab notebooks. It can also be used in Jupyter Lab notebooks. The graphics are drawn using SVG tags. The SVG commands can be printed on screen (after the drawing is completed) or saved to a file for use in a program like inkscape or Adobe Illustrator, or displaying the image in a webpage.

The ColabTurtlePlus module provides turtle graphics primitives, in both object-oriented and procedure-oriented ways. The procedural interface provides functions that are derived from the methods of the classes. They have the same names as the corresponding methods. A screen object is automatically created whenever a function derived from a Screen method is called. An (unnamed) turtle object is automatically created whenever any of the functions derived from a Turtle method is called.

To use multiple turtles on a screen one has to use the object-oriented interface for the turtles.

Installation
----
Create an empty code cell and type:

    !pip install ColabTurtlePlus

Run the code cell to install the library.

**Note:** The previous non-class version of ColabTurtlePlus can be installed using !pip install ColabTurtlePlus==1.5. 

Usage
----
In any code cell, import the module using

    from ColabTurtlePlus.Turtle import *

Example 1
---
This example uses the procedure-oriented interface.
```
from ColabTurtlePlus.Turtle import *
reset()
setup(300,300)
showborder()
color("red", "yellow")
shape("turtle")
pensize(2)
speed(7)
begin_fill()
for _ in range(4):
  forward(100)
  left(90)
circle(-50)
end_fill()
color("black","green")
saveSVG(turtle=True)
```
The resulting image is  
![](https://github.com/mathriddle/ColabTurtlePlus/raw/main/example.svg)

Example 2
----
This example has two turtles and uses the object-oriented interface.
```
from ColabTurtlePlus.Turtle import *
clearscreen()
setup(500,300)
T = Turtle()
T.color('red', 'yellow')
T.speed(13)
T.width(1.5)
S = T.clone()
T.fillrule("evenodd")
S.fillrule("nonzero")
x0 = -225
T.jumpto(x0,0)
S.jumpto(25,0)
T.begin_fill()
S.begin_fill()
while True:
    T.forward(200)
    T.left(170)
    S.forward(200)
    S.left(170)
    if (T.getx()-x0)**2 + T.gety()**2 < 1:
        break
T.end_fill()
S.end_fill()
```
The resulting image is  
![](https://github.com/mathriddle/ColabTurtlePlus/raw/main/stars.svg)

Main differences with ColabTurtle
----
This version implements classes. 

Some of the default values have been changed to mirror those in turtle.py. In particular,
* Default background color is white
* Default pen color is black
* Default pen size is 1
* Default shape is classic
* Default window size is 800x600
* Default mode is standard. Therefore
   * center of window has coordinates (0,0)
   * initial turtle heading is to the right (east)
   * positive angles are measured counterclockwise with 0° pointing right
   
The original default values in ColabTurtle can be used by calling oldDefaults() at the beginning.

This version extends ColabTurtle to include more of the commands found in the classic turtle.py module and some additional features.
* The possible turtle shapes include the ones from turtle.py: 'classic' (the default), 'arrow', 'triangle', 'square', 'circle', 'blank'. The 'turtle' shape is the one that Tolga Atam included in his original ColabTurtle version. Use 'turtle2' for the polygonal turtle shape form turtle.py. The circle shape from the original ColabTurtle was renamed 'ring'.
* Added the three modes from turtle.py, and an additional "svg" mode:
   * "standard" : initial turtle heading is to the right (east) and positive angles measured counterclockwise with 0° pointing right.
   * "logo" : initial turtle heading is upward (north) and positive angles are measured clockwise with 0° pointing up.
   * "world" : used with user-defined coordinates. Setup is same as "standard".
   * "svg": This is a special mode to handle how the original ColabTurtle worked. The coordinate system is the same as that used with SVG. The upper left corner is (0,0) with positive x direction going left to right, and the positive y direction going top to bottom. Positive angles are measured clockwise with 0° pointing right.
* Added functions to print or save the svg tags for the image.
* Added speed=0 option that displays final image with no animation. Need to call done() at end so the final image is displayed.
* Implemented begin_fill and end_fill functions from aronma/ColabTurtle_2 github. Added fillcolor, fillrule, and fillopacity functions. Because the fill is controlled by svg rules, the result may differ from classic turtle fill. The fill-rule and fill-opacity can be set as arguments to the begin_fill() function and will apply only to objects filled before the end_fill is called. There are two possible arguments to specify the SVG fill-rule: 'nonzero' (default) and 'evenodd'.  See https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/fill-rule for details.
* Implemented circle method from aronma/ColabTurtle_2 github. Modified this to match behavior of circle method in classic turtle.py package. If the radius is positive, the center of the circle is to the left of the turtle and the path is drawn in the counterclockwise direction. If the radius is negative, the center of the circle is to the right of the turtle and path is drawn in the clockwise direction. Number of steps is not used here since the circle is drawn using the svg circle function. However, the step argument is available but primarily for backward compatability with classic turtle.py circle. To get a true circular arc, do NOT use steps since the circle will be drawn using SVG commands. If steps > 20, it will be assumed that an arc of a circle was intended. While this function can still be used to draw a regular polygon with 20 or fewer sides, it is better to use the regularpolygon() method to take advantage of svg commands.
* Modified the color function to set both the pencolor as well as the fillcolor, just as in classic turtle.py package.
* Added animated motion along lines and circles, and for rotating right or left. Animation can be turned off/on using animationOff
  and animationOn. Default is animationOn.
* Added many of the screen and turtle methods from the classic turtle.py package.
  
Main differences with classic turtle.py
----

* The circle method draws smooth arcs using SVG. The step argument is available but primarily for backward compatability with classic turtle.py circle. To get a true circular arc, do NOT use steps since the circle will be drawn using SVG commands. If steps > 20, it will be assumed that an arc of a circle was intended. While this function can still be used to draw a regular polygon with 20 or fewer sides, it is better to use the regularPolygon() turtle method to take advantage of svg commands.
* A screen method to draw lines has been included.
* Added getcolor function to return a color string from the list of 140 valid HTML colors that are allowed as valid colors. 
* Setting speed = 0 draws only the final image with no intermediate animations. This is usually very quick. To turn off the animation but still show the turtle motion (equivalent to speed=0 in classic turtle.py), call animationOff(). This will use the current speed, but forward/back/circle makes the turtle jump and likewise left/right makes the turtle turn instantly. Keeping consistent with the original ColabTurtle, the non-zero speed values can be from 1 to 13 (slowest to fastest).
* There is a fillrule turtle method to set nonzero or evenodd as the options used by SVG to fill an object. The global default fill-rule is evenodd to match the behavior of classic turtle.py. The begin_fill() function can take an argument of 'nonzero' or 'evenodd' to set the fill-rule just for that fill. See details in the documentation.
* There is a fillopacity turtle method that sets the global fill-opacity used by SVG to fill an object. The default is 1. The begin_fill() function can take an argument between 0 and 1 to set the fill_opacity just for that fill. See details in the documentation.
* The stamp turtle method has an optional layer argument. The argument determines whether the stamp appears below other items (layer=0) or above other items (layer=1) in the order that SVG draws items. So if layer=0, a stamp may be covered by a filled object, for example, even if the stamp is originally drawn on top of the object during the animation. To prevent this, set layer=1 (or any nonzero number). The default is layer=0 if no argument is given.
* Not all the methods from classic turtle.py are included. Most of the missing ones are for user events, special turtle methods, and screen methods.

Documentation for the methods and functions in ColabTurtlePlus can be found at <a href="https://larryriddle.agnesscott.org/ColabTurtlePlus/documentation2.html">https://larryriddle.agnesscott.org/ColabTurtlePlus/documentation2.html.
