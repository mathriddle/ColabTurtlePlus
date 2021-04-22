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
Modified April 2021 by Larry Riddle
Changed some default values to match classic turtle.py package
  default background color is white, default pen color is black, default pen thickness is 1
  default mode is "standard"
  center of window has coordinates (0,0)
Added option for selecting a mode when initializing the turtle graphics
  "standard" : default direction is to the right (east) and positive angles measured counterclockwise
  "logo" : default directon is upward (north) and positive angles are measured clockwise with 0° pointing up.
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
  This should be done immediately after initializing the turtle window.
Added towards function to return the angle between the line from turtle position to specified position.
Implemented begin_fill and end_fill functions from aronma/ColabTurtle_2 github. Added fillcolor function.
  Because the fill is controlled by svg rules, the result may differ from classic turtle fill.
  The argument can have two values, 'nonzero' or 'evenodd', which specifies the svg fill-rule. The default is 'nonzero'
Implemented circle (arc) function from aronma/ColabTurtle_2 github. Modified these to match behavior of circle function in
  classic turtle.py package. If the radius is positive, the center of the circle is to the left of the turtle and the
  path is drawn in the counterclockwise direction. If the radius is negative, the center of the circle is to the right of
  the turtle and path is drawn in the clockwise direction. Number of steps is not used here since the circle is drawn using
  the svg circle function.
Modified the color function to set both the pencolor as well as the fillcolor, just as in classic turtle.py package.
Added dot function to draw a dot with given diameter and color.
Added shapesize function to scale the turtle shape.
Original ColabTurtle defaults can be set by calling OldDefaults() after importing the ColabTurtle package but before initializeTurtle.
  This sets default background to black, default pen color to white, default pen width to 4, default shape to Turtle, and
  default window size to 800x500. It also sets the mode to "svg".

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
DEFAULT_SCALEX = 1
DEFAULT_SCALEY = 1
# all 140 color names that modern browsers support. taken from https://www.w3schools.com/colors/colors_names.asp
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
                'papayawhip', 'lavenderblush', 'seashell', 'cornsilk', 'lemonchiffon', 'floralwhite', 'snow', 'yellow', 'lightyellow', 'ivory', 'white','none')
VALID_COLORS_SET = set(VALID_COLORS)
VALID_MODES = ('standard','logo','world','svg')
DEFAULT_TURTLE_SHAPE = 'classic'
VALID_TURTLE_SHAPES = ('turtle', 'ring', 'classic', 'arrow', 'square', 'triangle', 'circle', 'turtle2', 'blank') 
DEFAULT_MODE = 'standard'
SVG_TEMPLATE = """
      <svg width="{window_width}" height="{window_height}">  
        <rect width="100%" height="100%" style="fill:{background_color};stroke:{kolor};stroke-width:1"/>
        {fill}
        {lines}
        {dots}
        {turtle}
      </svg>
    """
