from IPython.display import display, HTML
import time
import math
import re

""" 
Original Created at: 23rd October 2018
        by: Tolga Atam
v2.1.0 Updated at: 15th March 2021
         by: Tolga Atam
Module for drawing classic Turtle figures on Google Colab notebooks.
It uses html capabilites of IPython library to draw svg shapes inline.
Looks of the figures are inspired from Blockly Games / Turtle (blockly-games.appspot.com/turtle)

--------
v1.0.0 Modified April/May 2021 by Larry Riddle
v.1.1.0 Updated July 17
Changed some default values to match classic turtle.py package
  default background color is white, default pen color is black, default pen thickness is 1
  default mode is "standard"
  center of window has coordinates (0,0)
Added option for selecting a mode when initializing the turtle graphics
  "standard" : default direction is to the right (east) and positive angles measured counterclockwise
  "logo" : default directon is upward (north) and positive angles are measured clockwise with 0° pointing up.
  "world" : like standard but with user-defined coordinates. Initial turtle position is (0,0).
  "svg": This is a special mode to handle how the original ColabTurtle worked. The coordinate system is the same
         as that used with SVG. The upper left corner is (0,0) with positive x direction being to the right, and the 
         positive y direction being to the bottom. Positive angles are measured clockwise with 0° pointing right.
Added functions to print or save the svg coding for the image.
Added additional shapes from classic turtle.py: 'classic' (the default shape), 'arrow', 'square', 'triangle', 'circle','turtle2', 'blank'
  The circle shape in the original ColabTurtle has been renamed to 'ring'.
  The turtle2 shape is the same as the turtle shape in the classic turtle.py package.
Added speed=0 option that displays final image with no animation. 
  Added done function so that final image is displayed on screen when speed=0.
Added setworldcoordinates function to allow for setting world coordinate system. This sets the mode to "world".
  If this is done *before* initializing the turtle window, the graphic window is adjusted to maintain
  the same aspect ratio as the axes, so angles are true. It the world coordinates are set *after* initializing
  the turtle window, no adjustment is made to the window size so angles may appear distorted.
Added towards function to return the angle between the line from turtle position to specified position.
Implemented begin_fill and end_fill functions from aronma/ColabTurtle_2 github. Added fillcolor function and fillrule function.
  The fillrule function can be used to specify the SVG fill_rule (nonzero or evenodd). The default is evenodd to match turtle.py behavior.
  When calling begin_fill, a value for the fill_rule can be given that will apply only to that fill.
  Because the fill is controlled by svg rules, the result may differ from classic turtle fill.
Implemented circle (arc) function from aronma/ColabTurtle_2 github. Modified these to match behavior of circle function in
  classic turtle.py package. If the radius is positive, the center of the circle is to the left of the turtle and the
  path is drawn in the counterclockwise direction. If the radius is negative, the center of the circle is to the right of
  the turtle and path is drawn in the clockwise direction. Number of steps is not used here since the circle is drawn using
  the svg circle function.
Modified the color function to set both the pencolor as well as the fillcolor, just as in classic turtle.py package.
Added dot function to draw a dot with given diameter and color.
Added shapesize function to scale the turtle shape.
Added shearfactor function.
Added stamp, clearstamp, and clearstamps to stamp a copy of the turtle shape onto the canvas at the current turtle position, or to
  delete stamps. Use stamp() or stamp(0) to put stamp at bottom of SVG order while stamp(1) will put it at top of SVG order.
Added pen function.
Added tilt and tiltangle functions.
Added degrees and radians functions.
Added animated motion along lines and circles, and for rotating right or left. Animation can be turned off/on using animationOff
  and animationOn. Default is animationOn.
Added a function to draw a line segment independent of the turtle motion.
Added a function for the turtle to move along a regular polygon.
Original ColabTurtle defaults can be set by calling oldDefaults() after importing the ColabTurtle package but before initializeTurtle.
  This sets default background to black, default pen color to white, default pen width to 4, default shape to Turtle, and
  default window size to 800x500. It also sets the mode to "svg".
Added jumpto function to go directly to a given location with drawing or animation.

"""

DEFAULT_WINDOW_SIZE = (800, 600)
DEFAULT_SPEED = 5
DEFAULT_TURTLE_VISIBILITY = True
DEFAULT_PEN_COLOR = 'black'
DEFAULT_TURTLE_DEGREE = 0
DEFAULT_BACKGROUND_COLOR = 'white'
DEFAULT_FILL_COLOR = 'black'
DEFAULT_BORDER_COLOR = ""
DEFAULT_IS_PEN_DOWN = True
DEFAULT_SVG_LINES_STRING = ""
DEFAULT_PEN_WIDTH = 1
DEFAULT_OUTLINE_WIDTH = 1
DEFAULT_STRETCHFACTOR = (1,1)
DEFAULT_SHEARFACTOR = 0
DEFAULT_TILT_ANGLE = 0
DEFAULT_FILL_RULE = 'evenodd'
DEFAULT_FILL_OPACITY = 1
# All 140 color names that modern browsers support, plus 'none'. Taken from https://www.w3schools.com/colors/colors_names.asp
VALID_COLORS = ('black', 'navy', 'darkblue', 'mediumblue', 'blue', 'darkgreen', 'green', 'teal', 'darkcyan', 'deepskyblue', 'darkturquoise', 
                'mediumspringgreen', 'lime', 'springgreen', 'aqua', 'cyan', 'midnightblue', 'dodgerblue', 'lightseagreen', 'forestgreen', 'seagreen', 
                'darkslategray', 'darkslategrey', 'limegreen', 'mediumseagreen', 'turquoise', 'royalblue', 'steelblue', 'darkslateblue', 'mediumturquoise', 
                'indigo', 'darkolivegreen', 'cadetblue', 'cornflowerblue', 'rebeccapurple', 'mediumaquamarine', 'dimgray', 'dimgrey', 'slateblue', 'olivedrab', 
                'slategray', 'slategrey', 'lightslategray', 'lightslategrey', 'mediumslateblue', 'lawngreen', 'chartreuse', 'aquamarine', 'maroon', 'purple', 
                'olive', 'gray', 'grey', 'skyblue', 'lightskyblue', 'blueviolet', 'darkred', 'darkmagenta', 'saddlebrown', 'darkseagreen', 'lightgreen', 
                'mediumpurple', 'darkviolet', 'palegreen', 'darkorchid', 'yellowgreen', 'sienna', 'brown', 'darkgray', 'darkgrey', 'lightblue', 'greenyellow', 
                'paleturquoise', 'lightsteelblue', 'powderblue', 'firebrick', 'darkgoldenrod', 'mediumorchid', 'rosybrown', 'darkkhaki', 'silver', 
                'mediumvioletred', 'indianred', 'peru', 'chocolate', 'tan', 'lightgray', 'lightgrey', 'thistle', 'orchid', 'goldenrod', 'palevioletred', 
                'crimson', 'gainsboro', 'plum', 'burlywood', 'lightcyan', 'lavender', 'darksalmon', 'violet', 'palegoldenrod', 'lightcoral', 'khaki', 
                'aliceblue', 'honeydew', 'azure', 'sandybrown', 'wheat', 'beige', 'whitesmoke', 'mintcream', 'ghostwhite', 'salmon', 'antiquewhite', 'linen', 
                'lightgoldenrodyellow', 'oldlace', 'red', 'fuchsia', 'magenta', 'deeppink', 'orangered', 'tomato', 'hotpink', 'coral', 'darkorange', 
                'lightsalmon', 'orange', 'lightpink', 'pink', 'gold', 'peachpuff', 'navajowhite', 'moccasin', 'bisque', 'mistyrose', 'blanchedalmond', 
                'papayawhip', 'lavenderblush', 'seashell', 'cornsilk', 'lemonchiffon', 'floralwhite', 'snow', 'yellow', 'lightyellow', 'ivory', 'white','none','')
#VALID_COLORS_SET = set(VALID_COLORS)
VALID_MODES = ('standard','logo','world','svg')
DEFAULT_TURTLE_SHAPE = 'classic'
VALID_TURTLE_SHAPES = ('turtle', 'ring', 'classic', 'arrow', 'square', 'triangle', 'circle', 'turtle2', 'blank') 
DEFAULT_MODE = 'standard'
DEFAULT_ANGLE_MODE = 'degrees'
SVG_TEMPLATE = """
      <svg width="{window_width}" height="{window_height}">  
        <rect width="100%" height="100%" style="fill:{background_color};stroke:{kolor};stroke-width:1"/>
        {stampsB}
        {lines}
        {dots}
        {stampsT}
        {turtle}
      </svg>
    """
