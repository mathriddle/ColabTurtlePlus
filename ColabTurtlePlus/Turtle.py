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
        <rect width="100%" height="100%" style="fill:{backcolor};stroke:{kolor};stroke-width:1"/>
        {stampsB}
        {lines}
        {dots}
        {stampsT}
        {turtle}
      </svg>
    """
TURTLE_TURTLE_SVG_TEMPLATE = """<g id="turtle" visibility="{visibility}" transform="rotate({degrees},{rotation_x},{rotation_y}) translate({turtle_x}, {turtle_y})">
<path style="stroke:{pcolor};fill-rule:evenodd;fill:{turtle_color};fill-opacity:1;" transform="skewX({sk}) scale({sx},{sy})" d="m 1.1536693,-18.56101 c -2.105469,1.167969 -3.203125,3.441407 -3.140625,6.5 l 0.011719,0.519532 -0.300782,-0.15625 c -1.308594,-0.671875 -2.828125,-0.824219 -4.378906,-0.429688 -1.9375,0.484375 -3.8906253,2.089844 -6.0117193,4.9257825 -1.332031,1.785156 -1.714843,2.644531 -1.351562,3.035156 l 0.113281,0.125 h 0.363281 c 0.71875,0 1.308594,-0.265625 4.6679693,-2.113282 1.199219,-0.660156 2.183594,-1.199218 2.191406,-1.199218 0.00781,0 -0.023437,0.089844 -0.074218,0.195312 -0.472657,1.058594 -1.046876,2.785156 -1.335938,4.042969 -1.054688,4.574219 -0.351562,8.453125 2.101562,11.582031 0.28125,0.355469 0.292969,0.253906 -0.097656,0.722656 -2.046875,2.4609375 -3.027344,4.8984375 -2.734375,6.8046875 0.050781,0.339844 0.042969,0.335938 0.679688,0.335938 2.023437,0 4.15625,-1.316407 6.21875,-3.835938 0.222656,-0.269531 0.191406,-0.261719 0.425781,-0.113281 0.730469,0.46875 2.460938,1.390625 2.613281,1.390625 0.160157,0 1.765625,-0.753906 2.652344,-1.246094 0.167969,-0.09375 0.308594,-0.164062 0.308594,-0.160156 0.066406,0.105468 0.761719,0.855468 1.085937,1.171875 1.613282,1.570312 3.339844,2.402343 5.3593747,2.570312 0.324219,0.02734 0.355469,0.0078 0.425781,-0.316406 0.375,-1.742187 -0.382812,-4.058594 -2.1445307,-6.5585935 l -0.320312,-0.457031 0.15625,-0.183594 c 3.2460927,-3.824218 3.4335927,-9.08593704 0.558593,-15.816406 l -0.050781,-0.125 1.7382807,0.859375 c 3.585938,1.773437 4.371094,2.097656 5.085938,2.097656 0.945312,0 0.75,-0.863281 -0.558594,-2.507812 C 11.458356,-11.838353 8.3333563,-13.268041 4.8607003,-11.721166 l -0.363281,0.164063 0.019531,-0.09375 c 0.121094,-0.550781 0.183594,-1.800781 0.121094,-2.378907 -0.203125,-1.867187 -1.035157,-3.199218 -2.695313,-4.308593 -0.523437,-0.351563 -0.546875,-0.355469 -0.789062,-0.222657" />
</g>"""
TURTLE_RING_SVG_TEMPLATE = """<g id="ring" visibility="{visibility}" transform="rotate({degrees},{rotation_x},{rotation_y}) translate({turtle_x}, {turtle_y})">
<ellipse stroke="{pcolor}" transform="skewX({sk})" stroke-width="3" fill="transparent" rx="{rx}" ry = "{ry}" cx="0" cy="{cy}" />
<polygon points="0,5 5,0 -5,0" transform="skewX({sk}) scale({sx},{sy})" style="fill:{turtle_color};stroke:{pcolor};stroke-width:1" />
</g>"""
TURTLE_CLASSIC_SVG_TEMPLATE = """<g id="classic" visibility="{visibility}" transform="rotate({degrees},{rotation_x},{rotation_y}) translate({turtle_x}, {turtle_y})">
<polygon points="-5,-4.5 0,-2.5 5,-4.5 0,4.5" transform="skewX({sk}) scale({sx},{sy})" style="stroke:{pcolor};fill:{turtle_color};stroke-width:{pw}" />
</g>"""
TURTLE_ARROW_SVG_TEMPLATE = """<g id="arrow" visibility="{visibility}" transform="rotate({degrees},{rotation_x},{rotation_y}) translate({turtle_x}, {turtle_y})">
<polygon points="-10,-5 0,5 10,-5" transform="skewX({sk}) scale({sx},{sy})" style="stroke:{pcolor};fill:{turtle_color};stroke-width:{pw}" />
</g>"""
TURTLE_SQUARE_SVG_TEMPLATE = """<g id="square" visibility="{visibility}" transform="rotate({degrees},{rotation_x},{rotation_y}) translate({turtle_x}, {turtle_y})">
<polygon points="10,-10 10,10 -10,10 -10,-10" transform="skewX({sk}) scale({sx},{sy})" style="stroke:{pcolor};fill:{turtle_color};stroke-width:{pw}" />
</g>"""
TURTLE_TRIANGLE_SVG_TEMPLATE = """<g id="triangle" visibility="{visibility}" transform="rotate({degrees},{rotation_x},{rotation_y}) translate({turtle_x}, {turtle_y})">
<polygon points="10,-8.66 0,8.66 -10,-8.66" transform="skewX({sk}) scale({sx},{sy})" style="stroke:{pcolor};fill:{turtle_color};stroke-width:{pw}" />
</g>"""
TURTLE_CIRCLE_SVG_TEMPLATE = """<g id="ellipse" visibility="{visibility}" transform="rotate({degrees},{rotation_x},{rotation_y}) translate({turtle_x}, {turtle_y})">
<ellipse transform="skewX({sk}) scale({sx},{sy})" style="stroke:{pcolor};fill:{turtle_color};stroke-width:{pw}" rx="{rx}" ry = "{ry}" cx="0" cy="0" />
</g>"""
TURTLE_TURTLE2_SVG_TEMPLATE = """<g id="turtle2" visibility="{visibility}" transform="rotate({degrees},{rotation_x},{rotation_y}) translate({turtle_x}, {turtle_y})">
<polygon points="0,16 2,14 1,10 4,7 7,9 9,8 6,5 7,1 5,-3 8,-6 6,-8 4,-5 0,-7 -4,-5 -6,-8 -8,-6 -5,-3 -7,1 -6,5 -9,8 -7,9 -4,7 -1,10 -2,14" transform="skewX({sk}) scale({sx},{sy})" style="stroke:{pcolor};stroke-width:1;fill:{turtle_color}" />
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