TURTLE_TURTLE_SVG_TEMPLATE = """<g id="turtle" visibility="{visibility}" transform="rotate({degrees},{rotation_x},{rotation_y}) translate({turtle_x}, {turtle_y})">
<path style="stroke:{pen_color};fill-rule:evenodd;fill:{turtle_color};fill-opacity:1;" transform="scale({sx},{sy})" d="M 18.214844 0.632812 C 16.109375 1.800781 15.011719 4.074219 15.074219 7.132812 L 15.085938 7.652344 L 14.785156 7.496094 C 13.476562 6.824219 11.957031 6.671875 10.40625 7.066406 C 8.46875 7.550781 6.515625 9.15625 4.394531 11.992188 C 3.0625 13.777344 2.679688 14.636719 3.042969 15.027344 L 3.15625 15.152344 L 3.519531 15.152344 C 4.238281 15.152344 4.828125 14.886719 8.1875 13.039062 C 9.386719 12.378906 10.371094 11.839844 10.378906 11.839844 C 10.386719 11.839844 10.355469 11.929688 10.304688 12.035156 C 9.832031 13.09375 9.257812 14.820312 8.96875 16.078125 C 7.914062 20.652344 8.617188 24.53125 11.070312 27.660156 C 11.351562 28.015625 11.363281 27.914062 10.972656 28.382812 C 8.925781 30.84375 7.945312 33.28125 8.238281 35.1875 C 8.289062 35.527344 8.28125 35.523438 8.917969 35.523438 C 10.941406 35.523438 13.074219 34.207031 15.136719 31.6875 C 15.359375 31.417969 15.328125 31.425781 15.5625 31.574219 C 16.292969 32.042969 18.023438 32.964844 18.175781 32.964844 C 18.335938 32.964844 19.941406 32.210938 20.828125 31.71875 C 20.996094 31.625 21.136719 31.554688 21.136719 31.558594 C 21.203125 31.664062 21.898438 32.414062 22.222656 32.730469 C 23.835938 34.300781 25.5625 35.132812 27.582031 35.300781 C 27.90625 35.328125 27.9375 35.308594 28.007812 34.984375 C 28.382812 33.242188 27.625 30.925781 25.863281 28.425781 L 25.542969 27.96875 L 25.699219 27.785156 C 28.945312 23.960938 29.132812 18.699219 26.257812 11.96875 L 26.207031 11.84375 L 27.945312 12.703125 C 31.53125 14.476562 32.316406 14.800781 33.03125 14.800781 C 33.976562 14.800781 33.78125 13.9375 32.472656 12.292969 C 28.519531 7.355469 25.394531 5.925781 21.921875 7.472656 L 21.558594 7.636719 L 21.578125 7.542969 C 21.699219 6.992188 21.761719 5.742188 21.699219 5.164062 C 21.496094 3.296875 20.664062 1.964844 19.003906 0.855469 C 18.480469 0.503906 18.457031 0.5 18.214844 0.632812" />
</g>"""
TURTLE_RING_SVG_TEMPLATE = """<g id="ring" visibility="{visibility}" transform="rotate({degrees},{rotation_x},{rotation_y}) translate({turtle_x}, {turtle_y})">
<ellipse stroke="{turtle_color}" stroke-width="3" fill="transparent" rx="{rx}" ry = "{ry}" cx="0" cy="{cy}" />
<polygon points="0,5 5,0 -5,0" transform="scale({sx},{sy})" style="fill:{turtle_color};stroke:{pen_color};stroke-width:0" />
</g>"""
TURTLE_CLASSIC_SVG_TEMPLATE = """<g id="classic" visibility="{visibility}" transform="rotate({degrees},{rotation_x},{rotation_y}) translate({turtle_x}, {turtle_y})">
<polygon points="-5,0 0,2 5,0 0,9" transform="scale({sx},{sy})" style="stroke:{pen_color};fill-rule:evenodd;fill:{turtle_color};fill-opacity:1;stroke-width:{pw}" />
</g>"""
TURTLE_ARROW_SVG_TEMPLATE = """<g id="arrow" visibility="{visibility}" transform="rotate({degrees},{rotation_x},{rotation_y}) translate({turtle_x}, {turtle_y})">
<polygon points="-10,0 0,10 10,0" transform="scale({sx},{sy})" style="stroke:{pen_color};fill-rule:evenodd;fill:{turtle_color};fill-opacity:1;stroke-width:{pw}" />
</g>"""
TURTLE_SQUARE_SVG_TEMPLATE = """<g id="square" visibility="{visibility}" transform="rotate({degrees},{rotation_x},{rotation_y}) translate({turtle_x}, {turtle_y})">
<polygon points="10,-10 10,10 -10,10 -10,-10" transform="scale({sx},{sy})" style="stroke:{pen_color};fill-rule:evenodd;fill:{turtle_color};fill-opacity:1;stroke-width:{pw}" />
</g>"""
TURTLE_TRIANGLE_SVG_TEMPLATE = """<g id="triangle" visibility="{visibility}" transform="rotate({degrees},{rotation_x},{rotation_y}) translate({turtle_x}, {turtle_y})">
<polygon points="10,0 0,17.32 -10,0" transform="scale({sx},{sy})" style="stroke:{pen_color};fill-rule:evenodd;fill:{turtle_color};fill-opacity:1;stroke-width:{pw}" />
</g>"""
TURTLE_CIRCLE_SVG_TEMPLATE = """<g id="ellipse" visibility="{visibility}" transform="rotate({degrees},{rotation_x},{rotation_y}) translate({turtle_x}, {turtle_y})">
<ellipse stroke="{turtle_color}" style="stroke:{pen_color};fill-rule:evenodd;fill:{turtle_color};fill-opacity:1;stroke-width:{pw}" rx="{rx}" ry = "{ry}" cx="0" cy="0" />
</g>"""
TURTLE_TURTLE2_SVG_TEMPLATE = """<g id="turtle2" visibility="{visibility}" transform="rotate({degrees},{rotation_x},{rotation_y}) translate({turtle_x}, {turtle_y})">
<polygon points="0,-16 2,-14 1,-10 4,-7 7,-9 9,-8 6,-5 7,-1 5,3 8,6 6,8 4,5 0,7 -4,5 -6,8 -8,6 -5,3 -7,-1 -6,-5 -9,-8 -7,-9 -4,-7 -1,-10 -2,-14" transform="scale({sx},{sy})" style="stroke:none;fill:{turtle_color};fill-opacity:1;" />
</g>"""