TURTLE_TURTLE_SVG_TEMPLATE = """<g id="turtle" visibility="{visibility}" transform="rotate({degrees},{rotation_x},{rotation_y}) translate({turtle_x}, {turtle_y})">
<path style="stroke:{pen_color};fill-rule:evenodd;fill:{turtle_color};fill-opacity:1;" transform="skewX({sk}) scale({sx},{sy})" d="m 1.1536693,-18.56101 c -2.105469,1.167969 -3.203125,3.441407 -3.140625,6.5 l 0.011719,0.519532 -0.300782,-0.15625 c -1.308594,-0.671875 -2.828125,-0.824219 -4.378906,-0.429688 -1.9375,0.484375 -3.8906253,2.089844 -6.0117193,4.9257825 -1.332031,1.785156 -1.714843,2.644531 -1.351562,3.035156 l 0.113281,0.125 h 0.363281 c 0.71875,0 1.308594,-0.265625 4.6679693,-2.113282 1.199219,-0.660156 2.183594,-1.199218 2.191406,-1.199218 0.00781,0 -0.023437,0.089844 -0.074218,0.195312 -0.472657,1.058594 -1.046876,2.785156 -1.335938,4.042969 -1.054688,4.574219 -0.351562,8.453125 2.101562,11.582031 0.28125,0.355469 0.292969,0.253906 -0.097656,0.722656 -2.046875,2.4609375 -3.027344,4.8984375 -2.734375,6.8046875 0.050781,0.339844 0.042969,0.335938 0.679688,0.335938 2.023437,0 4.15625,-1.316407 6.21875,-3.835938 0.222656,-0.269531 0.191406,-0.261719 0.425781,-0.113281 0.730469,0.46875 2.460938,1.390625 2.613281,1.390625 0.160157,0 1.765625,-0.753906 2.652344,-1.246094 0.167969,-0.09375 0.308594,-0.164062 0.308594,-0.160156 0.066406,0.105468 0.761719,0.855468 1.085937,1.171875 1.613282,1.570312 3.339844,2.402343 5.3593747,2.570312 0.324219,0.02734 0.355469,0.0078 0.425781,-0.316406 0.375,-1.742187 -0.382812,-4.058594 -2.1445307,-6.5585935 l -0.320312,-0.457031 0.15625,-0.183594 c 3.2460927,-3.824218 3.4335927,-9.08593704 0.558593,-15.816406 l -0.050781,-0.125 1.7382807,0.859375 c 3.585938,1.773437 4.371094,2.097656 5.085938,2.097656 0.945312,0 0.75,-0.863281 -0.558594,-2.507812 C 11.458356,-11.838353 8.3333563,-13.268041 4.8607003,-11.721166 l -0.363281,0.164063 0.019531,-0.09375 c 0.121094,-0.550781 0.183594,-1.800781 0.121094,-2.378907 -0.203125,-1.867187 -1.035157,-3.199218 -2.695313,-4.308593 -0.523437,-0.351563 -0.546875,-0.355469 -0.789062,-0.222657" >
</g>"""
TURTLE_RING_SVG_TEMPLATE = """<g id="ring" visibility="{visibility}" transform="rotate({degrees},{rotation_x},{rotation_y}) translate({turtle_x}, {turtle_y})">
<ellipse stroke="{pen_color}" transform="skewX({sk})" stroke-width="3" fill="transparent" rx="{rx}" ry = "{ry}" cx="0" cy="{cy}" />
<polygon points="0,5 5,0 -5,0" transform="skewX({sk}) scale({sx},{sy})" style="fill:{turtle_color};stroke:{pen_color};stroke-width:1" />
</g>"""
TURTLE_CLASSIC_SVG_TEMPLATE = """<g id="classic" visibility="{visibility}" transform="rotate({degrees},{rotation_x},{rotation_y}) translate({turtle_x}, {turtle_y})">
<polygon points="-5,-4.5 0,-2.5 5,-4.5 0,4.5" transform="skewX({sk}) scale({sx},{sy})" style="stroke:{pen_color};fill:{turtle_color};stroke-width:{pw}" >
</g>"""
TURTLE_ARROW_SVG_TEMPLATE = """<g id="arrow" visibility="{visibility}" transform="rotate({degrees},{rotation_x},{rotation_y}) translate({turtle_x}, {turtle_y})">
<polygon points="-10,-5 0,5 10,-5" transform="skewX({sk}) scale({sx},{sy})" style="stroke:{pen_color};fill:{turtle_color};stroke-width:{pw}" >
</g>"""
TURTLE_SQUARE_SVG_TEMPLATE = """<g id="square" visibility="{visibility}" transform="rotate({degrees},{rotation_x},{rotation_y}) translate({turtle_x}, {turtle_y})">
<polygon points="10,-10 10,10 -10,10 -10,-10" transform="skewX({sk}) scale({sx},{sy})" style="stroke:{pen_color};fill:{turtle_color};stroke-width:{pw}" >
</g>"""
TURTLE_TRIANGLE_SVG_TEMPLATE = """<g id="triangle" visibility="{visibility}" transform="rotate({degrees},{rotation_x},{rotation_y}) translate({turtle_x}, {turtle_y})">
<polygon points="10,-8.66 0,8.66 -10,-8.66" transform="skewX({sk}) scale({sx},{sy})" style="stroke:{pen_color};fill:{turtle_color};stroke-width:{pw}" >
</g>"""
TURTLE_CIRCLE_SVG_TEMPLATE = """<g id="ellipse" visibility="{visibility}" transform="rotate({degrees},{rotation_x},{rotation_y}) translate({turtle_x}, {turtle_y})">
<ellipse transform="skewX({sk}) scale({sx},{sy})" style="stroke:{pen_color};fill:{turtle_color};stroke-width:{pw}" rx="{rx}" ry = "{ry}" cx="0" cy="0" >
</g>"""
TURTLE_TURTLE2_SVG_TEMPLATE = """<g id="turtle2" visibility="{visibility}" transform="rotate({degrees},{rotation_x},{rotation_y}) translate({turtle_x}, {turtle_y})">
<polygon points="0,16 2,14 1,10 4,7 7,9 9,8 6,5 7,1 5,-3 8,-6 6,-8 4,-5 0,-7 -4,-5 -6,-8 -8,-6 -5,-3 -7,1 -6,5 -9,8 -7,9 -4,7 -1,10 -2,14" transform="skewX({sk}) scale({sx},{sy})" style="stroke:{pen_color};stroke-width:1;fill:{turtle_color}" >
</g>"""

shapeDict = {"turtle":TURTLE_TURTLE_SVG_TEMPLATE, 
              "ring":TURTLE_RING_SVG_TEMPLATE, 
              "classic":TURTLE_CLASSIC_SVG_TEMPLATE,
              "arrow":TURTLE_ARROW_SVG_TEMPLATE,
              "square":TURTLE_SQUARE_SVG_TEMPLATE,
              "triangle":TURTLE_TRIANGLE_SVG_TEMPLATE,
              "circle":TURTLE_CIRCLE_SVG_TEMPLATE,
              "turtle2":TURTLE_TURTLE2_SVG_TEMPLATE,
              "blank":""}

SPEED_TO_SEC_MAP = {0: 0, 1: 1.0, 2: 0.8, 3: 0.5, 4: 0.3, 5: 0.25, 6: 0.20, 7: 0.15, 8: 0.125, 9: 0.10, 10: 0.08, 11: 0.04, 12: 0.02, 13: 0.005}

# Helper function that maps [0,13] speed values to ms delays
def _speedToSec(speed):
    return SPEED_TO_SEC_MAP[speed]

timeout = _speedToSec(DEFAULT_SPEED)
turtle_speed = DEFAULT_SPEED
is_turtle_visible = DEFAULT_TURTLE_VISIBILITY
pen_color = DEFAULT_PEN_COLOR
window_size = DEFAULT_WINDOW_SIZE
turtle_pos = (DEFAULT_WINDOW_SIZE[0] / 2, DEFAULT_WINDOW_SIZE[1] / 2)
xmin = xmax = ymin = ymax = None
turtle_degree = DEFAULT_TURTLE_DEGREE
turtle_orient = DEFAULT_TURTLE_DEGREE
background_color = DEFAULT_BACKGROUND_COLOR
is_pen_down = DEFAULT_IS_PEN_DOWN
svg_lines_string = DEFAULT_SVG_LINES_STRING
pen_width = DEFAULT_PEN_WIDTH
turtle_shape = DEFAULT_TURTLE_SHAPE
_mode = DEFAULT_MODE
angle_mode = DEFAULT_ANGLE_MODE
border_color = DEFAULT_BORDER_COLOR
is_filling = False
fill_color = DEFAULT_FILL_COLOR
stretchfactor = DEFAULT_STRETCHFACTOR
shear_factor = DEFAULT_SHEARFACTOR
tilt_angle = DEFAULT_TILT_ANGLE
outline_width = DEFAULT_OUTLINE_WIDTH
fill_rule = DEFAULT_FILL_RULE
fill_opacity = DEFAULT_FILL_OPACITY
animate = True
angle_conv = 1

drawing_window = None

# Construct the display for turtle
def initializeTurtle(window=None, mode=None, speed=None):
    """Initializes the turtle and drawing window
    
    Args:
        window: (optional) the (width,height) in pixels
        mode: (optional) one of "standard, "logo", "world", or "svg"
        speed: (optional) integer in range 0..13
    
    The defaults are (800,600), "standard", and 5.
    """

    global window_size
    global drawing_window
    global turtle_speed
    global is_turtle_visible
    global pen_color
    global turtle_pos
    global turtle_degree
    global turtle_orient
    global background_color
    global is_pen_down
    global is_filling
    global svg_lines_string
    global svg_fill_string
    global fill_rule
    global svg_dots_string
    global svg_stampsB_string
    global svg_stampsT_string
    global pen_width
    global turtle_shape
    global _mode
    global xmin,ymin,xmax,ymax
    global xscale
    global yscale
    global timeout
    global stampdictB, stampdictT
    global stampnum
    global stamplist
    global tilt_angle
    global stretchfactor
    global shear_factor
    
    if window is None:
        window_size = DEFAULT_WINDOW_SIZE
    elif not (isinstance(window, tuple) and len(window) == 2 and isinstance(
            window[0], int) and isinstance(window[1], int)):
        raise ValueError('Window must be a tuple of 2 integers')
    else:
        window_size = window

    if speed is None:
         turtle_speed = DEFAULT_SPEED
    elif isinstance(speed,int) == False or speed not in range(0, 14):
        raise ValueError('Speed must be an integer in the interval [0,13]')
    else:
        turtle_speed = speed
    timeout = _speedToSec(turtle_speed)
    
    if _mode != "world":   
        if mode is None:
            _mode = DEFAULT_MODE
        elif mode not in VALID_MODES:
            raise ValueError('Mode must be standard, logo, or svg')
        else:
            _mode = mode
 
    if _mode == "world":
        if xmin is None:
            raise AttributeError("Coordinates not set. Run setworldcoordinates() before initializeTurtle or don't set mode='world' in initializeTurtle.")    
        if ymax-ymin > xmax-xmin:
            ysize = window_size[1]
            window_size = round((xmax-xmin)/(ymax-ymin)*ysize),ysize
        else:
            xsize = window_size[0]
            window_size = xsize, round((ymax-ymin)/(xmax-xmin)*xsize)
        xscale = yscale = window_size[0]/(xmax-xmin)
    elif _mode != "svg":
        xmin,ymin,xmax,ymax = -window_size[0]/2,-window_size[1]/2,window_size[0]/2,window_size[1]/2
        xscale = 1  #window_size[0]/(xmax-xmin)
        yscale = 1  #window_size[1]/(ymax-ymin)
    else:
        xmin = ymax = 0
        xscale = 1
        yscale = -1
       
    is_turtle_visible = DEFAULT_TURTLE_VISIBILITY
    if _mode != "world":
        turtle_pos = (window_size[0] / 2, window_size[1] / 2)
    else:
        turtle_pos = (_convertx(0),_converty(0))
    turtle_degree = DEFAULT_TURTLE_DEGREE if (_mode in ["standard","world"]) else (270 - DEFAULT_TURTLE_DEGREE)
    turtle_orient = turtle_degree
    background_color = DEFAULT_BACKGROUND_COLOR
    pen_color = DEFAULT_PEN_COLOR
    is_pen_down = DEFAULT_IS_PEN_DOWN
    svg_lines_string = DEFAULT_SVG_LINES_STRING
    pen_width = DEFAULT_PEN_WIDTH
    turtle_shape = DEFAULT_TURTLE_SHAPE
    tilt_angle = DEFAULT_TILT_ANGLE
    angle_mode = DEFAULT_ANGLE_MODE
    stretchfactor = DEFAULT_STRETCHFACTOR
    shear_factor = DEFAULT_SHEARFACTOR
    is_filling = False
    svg_fill_string = ''
    svg_dots_string = ''
    svg_stampsB_string = ''
    svg_stampsT_string = ''
    fill_color = DEFAULT_FILL_COLOR
    fill_rule = DEFAULT_FILL_RULE
    stampdictB = {}
    stampdictT = {}
    stampnum = 0
    stamplist=[]

    drawing_window = display(HTML(_generateSvgDrawing()), display_id=True)  

#=======================
# SVG functions
#=======================

# Helper function for generating svg string of the turtle
def _generateTurtleSvgDrawing():
    if is_turtle_visible:
        vis = 'visible'
    else:
        vis = 'hidden'

    turtle_x = turtle_pos[0]
    turtle_y = turtle_pos[1]
    if _mode == "standard":
        degrees = turtle_degree - tilt_angle    
    elif _mode == "world":
        degrees = turtle_orient - tilt_angle
    else:
        degrees = turtle_degree + tilt_angle
    
    if turtle_shape == 'turtle':
        degrees += 90
    elif turtle_shape == 'ring':
        turtle_y += 10*stretchfactor[1]+4
        degrees -= 90
    else:
        degrees -= 90
       
    return shapeDict[turtle_shape].format(
                           turtle_color=fill_color,
                           pen_color=pen_color,
                           turtle_x=turtle_x, 
                           turtle_y=turtle_y,
                           visibility=vis, 
                           degrees=degrees,
                           sx=stretchfactor[0],
                           sy=stretchfactor[1],
                           sk=shear_factor,
                           rx=10*stretchfactor[0],
                           ry=10*stretchfactor[1],
                           cy=-(10*stretchfactor[1]+4),
                           pw = outline_width,
                           rotation_x=turtle_pos[0], 
                           rotation_y=turtle_pos[1])