class Screen:
    def __init__(self, window_size : tuple = DEFAULT_WINDOW_SIZE):
        if not (isinstance(window_size, tuple) and len(window_size) == 2 and isinstance(
                window_size[0], int) and isinstance(window_size[1], int)):
            raise ValueError('window_size must be a tuple of 2 integers')

        self.window_size = window_size
        self.mode = DEFAULT_MODE
        self.xmin,self.ymin,self.xmax,self.ymax = -self.window_size[0]/2,-self.window_size[1]/2,self.window_size[0]/2,self.window_size[1]/2
        self.xscale = self.yscale = 1
        self.background_color = DEFAULT_BACKGROUND_COLOR
        self.border_color = DEFAULT_BORDER_COLOR
        self.turtles = []
        self.drawing_window = display(HTML(self._generateSvgDrawing()), display_id=True)

    # Helper function that maps [0,13] speed values to ms delays
    def _speedToSec(self, speed):
        return SPEED_TO_SEC_MAP[speed]

    # Helper function for generating svg string of the turtle
    def _generateTurtlesSvgDrawing(self):
        res = ""
        for turtle in self.turtles:
            if turtle.is_turtle_visible:
                vis = 'visible'
            else:
                vis = 'hidden'

            turtle_x = turtle.turtle_pos[0]
            turtle_y = turtle.turtle_pos[1]
            if self.mode == "standard":
                degrees = turtle.turtle_degree - turtle.tilt_angle    
            elif self.mode == "world":
                degrees = turtle.turtle_orient - turtle.tilt_angle
            else:
                degrees = turtle.turtle_degree + turtle.tilt_angle
    
            if turtle.turtle_shape == 'turtle':
                degrees += 90
            elif turtle.turtle_shape == 'ring':
                turtle_y += 10*turtle.stretchfactor[1]+4
                degrees -= 90
            else:
                degrees -= 90
       
            res += shapeDict[turtle.turtle_shape].format(
                           turtle_color=turtle.fill_color,
                           pcolor=turtle.pen_color,
                           turtle_x=turtle_x, 
                           turtle_y=turtle_y,
                           visibility=vis, 
                           degrees=degrees,
                           sx=turtle.stretchfactor[0],
                           sy=turtle.stretchfactor[1],
                           sk=turtle.shear_factor,
                           rx=10*turtle.stretchfactor[0],
                           ry=10*turtle.stretchfactor[1],
                           cy=-(10*turtle.stretchfactor[1]+4),
                           pw = turtle.outline_width,
                           rotation_x=turtle.turtle_pos[0], 
                           rotation_y=turtle.turtle_pos[1])
        return res
    
    # helper function for linking svg strings of text
    def _generateSvgLines(self):
        res = ""
        for turtle in self.turtles:
            res+=turtle.svg_lines_string 
        return res

    # helper function for linking svg strings of text
    def _generateSvgFill(self):
        res = ""
        for turtle in self.turtles:
            res+=turtle.svg_fill_string 
        return res
    
    # helper function for linking svg strings of text
    def _generateSvgDots(self):
        res = ""
        for turtle in self.turtles:
            res+=turtle.svg_dots_string 
        return res
    
    # helper function for linking svg strings of text
    def _generateSvgStampsB(self):
        res = ""
        for turtle in self.turtles:
            res+=turtle.svg_stampsB_string 
        return res
    
    # helper function for linking svg strings of text
    def _generateSvgStampsT(self):
        res = ""
        for turtle in self.turtles:
            res+=turtle.svg_stampsT_string 
        return res
    
    # Helper function for generating the whole svg string
    def _generateSvgDrawing(self):
        return SVG_TEMPLATE.format(window_width=self.window_size[0], 
                               window_height=self.window_size[1],
                               backcolor=self.background_color,
                               fill=self._generateSvgFill(),
                               lines=self._generateSvgLines(),
                               dots=self._generateSvgDots(),
                               stampsB=self._generateSvgStampsB(),
                               stampsT=self._generateSvgStampsT(),
                               turtle=self._generateTurtlesSvgDrawing(),
                               kolor=self.border_color)

    # Helper functions for updating the screen using the latest positions/angles/lines etc.
    # If the turtle speed is 0, the update is skipped so animation is done.
    # If the delay is False (or 0), update immediately without any delay
    def _updateDrawing(self, turtle=None, delay=True):
        if turtle is not None:
            if turtle.turtle_speed != 0:
                self.drawing_window.update(HTML(self._generateSvgDrawing()))         
                if delay:
                    time.sleep(turtle.timeout)  

    # Helper function for managing any kind of move to a given 'new_pos' and draw lines if pen is down
    # Animate turtle motion along line
    def _moveToNewPosition(self, new_pos, turtle, units):
    
        # rounding the new_pos to eliminate floating point errors.
        new_pos = ( round(new_pos[0],3), round(new_pos[1],3) ) 
    
        timeout_orig = turtle.timeout
        start_pos = turtle.turtle_pos           
        svg_lines_string_orig = turtle.svg_lines_string       
        s = 1 if units > 0 else -1            
        if turtle.turtle_speed != 0 and turtle.animate:
            if self.xscale == abs(self.yscale):
                # standard, logo, svg mode, or world mode with same aspect ratio for axes and window
                initial_pos = turtle.turtle_pos         
                alpha = math.radians(turtle.turtle_degree)
                tenx, teny = 10/self.xscale, 10/abs(self.yscale)
                dunits = s*10/self.xscale
                turtle.timeout = turtle.timeout*.20    
                while s*units > 0:
                    dx = min(tenx,s*units)
                    dy = min(teny,s*units)
                    turtle.turtle_pos = (initial_pos[0] + s * dx *self.xscale * math.cos(alpha), initial_pos[1] + s * dy * abs(self.yscale) * math.sin(alpha))
                    if turtle.is_pen_down:
                        turtle.svg_lines_string += \
                        """<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke-linecap="round" style="stroke:{pcolor};stroke-width:{pwidth}" />""".format(
                            x1=initial_pos[0],
                            y1=initial_pos[1],
                            x2=turtle.turtle_pos[0],
                            y2=turtle.turtle_pos[1],
                            pcolor=turtle.pen_color, 
                            pwidth=turtle.pen_width) 
                    initial_pos = turtle.turtle_pos
                    self._updateDrawing(turtle=turtle)
                    units -= dunits
            else:
                # world mode with aspect ratio of axes different than aspect ratio of the window
                initial_pos = turtle.position()
                alpha = math.radians(turtle.turtle_degree)
                turtle.timeout = turtle.timeout*0.20
                xpixunits = self.convertx(1)-self.convertx(0)  #length of 1 world unit along x-axis in pixels
                ypixunits = self.converty(1)-self.converty(0)  #length of 1 world unit along y-axis in pixels
                xstep = 10/(max(xpixunits,ypixunits))  #length of 10 pixels in world units 
                ystep = xstep
                dunits = s*xstep
                while s*units > 0:
                    dx = min(xstep,s*units)
                    dy = min(ystep,s*units)
                    temp_turtle_pos = (initial_pos[0] + s * dx * math.cos(alpha), initial_pos[1] - s * dy * math.sin(alpha))
                    turtle.turtle_pos = (self.convertx(temp_turtle_pos[0]), self.converty(temp_turtle_pos[1]))
                    if turtle.is_pen_down:
                        turtle.svg_lines_string += \
                        """<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke-linecap="round" style="stroke:{pcolor};stroke-width:{pwidth}" />""".format(
                            x1=self.convertx(initial_pos[0]),
                            y1=self.converty(initial_pos[1]),
                            x2= turtle.turtle_pos[0],
                            y2= turtle.turtle_pos[1],
                            pcolor=turtle.pen_color, 
                            pwidth=turtle.pen_width) 
                    initial_pos = temp_turtle_pos
                    self._updateDrawing(turtle=turtle)
                    units -= dunits
        if turtle.is_pen_down:
            # now create the permanent svg string that does not display the animation
            turtle.svg_lines_string = svg_lines_string_orig + \
                """<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke-linecap="round" style="stroke:{pcolor};stroke-width:{pwidth}" />""".format(
                        x1=start_pos[0],
                        y1=start_pos[1],
                        x2=new_pos[0],
                        y2=new_pos[1],
                        pcolor=turtle.pen_color, 
                        pwidth=turtle.pen_width)
        if turtle.is_filling:
            turtle.svg_fill_string += """ L {x1} {y1} """.format(x1=new_pos[0],y1=new_pos[1])  
        turtle.turtle_pos = new_pos
        turtle.timeout = timeout_orig
        if not turtle.animate: self._updateDrawing(turtle=turtle)                    
                    
    def add(self, turtle):
        self.turtles.append(turtle)
        self._updateDrawing(delay=False)                
   
    # Convert user coordinates to SVG coordinates
    def _convertx(x):
        return (x-self.xmin)*self.xscale 
    def _converty(y):
        return (self.ymax-y)*self.yscale                