SPEED_TO_SEC_MAP = {0: 0, 1: 1.5, 2: 0.9, 3: 0.7, 4: 0.5, 5: 0.3, 6: 0.18, 7: 0.12, 8: 0.06, 9: 0.04, 10: 0.02, 11: 0.01, 12: 0.001, 13: 0.0001}


# Helper function that maps [0,13] speed values to ms delays
def _speedToSec(speed):
    return SPEED_TO_SEC_MAP[speed]

timeout = _speedToSec(DEFAULT_SPEED)
turtle_speed = DEFAULT_SPEED
is_turtle_visible = DEFAULT_TURTLE_VISIBILITY
pen_color = DEFAULT_PEN_COLOR
window_size = DEFAULT_WINDOW_SIZE
turtle_pos = (DEFAULT_WINDOW_SIZE[0] / 2, DEFAULT_WINDOW_SIZE[1] / 2)
turtle_degree = DEFAULT_TURTLE_DEGREE
background_color = DEFAULT_BACKGROUND_COLOR
is_pen_down = DEFAULT_IS_PEN_DOWN
svg_lines_string = DEFAULT_SVG_LINES_STRING
pen_width = DEFAULT_PEN_WIDTH
turtle_shape = DEFAULT_TURTLE_SHAPE
_mode = DEFAULT_MODE
border_color = DEFAULT_BORDER_COLOR
is_filling = False
fill_color = DEFAULT_FILL_COLOR
turtle_scalex = DEFAULT_SCALEX
turtle_scaley = DEFAULT_SCALEY
outline_width = DEFAULT_OUTLINE_WIDTH


drawing_window = None


# Construct the display for turtle
def initializeTurtle(window=None, speed=None, mode=None):
    global window_size
    global drawing_window
    global turtle_speed
    global is_turtle_visible
    global pen_color
    global turtle_pos
    global turtle_degree
    global background_color
    global is_pen_down
    global svg_lines_string
    global svg_fill_string
    global svg_dots_string
    global pen_width
    global turtle_shape
    global _mode
    global xmin,ymin,xmax,ymax
    global xscale
    global yscale
    global timeout
    
    if window == None:
        window_size = DEFAULT_WINDOW_SIZE
    elif not (isinstance(window, tuple) and len(window) == 2 and isinstance(
            window[0], int) and isinstance(window[1], int)):
        raise ValueError('Window must be a tuple of 2 integers')
    else:
        window_size = window

    if speed == None:
         turtle_speed = DEFAULT_SPEED
    elif isinstance(speed,int) == False or speed not in range(0, 14):
        raise ValueError('Speed must be an integer in the interval [0,13]')
    else:
        turtle_speed = speed
    timeout = _speedToSec(turtle_speed)
    
    if mode == None:
        _mode = DEFAULT_MODE
    elif mode not in VALID_MODES:
        raise ValueError('Mode must be standard, world, logo, or svg')
    else:
        _mode = mode
    
    if _mode != "svg":
        xmin,ymin,xmax,ymax = -window_size[0]/2,-window_size[1]/2,window_size[0]/2,window_size[1]/2
        xscale = window_size[0]/(xmax-xmin)
        yscale = window_size[1]/(ymax-ymin)
    else:
        xmin,ymax = 0,0
        xscale = 1
        yscale = -1
       

    is_turtle_visible = DEFAULT_TURTLE_VISIBILITY
    turtle_pos = (window_size[0] / 2, window_size[1] / 2)
    turtle_degree = DEFAULT_TURTLE_DEGREE if (_mode in ["standard","world"]) else (270 - DEFAULT_TURTLE_DEGREE)
    background_color = DEFAULT_BACKGROUND_COLOR
    pen_color = DEFAULT_PEN_COLOR
    is_pen_down = DEFAULT_IS_PEN_DOWN
    svg_lines_string = DEFAULT_SVG_LINES_STRING
    pen_width = DEFAULT_PEN_WIDTH
    turtle_shape = DEFAULT_TURTLE_SHAPE
    is_filling = False
    svg_fill_string = ''
    svg_dots_string = ''
    fill_color = DEFAULT_FILL_COLOR
    

    drawing_window = display(HTML(_generateSvgDrawing()), display_id=True)