# Helper function for generating the whole svg string
def _generateSvgDrawing():
    return SVG_TEMPLATE.format(window_width=window_size[0], 
                               window_height=window_size[1],
                               background_color=background_color,
                               fill=svg_fill_string,
                               lines=svg_lines_string,
                               dots=svg_dots_string,
                               stampsB=svg_stampsB_string,
                               stampsT=svg_stampsT_string,
                               turtle=_generateTurtleSvgDrawing(),
                               kolor=border_color)

# Save the image as an SVG file using given filename. Set turtle=True to include turtle in svg output
def saveSVG(file=None, turtle=False):
    """Saves the image as an SVG file.
    
    Args:
        file: a string giving filename for saved file. The extension 
            ".svg" will be added if missing. If no filename is given,
            the default name SVGimage.svg will be used.
        turtle: an optional boolean that determines if the turtle 
            is included in the svg output saved to the file. Default is False.
    
    The SVG commands can be printed on screen (after the drawing is 
    completed) or saved to a file for use in a program like inkscape 
    or Adobe Illustrator, or displaying the image in a webpage.
    """
    
    if drawing_window == None:
        raise AttributeError("Display has not been initialized yet. Call initializeTurtle() before using.")
    if file is None:
        file = "SVGimage.svg"
    elif not isinstance(file, str):
        raise ValueError("File name must be a string")
    if not file.endswith(".svg"):
        file += ".svg"
    text_file = open(file, "w")
    header = ("""<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">\n""").format(
            w=window_size[0],
            h=window_size[1]) 
    header += ("""<rect width="100%" height="100%" style="fill:{fillcolor};stroke:{kolor};stroke-width:1" />\n""").format(
            fillcolor=background_color,
            kolor=border_color)
    image = svg_lines_string.replace("/>","/>\n")
    stampsB = svg_stampsB_string.replace("</g>","</g>\n")
    stampsT = svg_stampsT_string.replace("</g>","</g>\n")
    dots = svg_dots_string.replace(">",">\n")
    turtle_svg = (_generateTurtleSvgDrawing() + " \n") if turtle else ""
    output = header + stampsB + image + dots + stampsT + turtle_svg + "</svg>"
    text_file.write(output)
    text_file.close()

# Print the SVG code for the image to the screen. Set turtle=True to include turtle in svg output.
def showSVG(turtle=False):
    """Shows the SVG code for the image to the screen.
    
    Args:
        turtle: (optional) a boolean that determines if the turtle
            is included in the svg output
    
    The SVG commands can be printed on screen (after the drawing is 
    completed) or saved to a file for use in a program like inkscape 
    or Adobe Illustrator, or displaying the image in a webpage.
    """

    if drawing_window == None:
        raise AttributeError("Display has not been initialized yet. Call initializeTurtle() before using.")
    header = ("""<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">\n""").format(
            w=window_size[0],
            h=window_size[1]) 
    header += ("""<rect width="100%" height="100%" style="fill:{fillcolor};stroke:{kolor};stroke-width:1" />\n""").format(
            fillcolor=background_color,
            kolor=border_color)
    image = svg_lines_string.replace(">","/>\n")
    stampsB = svg_stampsB_string.replace("</g>","</g>\n")
    stampsT = svg_stampsT_string.replace("</g>","</g>\n")    
    dots = svg_dots_string.replace(">",">\n")
    turtle_svg = (_generateTurtleSvgDrawing() + " \n") if turtle else ""
    output = header + stampsB + image + dots + stampsT + turtle_svg + "</svg>"
    print(output) 

# Convert user coordinates to SVG coordinates
def _convertx(x):
    return (x-xmin)*xscale 
def _converty(y):
    return (ymax-y)*yscale

#================================
# Turtle Motion - Move and Draw
#================================

# Helper functions for updating the screen using the latest positions/angles/lines etc.
# If the turtle speed is 0, the update is skipped so animation is done.
# If the delay is False (or 0), update immediately without any delay
def _updateDrawing(delay=True):
    if drawing_window == None:
        raise AttributeError("Display has not been initialized yet. Call initializeTurtle() before using.")
    if (turtle_speed != 0):
        drawing_window.update(HTML(_generateSvgDrawing()))         
        if delay: time.sleep(timeout)          
            
# Helper function for managing any kind of move to a given 'new_pos' and draw lines if pen is down
# Animate turtle motion along line
def _moveToNewPosition(new_pos,units):
    global turtle_pos
    global svg_lines_string
    global svg_fill_string
    global timeout
    
    # rounding the new_pos to eliminate floating point errors.
    new_pos = ( round(new_pos[0],3), round(new_pos[1],3) ) 
    
    timeout_orig = timeout
    start_pos = turtle_pos           
    svg_lines_string_orig = svg_lines_string       
    s = 1 if units > 0 else -1            
    if turtle_speed != 0 and animate:
        if xscale == abs(yscale):
            # standard, logo, svg mode, or world mode with same aspect ratio for axes and window
            initial_pos = turtle_pos         
            alpha = math.radians(turtle_degree)
            tenx, teny = 10/xscale, 10/abs(yscale)
            dunits = s*10/xscale
            timeout = timeout*.20    
            while s*units > 0:
                dx = min(tenx,s*units)
                dy = min(teny,s*units)
                turtle_pos = (initial_pos[0] + s * dx * xscale * math.cos(alpha), initial_pos[1] + s * dy * abs(yscale) * math.sin(alpha))
                if is_pen_down:
                    svg_lines_string += \
                    """<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke-linecap="round" style="stroke:{pen_color};stroke-width:{pen_width}" />""".format(
                        x1=initial_pos[0],
                        y1=initial_pos[1],
                        x2=turtle_pos[0],
                        y2=turtle_pos[1],
                        pen_color=pen_color, 
                        pen_width=pen_width) 
                initial_pos = turtle_pos
                _updateDrawing()
                units -= dunits
        else:
            # world mode with aspect ratio of axes different than aspect ratio of the window
            initial_pos = position()
            alpha = math.radians(turtle_degree)
            timeout = timeout*0.20
            xpixunits = _convertx(1)-_convertx(0)  #length of 1 world unit along x-axis in pixels
            ypixunits = _converty(1)-_converty(0)  #length of 1 world unit along y-axis in pixels
            xstep = 10/(max(xpixunits,ypixunits))  #length of 10 pixels in world units 
            ystep = xstep
            dunits = s*xstep
            while s*units > 0:
                dx = min(xstep,s*units)
                dy = min(ystep,s*units)
                temp_turtle_pos = (initial_pos[0] + s * dx * math.cos(alpha), initial_pos[1] - s * dy * math.sin(alpha))
                turtle_pos = (_convertx(temp_turtle_pos[0]), _converty(temp_turtle_pos[1]))
                if is_pen_down:
                    svg_lines_string += \
                    """<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke-linecap="round" style="stroke:{pen_color};stroke-width:{pen_width}" />""".format(
                        x1=_convertx(initial_pos[0]),
                        y1=_converty(initial_pos[1]),
                        x2= turtle_pos[0],
                        y2= turtle_pos[1],
                        pen_color=pen_color, 
                        pen_width=pen_width) 
                initial_pos = temp_turtle_pos
                _updateDrawing()
                units -= dunits
    if is_pen_down:
        # now create the permanent svg string that does not display the animation
        svg_lines_string = svg_lines_string_orig + \
            """<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke-linecap="round" style="stroke:{pen_color};stroke-width:{pen_width}" />""".format(
                        x1=start_pos[0],
                        y1=start_pos[1],
                        x2=new_pos[0],
                        y2=new_pos[1],
                        pen_color=pen_color, 
                        pen_width=pen_width)
    if is_filling:
        svg_fill_string += """ L {x1} {y1} """.format(x1=new_pos[0],y1=new_pos[1])  
    turtle_pos = new_pos
    timeout = timeout_orig
    if not animate: _updateDrawing()
       
# Helper function for drawing arcs of radius 'r' to 'new_pos' and draw line if pen is down.
# Modified from aronma/ColabTurtle_2 github to allow arc on either side of turtle.
# Positive radius has circle to left of turtle moving counterclockwise.
# Negative radius has circle to right of turtle moving clockwise.
def _arctoNewPosition(r,new_pos):
    global turtle_pos
    global svg_lines_string
    global svg_fill_string
    
    sweep = 0 if r > 0 else 1  # SVG arc sweep flag
    rx = r*xscale
    ry = r*abs(yscale)
    
    start_pos = turtle_pos
    if is_pen_down:  
        svg_lines_string += \
        """<path d="M {x1} {y1} A {rx} {ry} 0 0 {s} {x2} {y2}" stroke-linecap="round" fill="transparent" fill-opacity="0" style="stroke:{pen_color};stroke-width:{pen_width}"/>""".format(
            x1=start_pos[0], 
            y1=start_pos[1],
            rx = rx,
            ry = ry,
            x2=new_pos[0],
            y2=new_pos[1],
            pen_color=pen_color,
            pen_width=pen_width,
            s=sweep)    
    if is_filling:
        svg_fill_string += """ A {rx} {ry} 0 0 {s} {x2} {y2} """.format(rx=r,ry=r,x2=new_pos[0],y2=new_pos[1],s=sweep)  
    turtle_pos = new_pos
     
# Helper function to draw a circular arc
# Modified from aronma/ColabTurtle_2 github repo
# Positive radius has arc to left of turtle, negative radius has arc to right of turtle.
def _arc(radius, degrees, draw):
    global turtle_degree
    global turtle_orient
    alpha = math.radians(turtle_degree)
    theta = math.radians(degrees)
    s = radius/abs(radius)  # 1=left, -1=right
    gamma = alpha-s*theta

    circle_center = (turtle_pos[0] + radius*xscale*math.sin(alpha), turtle_pos[1] - radius*abs(yscale)*math.cos(alpha))
    ending_point = (round(circle_center[0] - radius*xscale*math.sin(gamma),3) , round(circle_center[1] + radius*abs(yscale)*math.cos(gamma),3))
  
    _arctoNewPosition(radius,ending_point)
   
    turtle_degree = (turtle_degree - s*degrees) % 360
    turtle_orient = _turtleOrientation()
    if draw: _updateDrawing()
        
# Makes the turtle move forward by 'units' units
def forward(units):
    """Moves the turtle forward by the specified distance.

    Aliases: forward | fd

    Args:
        units: a number (integer or float)

    Moves the turtle forward by the specified distance, in the 
    direction the turtle is headed.
    """

    if not isinstance(units, (int,float)):
        raise ValueError('Units must be a number.')
    alpha = math.radians(turtle_degree)
    new_pos = (turtle_pos[0] + units * xscale * math.cos(alpha), turtle_pos[1] + units * abs(yscale) * math.sin(alpha))
    _moveToNewPosition(new_pos,units)
fd = forward # alias

