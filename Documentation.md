# Documentation for ColabTurtlePlus

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

Functions
----

See https://docs.python.org/3/library/turtle.html for more details on most of these commands from classic turtle.py.

`initializeTurtle(window,mode,speed)` -> Constructs the display for the turtle. The three arguments are optional. Set `window=(w,h)` to specify a window of width w pixels and height h pixels. The `speed` sets the initial speed and `mode` specifies either 'standard', 'lego', 'world', or 'svg'. Default values [(800,600), 'standard', 5] are used if an argument is not given.

`oldDefaults()` -> Set the defaults used in the original version of ColabTurtle package for backward compatability. This should be called **before** initializeTurtle.

#### SVG Functions

`showSVG(show_turtle)` -> Print the SVG tags to the screen. The `show_turtle` argument (True or False) determines whether or not the turtle is included.\
`saveSVG(filename, show_turtle)` -> Save the SVG tags to the file `filename`. The `show_turtle` argument (True or False) determines whether or not the turtle is included. If the filename is omitted, "SVGimage.svg" will be used.

#### Turtle Motion - Move and Draw

`forward(units) | fd(units)` -> Moves the turtle in the direction it is facing, by `units` pixels

`backward(units) | bk(units) | back(units)` -> Moves the turtle in the opposite of the direction it is facing, by `units` pixels

`right(degrees) | rt(degrees)` -> Turns the turtle to right by the given `degrees` 

`left(degrees) | lt(degrees)` -> Turns the turtle to left by the given `degrees` 

`goto(x,y) | setpos(x,y) | setposition(x,y)`\
`goto((x,y)) | setpos((x,y)) | setposition((x,y))`\
Moves the turtle to the point defined by x,y. The coordinates can be given separately, or in a single tuple.

`setx(x)` -> Moves the turtle to the given `x` position, the y coordinate of the turtle stays the same.

`sety(y)` -> Moves the turtle to the given `y` position, the x coordinate of the turtle stays the same.

`setheading(to_angle) | heading(to_angle) | face(to_angle)` -> Sets the orientation of the turtle to `to_angle`. The result depends on the mode.

`home()` -> Returns the turtle to the beginning position and angle. The turtle will continue drawing during this operation if the pen is down.

`jumpto(x,y)` -> Jump immediately to the point (x,y) without drawing or animation. The coordinates can be given separately, or in a single tuple.

`circle(radius, extent, steps)` -> Draws a circle of radius `radius` covering an extent of `extent` degrees. If extent is not given, draws the complete circle. If the radius is positive, the center of the circle is to the left of the turtle and the path is drawn in the counterclockwise direction. If the radius is negative, the center of the circle is to the right of the turtle and path is drawn in the clockwise direction. Number of steps is not used here for an actual circular arc since the circle is drawn using the svg circle function. However, the step argument is available primarily for backward compatability with classic turtle.py circle. To get a true circular arc, do NOT use steps since the circle will be drawn using SVG commands. If steps > 20, it will be assumed that an arc of a circle was intended. While this function can still be used to draw a regular polygon with 20 or fewer sides, it is better to use the regularpolygon() function (see below) to take advantage of svg commands.

`dot(size,color)` -> Draw a circular dot with diameter size, using color.

`stamp(layer)` -> Stamp a copy of the turtle shape onto the canvas at the current turtle position. Return a stamp_id for that stamp, which can be used to delete it by calling clearstamp(stamp_id). The optional layer argument determines whether the stamp appears below other items (layer=0) or above other items (layer=1) in the order that SVG draws items. So if layer=0, a stamp may be covered by a filled object, for example, even if the stamp is originally drawn on top of the object during the animation. To prevent this, set layer=1 (or any nonzero number). The default is layer=0 if no argument is given.

`clearstamp(stampid)` -> Delete stamp with given stampid, which can be an integer or a tuple of integers.

`clearstamps(n)` -> Delete all or first/last n of turtle’s stamps. If n is None, delete all stamps, if n > 0 delete first n stamps, else if n < 0 delete last n stamps.

`speed(s)` -> Sets the speed of turtle's movements. `s` can be a value in interval [0,13] where 1 is the slowest and 13 is the fastest for animation. If the speed is 0, no animation is drawn and only the final result is shown. The command `done()` must be executed to see the final image if speed=0. If `s` is omitted, the function returns the current speed.

`done() | update()` -> Redraws the image. Needed if speed = 0 so that final image is drawn.

`drawline(x1,y1,x2,y2) | line(x1,y1,x2,y2)`\
`drawline((x1,y1),(x2,y2) | line((x1,y1),(x2,y2))`\
Draw a line from (x1,y1) to (x2,y2)