# Helper function for generating svg string of the turtle
def _generateTurtleSvgDrawing():
    if is_turtle_visible:
        vis = 'visible'
    else:
        vis = 'hidden'

    turtle_x = turtle_pos[0]
    turtle_y = turtle_pos[1]
    degrees = turtle_degree
    template = ''

    if turtle_shape == 'turtle':
        turtle_x -= 18*turtle_scalex
        turtle_y -= 18*turtle_scaley
        degrees += 90
        template = TURTLE_TURTLE_SVG_TEMPLATE
    elif turtle_shape == 'classic':
        turtle_y -= 4.5*turtle_scaley
        degrees -= 90
        template = TURTLE_CLASSIC_SVG_TEMPLATE
    elif turtle_shape == 'ring':
        turtle_y += 10*turtle_scaley+4
        degrees -= 90
        template = TURTLE_RING_SVG_TEMPLATE
    elif turtle_shape == 'arrow':
        turtle_y -= 5*turtle_scaley
        degrees -= 90
        template = TURTLE_ARROW_SVG_TEMPLATE
    elif turtle_shape == 'square':
        degrees -= 90
        template = TURTLE_SQUARE_SVG_TEMPLATE
    elif turtle_shape == 'triangle':
        turtle_y -= 8.66*turtle_scaley
        degrees -= 90
        template = TURTLE_TRIANGLE_SVG_TEMPLATE
    elif turtle_shape == 'circle':
        degrees -= 90
        template = TURTLE_CIRCLE_SVG_TEMPLATE
    elif turtle_shape == 'turtle2':
        degrees += 90
        template = TURTLE_TURTLE2_SVG_TEMPLATE
    elif turtle_shape == 'blank':
        template = ""

    return template.format(turtle_color=fill_color,
                           pen_color=pen_color,
                           turtle_x=turtle_x, 
                           turtle_y=turtle_y,
                           visibility=vis, 
                           degrees=degrees,
                           sx=turtle_scalex,
                           sy=turtle_scaley,
                           rx=10*turtle_scalex,
                           ry=10*turtle_scaley,
                           cy=-(10*turtle_scaley+4),
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
                               turtle=_generateTurtleSvgDrawing(),
                               kolor=border_color)


# Helper functions for updating the screen using the latest positions/angles/lines etc.
# If the turtle speed is 0, the update is skipped so animation is done.
def _updateDrawing():
    if drawing_window == None:
        raise AttributeError("Display has not been initialized yet. Call initializeTurtle() before using.")
    if (turtle_speed != 0):
        time.sleep(timeout)
        drawing_window.update(HTML(_generateSvgDrawing()))

# Convert to world coordinates
def _convertx(x):
    return (x-xmin)*xscale
  
def _converty(y):
    return (ymax-y)*yscale

# Helper function for managing any kind of move to a given 'new_pos' and draw lines if pen is down
def _moveToNewPosition(new_pos):
    global turtle_pos
    global svg_lines_string
    global tmp_fill_string

    # rounding the new_pos to eliminate floating point errors.
    new_pos = ( round(new_pos[0],3), round(new_pos[1],3) )
    
    start_pos = turtle_pos
    if is_pen_down:
        svg_lines_string += \
            """<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke-linecap="round" style="stroke:{pen_color};stroke-width:{pen_width}" />""".format(
                        x1=start_pos[0],
                        y1=start_pos[1],
                        x2=new_pos[0],
                        y2=new_pos[1],
                        pen_color=pen_color, 
                        pen_width=pen_width)
    if is_filling:
        tmp_fill_string += """ L {x1} {y1} """.format(x1=new_pos[0],y1=new_pos[1])
    turtle_pos = new_pos
    _updateDrawing()

# Helper function for drawing arcs of radius 'r' to 'new_pos' and draw line if pen is down.
# Modified from aronma/ColabTurtle_2 github to allow arc on either side of turtle.
# Positive radius has circle to left of turtle moving counterclockwise.
# Negative radius has circle to right of turtle moving clockwise.
def _arctoNewPosition(r,new_pos):
    global turtle_pos
    global svg_lines_string
    global tmp_fill_string
    
    sweep = 0 if r > 0 else 1  # SVG arc sweep flag
    rx = r*xscale
    ry = r*abs(yscale)
    
    start_pos = turtle_pos
    if is_pen_down:  
        svg_lines_string += """<path d="M {x1} {y1} A {rx} {ry} 0 0 {s} {x2} {y2}" stroke-linecap="round" fill="transparent" fill-opacity="0" style="stroke:{pen_color};stroke-width:{pen_width}"/>""".format(
            x1=start_pos[0], y1=start_pos[1],rx = rx, ry = ry, x2=new_pos[0], y2=new_pos[1], pen_color=pen_color, pen_width=pen_width, s=sweep)    
    if is_filling:
        tmp_fill_string += """ A {rx} {ry} 0 0 {s} {x2} {y2} """.format(rx=r,ry=r,x2=new_pos[0],y2=new_pos[1],s=sweep)
    
    turtle_pos = new_pos
    #_updateDrawing()    
    