# Makes the turtle move backward by 'units' units
def backward(units):
    """Moves the turtle backward by the specified distance.

    Aliases: backward | back | bk

    Args:
        units: a number (integer or float)

    Move the turtle backward by the specified distance, opposite
    to the direction the turtle is headed. Do not change the turtle's 
    heading.
    """

    if not isinstance(units, (int,float)):
        raise ValueError('Units must be a number.')
    forward(-1 * units)
bk = backward # alias
back = backward # alias

# Makes the turtle move right by 'angle' degrees or radians
# Uses SVG animation to rotate turtle.
# But this doesn't work for turtle=ring and if stretch factors are different for x and y directions,
# so in that case break the rotation into pieces of at most 30 degrees.
def right(angle):
    """Turns the turtle right by angle units.

    Aliases: right | rt

    Args:
        angle: a number (integer or float)

    Turns the turtle right by angle units. (Units are by default 
    degrees, but can be set via the degrees() and radians() functions.)
    Angle orientation depends on mode. 
    """

    global turtle_degree
    global turtle_orient
    global stretchfactor
    global timeout
    if not isinstance(angle, (int,float)):
        raise ValueError('Degrees must be a number.')  
    timeout_orig = timeout
    deg = angle*angle_conv
    if turtle_speed == 0 or not animate:
        turtle_degree = (turtle_degree + deg) % 360
        _updateDrawing()
    elif turtle_shape != 'ring' and stretchfactor[0]==stretchfactor[1]:
        stretchfactor_orig = stretchfactor
        template = shapeDict[turtle_shape]        
        tmp = """<animateTransform id = "one" attributeName="transform" 
                      type="scale"
                      from="1 1" to="{sx} {sy}"
                      begin="0s" dur="0.01s"
                      repeatCount="1"
                      additive="sum"
                      fill="freeze"
            /><animateTransform attributeName="transform"
                    type="rotate"
                    from="0 0 0" to ="{extent} 0 0"
                    begin="one.end" dur="{t}s"
                    repeatCount="1"
                    additive="sum"
                    fill="freeze"
          /></g>""".format(extent=deg, t=timeout*abs(deg)/90, sx=stretchfactor[0], sy=stretchfactor[1])
        newtemplate = template.replace("</g>",tmp)
        shapeDict.update({turtle_shape:newtemplate})
        stretchfactor = 1,1
        timeout = timeout*abs(deg)/90+0.001
        _updateDrawing()
        turtle_degree = (turtle_degree + deg) % 360
        turtle_orient = _turtleOrientation()
        shapeDict.update({turtle_shape:template})
        stretchfactor = stretchfactor_orig
        timeout = timeout_orig
    else: #turtle_shape == 'ring' or stretchfactor[0] != stretchfactor[1]
        turtle_degree_orig = turtle_degree
        timeout = timeout
        s = 1 if angle > 0 else -1
        while s*deg > 0:
            if s*deg > 30:
                turtle_degree = (turtle_degree + s*30) % 360
                turtle_orient = _turtleOrientation()
            else:
                turtle_degree = (turtle_degree + deg) % 360
                turtle_orient = _turtleOrientation()
            _updateDrawing()
            deg -= s*30
        timeout = timeout_orig
        turtle_degree = (turtle_degree + deg) % 360
        turtle_orient = _turtleOrientation()
rt = right # alias

# Makes the turtle move right by 'angle' degrees or radians
def left(angle):
    """Turns the turtle left by angle units.

    Aliases: left | lt

    Args:
        angle: a number (integer or float)

    Turns turtle left by angle units. (Units are by default 
    degrees, but can be set via the degrees() and radians() functions.)
    Angle orientation depends on mode. 
    """

    right(-1 * angle)
lt = left

# Move the turtle to a designated position.
def goto(x, y=None):
    """Moves turtle to an absolute position.

    Aliases: setpos | setposition | goto

    Args:
        x: a number     or      a pair of numbers
        y: a number     or      None

        goto(x, y)      or      goto((x,y))     

    Moves turtle to an absolute position. If the pen is down,
    a line will be drawn. The turtle's orientation does not change.   
    """

    global turtle_degree
    global tilt_angle
    if isinstance(x, tuple) and y is None:
        if len(x) != 2:
            raise ValueError('The tuple argument must be of length 2.')
        y = x[1]
        x = x[0]
    if not isinstance(x, (int,float)):
        raise ValueError('New x position must be a number.')
    if not isinstance(y, (int,float)):
        raise ValueError('New y position must be a number.')
    tilt_angle_orig = tilt_angle
    turtle_angle_orig = turtle_degree
    alpha = towards(x,y)*angle_conv
    units = distance(x,y)
    if _mode == "standard": 
        turtle_degree = (360 - alpha) % 360
        tilt_angle = -((turtle_angle_orig-tilt_angle+alpha) % 360)
    elif _mode == "logo":
        turtle_degree = (270 + alpha) % 360
        tilt_angle = turtle_angle_orig+tilt_angle-alpha-270
    elif _mode == "world":
        turtle_degree = (360 - alpha) % 360
    else: # mode = "svg"
        turtle_degree = alpha % 360
        tilt_angle = turtle_angle_orig+tilt_angle-alpha
    _moveToNewPosition((_convertx(x), _converty(y)),units)
    tilt_angle = tilt_angle_orig
    turtle_degree = turtle_angle_orig
setpos = goto # alias
setposition = goto # alias

# Move the turtle to a designated 'x' x-coordinate, y-coordinate stays the same
def setx(x):
    """Set the turtle's first coordinate to x

    Args:
        x: a number (integer or float)

    Set the turtle's first coordinate to x, leave second coordinate
    unchanged.
    """

    if not isinstance(x, (int,float)):
        raise ValueError('new x position must be a number.')
    goto(x, gety())

# Move the turtle to a designated 'y' y-coordinate, x-coordinate stays the same
def sety(y):
    """Set the turtle's second coordinate to y

    Args:
        y: a number (integer or float)

    Set the turtle's second coordinate to y, leave first coordinate
    unchanged.
    """

    if not isinstance(y, (int,float)):
        raise ValueError('New y position must be a number.')
    goto(getx(), y)

# Makes the turtle face a given direction
def setheading(angle):
    """Set the orientation of the turtle to angle

    Aliases: setheading | seth

    Args:
        angle: a number (integer or float) 
    
    Units are by default degrees, but can be set via 
    the degrees() and radians() functions.

    Set the orientation of the turtle to angle.
    This depends on the mode.
    """

    global turtle_degree
    global turtle_orient
    deg = angle*angle_conv
    if not isinstance(angle, (int,float)):
        raise ValueError('Degrees must be a number.')
    if _mode in ["standard","world"]: 
        new_degree = (360 - deg) 
    elif _mode == "logo":
        new_degree = (270 + deg) 
    else: # mode = "svg"
        new_degree = deg % 360
    alpha = (new_degree - turtle_degree) % 360
    if turtle_speed !=0 and animate:
        if alpha <= 180:
            if angle_mode == "degrees":
                right(alpha)
            else:
                right(math.radians(alpha))
        else:
            if angle_mode == "degrees":
                left(360-alpha)
            else:
                left(math.radians(360-alpha))
    else:
        turtle_degree = new_degree
        turtle_orient = _turtleOrientation()
        _updateDrawing()
seth = setheading # alias
face = setheading # alias

# Move turtle to the origin and set its heading to its 
# start-orientation (which depends on the mode).
def home():
    """Moves the turtle to the origin - coordinates (0,0).

    No arguments.

    Moves the turtle to the origin (0,0) and sets its
    heading to its start-orientation (which depends on mode).
    
    If the mode is "svg", moves the turtle to the center of 
    the drawing window.)
    """

    global turtle_degree
    if _mode != 'svg':
        goto(0,0)
    else:
        goto( (window_size[0] / 2, window_size[1] / 2) )
    #turtle_degree is always in degrees, but angle mode might be radians
    #divide by angle_conv so angle sent to left or right is in the correct mode
    if _mode in ['standard','world']:
        if turtle_degree <= 180:
            left(turtle_degree/angle_conv)
        else:
            right((360-turtle_degree)/angle_conv)
        turtle_orient = _turtleOrientation()
        _updateDrawing(0)
    else:
        if turtle_degree < 90:
            left((turtle_degree+90)/angle_conv)
        elif turtle_degree< 270:
            right((270-turtle_degree)/angle_conv)
        else:
            left((turtle_degree-270)/angle_conv)
    

# Since SVG has some ambiguity when using an arc path for a complete circle,
# the circle function is broken into chunks of at most 90 degrees.
# This is modified from aronma/ColabTurtle_2 github.
# Positive radius has circle to left of turtle, negative radius has circle to right of turtle.
# The step argument is here only for backward compatability with classic turtle.py circle.
# To get a true circular arc, do NOT use steps. Can still be used to draw a regular polygon, but better
# to use the regularpolygon() function.
def circle(radius, extent=None, steps=None):
    """ Draws a circle with the given radius.

    Args:
        radius: a number
        extent: (optional) a number
        steps: (optional) a positive integer
    
    Draws a circle with given radius. The center is radius units left
    of the turtle. The extent, an angle, determines which part of the
    circle is drawn. If extent is not given, draws the entire circle.
    If extent is not a full circle, one endpoint of the arc is the
    current pen position. Draws the arc in counterclockwise direction
    if radius is positive, otherwise in clockwise direction. Finally
    the direction of the turtle is changed by the amount of extent.
    
    The step argument is here only for backward compatability with 
    classic turtle.py circle. To get a true circular arc, do NOT use
    steps since the circle will be drawn using SVG commands.
    If steps > 20, it will be assumed that an arc of a circle was
    intended. 
    
    This function can still be used to draw a regular polygon with 
    20 or fewer sides, but it is better to use the regularpolygon() 
    function. 
    """

    global timeout
    global svg_lines_string
    global svg_fill_string
    global turtle_degree
    global turtle_pos
    if not isinstance(radius, (int,float)):
        raise ValueError('Circle radius should be a number')
    if extent is None:
        extent = 360 if angle_mode == "degrees" else 2*math.pi 
    elif not isinstance(extent, (int,float)):
        raise ValueError('Extent should be a number')      
    elif extent < 0:
        raise ValueError('Extent should be a positive number')
    # If steps is used, only draw polygon if less than 20 sides.
    # Otherwise, assume user really wants a circular arc.
    if (steps is not None) and (steps <= 20):
        alpha = 1.0*extent/steps
        length = 2*radius*math.sin(alpha/2*math.pi/180)
        if radius < 0: 
            alpha = -alpha
            length = -radius
        left(alpha/2)
        for _ in range(steps-1):
            forward(length)
            left(alpha)
        forward(length)
        left(alpha/2)  
    elif turtle_speed != 0 and animate:
        timeout_temp = timeout 
        timeout = timeout*0.5
        degrees = extent*angle_conv
        extent = degrees
        # Use temporary svg strings for animation
        svg_lines_string_temp = svg_lines_string
        svg_fill_string_temp = svg_fill_string 
        turtle_degree_orig = turtle_degree
        turtle_pos_orig = turtle_pos        
        while extent > 0:
            _arc(radius,min(15,extent),True)
            extent -= 15 
        # return to original position and redo circle for svg strings without animation
        svg_lines_string = svg_lines_string_temp
        svg_fill_string = svg_fill_string_temp
        turtle_degree = turtle_degree_orig
        turtle_pos = turtle_pos_orig
        while degrees > 0:
            _arc(radius,min(180,degrees),False)
            degrees -= 180 
        timeout = timeout_temp
    else:  # no animation
        extent = extent*angle_conv
        while extent > 0:
            _arc(radius,min(180,extent),True)
            extent -= 180         