`regularPolygon(sides,length,steps)` -> Moves the turtle around a regular polygon of with size sides, with length being the length of each side. The optional steps argument indicates how many sides are drawn. The initial and concluding angle is half of the exterior angle. Positive values for sides or length draws the polygon to the left of the turtle's current direction, and a negative value foreither sides or length draws it to the right of the turtle's current direction. The number of sides from 3 to 10 can also be given as a string using the name of the regular polygon (i.e. "triangle", "square", "pentagon", etc.)

#### Turtle Motion - Tell Turtle's State

`position() | pos()` -> Returns the current x,y coordinates of the turtle as a tuple.

`towards(x,y) | towards((x,y))` -> Return the angle between the line from turtle position to position specified by (x,y). This depends on the turtle’s start orientation which depends on the mode - standard/world/logo/svg.

`xcor() | getx()` -> Returns the current x coordinate of the turtle.

`ycor() | gety()` -> Returns the current y coordinate of the turtle.

`heading() | getheading()` -> Returns the direction that the turtle is looking at right now, in degrees.

`distance(x,y) | distance((x,y))` -> Returns the turtle's distance to a given point x,y. The coordinates can be given separately or as a single tuple.

#### Turtle Motion -- Setting and measurement

`degrees()`\
`radians()`
Sets the angle measurement for user input requiring an angle. All internal calculations are done in degrees after radians are converted.

#### Pen Control - Drawing State

`pendown() | pd()` -> Puts the pen down, causing the turtle movements to start drawing again.

`penup() | pu() | up()` -> Lifts the pen, turtles movement will not draw anything after this function is called.

`pensize(w) | width(w)` -> Changes the width of the pen. If the parameter is omitted, returns the current pen width.

`pen(pen, **pendict)` -> Return or set the pen's attributes.

`isdown()` -> Return True if pen is down, False if it’s up.

#### Pen Control - Color Control

`color()` -> Return the current pencolor and the current fillcolor\
`color(colorstring), color((r,g,b)` -> set both fillcolor and pencolor to the given value\
`color(string1,string2), color((r1,g1,b1),(r2,g2,b2))` -> Equivalent to pencolor(string1) and fillcolor(string2)