# Initialize the string for the svg path of the filled shape.
# Modified from aronma/ColabTurtle_2 github repo
# The current svg_lines_string is stored to be used when the fill is finished because the svg_fill_string will include
# the svg code for the path generated between the begin and end fill commands.
def begin_fill(rule='nonzero'):
    global is_filling
    global svg_lines_string_orig
    global tmp_fill_string
    rule = rule.lower()
    if not (rule == 'nonzero' or rule == 'evenodd'):
        raise ValueError("The fill-rule must be 'nonzero' or 'evenodd'.")
    if not is_filling:
        svg_lines_string_orig = svg_lines_string
        tmp_fill_string = """<path fill-rule="{rule}" d="M {x1} {y1} """.format(
                x1=turtle_pos[0],
                y1=turtle_pos[1],
                rule=rule)  
        is_filling = True

# Terminate the string for the svg path of the filled shape
# Modified from aronma/ColabTurtle_2 github repo
# The original svg_lines_string was previously stored to be used when the fill is finished because the svg_fill_string will include
# the svg code for the path generated between the begin and end fill commands. 
def end_fill():
    global is_filling   
    global svg_fill_string
    global svg_lines_string
    global tmp_fill_string
    if is_filling:
        is_filling = False
        tmp_fill_string += """" stroke-linecap="round" style="stroke:{pencolor};stroke-width:{penwidth}" fill="{fillcolor}" />""".format(
                pencolor=pen_color,
                penwidth=pen_width,
                fillcolor=fill_color)
        svg_lines_string = svg_lines_string_orig
        svg_fill_string += tmp_fill_string
        _updateDrawing()

# Helper function to draw a circular arc
# Modified from aronma/ColabTurtle_2 github repo
# Positive radius has arc to left of turtle, negative radius has arc to right of turtle.
def _arc(radius, degrees):
    global turtle_degree
    alpha = math.radians(turtle_degree)
    theta = math.radians(degrees)
    
    s = radius/abs(radius)  # 1=left, -1=right
    gamma = alpha-s*theta

    circle_center = (turtle_pos[0] + radius*xscale*math.sin(alpha), turtle_pos[1] - radius*abs(yscale)*math.cos(alpha))
    ending_point = (round(circle_center[0] - radius*xscale*math.sin(gamma),3) , round(circle_center[1] + radius*abs(yscale)*math.cos(gamma),3))
  
    _arctoNewPosition(radius,ending_point)
    
    turtle_degree = (turtle_degree - s*degrees) % 360
    _updateDrawing()

# Since SVG has some ambiguity when using an arc path for a complete circle,
# the circle function is broken into chunks of at most 90 degrees.
# From aronma/ColabTurtle_2 github
# Positive radius has circle to left of turtle, negative radius has circle to right of turtle.
# This circle function does NOT use the steps argument found in classical turtle.py. The kwargs
# will ignore any keyword parameter using steps.
def circle(radius, extent=360, **kwargs):
    if not isinstance(radius, (int,float)):
        raise ValueError('Circle radius should be a number')
    if not isinstance(extent, (int,float)):
        raise ValueError('Extent should be a number')      
    if extent < 0:
        raise ValueError('Extent should be a positive number')
     
    while extent > 0:
        if extent > 90:
            _arc(radius, 90)
        else:
            _arc(radius, extent)
        extent += -90        

# Draw a dot with diameter size, using color
# If size is not given, the maximum of pensize+4 and 2*pensize is used.
def dot(size = None, *color):
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
        
# Makes the turtle move forward by 'units' units
def forward(units):
    if not isinstance(units, (int,float)):
        raise ValueError('Units must be a number.')
     
    alpha = math.radians(turtle_degree)
    ending_point = (turtle_pos[0] + units * xscale * math.cos(alpha), turtle_pos[1] + units * abs(yscale) * math.sin(alpha))

    _moveToNewPosition(ending_point)

fd = forward # alias

# Makes the turtle move backward by 'units' units
def backward(units):
    if not isinstance(units, (int,float)):
        raise ValueError('Units must be a number.')
    forward(-1 * units)

bk = backward # alias
back = backward # alias


# Makes the turtle move right by 'degrees' degrees (NOT radians)
def right(degrees):
    global turtle_degree

    if not isinstance(degrees, (int,float)):
        raise ValueError('Degrees must be a number.')

    turtle_degree = (turtle_degree + degrees) % 360
    _updateDrawing()

rt = right # alias

# Makes the turtle face a given direction
def face(degrees):
    global turtle_degree

    if not isinstance(degrees, (int,float)):
        raise ValueError('Degrees must be a number.')

    if _mode in ["standard","world"]: 
        turtle_degree = (360 - degrees) % 360
    elif _mode == "logo":
        turtle_degree = (270 + degrees) % 360
    else: # mode = "svg"
        turtle_degree = degrees % 360
    _updateDrawing()

setheading = face # alias
seth = face # alias

# Makes the turtle move right by 'degrees' degrees (NOT radians, this library does not support radians right now)
def left(degrees):
    if not isinstance(degrees, (int,float)):
        raise ValueError('Degrees must be a number.')
    right(-1 * degrees)