# Draw a dot with diameter size, using color
# If size is not given, the maximum of pen_width+4 and 2*pen_width is used.
def dot(size = None, *color):
    """Draws a dot with diameter size, using color.

    Args:
        size: (optional) a positive integer
        *color: (optional) a colorstring or a numeric color tuple

    Draw a circular dot with diameter size, using color.
    If size is not given, the maximum of pensize+4 and 2*pensize 
    is used. If no color is given, the pencolor is used.
    """

    global svg_dots_string

    if not color:
        if isinstance(size, (str, tuple)):
            color = _processColor(size)
            size = pen_width + max(pen_width,4)
        else:
            color = pen_color
            if not size:
                size = pen_width + max(pen_width,4)
    else:
        if size is None:
            size = pen_width + max(pen_width,4)
        color = _processColor(color[0])
    svg_dots_string += """<circle cx="{cx}" cy="{cy}" r="{radius}" fill="{kolor}" fill-opacity="1" />""".format(
            radius=size/2,
            cx=turtle_pos[0],
            cy=turtle_pos[1],
            kolor=color)
    _updateDrawing()
        
# Stamp a copy of the turtle shape onto the canvas at the current turtle position.
# The argument determines whether the stamp appears below other items (layer=0) or above other items (layer=1) in 
# the order that SVG draws items. So if layer=0, a stamp may be covered by a filled object, for example, even if
# the stamp is originally drawn on top of the object during the animation. To prevent this, set layer=1 (or any nonzero number).
# Returns a stamp_id for that stamp, which can be used to delete it by calling clearstamp(stamp_id).
def stamp(layer=0):
    """Stamps a copy of the turtleshape onto the canvas and return its id.

    Args:
        layer (int): an optional integer that determines whether the stamp 
            appears below other items (layer=0) or above other items (layer=1) 
            in the order that SVG draws items. 
    
    Returns: 
        integer: a stamp_id for that stamp, which can be
            used to delete it by calling clearstamp(stamp_id).

    Stamps a copy of the turtle shape onto the canvas at the current
    turtle position.
    
    If layer=0, a stamp may be covered by a filled object, for example, 
    even if the stamp is originally drawn on top of that object during 
    the animation. To prevent this, set layer=1 or any nonzero number.
    """

    global svg_stampsB_string
    global svg_stampsT_string
    global stampnum
    global stamplist
    stampnum += 1
    stamplist.append(stampnum)
    if layer != 0:

        stampdictT[stampnum] = _generateTurtleSvgDrawing()
        svg_stampsT_string += stampdictT[stampnum]
    else:
        stampdictB[stampnum] = _generateTurtleSvgDrawing()
        svg_stampsB_string += stampdictB[stampnum]
    _updateDrawing(0)
    return stampnum

# Helper function to do the work for clearstamp() and clearstamps()
def _clearstamp(stampid):
    global stampdictB
    global stampdictT
    global svg_stampsB_string
    global svg_stampsT_string  
    global stamplist
    tmp = ""
    if stampid in stampdictB.keys():
        stampdictB.pop(stampid)
        stamplist.remove(stampid)
        for n in stampdictB:
            tmp += stampdictB[n]
        svg_stampsB_string = tmp        
    elif stampid in stampdictT.keys():
        stampdictT.pop(stampid)
        stamplist.remove(stampid)
        for n in stampdictT:
            tmp += stampdictT[n]
        svg_stampsT_string = tmp
    _updateDrawing(0)

# Delete stamp with given stampid.
# stampid – an integer or tuple of integers, which must be return values of previous stamp() calls
def clearstamp(stampid):
    """Deletes the stamp with given stampid

    Args:
        stampid - an integer, must be return value of previous stamp() call.
    """

    if isinstance(stampid,tuple):
        for subitem in stampid:
            _clearstamp(subitem)
    else:
        _clearstamp(stampid)

# Delete all or first/last n of turtle’s stamps. If n is None, delete all stamps, if n > 0 delete first n stamps,
# else if n < 0 delete last n stamps.
def clearstamps(n=None):
    """Deletes all or first/last n of turtle's stamps.

    Args:
        n: an optional integer

    If n is None, deletes all of the turtle's stamps.
    If n > 0, deletes the first n stamps.
    If n < 0, deletes the last n stamps.
    """

    if n is None:
        [_clearstamp(k) for k in stamplist]
    elif n > 0:
        [_clearstamp(k) for k in stamplist[:n]]
    elif n < 0:
        [_clearstamp(k) for k in stamplist[n:]]
        
# Update the speed of the moves, [0,13]
# If argument is omitted, it returns the speed.
def speed(speed = None):
    """Returns or set the turtle's speed.

    Args:
        speed: an integer in the range 0..13 or a speedstring (see below)

    Sets the turtle's speed to an integer value in the range 0 .. 13.
    If no argument is given, returns the current speed.

    If input is a number greater than 13 or smaller than 0.5,
    speed is set to 13.
    
    Speedstrings  are mapped to speedvalues in the following way:
        'fastest' :  13
        'fast'    :  10
        'normal'  :  6
        'slow'    :  3
        'slowest' :  1
    Speeds from 1 to 13 enforce increasingly faster animation of
    line drawing and turtle turning.

    Attention:
    speed = 0 displays final image with no animation. Need to call done() 
    at the end so the final image is displayed.
    
    Calling animationOff will show the drawing but with no animation.
    This means forward/back makes the turtle jump and likewise left/right 
    makes the turtle turn instantly.
    """

    global timeout
    global turtle_speed    
    if speed is None:
        return turtle_speed
    speeds = {'fastest':13, 'fast':10, 'normal':5, 'slow':3, 'slowest':1}
    if speed in speeds:
        turtle_speed = speeds[speed]
    elif not isinstance(speed,(int,float)):
        raise ValueError("speed should be a number between 0 and 13")
    turtle_speed = speed
    if 0.5 < speed < 13.5:
        turtle_speed = int(round(speed))
    elif speed != 0:
        turtle_speed = 13
    timeout = _speedToSec(turtle_speed) 

# jump to a point without drawing or animation
def jumpto(x,y=None):
    """Jumps to a specified point without drawing/animation
    
    Args:
        x: a number     or      a pair of numbers
        y: a number     or      None

        jumpto(x, y)      or    jumpto((x,y))  
    """
    global animate
    animate_temp = animate
    penup()
    animationOff()
    goto(x,y)
    animate = animate_temp
    pendown()

# Call this function at end of turtle commands when speed=0 (no animation) so that final image is drawn
def done():
    """Shows the final image when speed=0
    
    No argument
    
    speed = 0 displays final image with no animation. Need to
    call done() at the end so the final image is displayed.
    """
    if drawing_window == None:
        raise AttributeError("Display has not been initialized yet. Call initializeTurtle() before using.")
    drawing_window.update(HTML(_generateSvgDrawing()))   
update = done #alias

# Draw a line from diego2500garza
def drawline(x_1,y_1,x_2=None,y_2=None):
    """Draws a line between two points
    
    Args:
        x_1,y_1 : two numbers           or      a pair of numbers
        x_2,y_2 : two numbers                   a pair of numbers
        
        drawline(x_1,y_1,x_2,y_2)               drawline((x_1,y_1),(x_2,y_2))       
    
    Draws a line from (x_1,y_1) to (x_2,y_2). This line is 
    independent of the turtle motion.
    """

    global svg_lines_string
    if isinstance(x_1,tuple) and isinstance(y_1,tuple) and x_2==None and y_2==None:
        if len(x_1) != 2 or len(y_1) != 2:
            raise ValueError('The tuple argument must be of length 2.')
        x_1,y = x_1
        x_2,y_2 = y_1
        y_1 = y
    svg_lines_string += """<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke-lineca="round" style="stroke:{pencolor};stroke-width:{penwidth}" />""".format(
        x1=_convertx(x_1),
        y1=_converty(y_1),
        x2=_convertx(x_2),
        y2=_converty(y_2),
        pencolor = pen_color,
        penwidth = pen_width)
    _updateDrawing(0)   
line = drawline #alias
        
# Move along a regular polygon of size sides, with length being the length of each side. The steps indicates how many sides are drawn.
# The initial and concluding angle is half of the exteral angle.
# A positive length draws the polygon to the left of the turtle's current direction and a negative length draws it to the right
# of the turtle's current direction.
# Sets fillcolor to "none" if necessary and turns on filling so that the polygon is coded as one path for SVG purposes rather than
# as a sequence of line segments.
def regularPolygon(sides, length, steps=None):
    """Draws a regular polygon 
    
    Args:
        sides: an integer giving the number of sides of the polygon, or
            a string with the name of a regular polygon of at most 10 sides
        length: a number giving the length of each side
        steps: an optional integer indicating how many sides of the
            polygon to draw
    
    Moves the turtle along a regular polygon of size sides, with length being 
    the length of each side. The steps indicates how many sides are drawn.
    
    The initial and concluding angle is half of the exterior angle.
   
    Positive values for sides or length draws the polygon to the 
    left of the turtle's current direction, and a negative value for
    either sides or length draws it to the right of the turtle's current 
    direction.
    """

    global fill_color
    polygons = {"triangle":3, "square":4, "pentagon":5, "hexagon":6, "heptagon":7, "octagon":8, "nonagon":9, "decagon":10}
    if sides in polygons:
        sides = polygons[sides]
    if steps is None:
        steps = abs(sides)   
    if not isinstance(sides, int):
        raise ValueError('The number of sides should be an integer.')
    elif not isinstance(steps, int):
        raise ValueError('The number of steps should be a positive integer.')
    elif steps < 1:
        raise ValueError('The number of steps should be a positive integer.')
    polyfilling = False
    if not is_filling:
        polyfilling = True
        fillcolor_temp = fill_color
        begin_fill()
    alpha = (360/angle_conv)/sides
    print(alpha)
    if length < 0: 
        alpha = -alpha
        length = -length
    left(alpha/2)
    for _ in range(steps-1):
        forward(length)
        left(alpha)
    forward(length)
    left(alpha/2)
    if polyfilling: 
        fill_color = "none"
        end_fill()       
        fill_color = fillcolor_temp
        _updateDrawing()
    
#====================================
# Turtle Motion - Tell Turtle's State
#====================================

# Retrieve the turtle's current position as a (x,y) tuple vector in current coordinate system
def position():
    """Returns the turtle's current location (x,y)

    Aliases: pos | position

    Returns:
        tuple: the current turtle location (x,y)
    """

    return (turtle_pos[0]/xscale+xmin, ymax-turtle_pos[1]/yscale)
pos = position # alias

