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

    # Add to list of turtles when new object created
    def _add(self, turtle):
        self.turtles.append(turtle)
        self._updateDrawing(delay=False) 

    #=======================
    # SVG functions
    #=======================
        
    # Helper function for generating svg string of all the turtles
    def _generateTurtlesSvgDrawing(self):
        svg = ""
        for turtle in self.turtles:
            svg += self._generateOneSvgTurtle(turtle = turtle)
        return svg

    # Helper function for generating svg string of one turtle
    def _generateOneSvgTurtle(self,turtle):
        svg = ""
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
       
        svg = shapeDict[turtle.turtle_shape].format(
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
        return svg
    
    # helper function for linking svg strings of text
    def _generateSvgLines(self):
        svg = ""
        for turtle in self.turtles:
            svg+=turtle.svg_lines_string 
        return svg

    # helper function for linking svg strings of text
    def _generateSvgFill(self):
        svg = ""
        for turtle in self.turtles:
            svg+=turtle.svg_fill_string 
        return svg
    
    # helper function for linking svg strings of text
    def _generateSvgDots(self):
        svg = ""
        for turtle in self.turtles:
            svg+=turtle.svg_dots_string 
        return svg
    
    # helper function for linking svg strings of text
    def _generateSvgStampsB(self):
        svg = ""
        for turtle in self.turtles:
            svg+=turtle.svg_stampsB_string 
        return svg
    
    # helper function for linking svg strings of text
    def _generateSvgStampsT(self):
        svg = ""
        for turtle in self.turtles:
            svg+=turtle.svg_stampsT_string 
        return svg
    
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

    def showSVG(self, turtle=False):
        """Shows the SVG code for the image to the screen.
    
        Args:
            turtle: (optional) a boolean that determines if the turtles
                are included in the svg output
    
        The SVG commands can be printed on screen (after the drawing is 
        completed) or saved to a file for use in a program like inkscape 
        or Adobe Illustrator, or displaying the image in a webpage.
        """

        header = ("""<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">\n""").format(
            w= self.window_size[0],
            h= self.window_size[1]) 
        header += ("""<rect width="100%" height="100%" style="fill:{fillcolor};stroke:{kolor};stroke-width:1" />\n""").format(
            fillcolor=self.background_color,
            kolor=self.border_color)
        image = self._generateSvgLines().replace("/>","/>\n")
        stampsB = self._generateSvgStampsB().replace("</g>","</g>\n")
        stampsT = self._generateSvgStampsT().replace("</g>","</g>\n")    
        dots = self._generateSvgDots().replace(">",">\n")
        turtle_svg = (self._generateTurtlesSvgDrawing() + " \n") if turtle else ""
        output = header + stampsB + image + dots + stampsT + turtle_svg + "</svg>"
        print(output) 

    # Save the image as an SVG file using given filename. Set turtle=True to include turtle in svg output
    def saveSVG(self, file=None, turtle=False):
        """Saves the image as an SVG file.
    
        Args:
            file: a string giving filename for saved file. The extension 
                ".svg" will be added if missing. If no filename is given,
                the default name SVGimage.svg will be used.
            turtle: an optional boolean that determines if the turtles 
                are included in the svg output saved to the file. Default is False.
    
        The SVG commands can be printed on screen (after the drawing is 
        completed) or saved to a file for use in a program like inkscape 
        or Adobe Illustrator, or displaying the image in a webpage.
        """
    
        if file is None:
            file = "SVGimage.svg"
        elif not isinstance(file, str):
            raise ValueError("File name must be a string")
        if not file.endswith(".svg"):
            file += ".svg"
        text_file = open(file, "w")
        header = ("""<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">\n""").format(
            w= self.window_size[0],
            h= self.window_size[1]) 
        header += ("""<rect width="100%" height="100%" style="fill:{fillcolor};stroke:{kolor};stroke-width:1" />\n""").format(
            fillcolor=self.background_color,
            kolor=self.border_color)
        image = self._generateSvgLines().replace("/>","/>\n")
        stampsB = self._generateSvgStampsB().replace("</g>","</g>\n")
        stampsT = self._generateSvgStampsT().replace("</g>","</g>\n")    
        dots = self._generateSvgDots().replace(">",">\n")
        turtle_svg = (self._generateTurtlesSvgDrawing() + " \n") if turtle else ""
        output = header + stampsB + image + dots + stampsT + turtle_svg + "</svg>"
        text_file.write(output)
        text_file.close()   

    #=========================
    # screen drawing functions
    #=========================

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
    def _moveToNewPosition(self, new_pos, units, turtle):
    
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
                    turtle.turtle_pos = (initial_pos[0] + s * dx * self.xscale * math.cos(alpha), initial_pos[1] + s * dy * abs(self.yscale) * math.sin(alpha))
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
 
    # Helper function for drawing arcs of radius 'r' to 'new_pos' and draw line if pen is down.
    # Modified from aronma/ColabTurtle_2 github to allow arc on either side of turtle.
    # Positive radius has circle to left of turtle moving counterclockwise.
    # Negative radius has circle to right of turtle moving clockwise.
    def _arctoNewPosition(self, r, new_pos, turtle):
 
        sweep = 0 if r > 0 else 1  # SVG arc sweep flag
        rx = r*self.xscale
        ry = r*abs(self.yscale)
    
        start_pos = turtle.turtle_pos
        if turtle.is_pen_down:  
            turtle.svg_lines_string += \
            """<path d="M {x1} {y1} A {rx} {ry} 0 0 {s} {x2} {y2}" stroke-linecap="round" fill="transparent" fill-opacity="0" style="stroke:{pcolor};stroke-width:{pwidth}"/>""".format(
            x1=start_pos[0], 
            y1=start_pos[1],
            rx = rx,
            ry = ry,
            x2=new_pos[0],
            y2=new_pos[1],
            pcolor=turtle.pen_color,
            pwidth=turtle.pen_width,
            s=sweep)    
        if turtle.is_filling:
            turtle.svg_fill_string += """ A {rx} {ry} 0 0 {s} {x2} {y2} """.format(rx=r,ry=r,x2=new_pos[0],y2=new_pos[1],s=sweep)  
        turtle.turtle_pos = new_pos

    # Helper function to draw a circular arc
    # Modified from aronma/ColabTurtle_2 github repo
    # Positive radius has arc to left of turtle, negative radius has arc to right of turtle.
    def _arc(self, radius, degrees, draw, turtle):
        alpha = math.radians(turtle.turtle_degree)
        theta = math.radians(degrees)
        s = radius/abs(radius)  # 1=left, -1=right
        gamma = alpha-s*theta

        circle_center = (turtle.turtle_pos[0] + radius*self.xscale*math.sin(alpha), turtle.turtle_pos[1] - radius*abs(self.yscale)*math.cos(alpha))
        ending_point = (round(circle_center[0] - radius*self.xscale*math.sin(gamma),3) , round(circle_center[1] + radius*abs(self.yscale)*math.cos(gamma),3))
  
        self._arctoNewPosition(radius,ending_point,turtle)
   
        turtle.turtle_degree = (turtle.turtle_degree - s*degrees) % 360
        turtle.turtle_orient = turtle._turtleOrientation()
        if draw: self._updateDrawing(turtle=turtle)                      
   
    # Convert user coordinates to SVG coordinates
    def _convertx(self, x):
        return (x-self.xmin)*self.xscale 
    def _converty(self, y):
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
        self.svg_lines_string_temp = ""
        self.is_pen_down = DEFAULT_IS_PEN_DOWN
        self.pen_width = DEFAULT_PEN_WIDTH
        self.turtle_shape = DEFAULT_TURTLE_SHAPE
        self.tilt_angle = DEFAULT_TILT_ANGLE
        self.stretchfactor = DEFAULT_STRETCHFACTOR
        self.shear_factor = DEFAULT_SHEARFACTOR
        self.outline_width = DEFAULT_OUTLINE_WIDTH
        self.turtle_pos = (window.window_size[0] / 2, window.window_size[1] / 2)
        self.win = window
        self.timeout = window._speedToSec(DEFAULT_SPEED)
        self.animate = True
        self.is_filling = False
        self.is_pen_down = True
        self.angle_conv = 1
        self.angle_mode = DEFAULT_ANGLE_MODE
        self.fill_rule = "evenodd"
        self.fill_opacity = 1
        self.stampdictB = {}
        self.stampdictT = {}
        self.stampnum = 0
        self.stamplist=[]
        window._add(self)
        
    def __str__(self):
        return self.name

    #================================
    # Turtle Motion - Move and Draw
    #================================
        
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
        new_pos = (self.turtle_pos[0] + units * self.win.xscale * math.cos(alpha), self.turtle_pos[1] + units * abs(self.win.yscale) * math.sin(alpha))
        self.win._moveToNewPosition(new_pos,units, turtle=self)
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
            self.win._updateDrawing(turtle=self)
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
            self.win._updateDrawing(self)
            self.turtle_degree = (self.turtle_degree + deg) % 360
            self.turtle_orient = self._turtleOrientation()
            shapeDict.update({self.turtle_shape:template})
            self.stretchfactor = stretchfactor_orig
            self.timeout = timeout_orig
        else: #_turtle_shape == 'ring' or _stretchfactor[0] != _stretchfactor[1]
            turtle_degree_orig = self.turtle_degree
            s = 1 if angle > 0 else -1
            while s*deg > 0:
                if s*deg > 30:
                    self.turtle_degree = (self.turtle_degree + s*30) % 360
                    self.turtle_orient = self._turtleOrientation()
                else:
                    self.turtle_degree = (self.turtle_degree + deg) % 360
                    self.turtle_orient = self._turtleOrientation()
                self.win._updateDrawing(turtle=self)
                deg -= s*30
            self.timeout = timeout_orig
            self.turtle_degree = (self.turtle_degree + deg) % 360
            self.turtle_orient = self._turtleOrientation()
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
        self.right(-1 * angle)
    lt = left # alias 

    # Since SVG has some ambiguity when using an arc path for a complete circle,
    # the circle function is broken into chunks of at most 90 degrees.
    # This is modified from aronma/ColabTurtle_2 github.
    # Positive radius has circle to left of turtle, negative radius has circle to right of turtle.
    # The step argument is here only for backward compatability with classic turtle.py circle.
    # To get a true circular arc, do NOT use steps. Can still be used to draw a regular polygon, but better
    # to use the regularpolygon() function.
    def circle(self, radius, extent=None, steps=None):
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

        if not isinstance(radius, (int,float)):
            raise ValueError('Circle radius should be a number')
        if extent is None:
            extent = 360 if self.angle_mode == "degrees" else 2*math.pi 
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
            self.left(alpha/2)
            for _ in range(steps-1):
                self.forward(length)
                self.left(alpha)
            self.forward(length)
            self.left(alpha/2)  
        elif self.turtle_speed != 0 and self.animate:
            timeout_temp = self.timeout 
            self.timeout = self.timeout*0.5
            degrees = extent*self.angle_conv
            extent = degrees
            # Use temporary svg strings for animation
            svg_lines_string_temp = self.svg_lines_string
            svg_fill_string_temp = self.svg_fill_string 
            turtle_degree_orig = self.turtle_degree
            turtle_pos_orig = self.turtle_pos        
            while extent > 0:
                self.win._arc(radius,min(15,extent),True, turtle=self)
                extent -= 15 
            # return to original position and redo circle for svg strings without animation
            self.svg_lines_string = svg_lines_string_temp
            self.svg_fill_string = svg_fill_string_temp
            self.turtle_degree = turtle_degree_orig
            self.turtle_pos = turtle_pos_orig
            while degrees > 0:
                self.win._arc(radius,min(180,degrees),False, turtle=self)
                degrees -= 180 
            self.timeout = timeout_temp
        else:  # no animation
            extent = extent*self.angle_conv
            while extent > 0:
                self.win._arc(radius,min(180,extent),True, turtle=self)
                extent -= 180         

    # Draw a dot with diameter size, using color
    # If size is not given, the maximum of _pen_width+4 and 2*_pen_width is used.
    def dot(self, size = None, *color):
        """Draws a dot with diameter size, using color.
    
        Args:
            size: (optional) a positive integer
            *color: (optional) a colorstring or a numeric color tuple

        Draw a circular dot with diameter size, using color.
        If size is not given, the maximum of pensize+4 and 2*pensize 
        is used. If no color is given, the pencolor is used.
        """

        if not color:
            if isinstance(size, (str, tuple)):
                color = _processColor(size)
                size = self.pen_width + max(self.pen_width,4)
            else:
                color = self.pen_color
                if not size:
                    size = self.pen_width + max(self.pen_width,4)
        else:
            if size is None:
                size = self.pen_width + max(self.pen_width,4)
            color = _processColor(color[0])
        self.svg_dots_string += """<circle cx="{cx}" cy="{cy}" r="{radius}" fill="{kolor}" fill-opacity="1" />""".format(
            radius=size/2,
            cx=self.turtle_pos[0],
            cy=self.turtle_pos[1],
            kolor=color)
        self.win._updateDrawing(turtle = self)
                
    # Move the turtle to a designated position.
    def goto(self, x, y=None):
        """Moves turtle to an absolute position.

        Aliases: setpos | setposition | goto

        Args:
            x: a number     or      a pair of numbers
            y: a number     or      None

            goto(x, y)      or      goto((x,y))     

        Moves turtle to an absolute position. If the pen is down,
        a line will be drawn. The turtle's orientation does not change.   
        """
        
        if isinstance(x, tuple) and y is None:
            if len(x) != 2:
                raise ValueError('The tuple argument must be of length 2.')
            y = x[1]
            x = x[0]
        if not isinstance(x, (int,float)):
            raise ValueError('New x position must be a number.')
        if not isinstance(y, (int,float)):
            raise ValueError('New y position must be a number.')
        tilt_angle_orig = self.tilt_angle
        turtle_angle_orig = self.turtle_degree
        alpha = self.towards(x,y)*self.angle_conv
        units = self.distance(x,y)
        if self.win.mode == "standard": 
            self.turtle_degree = (360 - alpha) % 360
            self.tilt_angle = -((turtle_angle_orig-self.tilt_angle+alpha) % 360)
        elif self.win.mode == "logo":
            self.turtle_degree = (270 + alpha) % 360
            self.tilt_angle = turtle_angle_orig+self.tilt_angle-alpha-270
        elif self.win.mode == "world":
            self.turtle_degree = (360 - alpha) % 360
        else: # mode = "svg"
            self.turtle_degree = alpha % 360
            self.tilt_angle = turtle_angle_orig+self.tilt_angle-alpha
        self.win._moveToNewPosition((self.win._convertx(x), self.win._converty(y)), units, turtle=self)
        self.tilt_angle = tilt_angle_orig
        self.turtle_degree = turtle_angle_orig
    setpos = goto # alias
    setposition = goto # alias               

    # jump to a point without drawing or animation
    def jumpto(self,x,y=None):
        """Jumps to a specified point without drawing/animation
    
        Args:
            x: a number     or      a pair of numbers
            y: a number     or      None

            jumpto(x, y)      or    jumpto((x,y))  
        """
        if isinstance(x, tuple) and y is None:
            if len(x) != 2:
                raise ValueError('The tuple argument must be of length 2.')
            x = x[0]
            y = x[1]
        animate_temp = self.animate
        self.penup()
        self.animationOff()
        self.goto(x,y)
        self.animate = animate_temp
        self.pendown()        
        
    # Move the turtle to a designated 'x' x-coordinate, y-coordinate stays the same
    def setx(self, x):
        """Set the turtle's first coordinate to x

        Args:
            x: a number (integer or float)

        Set the turtle's first coordinate to x, leave second coordinate
        unchanged.
        """

        if not isinstance(x, (int,float)):
            raise ValueError('new x position must be a number.')
        self.goto(x, self.gety())

    # Move the turtle to a designated 'y' y-coordinate, x-coordinate stays the same
    def sety(self,y):
        """Set the turtle's second coordinate to y

        Args:
            y: a number (integer or float)

        Set the turtle's second coordinate to y, leave first coordinate
        unchanged.
        """

        if not isinstance(y, (int,float)):
            raise ValueError('New y position must be a number.')
        self.goto(self.getx(), y)        
 
    # Makes the turtle face a given direction
    def setheading(self, angle):
        """Set the orientation of the turtle to angle

        Aliases: setheading | seth

        Args:
            angle: a number (integer or float) 
    
        Units are by default degrees, but can be set via 
        the degrees() and radians() functions.

        Set the orientation of the turtle to angle.
        This depends on the mode.
        """

        deg = angle*self.angle_conv
        if not isinstance(angle, (int,float)):
            raise ValueError('Degrees must be a number.')
        if self.win.mode in ["standard","world"]: 
            new_degree = (360 - deg) 
        elif self.win.mode == "logo":
            new_degree = (270 + deg) 
        else: # mode = "svg"
            new_degree = deg % 360
        alpha = (new_degree - self.turtle_degree) % 360
        if self.turtle_speed !=0 and self.animate:
            if alpha <= 180:
                if self.angle_mode == "degrees":
                    self.right(alpha)
                else:
                    self.right(math.radians(alpha))
            else:
                if self.angle_mode == "degrees":
                    self.left(360-alpha)
                else:
                    self.left(math.radians(360-alpha))
        else:
            self.turtle_degree = new_degree
            self.turtle_orient = self._turtleOrientation()
            self.win._updateDrawing(turtle=self)
    seth = setheading # alias
    face = setheading # alias

    # Move turtle to the origin and set its heading to its 
    # start-orientation (which depends on the mode).
    def home(self):
        """Moves the turtle to the origin - coordinates (0,0).

        No arguments.

        Moves the turtle to the origin (0,0) and sets its
        heading to its start-orientation (which depends on mode).
    
        If the mode is "svg", moves the turtle to the center of 
        the drawing window.)
        """
        if self.win.mode != 'svg':
            self.goto(0,0)
        else:
            self.goto( (self.win.window_size[0] / 2, self.win.window_size[1] / 2) )
        #_turtle_degree is always in degrees, but angle mode might be radians
        #divide by _angle_conv so angle sent to left or right is in the correct mode
        if self.win.mode in ['standard','world']:
            if self.turtle_degree <= 180:
                self.left(self.turtle_degree/self.angle_conv)
            else:
                self.right((360-self.turtle_degree)/self.angle_conv)
            self.turtle_orient = self._turtleOrientation()
            self.win._updateDrawing(turtle=self, delay=False)
        else:
            if self.turtle_degree < 90:
                self.left((self.turtle_degree+90)/self.angle_conv)
            elif self.turtle_degree< 270:
                self.right((270-self.turtle_degree)/self.angle_conv)
            else:
                self.left((self.turtle_degree-270)/self.angle_conv)        

    #============================
    # Pen Control - Drawing State
    #============================

    # Lowers the pen such that following turtle moves will now cause drawings
    def pendown(self):
        """Pulls the pen down -- drawing when moving.

        Aliases: pendown | pd | down
        """
        self.is_pen_down = True
    pd = pendown # alias
    down = pendown # alias

    # Raises the pen such that following turtle moves will not cause any drawings
    def penup(self):
        """Pulls the pen up -- no drawing when moving.

        Aliases: penup | pu | up
       """
        self.is_pen_down = False
    pu = penup # alias
    up = penup # alias                
                
    #======================
    # Stamps
    #======================

    # Stamp a copy of the turtle shape onto the canvas at the current turtle position.
    # The argument determines whether the stamp appears below other items (layer=0) or above other items (layer=1) in 
    # the order that SVG draws items. So if layer=0, a stamp may be covered by a filled object, for example, even if
    # the stamp is originally drawn on top of the object during the animation. To prevent this, set layer=1 (or any nonzero number).
    # Returns a stamp_id for that stamp, which can be used to delete it by calling clearstamp(stamp_id).
    def stamp(self, layer=0):
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

        self.stampnum += 1
        self.stamplist.append(self.stampnum)
        if layer != 0:
            self.stampdictT[self.stampnum] = self.win._generateTurtlesSvgDrawing()
            self.svg_stampsT_string += self.stampdictT[self.stampnum]
        else:
            self.stampdictB[self.stampnum] = self.win._generateOneSvgTurtle(turtle=self)
            self.svg_stampsB_string += self.stampdictB[self.stampnum]
        self.win._updateDrawing(turtle=self, delay=False)
        return self.stampnum

    # Helper function to do the work for clearstamp() and clearstamps()
    def _clearstamp(self, stampid):
        tmp = ""
        if stampid in self.stampdictB.keys():
            self.stampdictB.pop(stampid)
            self.stamplist.remove(stampid)
            for n in self.stampdictB:
                tmp += self.stampdictB[n]
            self.svg_stampsB_string = tmp        
        elif stampid in self.stampdictT.keys():
            self.stampdictT.pop(stampid)
            self.stamplist.remove(stampid)
            for n in self.stampdictT:
                tmp += self.stampdictT[n]
            self.svg_stampsT_string = tmp
        self.win._updateDrawing(turtle=self, delay=False)

    # Delete stamp with given stampid.
    # stampid – an integer or tuple of integers, which must be return values of previous stamp() calls
    def clearstamp(self, stampid):
        """Deletes the stamp with given stampid

        Args:
            stampid - an integer, must be return value of previous stamp() call.
        """

        if isinstance(stampid,tuple):
            for subitem in stampid:
                self._clearstamp(subitem)
        else:
            self._clearstamp(stampid)

    # Delete all or first/last n of turtle’s stamps. If n is None, delete all stamps, if n > 0 delete first n stamps,
    # else if n < 0 delete last n stamps.
    def clearstamps(self, n=None):
        """Deletes all or first/last n of turtle's stamps.

        Args:
            n: an optional integer

        If n is None, deletes all of the turtle's stamps.
        If n > 0, deletes the first n stamps.
        If n < 0, deletes the last n stamps.
        """

        if n is None:
            toDelete = self.stamplist[:]
        elif n > 0:
            toDelete = self.stamplist[:n]
        elif n < 0:
            toDelete = self.stamplist[n:]
        for k in toDelete:
            self._clearstamp(k)

        
    # Set turtle shape to shape with given name or, if name is not given, return name of current shape
    def shape(self, name=None):
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

        if name is None:
            return self.turtle_shape
        elif name.lower() not in VALID_TURTLE_SHAPES:
            raise ValueError('Shape is invalid. Valid options are: ' + str(VALID_TURTLE_SHAPES)) 
        self.turtle_shape = name.lower()
        self.win._updateDrawing(turtle=self)
 
    # Update the speed of the moves, [0,13]
    # If argument is omitted, it returns the speed.
    def speed(self, speed = None):
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
  
        if speed is None:
            return self.turtle_speed
        speeds = {'fastest':13, 'fast':10, 'normal':5, 'slow':3, 'slowest':1}
        if speed in speeds:
            self.turtle_speed = speeds[speed]
        elif not isinstance(speed,(int,float)):
            raise ValueError("speed should be a number between 0 and 13")
        self.turtle_speed = speed
        if 0.5 < speed < 13.5:
            self.turtle_speed = int(round(speed))
        elif speed != 0:
            self.turtle_speed = 13
        self.timeout = self.win._speedToSec(self.turtle_speed) 

    # Call this function at end of turtle commands when speed=0 (no animation) so that final image is drawn
    def done(self):
        """Shows the final image when speed=0
    
        No argument
    
        speed = 0 displays final image with no animation. Need to
        call done() at the end so the final image is displayed.
        """
        self.win.drawing_window.update(HTML(self.win._generateSvgDrawing()))  
    update = done #alias
        
    # If world coordinates are such that the aspect ratio of the axes does not match the
    # aspect ratio of the graphic window (xscale != yscale), then this function is used to 
    # set the orientation of the turtle to line up with the direction of motion in the 
    # world coordinates.
    def _turtleOrientation(self):
        if self.win.xscale == abs(self.win.yscale):
            return self.turtle_degree
        else:
            alpha = math.radians(self.heading()*self.angle_conv)
            Dxy = (self.win.convertx(self.getx()+math.cos(alpha))-self.win.convertx(self.getx()),
                   self.win.converty(self.gety()+math.sin(alpha))-self.win.converty(self.gety()))
            deg = math.degrees(math.atan2(-Dxy[1],Dxy[0])) % 360
            return 360-deg    
    
    # Change the color of the pen
    # If no params, return the current pen color
    def pencolor(self, color = None, c2 = None, c3 = None):
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

        if color is None:
            return self.pen_color
        elif c2 is not None:
            if c3 is None:
                raise ValueError('If the second argument is set, the third arguments must be set as well to complete the rgb set.')
            color = (color, c2, c3)

        self.pen_color = _processColor(color)
        self.win._updateDrawing(turtle=self, delay=False)    

    # Change the fill color
    # If no params, return the current fill color
    def fillcolor(self, color = None, c2 = None, c3 = None):
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

        if color is None:
            return _fill_color
        elif c2 is not None:
           if c3 is None:
                raise ValueError('If the second argument is set, the third arguments must be set as well to complete the rgb set.')
           color = (color, c2, c3)

        self.fill_color = _processColor(color)
        self.win._updateDrawing(turtle=self, delay=False)
        
    # Return or set pencolor and fillcolor
    def color(self, *args):
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
        
        if args:
            narg = len(args)
            if narg == 1:
                self.pen_color = self.fill_color = _processColor(args[0])
            elif narg == 2:
                self.pen_color = _processColor(args[0])
                self.fill_color = _processColor(args[1])
            elif narg == 3:
                kolor = (args[0],args[1],args[2])
                self.pen_color = self.fill_color = _processColor(kolor)
            else:
                raise ValueError('Syntax: color(colorstring), color((r,g,b)), color(r,g,b), color(string1,string2), color((r1,g1,b1),(r2,g2,b2))')
        else:
            return self.pen_color, self.fill_color
        self.win._updateDrawing(turtle=self, delay=False)              

        
    #====================================
    # Turtle Motion - Tell Turtle's State
    #====================================  

    # Retrieve the turtle's current position as a (x,y) tuple vector in current coordinate system
    def position(self):
        """Returns the turtle's current location (x,y)

        Aliases: pos | position

        Returns:
            tuple: the current turtle location (x,y)
        """
        return (self.xcor(),self.ycor())
    pos = position # alias

    # Retrieve the turtle's currrent 'x' x-coordinate in current coordinate system
    def xcor(self):
        """Returns the turtle's x coordinate."""

        return(self.turtle_pos[0]/self.win.xscale+self.win.xmin)
    getx = xcor # alias

    # Retrieve the turtle's currrent 'y' y-coordinate in current coordinate system
    def ycor(self):
        """Return the turtle's y coordinate."""
   
        return(self.win.ymax-self.turtle_pos[1]/self.win.yscale)
    gety = ycor # alias        

    # Return the angle between the line from turtle position to position specified by (x,y)
    # This depends on the turtle’s start orientation which depends on the mode - standard/world or logo.  
    def towards(self, x, y=None):
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
        dx = x - self.getx()
        dy = y - self.gety()
        if self.win.mode == "svg":
            dy = -dy
        result = round(math.atan2(dy,dx)*180.0/math.pi, 10) % 360.0
        if self.win.mode in ["standard","world"]:
            angle = result
        elif self.win.mode == "logo":
            angle = (90 - result) % 360
        else:  # mode = "svg"
            angle = (360 - result) % 360
        if self.angle_mode == "degrees":
            return round(angle,7)
        else:
            return round(math.radians(angle),7)
        
    # Retrieve the turtle's current angle in current _angle_mode
    def heading(self):
        """Returns the turtle's current heading"""

        if self.win.mode in ["standard","world"]:
            angle = (360 - self.turtle_degree) % 360
        elif self.win.mode == "logo":
            angle = (self.turtle_degree - 270) % 360
        else: # mode = "svg"
            angle = self.turtle_degree % 360
        if self.angle_mode == "degrees":
            return angle
        else:
            return math.radians(angle)
    getheading = heading # alias
 
    # Calculate the distance between the turtle and a given point
    def distance(self, x, y=None):
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
        return round(math.sqrt( (self.getx() - x) ** 2 + (self.gety() - y) ** 2 ), 8)     
        
    #=============================
    # Turtle Pen Control - Filling
    #=============================

    # Return fillstate (True if filling, False else)
    def filling(self):
        """Return fillstate (True if filling, False else)."""

        return self.is_filling

    # Initialize the string for the svg path of the filled shape.
    # Modified from aronma/ColabTurtle_2 github repo
    # The current _svg_lines_string is stored to be used when the fill is finished because the svg_fill_string will include
    # the svg code for the path generated between the begin and end fill commands.
    # When calling begin_fill, a value for the _fill_rule can be given that will apply only to that fill.
    def begin_fill(self, rule=None, opacity=None):
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

        if rule is None:
            rule = self.fill_rule
        if opacity is None:
            opacity = self.fill_opacity
        rule = rule.lower()
        if not rule in ['evenodd','nonzero']:
            raise ValueError("The fill-rule must be 'nonzero' or 'evenodd'.")
        if (opacity < 0) or (opacity > 1):
            raise ValueError("The fill-opacity should be between 0 and 1.")
        if not self.is_filling:
            self.svg_lines_string_temp = self.svg_lines_string
            self.svg_fill_string = """<path fill-rule="{rule}" fill-opacity="{opacity}" d="M {x1} {y1} """.format(
                x1=self.turtle_pos[0],
                y1=self.turtle_pos[1],
                rule=rule,
                opacity = opacity)
            self.is_filling = True

    # Terminate the string for the svg path of the filled shape
    # Modified from aronma/ColabTurtle_2 github repo
    # The original _svg_lines_string was previously stored to be used when the fill is finished because the svg_fill_string will include
    # the svg code for the path generated between the begin and end fill commands.
    # the svg code for the path generated between the begin and end fill commands.
    def end_fill(self):
        """Fill the shape drawn after the call begin_fill()."""

        if self.is_filling:
            self.is_filling = False
            if self.is_pen_down:
                bddry = self.pen_color
            else:
                bddry = 'none'
            self.svg_fill_string += """" stroke-linecap="round" style="stroke:{pen};stroke-width:{size}" fill="{fillcolor}" />""".format(
                    fillcolor=self.fill_color,
                    pen = bddry,
                    size = self.pen_width)
            self.svg_lines_string = self.svg_lines_string_temp + self.svg_fill_string 
            self.win._updateDrawing(turtle=self, delay=False)         

    # Allow user to set the svg fill-rule. Options are only 'nonzero' or 'evenodd'. If no argument, return current fill-rule.
    # This can be overridden for an individual object by setting the fill-rule as an argument to begin_fill().
    def fillrule(self, rule=None):
        """Allows user to set the global svg fill-rule.

        Args:
            rule: (optional) Either evenodd or nonzero
                Default is current fill-rule
        """

        if rule is None:
            return self.fill_rule
        if not isinstance(rule,str):
            raise ValueError("The fill-rule must be 'nonzero' or 'evenodd'.")   
        rule = rule.lower()
        if not rule in ['evenodd','nonzero']:
            raise ValueError("The fill-rule must be 'nonzero' or 'evenodd'.")   
        self.fill_rule = rule

    # Allow user to set the svg fill-opacity. If no argument, return current fill-opacity.
    # This can be overridden for an individual object by setting the fill-opacity as an argument to begin_fill().
    def fillopacity(self, opacity=None):
        """Allows user to set the global svg fill-opacity.

        Args:
            opacity: (optional) a number between 0 and 1
                Default is current fill-opacity
        """

        if opacity is None:
            return self.fill_opacity
        if not isinstance(opacity,(int,float)):
            raise ValueError("The fill-opacity must be a number between 0 and 1.")
        if (opacity < 0) or (opacity > 1):
            raise ValueError("The fill-opacity should be between 0 and 1.")
        self.fill_opacity = opacity
        
    #===========================
    # Animation Controls
    #===========================

    # Delay execution of next object for given delay time (in seconds)
    def delay(self, delay_time):
       """Delays execution of next object
   
       Args:
       delay_time: positive number giving time in seconds
       """

       time.sleep(delay_time)

    # Turn off animation. Forward/back/circle makes turtle jump and likewise left/right make the turtle turn instantly.
    def animationOff(self):
        """Turns off animation
    
        Forward/back/circle makes the turtle jump and likewise left/right 
        makes the turtle turn instantly.
        """

        self.animate = False
        
    # Turn animation on.
    def animationOn(self):
        """Turns animation on"""

        self.animate = True        
        
        
        
        
#########################################
#  Helper functions for color control
#########################################        
        
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