lt = left

# Raises the pen such that following turtle moves will not cause any drawings
def penup():
    global is_pen_down
    is_pen_down = False

pu = penup # alias
up = penup # alias

# Lowers the pen such that following turtle moves will now cause drawings
def pendown():
    global is_pen_down
    is_pen_down = True

pd = pendown # alias
down = pendown # alias

def isdown():
    return is_pen_down

# Update the speed of the moves, [0,13]
# If argument is omitted, it returns the speed.
def speed(speed = None):
    global timeout
    global turtle_speed
    
    if speed is None:
        return turtle_speed

    if isinstance(speed,int) == False or speed not in range(0, 14):
        raise ValueError('Speed must be an integer in the interval [0,13].')
        
    turtle_speed = speed
    timeout = _speedToSec(speed)

# Call this function at end of turtle commands when speed=0 (no animation) so that final image is drawn
def done():
    if drawing_window == None:
        raise AttributeError("Display has not been initialized yet. Call initializeTurtle() before using.")
    drawing_window.update(HTML(_generateSvgDrawing()))        
        
# Move the turtle to a designated 'x' x-coordinate, y-coordinate stays the same
def setx(x):
    if not isinstance(x, (int,float)):
        raise ValueError('new x position must be a number.')
    _moveToNewPosition((_convertx(x), turtle_pos[1]))

# Move the turtle to a designated 'y' y-coordinate, x-coordinate stays the same
def sety(y):
    if not isinstance(y, (int,float)):
        raise ValueError('New y position must be a number.')
    _moveToNewPosition((turtle_pos[0], _converty(y)))

# Move turtle to center of widnow – coordinates (0,0) except for svg mode – and set its heading to its 
# start-orientation (which depends on the mode).
def home():
    global turtle_degree

    _moveToNewPosition( (window_size[0] / 2, window_size[1] / 2) ) # this will handle updating the drawing.
    turtle_degree = DEFAULT_TURTLE_DEGREE if (_mode in ["standard","world"]) else (270 - DEFAULT_TURTLE_DEGREE)
    _updateDrawing()
    
reset = home # alias

# Retrieve the turtle's currrent 'x' x-coordinate
def getx():
    return(turtle_pos[0]/xscale+xmin)

xcor = getx # alias

# Retrieve the turtle's currrent 'y' y-coordinate
def gety():
    return(ymax-turtle_pos[1]/yscale)

ycor = gety # alias

# Retrieve the turtle's current position as a (x,y) tuple vector
def position():
    return (turtle_pos[0]/xscale+xmin, ymax-turtle_pos[1]/yscale)

pos = position # alias

# Retrieve the turtle's current angle
def getheading():
    if _mode in ["standard","world"]:
        return (360 - turtle_degree) % 360
    elif _mode == "logo":
        return (turtle_degree - 270) % 360
    else: # mode = "svg"
        return turtle_degree % 360

heading = getheading # alias

# Move the turtle to a designated position.
def goto(x, y=None):
    if isinstance(x, tuple) and y is None:
        if len(x) != 2:
            raise ValueError('The tuple argument must be of length 2.')

        y = x[1]
        x = x[0]

    if not isinstance(x, (int,float)):
        raise ValueError('New x position must be a number.')
    if not isinstance(y, (int,float)):
        raise ValueError('New y position must be a number.')
    _moveToNewPosition((_convertx(x), _converty(y)))

setpos = goto # alias
setposition = goto # alias

# Switch turtle visibility to ON
def showturtle():
    global is_turtle_visible
    is_turtle_visible = True
    _updateDrawing()

st = showturtle # alias

# Switch turtle visibility to OFF
def hideturtle():
    global is_turtle_visible
    is_turtle_visible = False
    _updateDrawing()

ht = hideturtle # alias

def isvisible():
    return is_turtle_visible

def _validateColorString(color):
    if color in VALID_COLORS_SET: # 140 predefined html color names
        return True
    if re.search("^#(?:[0-9a-fA-F]{3}){1,2}$", color): # 3 or 6 digit hex color code
        return True
    if re.search("rgb\(\s*(?:(?:\d{1,2}|1\d\d|2(?:[0-4]\d|5[0-5]))\s*,?){3}\)$", color): # rgb color code
        return True
    return False

def _validateColorTuple(color):
    if len(color) != 3:
        return False
    if not isinstance(color[0], int) or not isinstance(color[1], int) or not isinstance(color[2], int):
        return False
    if not 0 <= color[0] <= 255 or not 0 <= color[1] <= 255 or not 0 <= color[2] <= 255:
        return False
    return True

