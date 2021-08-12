# ColabTurtlePlus
An extension of the original ColabTurtle by Tolga Atam (tolgaatam). Also includes some code from jaronma ColabTurtle_2 repo.


This is a module for drawing classic Turtle figures on Google Colab notebooks. It can also be used in Jupyter Lab notebooks. The graphics are drawn using SVG tags. The SVG commands can be printed on screen (after the drawing is completed) or saved to a file for use in a program like inkscape or Adobe Illustrator, or displaying the image in a webpage.

Installation
----
Create an empty code cell and type:

   !pip install ColabTurtlePlus

Run the code cell to install the library.

Usage
----
In any code cell, import the package using either

    from ColabTurtlePlus.Turtle import *

or

    import ColabTurtlePlus.Turtle as turtle

where turtle (or other name) is the name of the turtle. As Colab stores the declared variables in the runtime, call this before using 

    turtle.initializeTurtle()

Main differences from ColabTurtle
----
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
   
The original default values in ColabTurtle can be used by calling turtle.oldDefaults() **before** the initializeTurtle() command.

This version extends ColabTurtle to include more of the commands found in the classic turtle.py package and some additional features.
* The possible turtle shapes include the ones from turtle.py: 'classic' (the default), 'arrow', 'triangle', 'square', 'circle', 'blank'. The 'turtle' shape is the one that Tolga Atam included in his original ColabTurtle version. Use 'turtle2' for the polygonal turtle shape form turtle.py. The circle shape from the original ColabTurtle was renamed 'ring'.
* Added option for selecting a mode when initializing the turtle graphics
   * "standard" : initial turtle heading is to the right (east) and positive angles measured counterclockwise with 0° pointing right.
   * "logo" : initial turtle heading is upward (north) and positive angles are measured clockwise with 0° pointing up.
   * "world" : used with user-defined coordinates. Setup is same as "standard".
   * "svg": This is a special mode to handle how the original ColabTurtle worked. The coordinate system is the same as that used with SVG. The upper left corner is (0,0) with positive x direction going left to right, and the positive y direction going top to bottom. Positive angles are measured clockwise with 0° pointing right.
* Added functions to print or save the svg tags for the image.
* Added speed=0 option that displays final image with no animation. Need to call done() at end so the final image is displayed.
* Added setworldcoordinates function to allow for setting world coordinate system. This sets the mode to "world". If this is done *before* initializing the turtle window, the graphic window is adjusted to maintain
  the same aspect ratio as the axes, so angles are true. It the world coordinates are set *after* initializing
  the turtle window, angles and circles may be distorted. It is usually necessary to run the command resetwindow() before initializing the turle if you want to rerun the program without restarting the Colab runtime. Otherwise the graphic window may be resized to make the aspect ratios the same.
* Added towards function to return the angle between the line from turtle position to specified position.
* Implemented begin_fill and end_fill functions from aronma/ColabTurtle_2 github. Added fillcolor, fillrule, and fillopacity functions. Because the fill is controlled by svg rules, the result may differ from classic turtle fill. The fill-rule and fill-opacity can be set as arguments to the begin_fill() function and will apply only to objects filled before the end_fill is called. There are two possible arguments to specify the SVG fill-rule: 'nonzero' (default) and 'evenodd'.  See https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/fill-rule for details.
* Implemented circle function from aronma/ColabTurtle_2 github. Modified this to match behavior of circle function in classic turtle.py package. If the radius is positive, the center of the circle is to the left of the turtle and the path is drawn in the counterclockwise direction. If the radius is negative, the center of the circle is to the right of the turtle and path is drawn in the clockwise direction. Number of steps is not used here since the circle is drawn using the svg circle function. However, the step argument is available but primarily for backward compatability with classic turtle.py circle. To get a true circular arc, do NOT use steps since the circle will be drawn using SVG commands. If steps > 20, it will be assumed that an arc of a circle was intended. While this function can still be used to draw a regular polygon with 20 or fewer sides, it is better to use the regularpolygon() function to take advantage of svg commands.
* Modified the color function to set both the pencolor as well as the fillcolor, just as in classic turtle.py package.
* Added dot function to draw a dot with given diameter and color.
* Added shapesize and shearfactor functions to scale/shear the turtle shape.
* Added stamp, clearstamp, and clearstamps functions.
* Added getcolor function to return a color string from the list of 140 valid HTML colors that are allowed as valid colors. 
* Added radians and degrees functions to allow user to specify angle measurement for arguments to right/left/circle. 
  All internal calculations are done in degrees.
* Added animated motion along lines and circles, and for rotating right or left. Animation can be turned off/on using animationOff
  and animationOn. Default is animationOn.
  
Main differences with classic turtle.py
----

* Classes are not implemented, so only one turtle can be drawn at a time.
* The circle function draws smooth arcs using SVG. The step argument is available but primarily for backward compatability with classic turtle.py circle. To get a true circular arc, do NOT use steps since the circle will be drawn using SVG commands. If steps > 20, it will be assumed that an arc of a circle was intended. While this function can still be used to draw a regular polygon with 20 or fewer sides, it is better to use the regularpolygon() function to take advantage of svg commands.
* A function to draw lines has been included.
* Setting speed = 0 draws only the final image with no intermediate animations. This is usually very quick. To turn off the animation but still show the turtle motion (equivalent to speed=0 in classic turtle.py), call animationOff(). This will use the current speed, but forward/back/circle makes the turtle jump and likewise left/right makes the turtle turn instantly.
* There is a fillrule function to set nonzero or evenodd as the options used by SVG to fill an object. The global default fill-rule is evenodd to match the behavior of classic turtle.py. The begin_fill() function can take an argument of 'nonzero' or 'evenodd' to set the fill-rule just for that fill.
* There is a fillopacity function that sets the global fill-opacity used by SVG to fill an object. The default is 1. The begin_fill() function can take an argument between 0 and 1 to set the fill_opacity just for that fill. See details below.
* The stamp function has an optional layer argument. The argument determines whether the stamp appears below other items (layer=0) or above other items (layer=1) in the order that SVG draws items. So if layer=0, a stamp may be covered by a filled object, for example, even if the stamp is originally drawn on top of the object during the animation. To prevent this, set layer=1 (or any nonzero number). The default is layer=0 if no argument is given.
* Not all the functions from classic turtle.py are included. Most of the missing ones are for user events, special turtle methods, and screen methods.