class Turtle:    
    
    def __init__(self, window, name : str = None):
        if not isinstance(window, Screen) == True:
            raise TypeError("window must be a Screen object")
        self.turtle_speed = DEFAULT_SPEED
        self.name = name
        self.is_turtle_visible = DEFAULT_TURTLE_VISIBILITY
        self.pen_color = DEFAULT_PEN_COLOR
        self.fill_color = DEFAULT_FILL_COLOR
        self.turtle_degree = DEFAULT_TURTLE_DEGREE
        self.turtle_orient = self.turtle_degree
        self.svg_lines_string = self.svg_fill_string = self.svg_dots_string = ""
        self.svg_stampsB_string = self.svg_stampsT_string = ""
        self.is_pen_down = DEFAULT_IS_PEN_DOWN
        self.pen_width = DEFAULT_PEN_WIDTH
        self.turtle_shape = DEFAULT_TURTLE_SHAPE
        self.tilt_angle = DEFAULT_TILT_ANGLE
        self.stretchfactor = DEFAULT_STRETCHFACTOR
        self.shear_factor = DEFAULT_SHEARFACTOR
        self.outline_width = DEFAULT_OUTLINE_WIDTH
        self.turtle_pos = (window.window_size[0] / 2, window.window_size[1] / 2)
        self.drawing_window = window
        self.timeout = window._speedToSec(DEFAULT_SPEED)
        self.animate = True
        self.is_filling = False
        self.angle_conv = 1
        window.add(self)
        
    def __str__(self):
        return self.name

 # Makes the turtle move forward by 'units' units
    def forward(self,units):
        """Moves the turtle forward by the specified distance.

        Aliases: forward | fd

        Args:
            units: a number (integer or float)

        Moves the turtle forward by the specified distance, in the 
        direction the turtle is headed.
        """

        if not isinstance(units, (int,float)):
            raise ValueError('Units must be a number.')
        alpha = math.radians(self.turtle_degree)
        new_pos = (self.turtle_pos[0] + units * math.cos(alpha), self.turtle_pos[1] + units * math.sin(alpha))
        self.drawing_window._moveToNewPosition(new_pos,self,units)
    fd = forward # alias   
    