# Return the angle between the line from turtle position to position specified by (x,y)
# This depends on the turtle’s start orientation which depends on the mode - standard/world or logo.  
def towards(x, y=None):
    """Returns the angle of the line from the turtle's position to (x, y).

    Args:
        x: a number     or      a pair of numbers
        y: a number     or      None             
 
    distance(x, y)      or      distance((x, y))

    Returns:
        The angle between the line from turtle-position to position
            specified by x,y and the turtle's start orientation. 
            (Depends on modes - "standard" or "logo" or "svg")
    """

    if isinstance(x, tuple) and y is None:
        if len(x) != 2:
            raise ValueError('The tuple argument must be of length 2.')
        y = x[1]
        x = x[0]     
    if not isinstance(x, (int,float)):
        raise ValueError('The x position must be a number.')
    if not isinstance(y, (int,float)):
        raise ValueError('The y position must be a number.')   
    dx = x - getx()
    dy = y - gety()
    if _mode == "svg":
        dy = -dy
    result = round(math.atan2(dy,dx)*180.0/math.pi, 10) % 360.0
    if _mode in ["standard","world"]:
        angle = result
    elif _mode == "logo":
        angle = (90 - result) % 360
    else:  # mode = "svg"
        angle = (360 - result) % 360
    if angle_mode == "degrees":
        return round(angle,7)
    else:
        return round(math.radians(angle),7)

# Retrieve the turtle's currrent 'x' x-coordinate in current coordinate system
def xcor():
    """Returns the turtle's x coordinate."""

    return(turtle_pos[0]/xscale+xmin)
getx = xcor # alias

# Retrieve the turtle's currrent 'y' y-coordinate in current coordinate system
def ycor():
    """Return the turtle's y coordinate."""
   
    return(ymax-turtle_pos[1]/yscale)
gety = ycor # alias

# Retrieve the turtle's current angle in current angle_mode
def heading():
    """Returns the turtle's current heading"""

    if _mode in ["standard","world"]:
        angle = (360 - turtle_degree) % 360
    elif _mode == "logo":
        angle = (turtle_degree - 270) % 360
    else: # mode = "svg"
        angle = turtle_degree % 360
    if angle_mode == "degrees":
        return angle
    else:
        return math.radians(angle)
getheading = heading # alias
 
# Calculate the distance between the turtle and a given point
def distance(x, y=None):
    """Return the distance from the turtle to (x,y) in turtle step units.

    Args:
        x: a number     or      a pair of numbers  
        y: a number     or      None      

    distance(x, y)      or      distance((x, y))
    """

    if isinstance(x, tuple) and y is None:
        if len(x) != 2:
            raise ValueError('The tuple argument must be of length 2.')
        y = x[1]
        x = x[0]
    if not isinstance(x, (int,float)):
        raise ValueError('The x position must be a number.')
    if not isinstance(y, (int,float)):
        raise ValueError('The y position must be a number.')    
    return round(math.sqrt( (getx() - x) ** 2 + (gety() - y) ** 2 ), 8)        

#========================================
# Turtle Motion - Setting and Measurement
#========================================

# Set the angle measurement units to radians.
def radians():
    """ Sets the angle measurement units to radians."""

    global angle_conv
    global angle_mode
    angle_mode = 'radians'
    angle_conv = 180/math.pi

# Set the angle measurement units to degrees.
def degrees():
    """ Sets the angle measurement units to radians."""

    global angle_conv
    global angle_mode
    angle_mode = 'degrees'
    angle_conv = 1

#============================
# Pen Control - Drawing State
#============================

# Lowers the pen such that following turtle moves will now cause drawings
def pendown():
    """Pulls the pen down -- drawing when moving.

    Aliases: pendown | pd | down
    """

    global is_pen_down
    is_pen_down = True
pd = pendown # alias
down = pendown # alias

# Raises the pen such that following turtle moves will not cause any drawings
def penup():
    """Pulls the pen up -- no drawing when moving.

    Aliases: penup | pu | up
    """

    global is_pen_down
    is_pen_down = False
pu = penup # alias
up = penup # alias

# Change the width of the lines drawn by the turtle, in pixels
# If the function is called without arguments, it returns the current width
def pensize(width = None):
    """Sets or returns the line thickness.

    Aliases:  pensize | width

    Args:
        width: positive number

    Set the line thickness to width or return it. If no argument is given,
    current pensize is returned.
    """

    global pen_width
    if width is None:
        return pen_width
    else:
        if not isinstance(width, (int,float)):
            raise ValueError('New width value must be an integer.')
        if not width > 0:
            raise ValueError('New width value must be positive.')
        pen_width = width
    _updateDrawing(0)
width = pensize  #alias

# Return or set the pen's attributes
def pen(dictname=None, **pendict):
    """Returns or set the pen's attributes.

    Args:
        pen: a dictionary with some or all of the below listed keys.
        **pendict: one or more keyword-arguments with the below
            listed keys as keywords.

    Returns or sets the pen's attributes in a 'pen-dictionary'
    with the following key/value pairs:
           "shown"         :   True/False
           "pendown"       :   True/False
           "pencolor"      :   color-string or color-tuple
           "fillcolor"     :   color-string or color-tuple
           "pensize"       :   positive number
           "speed"         :   number in range 0..13
           "stretchfactor" :   (positive number, positive number)
           "shearfactor"   :   number
           "outline"       :   positive number
           "tilt"          :   number

    This dictionary can be used as argument for a subsequent
    pen()-call to restore the former pen-state. Moreover one
    or more of these attributes can be provided as keyword-arguments.
    This can be used to set several pen attributes in one statement.
    """

    global is_turtle_visible
    global is_pen_down
    global pen_color
    global fill_color
    global pen_width
    global turtle_speed
    global stretchfactor
    global shear_factor
    global outline_width
    global tilt_angle
    global timeout
    _pd = {"shown"          : is_turtle_visible,
           "pendown"        : is_pen_down,
           "pencolor"       : pen_color,
           "fillcolor"      : fill_color,
           "pensize"        : pen_width,
           "speed"          : turtle_speed,
           "stretchfactor"  : stretchfactor,
           "shearfactor"    : shear_factor,
           "tilt"           : tilt_angle,
           "outline"        : outline_width
          }
    if not (dictname or pendict):
        sf_tmp = shear_factor
        _pd["shearfactor"] = round(math.tan((360-shear_factor)*math.pi/180),8)
        return _pd
        _pd["shearfactor"] = sf_tmp
    if isinstance(dictname,dict):
        p = dictname
    else:
        p = {}

    p.update(pendict)
    if "shown" in p:
        is_turtle_visible = p["shown"]
    if "pendown" in p:
        is_pen_down = p["pendown"]
    if "pencolor" in p:
        pen_color = _processColor(p["pencolor"])
    if "fillcolor" in p:
        fill_color = _processColor(p["fillcolor"])
    if "pensize" in p:
        pen_width = p["pensize"]
    if "speed" in p:
        turtle_speed = p["speed"]
        timeout = _speedToSec(turtle_speed)
    if "stretchfactor" in p:
        sf = p["stretchfactor"]
        if isinstance(sf, (int,float)):
            sf = (sf,sf)
        stretchfactor = sf
    if "shearfactor" in p:
        alpha = math.atan(p["shearfactor"])*180/math.pi
        shear_factor = (360 - alpha) % 360
        p["shearfactor"] = shear_factor
    if "tilt" in p:
        tilt_angle = p["tilt"]*angle_conv
    if "outline" in p:
        outline_width = p["outline"]
    _updateDrawing(0)

def isdown():
    """Return True if pen is down, False if it's up."""

    return is_pen_down

#============================
# Pen Control - Color Control
#============================
        
# Return or set pencolor and fillcolor
def color(*args):
    """Returns or sets the pencolor and fillcolor.

    Args:
        Several input formats are allowed.
        They use 0, 1, 2, or 3 arguments as follows:

        color()
            Return the current pencolor and the current fillcolor
            as a pair of color specification strings as are returned
            by pencolor and fillcolor.
        color(colorstring), color((r,g,b)), color(r,g,b)
            inputs as in pencolor, set both, fillcolor and pencolor,
            to the given value.
        color(colorstring1, colorstring2),
        color((r1,g1,b1), (r2,g2,b2))
            equivalent to pencolor(colorstring1) and fillcolor(colorstring2)
            and analogously, if the other input format is used.
    """

    global pen_color
    global fill_color
    if args:
        narg = len(args)
        if narg == 1:
            pen_color = fill_color = _processColor(args[0])
        elif narg == 2:
            pen_color = _processColor(args[0])
            fill_color = _processColor(args[1])
        elif narg == 3:
            kolor = (args[0],args[1],args[2])
            pen_color = fill_color = _processColor(kolor)
        else:
            raise ValueError('Syntax: color(colorstring), color((r,g,b)), color(r,g,b), color(string1,string2), color((r1,g1,b1),(r2,g2,b2))')
    else:
        return pen_color,fill_color
    _updateDrawing(0)        
        
# Change the color of the pen
# If no params, return the current pen color
def pencolor(color = None, c2 = None, c3 = None):
    """Returns or sets the pencolor.

    Args:
    Four input formats are allowed:
        
    pencolor():
        Return the current pencolor as color specification string,
        possibly in hex-number format. May be used as input to another 
        color/pencolor/fillcolor call.
            
    pencolor(colorstring):
        Colorstring is an htmlcolor specification string, such as "red"
        or "yellow".
            
    pencolor((r, g, b)):
        A tuple of r, g, and b, which represent an RGB color,
        and each of r, g, and b are in the range 0..255.
            
    pencolor(r, g, b):
        r, g, and b represent an RGB color, and each of r, g, and b
        are in the range 0..255
    """

    global pen_color
    if color is None:
        return pen_color
    elif c2 is not None:
        if c3 is None:
            raise ValueError('If the second argument is set, the third arguments must be set as well to complete the rgb set.')
        color = (color, c2, c3)

    pen_color = _processColor(color)
    _updateDrawing(0)

# Change the fill color
# If no params, return the current fill color
def fillcolor(color = None, c2 = None, c3 = None):
    """ Returns or sets the fillcolor.

    Args:
    Four input formats are allowed:
        
    pencolor():
        Return the current pencolor as color specification string,
        possibly in hex-number format. May be used as input to another 
        color/pencolor/fillcolor call.
            
    pencolor(colorstring):
        Colorstring is an htmlcolor specification string, such as "red"
        or "yellow".
            
    pencolor((r, g, b)):
        A tuple of r, g, and b, which represent an RGB color,
        and each of r, g, and b are in the range 0..255.
            
    pencolor(r, g, b):
        r, g, and b represent an RGB color, and each of r, g, and b
        are in the range 0..255.
    
    The interior of the turtle is drawn with the newly set fillcolor.
    """

    global fill_color
    if color is None:
        return fill_color
    elif c2 is not None:
        if c3 is None:
            raise ValueError('If the second argument is set, the third arguments must be set as well to complete the rgb set.')
        color = (color, c2, c3)

    fill_color = _processColor(color)
    _updateDrawing(0)

# Used to validate a color string
def _validateColorString(color):
    if color in VALID_COLORS: # 140 predefined html color names
        return True
    if re.search("^#(?:[0-9a-fA-F]{3}){1,2}$", color): # 3 or 6 digit hex color code
        return True
    if re.search("rgb\(\s*(?:(?:\d{1,2}|1\d\d|2(?:[0-4]\d|5[0-5]))\s*,?){3}\)$", color): # rgb color code
        return True
    return False

# Used to validate if a 3 tuple of integers is a valid RGB color
def _validateColorTuple(color):
    if len(color) != 3:
        return False
    if not isinstance(color[0], int) or not isinstance(color[1], int) or not isinstance(color[2], int):
        return False
    if not 0 <= color[0] <= 255 or not 0 <= color[1] <= 255 or not 0 <= color[2] <= 255:
        return False
    return True