def _processColor(color):
    if isinstance(color, str):
        color = color.lower()
        if not _validateColorString(color):
            raise ValueError('Color is invalid. It can be a known html color name, 3-6 digit hex string, or rgb string.')
        return color
    elif isinstance(color, tuple):
        if not _validateColorTuple(color):
            raise ValueError('Color tuple is invalid. It must be a tuple of three integers, which are in the interval [0,255]')
        return 'rgb(' + str(color[0]) + ',' + str(color[1]) + ',' + str(color[2]) + ')'
    else:
        raise ValueError('The first parameter must be a color string or a tuple')

# Change the background color of the drawing area
# If color='none', the drawing window will have no background fill.
# If no params, return the current background color
def bgcolor(color = None, c2 = None, c3 = None):
    global background_color

    if color is None:
        return background_color
    elif c2 is not None:
        if c3 is None:
            raise ValueError('If the second argument is set, the third arguments must be set as well to complete the rgb set.')
        color = (color, c2, c3)

    background_color = _processColor(color)
    _updateDrawing()


# Change the color of the pen
# If no params, return the current pen color
def pencolor(color = None, c2 = None, c3 = None):
    global pen_color

    if color is None:
        return pen_color
    elif c2 is not None:
        if c3 is None:
            raise ValueError('If the second argument is set, the third arguments must be set as well to complete the rgb set.')
        color = (color, c2, c3)

    pen_color = _processColor(color)
    _updateDrawing()

# Change the fill color
# If no params, return the current fill color
def fillcolor(color = None, c2 = None, c3 = None):
    global fill_color

    if color is None:
        return fill_color
    elif c2 is not None:
        if c3 is None:
            raise ValueError('If the second argument is set, the third arguments must be set as well to complete the rgb set.')
        color = (color, c2, c3)

    fill_color = _processColor(color)
    _updateDrawing()

# Return or set pencolor and fillcolor
def color(*args):
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
        
# Change the width of the lines drawn by the turtle, in pixels
# If the function is called without arguments, it returns the current width
def width(width = None):
    global pen_width

    if width is None:
        return pen_width
    else:
        if not isinstance(width, int):
            raise ValueError('New width value must be an integer.')
        if not width > 0:
            raise ValueError('New width value must be positive.')

        pen_width = width
    _updateDrawing()

pensize = width  #alias

# Calculate the distance between the turtle and a given point
def distance(x, y=None):
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

# Return the angle between the line from turtle position to position specified by (x,y)
# This depends on the turtle’s start orientation which depends on the mode - standard/world or logo.  
def towards(x, y=None):
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
        return result
    elif _mode == "logo":
        return (90 - result) % 360
    else:  # mode = "svg"
        return (360 - result) % 360
  
# Clear any text or drawing on the screen
def clear():
    global svg_lines_string
    global svg_fill_string
    global svg_dots_string

    svg_lines_string = ""
    svg_fill_string = ""
    svg_dots_string = ""
    _updateDrawing()

def write(obj, **kwargs):
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
            raise ValueError('Font parameter must be a triplet consisting of font size (int), font family (str) and font type. Font type can be one of {bold, italic, underline, normal}')
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

# Set turtle shape to shape with given name or, if name is not given, return name of current shape
def shape(name=None):
    global turtle_shape
    if name is None:
        return turtle_shape
    elif name.lower() not in VALID_TURTLE_SHAPES:
        raise ValueError('Shape is invalid. Valid options are: ' + str(VALID_TURTLE_SHAPES))
    
    turtle_shape = name.lower()
    _updateDrawing()

# Set turtle mode (“standard”, “logo”, “world”, or "svg") and reset the window. If mode is not given, current mode is returned.
def mode(mode=None):
    global _mode
    if mode is None:
        return _mode
    elif mode.lower() not in VALID_MODES:
        raise ValueError('Mode is invalid. Valid options are: ' + str(VALID_MODES))
    
    _mode = mode.lower()   
    reset()
    
# Return turtle window width
def window_width():
    return window_size[0]

# Return turtle window height
def window_height():
    return window_size[1]

# Save the image as an SVG file using given filename. Set show_turtle=True to include turtle in svg output
def saveSVG(filename, show_turtle=False):
    if drawing_window == None:
        raise AttributeError("Display has not been initialized yet. Call initializeTurtle() before using.")
    if not isinstance(filename, str):
        raise ValueError("Filename must be a string")
    if not filename.endswith(".svg"):
        filename += ".svg"
    text_file = open(filename, "w")
    header = ("""<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">\n""").format(
            w=window_size[0],
            h=window_size[1]) 
    header += ("""<rect width="100%" height="100%" style="fill:{fillcolor};stroke:{kolor};stroke-width:1" />\n""").format(
            fillcolor=background_color,
            kolor=border_color)
    fill = svg_fill_string.replace(">",">\n")
    image = svg_lines_string.replace(">",">\n")
    dots = svg_dots_string.replace(">",">\n")
    if show_turtle:
        turtle_svg = _generateTurtleSvgDrawing() + " \n"
    else:
        turtle_svg = ""
    output = header + fill + image + dots + turtle_svg + "</svg>"
    text_file.write(output)
    text_file.close()