# Makes the turtle move backward by 'units' units
    def backward(self, units):
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
        self.forward(-1 * units)
    bk = backward # alias
    back = backward # alias    
    
# Makes the turtle move right by 'angle' degrees or radians
# Uses SVG animation to rotate turtle.
# But this doesn't work for turtle=ring and if stretch factors are different for x and y directions,
# so in that case break the rotation into pieces of at most 30 degrees.
    def right(self, angle):
        """Turns the turtle right by angle units.

        Aliases: right | rt

        Args:
            angle: a number (integer or float)

        Turns the turtle right by angle units. (Units are by default 
        degrees, but can be set via the degrees() and radians() functions.)
        Angle orientation depends on mode. 
        """

        if not isinstance(angle, (int,float)):
            raise ValueError('Degrees must be a number.')  
        timeout_orig = self.timeout
        deg = angle*self.angle_conv
        if self.turtle_speed == 0 or not self.animate:
            self.turtle_degree = (self.turtle_degree + deg) % 360
            screen._updateDrawing(turtle=self)
        elif self.turtle_shape != 'ring' and self.stretchfactor[0]==self.stretchfactor[1]:
            stretchfactor_orig = self.stretchfactor
            template = shapeDict[self.turtle_shape]        
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
                /></g>""".format(extent=deg, t=self.timeout*abs(deg)/90, sx=self.stretchfactor[0], sy=self.stretchfactor[1])
            newtemplate = template.replace("</g>",tmp)
            shapeDict.update({self.turtle_shape:newtemplate})
            self.stretchfactor = 1,1
            self.timeout = self.timeout*abs(deg)/90+0.001
            screen._updateDrawing(self)
            self.turtle_degree = (self.turtle_degree + deg) % 360
            #self.turtle_orient = _turtleOrientation()
            shapeDict.update({self.turtle_shape:template})
            self.stretchfactor = stretchfactor_orig
            self.timeout = timeout_orig
        else: #_turtle_shape == 'ring' or _stretchfactor[0] != _stretchfactor[1]
            turtle_degree_orig = self.turtle_degree
            s = 1 if angle > 0 else -1
            while s*deg > 0:
                if s*deg > 30:
                    self.turtle_degree = (self.turtle_degree + s*30) % 360
                   # _turtle_orient = _turtleOrientation()
                else:
                    self.turtle_degree = (_turtle_degree + deg) % 360
                   # _turtle_orient = _turtleOrientation()
                screen._updateDrawing(turtle=self)
                deg -= s*30
            self.timeout = timeout_orig
            self.turtle_degree = (self.turtle_degree + deg) % 360
           #_turtle_orient = _turtleOrientation()
    rt = right # alias    
    
    # Makes the turtle move right by 'angle' degrees or radians
    def left(self, angle):
        """Turns the turtle left by angle units.

        Aliases: left | lt

        Args:
            angle: a number (integer or float)

        Turns turtle left by angle units. (Units are by default 
        degrees, but can be set via the degrees() and radians() functions.)
        Angle orientation depends on mode. 
        """
        if not isinstance(angle, (int,float)):
            raise ValueError('Degrees must be a number.')
        right(-1 * angle)
    lt = left    
    
    
    
    
    
    