# Helps validate color input to functions
def _processColor(color):
    if isinstance(color, str):    
        if color == "": color = "none"
        color = color.lower().strip()
        if 'rgb' not in color: color = color.replace(" ","")
        if not _validateColorString(color):
            err = 'Color ' + color + ' is invalid. It can be a known html color name, 3-6 digit hex string, or rgb string.'
            raise ValueError(err)
        return color
    elif isinstance(color, tuple):
        if not _validateColorTuple(color):
            err = 'Color tuple ' + color + ' is invalid. It must be a tuple of three integers, which are in the interval [0,255]'
            raise ValueError(err)
        return 'rgb(' + str(color[0]) + ',' + str(color[1]) + ',' + str(color[2]) + ')'
    else:
        err = 'The color parameter ' + color + ' must be a color string or a tuple'
        raise ValueError(err)

# Get the color corresponding to position n in the valid color list
def getcolor(n):
    """ Returns the color string in the valid color list at position n
    
    Args:
        n: an integer between 0 and 139
    
    Returns:
        str: color string in the valid color list at position n
    """

    if not isinstance(n,(int,float)):
        raise valueError("color index must be an integer between 0 and 139")
    n = int(round(n))
    if (n < 0) or (n > 139):
        raise valueError("color index must be an integer between 0 and 139")
    return VALID_COLORS[n]


#=======================
# Pen Control - Filling
#=======================

# Return fillstate (True if filling, False else)
def filling():
    """Return fillstate (True if filling, False else)."""

    global is_filling
    return is_filling

# Initialize the string for the svg path of the filled shape.
# Modified from aronma/ColabTurtle_2 github repo
# When calling begin_fill, a value for the fill_rule can be given that will apply only to that fill.
def begin_fill(rule=None, opacity=None):
    """Called just before drawing a shape to be filled.

    Args:
        rule: (optional) either evenodd or nonzero
        opacity: (optional) a number between 0 and 1
    
    Because the fill is controlled by svg rules, the result may differ
    from classic turtle fill. The fill-rule and fill-opacity can be set 
    as arguments to the begin_fill() function and will apply only to objects 
    filled before the end_fill is called. There are two possible arguments
    to specify for the SVG fill-rule: 'nonzero' (default) and 'evenodd'. 
    The fill-opacity attribute ranges from 0 (transparent) to 1 (solid). 
    """

    global is_filling
    global svg_fill_string
    if rule is None:
         rule = fill_rule
    if opacity is None:
         opacity = fill_opacity
    rule = rule.lower()
    if not rule in ['evenodd','nonzero']:
        raise ValueError("The fill-rule must be 'nonzero' or 'evenodd'.")
    if (opacity < 0) or (opacity > 1):
        raise ValueError("The fill_opacity should be between 0 and 1.")
    if not is_filling:
        svg_fill_string = """<path fill-rule="{rule}" fill-opacity="{opacity}" d="M {x1} {y1} """.format(
                x1=turtle_pos[0],
                y1=turtle_pos[1],
                rule=rule,
                opacity = opacity)
        is_filling = True
    
# Terminate the string for the svg path of the filled shape
# Modified from aronma/ColabTurtle_2 github repo
def end_fill():
    """Fill the shape drawn after the call begin_fill()."""

    global is_filling   
    global svg_lines_string
    global svg_fill_string
    if is_filling:
        is_filling = False
        svg_fill_string += """" stroke-linecap="round" style="stroke-width=0" fill="{fillcolor}" />""".format(
                fillcolor=fill_color)
        svg_lines_string = svg_fill_string + svg_lines_string
        _updateDrawing(0)
     
# Allow user to set the svg fill-rule. Options are only 'nonzero' or 'evenodd'. If no argument, return current fill-rule.
# This can be overridden for an individual object by setting the fill-rule as an argument to begin_fill().
def fillrule(rule=None):
    """Allows user to set the global svg fill-rule.

    Args:
        rule: (optional) Either evenodd or nonzero
            Default is current fill-rule
    """

    global fill_rule
    if rule is None:
        return fill_rule
    if not isinstance(rule,str):
        raise ValueError("The fill-rule must be 'nonzero' or 'evenodd'.")   
    rule = rule.lower()
    if not rule in ['evenodd','nonzero']:
        raise ValueError("The fill-rule must be 'nonzero' or 'evenodd'.")   
    fill_rule = rule

# Allow user to set the svg fill-opacity. If no argument, return current fill-opacity.
# This can be overridden for an individual object by setting the fill-opacity as an argument to begin_fill().
def fillopacity(opacity=None):
    """Allows user to set the global svg fill-opacity.

    Args:
        opacity: (optional) a number between 0 and 1
            Default is current fill-opacity
    """

    global fill_opacity
    if opacity is None:
        return fill_opacity
    if not isinstance(opacity,(int,float)):
        raise ValueError("The fill-opacity must be a number between 0 and 1.")
    if (opacity < 0) or (opacity > 1):
        raise ValueError("The fill_opacity should be between 0 and 1.")
    fill_opacity = opacity

#===================================
# Pen Control - More Drawing Control
#=================================== 

# Delete the turtle’s drawings from the screen, re-center the turtle and set (most) variables to the default values.
def reset():
    """Resets the turtle to its initial state and clears drawing."""

    global is_turtle_visible
    global pen_color
    global is_pen_down
    global pen_width
    global svg_lines_string
    global svg_fill_string
    global svg_dots_string
    global turtle_degree 
    global turtle_orient
    global turtle_pos
    global fill_color
    global border_color
    global stretchfactor
    global shear_factor
    global tilt_angle
    global outline_width

    if drawing_window == None:
        raise AttributeError("Display has not been initialized yet. Call initializeTurtle() before using.")
    is_turtle_visible = True
    pen_color = DEFAULT_PEN_COLOR
    fill_color = DEFAULT_FILL_COLOR
    is_pen_down = True
    pen_width = DEFAULT_PEN_WIDTH
    stretchfactor = DEFAULT_STRETCHFACTOR
    shear_factor = DEFAULT_SHEARFACTOR
    tilt_angle = DEFAULT_TILT_ANGLE
    outline_width = DEFAULT_OUTLINE_WIDTH
    svg_lines_string = ""
    svg_fill_string = ""
    svg_dots_string = ""
    svg_stampsB_string = ""
    svg_stampsT_string = ""
    stampdictB = {}
    stampdictT = {}
    stampnum = 0
    stamplist = []
    turtle_degree = DEFAULT_TURTLE_DEGREE if (_mode in ["standard","world"]) else (270 - DEFAULT_TURTLE_DEGREE)
    turtle_orient = turtle_degree
    if _mode != "world":
        turtle_pos = (window_size[0] / 2, window_size[1] / 2)
    else:
        turtle_pos = (_convertx(0),_converty(0))
    #_updateDrawing(0)
    

# Clear any text or drawing on the screen
def clear():
    """Clears any text or drawing on the screen."""
    
    global svg_lines_string
    global svg_fill_string
    global svg_dots_string

    svg_lines_string = ""
    svg_fill_string = ""
    svg_dots_string = ""
    _updateDrawing(0)

def write(obj, **kwargs):
    """Write text at the current turtle position.

    Args:
        obj: string which is to be written to the TurtleScreen
        **kwargs:
            align: (optional) one of the strings "left", "center" or right"
            font: (optional) a triple (fontsize, fontname, fonttype)

    Write the string text at the current turtle position according 
    to align ("left", "center" or right") and with the given font.
    
    Defaults are left, ('Arial', 12, 'normal')
    """

    global svg_lines_string
    global turtle_pos
    text = str(obj)
    font_size = 12
    font_family = 'Arial'
    font_type = 'normal'
    align = 'start'

    if 'align' in kwargs and kwargs['align'] in ('left', 'center', 'right'):
        if kwargs['align'] == 'left':
            align = 'start'
        elif kwargs['align'] == 'center':
            align = 'middle'
        else:
            align = 'end'

    if "font" in kwargs:
        font = kwargs["font"]
        if len(font) != 3 or isinstance(font[0], int) == False \
                          or isinstance(font[1], str) == False \
                          or font[2] not in {'bold','italic','underline','normal'}:
            raise ValueError('Font parameter must be a triplet consisting of font size (int), font family (str), and font type (str). Font type can be one of {bold, italic, underline, normal}')
        font_size = font[0]
        font_family = font[1]
        font_type = font[2]
        
    style_string = ""
    style_string += "font-size:" + str(font_size) + "px;"
    style_string += "font-family:'" + font_family + "';"

    if font_type == 'bold':
        style_string += "font-weight:bold;"
    elif font_type == 'italic':
        style_string += "font-style:italic;"
    elif font_type == 'underline':
        style_string += "text-decoration: underline;"
            
    svg_lines_string += """<text x="{x}" y="{y}" fill="{fill_color}" text-anchor="{align}" style="{style}">{text}</text>""".format(
            x=turtle_pos[0], 
            y=turtle_pos[1], 
            text=text, 
            fill_color=pen_color, 
            align=align, 
            style=style_string)
    
    _updateDrawing()

# Set the defaults used in the original version of ColabTurtle package
def oldDefaults():
    """Set the defaults used in the original version of ColabTurtle package."""

    global DEFAULT_BACKGROUND_COLOR
    global DEFAULT_PEN_COLOR
    global DEFAULT_PEN_WIDTH
    global DEFAULT_MODE
    global DEFAULT_TURTLE_SHAPE
    global DEFAULT_WINDOW_SIZE
    global DEFAULT_TURTLE_DEGREE
    global DEFAULT_SPEED
    
    DEFAULT_BACKGROUND_COLOR = "black"
    DEFAULT_PEN_COLOR = "white"
    DEFAULT_PEN_WIDTH = 4
    DEFAULT_MODE = 'svg'
    DEFAULT_TURTLE_SHAPE = "turtle"
    DEFAULT_WINDOW_SIZE = (800, 500)
    DEFAULT_SPEED = 4
    shapeDict.update({"circle":TURTLE_RING_SVG_TEMPLATE})

#==========================
# Turtle State - Visibility
#==========================

# Switch turtle visibility to ON
def showturtle():
    """Makes the turtle visible.

    Aliases: showturtle | st
    """

    global is_turtle_visible
    is_turtle_visible = True
    _updateDrawing(0)
st = showturtle # alias

# Switch turtle visibility to OFF
def hideturtle():
    """Makes the turtle invisible.

    Aliases: hideturtle | ht
    """

    global is_turtle_visible
    is_turtle_visible = False
    _updateDrawing(0)
ht = hideturtle # alias

def isvisible():
    """Return True if the Turtle is shown, False if it's hidden."""

    return is_turtle_visible

#==========================
# Turtle State - Appearance
#==========================

# Set turtle shape to shape with given name or, if name is not given, return name of current shape
def shape(name=None):
    """Sets turtle shape to shape with given name / return current shapename.

    Args:
        name: an optional string, which is a valid shapename

    Sets the turtle shape to shape with given name or, if name is not given,
    returns the name of current shape.
    
    The possible turtle shapes include the ones from turtle.py: 
    'classic' (the default), 'arrow', 'triangle', 'square', 'circle', 'blank'. 
    The 'turtle' shape is the one that Tolga Atam included in his original 
    ColabTurtle version. Use 'turtle2' for the polygonal turtle shape form 
    turtle.py. The circle shape from the original ColabTurtle was renamed 'ring'.
    """

    global turtle_shape
    if name is None:
        return turtle_shape
    elif name.lower() not in VALID_TURTLE_SHAPES:
        raise ValueError('Shape is invalid. Valid options are: ' + str(VALID_TURTLE_SHAPES)) 
    turtle_shape = name.lower()
    _updateDrawing()