# Print the SVG code for the image
def showSVG(show_turtle=False):
    if drawing_window == None:
        raise AttributeError("Display has not been initialized yet. Call initializeTurtle() before using.")
    header = ("""<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">\n""").format(
            w=window_size[0],
            h=window_size[1]) 
    header += ("""<rect width="100%" height="100%" style="fill:{fillcolor};stroke:{kolor};stroke-width:1" />\n""").format(
            fillcolor=background_color,
            kolor=border_color)
    fill = svg_fill_string.replace(">",">\n")
    image = svg_lines_string.replace(">",">\n")
    dots = svg_dots_string.replace(">",">\n")
    turtle_svg = (_generateTurtleSvgDrawing() + " \n") if show_turtle else ""
    output = header + fill + image + dots + turtle_svg + "</svg>"
    print(output) 

# Set up user-defined coordinate system using lower left and upper right corners.
# ATTENTION: in user-defined coordinate systems angles may appear distorted.
def setworldcoordinates(llx, lly, urx, ury):
    global xmin
    global xmax
    global ymin
    global ymax
    global xscale
    global yscale
    global _mode
    
    if drawing_window == None:
        raise AttributeError("Display has not been initialized yet. Call initializeTurtle() before using.")
    elif (urx-llx <= 0):
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
    

# Show a border around the graphics window. Default (no parameters) is gray. A border can be turned off by setting color='none'. 
def showBorder(color = None, c2 = None, c3 = None):
    global border_color
    if color is None:
        color = "gray"
    elif c2 is not None:
        if c3 is None:
            raise ValueError('If the second argument is set, the third arguments must be set as well to complete the rgb set.')
        color = (color, c2, c3)

    border_color = _processColor(color)
    _updateDrawing()

# Hide the border around the graphics window.    
def hideBorder():
    global border_color
    border_color = "none"
    _updateDrawing()
  
# Set the defaults used in the original version of ColabTurtle package
def OldDefaults():
    global DEFAULT_BACKGROUND_COLOR
    global DEFAULT_PEN_COLOR
    global DEFAULT_PEN_WIDTH
    global DEFAULT_MODE
    global DEFAULT_TURTLE_SHAPE
    global DEFAULT_WINDOW_SIZE
    
    DEFAULT_BACKGROUND_COLOR = "black"
    DEFAULT_PEN_COLOR = "white"
    DEFAULT_PEN_WIDTH = 4
    DEFAULT_MODE = 'svg'
    DEFAULT_TURTLE_SHAPE = "turtle"
    DEFAULT_WINDOW_SIZE = (800, 500)

# Reset back to defaults
def reset():
    global is_turtle_visible
    global pen_color
    global background_color
    global is_pen_down
    global pen_width
    global svg_lines_string
    global svg_fill_string
    global svg_dots_string
    global turtle_degree  
    global turtle_pos
    global fill_color
    global border_color
    global turtle_shape
    global turtle_scalex
    global turtle_scaley
    global outline_width

    is_turtle_visible = True
    pen_color = DEFAULT_PEN_COLOR
    fill_color = DEFAULT_FILL_COLOR
    border_color = DEFAULT_BORDER_COLOR
    background_color = DEFAULT_BACKGROUND_COLOR
    #turtle_shape = DEFAULT_TURTLE_SHAPE
    is_pen_down = True
    pen_width = DEFAULT_PEN_WIDTH
    turtle_scalex = DEFAULT_SCALEX
    turtle_scaley = DEFAULT_SCALEY
    outline_width = DEFAULT_OUTLINE_WIDTH
    svg_lines_string = ""
    svg_fill_string = ""
    svg_dots_string = ""
    turtle_degree = DEFAULT_TURTLE_DEGREE if (_mode in ["standard","world"]) else (270 - DEFAULT_TURTLE_DEGREE)
    turtle_pos = (window_size[0] / 2, window_size[1] / 2)
    _updateDrawing()

# Scale the size of the turtle
# stretch_wid scales perpendicular to orientation
# stretch_len scales in direction of turtle's orientation
def shapesize(stretch_wid=None, stretch_len=None, outline=None):
    global turtle_scalex
    global turtle_scaley
    global outline_width

    if stretch_wid is stretch_len is outline is None:
        return turtle_scalex, turtle_scaley, outline_width

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
        
    turtle_scalex = stretchfactor[0]
    turtle_scaley = stretchfactor[1]
    outline_width = outline
        
turtlesize = shapesize #alias