```
pencolor()
pencolor(r,g,b)
pencolor((r,g,b))
pencolor(colorstring)
```
If no parameter given, returns the current background color as string. Else, changes the background color of the drawing area. The color can be given as three separate color arguments as in the RGB color encoding: red,green,blue. These three numbers can be given in a single tuple as well. The color can be given as a single color string, too! The following formats are accepted for this color string:
- HTML standard color names: 140 color names defined as standard ( https://www.w3schools.com/colors/colors_names.asp ) . Examples: `"red"`, `"black"`, `"magenta"`, `"cyan"` etc. Can also use 'none' for no background color.
- Hex string with 3 or 6 digits, like `"#fff"`, `"FFF"`, `"#dfdfdf"`, `"#DFDFDF"`
- RGB string, like `"rgb(10 20 30)"`, `"rgb(10, 20, 30)"`

```
fillcolor()
fillcolor(r,g,b)
fillcolor((r,g,b))
fillcolor(colorstring)
```
Works the same as `pencolor` for the fillcolor.

`getcolor(n)` -> Returns the color string in position n in the valid color list. Requires 0 <= n <= 139.

#### Pen Control - Filling

`filling()` -> Return fillstate (True if filling, False else)

`begin_fill()` -> To be called just before drawing a shape to be filled.

`end_fill()` -> Fill the shape drawn after the last call to begin_fill().

`fillrule(rule)` -> Sets the global fill_rule (nonzero or evenodd) used by SVG to fill an object. The global default fill-rule is evenodd to match the behavior of classic turtle.py. The `begin_fill()` function can take an argument of 'nonzero' or 'evenodd' to set the fill_rule just for that fill.

`fillopacity(opacity)` -> Sets the global fill-opacity used by SVG to fill an object. The default is 1. The `begin_fill()` function can take an argument between 0 and 1 to set the fill_opacity just for that fill.

Because the fill is controlled by svg rules, the result may differ from classic turtle fill. The fill-rule and fill-opacity can be set as arguments to the begin_fill() function and will apply only to objects filled before the end_fill is called. There are two possible arguments to specify the SVG fill-rule: 'nonzero' and 'evenodd'. The default is 'evenodd' to match the fill behavior in classic turtle.py. See https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/fill-rule for details.

Note: end_fill() will use the current pen color and current pen width for the boundary of the area being filled. If you want to change the pen color or width during the fill, you will need to do a separate begin_fill, end_fill pair for each separate color and/or width.

#### Pen Control - More Drawing Control

`reset()` -> Reset most (but not all) of the default values. Clears the drawing and moves turtle back to the middle of the drawing window.

`clear()` -> Clear any drawing on the screen.

`write(obj, align=, font=)` -> Writes the string equivalent of any value to the screen. `align` and `font` **named** parameters can be given as arguments optionally. `align` must be one of `"left","center","right"`. It specifies where to put the text with respect to the turtle. `font` must be a tuple of three values like `(20, "Arial", "bold")`. The first value is the size, second value is the font family (only the ones that your browser natively supports must be used), the third value is font style that must be one of `"normal","bold","italic","underline"`.

#### Turtle State - Visibility

`showturtle() | st()` -> Makes the turtle visible.

`hideturtle() | ht()` -> Makes the turtle invisible.

`isvisible()` -> Returns whether turtle is currently visible as boolean.

#### Turtle State - Appearance

`shape(sh)` -> Takes a shape name `sh` and transforms the main character's look. This library has `'classic'`, `'turtle'`, `'circle'`, `'arrow'`, `'triangle'`, `'square'`, `'ring'`, `'blank'`, and `'turtle2'` shapes available, with `'classic'` as the default. If no argument is supplied, this function returns the name of the current shape. The `'turtle'` shape is the one that Tolga Atam included in his original ColabTurtle version. Use `'turtle2'` for the polygonal turtle shape form turtle.py. The circle shape from the original ColabTurtle was renamed `'ring'`.

`shapesize(stretch_wid=None, stretch_len=None, outline=None) | turtlesize()` -> Scale the size of the turtle. The turtle will be displayed stretched according to its stretchfactors: `stretch_wid` is stretchfactor perpendicular to its orientation, `stretch_len` is stretchfactor in direction of its orientation, `outline` determines the width of the shapes’s outline.

`shearfactor(shear)` -> Set or return the current shearfactor. Shear the turtleshape according to the given shearfactor shear, which is the tangent of the shear angle. Do not change the turtle’s heading (direction of movement). If shear is not given: return the current shearfactor, i. e. the tangent of the shear angle, by which lines parallel to the heading of the turtle are sheared.

`tiltangle(angle)` -> Set or return the current tilt-angle. If angle is given, rotate the turtleshape to point in the direction specified by angle, regardless of its current tilt-angle. Do not change the turtle’s heading (direction of movement). If angle is not given, return the current tilt-angle, i. e. the angle between the orientation of the turtleshape and the heading of the turtle (its direction of movement).

`tilt(angle)` -> Rotate the turtle shape by angle from its current tilt-angle, but do not change the turtle’s heading (direction of movement).

#### Window Control

```
bgcolor()
bgcolor(r,g,b)
bgcolor((r,g,b))
bgcolor(colorstring)
```
Works the same as `pencolor` for the background color.

`window_width()` -> Return the width of the turtle window.

`window_height()` -> Return the height of the turtle window.

`setworldcoordinates(llx,lly,urx,ury)` -> Set up user-defined coordinate system and switch to mode “world”. If this is done before initializing the turtle window, the graphic window is adjusted to maintain the same aspect ratio as the axes, so angles are true. It the world coordinates are set after initializing
the turtle window, angles and circles may be distorted. Usually best to also run resetwindows() before initializing the turle when using world coordinates.\
* `llx` : x-coordinate of lower left corner of canvas
* `lly` : y-coordinate of lower left corner of canvas
* `urx` : x-coordinate of upper right corner of canvas
* `ury` : y-coordinate of upper right corner of canvas

`resetwindow()` -> Resets the axes min/max values and the mode to None. This should be executed if using world coordinates in a situation where the aspect
ratio of the graphing window is intended to be different than the aspect ratio of the axes, and you want to rerun a cell in Colab containing initializeTurtle. This should usually be the first line of the program (before initializeTurtle or setworldcoordinates).

`showborder(color)` -> Show a border around the graphics window. Default (no parameters) is gray. A color can be specified in a similar way as with `pencolor`.

`hideborder()` -> Hide the border around the graphics window.

`mode(mode)` -> Set turtle mode (“standard”, “logo”, “world”, or "svg") and reset the window. If mode is not given, current mode is returned.

#### Animation Controls

`delay(delay_time)` -> Delay execution of next object for given delay time (in seconds)

`animationOff()`\
`animationOn`\
Turn off\on animation. When off, forward/back/circle makes turtle jump and likewise left/right make the turtle turn instantly.

Examples
---

Examples of using ColabTurtlePlus in a Colaboratory or JupyterLab noteboook can be found in the examples folder.