# Scale the size of the turtle
# stretch_wid scales perpendicular to orientation
# stretch_len scales in direction of turtle's orientation
def shapesize(stretch_wid=None, stretch_len=None, outline=None):
    """Sets/returns turtle's stretchfactors/outline.

    Args:
        stretch_wid: positive number
        stretch_len: positive number
        outline: positive number

    Returns or sets the pen's attributes x/y-stretchfactors and/or outline.
    The turtle will be displayed stretched according to its stretchfactors.
    stretch_wid is stretchfactor perpendicular to orientation
    stretch_len is stretchfactor in direction of turtles orientation.
    outline determines the width of the shapes's outline.
    """

    global stretchfactor
    global outline_width

    if stretch_wid is stretch_len is outline is None:
        return stretchfactor[0], stretchfactor[1], outline_width

    if stretch_wid == 0 or stretch_len == 0:
        raise ValueError("stretch_wid/stretch_len must not be zero")
    if stretch_wid is not None:
        if not isinstance(stretch_wid, (int,float)):
            raise ValueError('The stretch_wid position must be a number.')        
        if stretch_len is None:
            stretchfactor = stretch_wid, stretch_wid
        else:
            if not isinstance(stretch_len, (int,float)):
                raise ValueError('The stretch_len position must be a number.')                
            stretchfactor = stretch_wid, stretch_len
    elif stretch_len is not None:
        if not isinstance(stretch_len, (int,float)):
            raise ValueError('The stretch_len position must be a number.')         
        stretchfactor = stretch_len, stretch_len
    if outline is None:
        outline = outline_width
    elif not isinstance(outline, (int,float)):
        raise ValueError('The outline must be a positive number.')        
    outline_width = outline   
turtlesize = shapesize #alias

# Set or return the current shearfactor. Shear the turtleshape according to the given shearfactor shear, which is the tangent of the shear angle. 
# Do not change the turtle’s heading (direction of movement). If shear is not given: return the current shearfactor, i. e. 
# the tangent of the shear angle, by which lines parallel to the heading of the turtle are sheared.
def shearfactor(shear=None):
    """Sets or returns the current shearfactor.

    Args:
        shear: number, tangent of the shear angle

    Shears the turtleshape according to the given shearfactor shear,
    which is the tangent of the shear angle. DOES NOT change the
    turtle's heading (direction of movement).
    
    If shear is not given, returns the current shearfactor, i. e. the
    tangent of the shear angle, by which lines parallel to the
    heading of the turtle are sheared.
    """

    global shear_factor
    if shear is None:              
        return round(math.tan((360-shear_factor)*math.pi/180),8)
    alpha = math.atan(shear)*180/math.pi
    shear_factor = (360 - alpha) % 360

# Rotate the turtleshape to point in the direction specified by angle, regardless of its current tilt-angle.
# DO NOT change the turtle's heading (direction of movement). Deprecated since Python version 3.1.
def settiltangle(angle):
    """Rotates the turtleshape to point in the specified direction

    Args:
        angle: number

    Rotates the turtleshape to point in the direction specified by angle,
    regardless of its current tilt-angle. DOES NOT change the turtle's
    heading (direction of movement).
    
    Deprecated since Python version 3.1.
    """

    global tilt_angle
    tilt_angle = angle*angle_conv
    _updateDrawing(0)  

# Set or return the current tilt-angle. 
# If angle is given, rotate the turtleshape to point in the direction specified by angle, regardless of its current tilt-angle. 
# Do not change the turtle’s heading (direction of movement). If angle is not given: return the current tilt-angle, 
# i. e. the angle between the orientation of the turtleshape and the heading of the turtle (its direction of movement).
def tiltangle(angle=None):
    """Sets or returns the current tilt-angle.

    Args:
        angle: number

    Rotates the turtle shape to point in the direction specified by angle,
    regardless of its current tilt-angle. DOES NOT change the turtle's
    heading (direction of movement).
    
    If angle is not given: returns the current tilt-angle, i. e. the angle
    between the orientation of the turtleshape and the heading of the
    turtle (its direction of movement).
    """

    global tilt_angle
    global turtle_degree
    global tilt_angle
    if angle == None:
        return tilt_angle
    if turtle_speed != 0 and animate: 
        turtle_degree_temp = turtle_degree
        if _mode in ["standard","world"]:
            left(-(tilt_angle-angle*angle_conv))
        else:
            right(tilt_angle-angle*angle_conv)
        turtle_degree = turtle_degree_temp
        tilt_angle = angle*angle_conv
    else:
        tilt_angle = angle*angle_conv
        _updateDrawing() 

# Rotate the turtle shape by angle from its current tilt-angle, but do not change the turtle’s heading (direction of movement).
def tilt(angle):
    """Rotates the turtleshape by angle.

    Args:
        angle: a number

    Rotates the turtle shape by angle from its current tilt-angle,
    but does NOT change the turtle's heading (direction of movement).
    """

    global tilt_angle
    global turtle_degree
    global turtle_orient
    if turtle_speed != 0 and animate and _mode != "world":
        turtle_degree_temp = turtle_degree
        if _mode in ["standard"]:
            left(angle*angle_conv)
        else:
            right(angle*angle_conv)
        turtle_degree = turtle_degree_temp
        tilt_angle += angle*angle_conv
    else:
        tilt_angle += angle*angle_conv
        _updateDrawing()

#=====================
# Window Control
#=====================

# Change the background color of the drawing area
# If color='none', the drawing window will have no background fill.
# If no params, return the current background color
def bgcolor(color = None, c2 = None, c3 = None):
    """Sets or returns the background color of the drawing area

    Args:
        a color string or three numbers in the range 0..255 
        or a 3-tuple of such numbers.
    """

    global background_color
    if color is None:
        return background_color
    elif c2 is not None:
        if c3 is None:
            raise ValueError('If the second argument is set, the third arguments must be set as well to complete the rgb set.')
        color = (color, c2, c3)

    background_color = _processColor(color)
    _updateDrawing(0)

# Return turtle window width
def window_width():
    """Returns the turtle window width"""

    return window_size[0]

# Return turtle window height
def window_height():
    """Returns the turtle window height"""
    return window_size[1]

# Set up user-defined coordinate system using lower left and upper right corners.
# if the xscale and yscale are not equal, the aspect ratio of the axes and the
# graphic window will differ.  
def setworldcoordinates(llx, lly, urx, ury):
    """Sets up a user defined coordinate-system.
    
    ATTENTION: Call BEFORE initializeTurtle command.
    
    Args:
        llx: a number, x-coordinate of lower left corner of window
        lly: a number, y-coordinate of lower left corner of window
        urx: a number, x-coordinate of upper right corner of window
        ury: a number, y-coordinate of upper right corner of window
    """

    global xmin
    global xmax
    global ymin
    global ymax
    global xscale
    global yscale
    global _mode
        
    if (urx-llx <= 0):
        raise ValueError("Lower left x-coordinate should be less than upper right x-coordinate")
    elif (ury-lly <= 0):
        raise ValueError("Lower left y-coordinate should be less than upper right y-coordinate")                      
    xmin = llx
    ymin = lly
    xmax = urx
    ymax = ury
    xscale = window_size[0]/(xmax-xmin)
    yscale = window_size[1]/(ymax-ymin)
    _mode = "world"

# Resets the window axes parameters to None in case user wants to rerun a Colab notebook
# without restarting the runtime. Only necessary when calling initializeTurtle after using
# world coordinates.
def resetwindow():
    """Reset the axes parameters for re-running a notebook that uses world coordinates.
    This should be done before setting world coordinates and initializeTurtle.
    """

    global xmin,xmax,ymin,ymax
    global _mode
    xmin = xmax = ymin = ymax = None
    _mode = None

# If world coordinates are such that the aspect ratio of the axes does not match the
# aspect ratio of the graphic window (xscale != yscale), then this function is used to 
# set the orientation of the turtle to line up with the direction of motion in the 
# world coordinates.
def _turtleOrientation():
    if xscale == abs(yscale):
        return turtle_degree
    else:
        alpha = math.radians(heading()*angle_conv)
        Dxy = (_convertx(getx()+math.cos(alpha))-_convertx(getx()),_converty(gety()+math.sin(alpha))-_converty(gety()))
        deg = math.degrees(math.atan2(-Dxy[1],Dxy[0])) % 360
        return 360-deg

# Show a border around the graphics window. Default (no parameters) is gray. A border can be turned off by setting color='none'. 
def showborder(color = None, c2 = None, c3 = None):
    """Shows a border around the graphics window.
    
    Args:
        a color string or three numbers in the range 0..255 
        or a 3-tuple of such numbers.
        
    Default (no argument values) is gray. A border can be turned off by 
    setting color='none' (or use hideborder())
    """

    global border_color
    if color is None:
        color = "gray"
    elif c2 is not None:
        if c3 is None:
            raise ValueError('If the second argument is set, the third arguments must be set as well to complete the rgb set.')
        color = (color, c2, c3)

    border_color = _processColor(color)
    _updateDrawing(0)

# Hide the border around the graphics window.    
def hideborder():
    """Hides the border around the graphics window."""

    global border_color
    border_color = "none"
    _updateDrawing(0)

# Set turtle mode (“standard”, “logo”, “world”, or "svg") and reset the window. If mode is not given, current mode is returned.
def mode(mode=None):
    """Sets turtle mode
    
    Arg:
        One of “standard”, “logo”, “world”, or "svg"
    
    "standard":
        initial turtle heading is to the right (east) and positive
        angles measured counterclockwise with 0° pointing right.
    "logo":
        initial turtle heading is upward (north) and positive angles
        are measured clockwise with 0° pointing up.
    "world":
        used with user-defined coordinates. Setup is same as "standard".
    "svg": 
        This is a special mode to handle how the original ColabTurtle
        worked. The coordinate system is the same as that used with SVG.
        The upper left corner is (0,0) with positive x direction going
        left to right, and the positive y direction going top to bottom.
        Positive angles are measured clockwise with 0° pointing right.
        
    """
    global _mode
    if mode is None:
        return _mode
    elif mode.lower() not in VALID_MODES:
        raise ValueError('Mode is invalid. Valid options are: ' + str(VALID_MODES))
    _mode = mode.lower()   
    reset()
   
#===========================
# Animation Controls
#===========================

# Delay execution of next object for given delay time (in seconds)
def delay(delay_time):
   """Delays execution of next object
   
   Args:
   delay_time: positive number giving time in seconds
   """

   time.sleep(delay_time)

# Turn off animation. Forward/back/circle makes turtle jump and likewise left/right make the turtle turn instantly.
def animationOff():
    """Turns off animation
    
    Forward/back/circle makes the turtle jump and likewise left/right 
    makes the turtle turn instantly.
    """

    global animate
    animate = False
        
# Turn animation on.
def animationOn():
    """Turns animation on"""

    global animate
    animate = True



