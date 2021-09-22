from IPython.display import display, HTML
import time
import math
import re
import sys
import inspect

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
Added additional functions and capabilities from classic turtle.py package
Made use of SVG functions for animating the motion of the turtle
v1.4-v1.5 uploaded to PyPI

v2.0.0 Sept. 2021, Switched to using classes to allow for multiple turtles
Uploaded to PyPI

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
        {drawlines}
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

SPEED_TO_SEC_MAP = {0: 0, 1: 1.0, 2: 0.8, 3: 0.5, 4: 0.3, 5: 0.25, 6: 0.20, 7: 0.15, 8: 0.125, 9: 0.10, 10: 0.08, 11: 0.04, 12: 0.02, 13: 0.005}

#------------------------------------------------------------------------------------------------

def Screen():
    """Return the singleton screen object.
    If none exists at the moment, create a new one and return it,
    else return the existing one."""
    if Turtle._screen is None:
        Turtle._screen = _Screen()
    return Turtle._screen

class _Screen:
    def __init__(self):
        self._turtles = []
        self.window_size = DEFAULT_WINDOW_SIZE
        self._mode = DEFAULT_MODE
        if self._mode in ['standard','logo']:
            self.xmin,self.ymin,self.xmax,self.ymax = -self.window_size[0]/2,-self.window_size[1]/2,self.window_size[0]/2,self.window_size[1]/2
            self.xscale = self.yscale = 1  
        else:
            self.xmin = self.ymax = 0
            self.xscale = 1
            self.yscale = -1
        self._svg_drawlines_string = ""
        self.background_color = DEFAULT_BACKGROUND_COLOR
        self.border_color = DEFAULT_BORDER_COLOR
        self.drawing_window = display(HTML(self._generateSvgDrawing()), display_id=True)

    # Helper function that maps [0,13] speed values to ms delays
    def _speedToSec(self, speed):
        return SPEED_TO_SEC_MAP[speed]

    # Add to list of turtles when new object created
    def _add(self, turtle):
        self._turtles.append(turtle)
        self._updateDrawing() 

    #=======================
    # SVG functions
    #=======================
        
    # Helper function for generating svg string of all the turtles
    def _generateTurtlesSvgDrawing(self):
        svg = ""
        for turtle in self._turtles:
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
        if self._mode == "standard":
            degrees = turtle.turtle_degree - turtle.tilt_angle    
        elif self._mode == "world":
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
       
        svg = turtle.shapeDict[turtle.turtle_shape].format(
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
        for turtle in self._turtles:
            svg+=turtle.svg_lines_string 
        return svg

    # helper function for linking svg strings of text
    def _generateSvgFill(self):
        svg = ""
        for turtle in self._turtles:
            svg+=turtle.svg_fill_string 
        return svg
    
    # helper function for linking svg strings of text
    def _generateSvgDots(self):
        svg = ""
        for turtle in self._turtles:
            svg+=turtle.svg_dots_string 
        return svg
    
    # helper function for linking svg strings of text
    def _generateSvgStampsB(self):
        svg = ""
        for turtle in self._turtles:
            svg+=turtle.svg_stampsB_string 
        return svg
    
    # helper function for linking svg strings of text
    def _generateSvgStampsT(self):
        svg = ""
        for turtle in self._turtles:
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
                               drawlines=self._svg_drawlines_string,
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
        else:
            self.drawing_window.update(HTML(self._generateSvgDrawing()))

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
            if round(self.xscale,6) == round(abs(self.yscale),6):
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
                xpixunits = self._convertx(1)-self._convertx(0)  #length of 1 world unit along x-axis in pixels
                ypixunits = self._converty(1)-self._converty(0)  #length of 1 world unit along y-axis in pixels
                xstep = 10/(max(xpixunits,ypixunits))  #length of 10 pixels in world units 
                ystep = xstep
                dunits = s*xstep
                while s*units > 0:
                    dx = min(xstep,s*units)
                    dy = min(ystep,s*units)
                    temp_turtle_pos = (initial_pos[0] + s * dx * math.cos(alpha), initial_pos[1] - s * dy * math.sin(alpha))
                    turtle.turtle_pos = (self._convertx(temp_turtle_pos[0]), self._converty(temp_turtle_pos[1]))
                    if turtle.is_pen_down:
                        turtle.svg_lines_string += \
                        """<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke-linecap="round" style="stroke:{pcolor};stroke-width:{pwidth}" />""".format(
                            x1=self._convertx(initial_pos[0]),
                            y1=self._converty(initial_pos[1]),
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
            """<path d="M {x1} {y1} A {rx} {ry} 0 0 {s} {x2} {y2}" stroke-linecap="round" 
            fill="transparent" fill-opacity="0" style="stroke:{pcolor};stroke-width:{pwidth}"/>""".format(
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
        circle_center = (turtle.turtle_pos[0] + radius*self.xscale*math.sin(alpha), 
                         turtle.turtle_pos[1] - radius*abs(self.yscale)*math.cos(alpha))
        ending_point = (round(circle_center[0] - radius*self.xscale*math.sin(gamma),3) , 
                        round(circle_center[1] + radius*abs(self.yscale)*math.cos(gamma),3))
  
        self._arctoNewPosition(radius,ending_point,turtle)
   
        turtle.turtle_degree = (turtle.turtle_degree - s*degrees) % 360
        turtle.turtle_orient = turtle._turtleOrientation()
        if draw: self._updateDrawing(turtle=turtle)                      
   
    # Convert user coordinates to SVG coordinates
    def _convertx(self, x):
        return (x-self.xmin)*self.xscale 
    def _converty(self, y):
        return (self.ymax-y)*self.yscale                

    def drawline(self,x_1,y_1,x_2=None,y_2=None, color=None, width=None):
        """Draws a line between two points
    
        Args:
            x_1,y_1 : two numbers           or      a pair of numbers
            x_2,y_2 : two numbers                   a pair of numbers
            drawline(x_1,y_1,x_2,y_2)               drawline((x_1,y_1),(x_2,y_2))
            
            color : string color or tuple of RGB values
            wdith: positive number
       
        Draws a line from (x_1,y_1) to (x_2,y_2) in specified color and width.
        This line is independent of any turtle motion.
        """
        if isinstance(x_1,tuple) and isinstance(y_1,tuple) and x_2==None and y_2==None:
            if len(x_1) != 2 or len(y_1) != 2:
                raise ValueError('The tuple argument must be of length 2.')
            x_1,y = x_1
            x_2,y_2 = y_1
            y_1 = y
        if color is None:
            color = DEFAULT_PEN_COLOR
        else:
            color = self._processColor(color)
        if width is None:
            width = DEFAULT_PEN_WIDTH
        
        self._svg_drawlines_string += """<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke-lineca="round" style="stroke:{pencolor};stroke-width:{penwidth}" />""".format(
            x1=self._convertx(x_1),
            y1=self._converty(y_1),
            x2=self._convertx(x_2),
            y2=self._converty(y_2),
            pencolor = color,
            penwidth = width)
        self._updateDrawing()   
    line = drawline #alias 

    #=====================
    # Window Control
    #=====================

    # Change the background color of the drawing area
    # If color='none', the drawing window will have no background fill.
    # If no params, return the current background color
    def bgcolor(self, color = None, c2 = None, c3 = None):
        """Sets or returns the background color of the drawing area

        Args:
            a color string or three numbers in the range 0..255 
            or a 3-tuple of such numbers.
        """
        if color is None:
            return self.background_color
        elif c2 is not None:
            if c3 is None:
                raise ValueError('If the second argument is set, the third arguments must be set as well to complete the rgb set.')
            color = (color, c2, c3)

        self.background_color = self._processColor(color)
        self._updateDrawing(delay=False)     

    # Return turtle window width
    def window_width(self):
        """Returns the turtle window width"""
        return self.window_size[0]

    # Return turtle window height
    def window_height(self):
        """Returns the turtle window height"""
        return self.window_size[1]

    def setup(self, width=DEFAULT_WINDOW_SIZE[0], height=DEFAULT_WINDOW_SIZE[1]):
        """Set the size of the graphics window.

        Args:
            width: as integer a size in pixels. Default 800.
            height: as integer the height in pixels. Default is 600
            Note: Percentages are not used in this version.
        """
        if (isinstance(width,float) or isinstance(height,float)):
            raise ValueError('Percentages not used in this turtle version, only integer pixels.')
        elif not (isinstance(width,int) and isinstance(height,int)):
            raise ValueError('The width and height must be integers.')
        self.window_size = width,height
       
        w = width
        h = height
        if self._mode == "svg":
            self.xmin = self.ymax = 0
            self.xscale = 1
            self.yscale = -1
        elif self._mode != "world":
            self.xmin,self.ymin,self.xmax,self.ymax = -w/2,-h/2,w/2,h/2
            self.xscale = self.yscale = 1
        else: # mode==world
            self.xmin,self.ymin,self.xmax,self.ymax = -w/2,-h/2,w/2,h/2   
            self.xscale = width/(self.xmax-self.xmin)
            self.yscale = height/(self.ymax-self.ymin)
        for turtle in self._turtles:
            if self._mode != "world":
                turtle.turtle_pos = (w/2, h/2)
            else:
                turtle.turtle_pos = (self._convertx(0),self._converty(0))
        self._updateDrawing(delay=False)
    
        
    # Show a border around the graphics window. Default (no parameters) is gray. A border can be turned off by setting color='none'. 
    def showborder(self, color = None, c2 = None, c3 = None):
        """Shows a border around the graphics window.
    
        Args:
            a color string or three numbers in the range 0..255 
            or a 3-tuple of such numbers.
        
        Default (no argument values) is gray. A border can be turned off by 
        setting color='none' (or use hideborder())
        """
        if color is None:
            color = "gray"
        elif c2 is not None:
            if c3 is None:
                raise ValueError('If the second argument is set, the third arguments must be set as well to complete the rgb set.')
            color = (color, c2, c3)
        self.border_color = self._processColor(color)
        self._updateDrawing() 

    # Hide the border around the graphics window.    
    def hideborder(self):
        """Hides the border around the graphics window."""
        self.border_color = "none"
        self._updateDrawing() 

    # Clear all text and all turtles on the screen
    def clear(self):
        """Clears any text or drawing on the screen. Deletes all turtles.
        
        No argument.
           
        Note: This method is not available as a function. Use clearscreen.    
        """
        for turtle in self._turtles:
            turtle.svg_lines_string = ""
            turtle.svg_fill_string = ""
            turtle.svg_dots_string = ""
            turtle.svg_stampsB_string = ""
            turtle.svg_stampsT_string = ""
            turtle.stampdictB = {}
            turtle.stampdictT = {}
            turtle.stampnum = 0
            turtle.stamplist=[]
            turtle.is_filling = False
            self._svg_drawlines_string = ""
        self._turtles = []
        Turtle._pen = None
        self._updateDrawing()        

    # Reset all Turtles on the Screen to their initial state.
    def reset(self):
        """Resets all turtles to their initial state.
        
        No argument.
        
        Note: This method is not available as a function. Use resetscreen.
        """
        for turtle in self._turtles:
            turtle.reset()
    
    clearscreen = clear
    resetscreen = reset

    # Set turtle mode (“standard”, “logo”, “world”, or "svg") and reset the window. If mode is not given, current mode is returned.
    def mode(self, mode=None):
        """Sets turtle mode
    
        Arg:
            One of “standard”, “logo”, “world”, or "svg"
    
        "standard":
            Initial turtle heading is to the right (east) and positive
            angles measured counterclockwise with 0° pointing right.
        "logo":
            Initial turtle heading is upward (north) and positive angles
            are measured clockwise with 0° pointing up.
        "world":
            Used with user-defined coordinates. Setup is same as "standard".
        "svg": 
            This is a special mode to handle how the original ColabTurtle
            worked. The coordinate system is the same as that used with SVG.
            The upper left corner is (0,0) with positive x direction going
            left to right, and the positive y direction going top to bottom.
            Positive angles are measured clockwise with 0° pointing right.
        
        """
        if mode is None:
            return self._mode
        elif mode.lower() not in VALID_MODES:
            raise ValueError('Mode is invalid. Valid options are: ' + str(VALID_MODES))
        self._mode = mode.lower()
        w,h = self.window_size 
        if self._mode == "svg":
            self.xmin = self.ymax = 0
            self.xscale = 1
            self.yscale = -1
        elif self._mode != "world":
            self.xmin,self.ymin,self.xmax,self.ymax = -w/2,-h/2,w/2,h/2
            self.xscale = self.yscale = 1
        self.resetscreen()        

    # Set up user-defined coordinate system using lower left and upper right corners.
    # Screen is reset.
    # if the xscale and yscale are not equal, the aspect ratio of the axes and the
    # graphic window will differ.  
    def setworldcoordinates(self, llx, lly, urx, ury, aspect=False):
        """Sets up a user defined coordinate-system.
    
        Args:
            llx: a number, x-coordinate of lower left corner of window
            lly: a number, y-coordinate of lower left corner of window
            urx: a number, x-coordinate of upper right corner of window
            ury: a number, y-coordinate of upper right corner of window
            aspect: boolean - if True, window will be resized to maintain proper
                    aspect ratio with the axes
        """      
        if (urx-llx <= 0):
            raise ValueError("Lower left x-coordinate should be less than upper right x-coordinate")
        elif (ury-lly <= 0):
            raise ValueError("Lower left y-coordinate should be less than upper right y-coordinate")                     
        self.xmin = llx
        self.ymin = lly
        self.xmax = urx
        self.ymax = ury
        if aspect:
            if self.ymax-self.ymin > self.xmax-self.xmin:
                ysize = self.window_size[1]
                self.window_size = round((self.xmax-self.xmin)/(self.ymax-self.ymin)*ysize),ysize
            else:
                xsize = self.window_size[0]
                self.window_size = xsize, round((self.ymax-self.ymin)/(self.xmax-self.xmin)*xsize)
            self.xscale = self.yscale = self.window_size[0]/(self.xmax-self.xmin)
        else: 
            self.xscale = self.window_size[0]/(self.xmax-self.xmin)
            self.yscale = self.window_size[1]/(self.ymax-self.ymin)
        self.mode("world") 
        #self.clearscreen()

    def turtles(self):
        """Return the list of turtles on the screen."""
        return self._turtles

    def initializescreen(self,window=DEFAULT_WINDOW_SIZE,mode=DEFAULT_MODE):
        """Initializes the drawing window
    
        Args:
            window: (optional) the (width,height) in pixels
            mode: (optional) one of "standard, "logo", "world", or "sv
    
        The defaults are (800,600) and "standard".
    """
        if window is not None:
            if not (isinstance(window, tuple) and len(window) == 2 and isinstance(
                    window[0], int) and isinstance(window[1], int)):
                raise ValueError('Window must be a tuple of 2 integers')
            else:
                self.setup(window[0],window[1])
        if mode is not None:
            self.mode(mode)
    initializeTurtle = initializescreen

    ########################################################################################
    #  Helper functions for color control
    ########################################################################################        
        
    # Used to validate a color string
    def _validateColorString(self, color):
        if color in VALID_COLORS: # 140 predefined html color names
            return True
        if re.search("^#(?:[0-9a-fA-F]{3}){1,2}$", color): # 3 or 6 digit hex color code
            return True
        if re.search("rgb\(\s*(?:(?:\d{1,2}|1\d\d|2(?:[0-4]\d|5[0-5]))\s*,?){3}\)$", color): # rgb color code
            return True
        return False

    # Used to validate if a 3 tuple of integers is a valid RGB color
    def _validateColorTuple(self, color):
        if len(color) != 3:
            return False
        if not isinstance(color[0], int) or not isinstance(color[1], int) or not isinstance(color[2], int):
            return False
        if not 0 <= color[0] <= 255 or not 0 <= color[1] <= 255 or not 0 <= color[2] <= 255:
            return False
        return True

    # Helps validate color input to functions
    def _processColor(self,color):
        if isinstance(color, str):    
            if color == "": color = "none"
            color = color.lower().strip()
            if 'rgb' not in color: color = color.replace(" ","")
            if not self._validateColorString(color):
                err = 'Color ' + color + ' is invalid. It can be a known html color name, 3-6 digit hex string, or rgb string.'
                raise ValueError(err)
            return color
        elif isinstance(color, tuple):
            if not self._validateColorTuple(color):
                err = 'Color tuple ' + color + ' is invalid. It must be a tuple of three integers, which are in the interval [0,255]'
                raise ValueError(err)
            return 'rgb(' + str(color[0]) + ',' + str(color[1]) + ',' + str(color[2]) + ')'
        else:
            err = 'The color parameter ' + color + ' must be a color string or a tuple'
            raise ValueError(err)



#----------------------------------------------------------------------------------------------        
      
        
class RawTurtle:     
        
    def __init__(self, window=None):
        if window is None:
            self.screen = Screen()
        elif not isinstance(window, _Screen) == True:
            raise TypeError("window must be a Screen object")
        else:
            self.screen = window
        screen = self.screen
        self.turtle_speed = DEFAULT_SPEED
        self.is_turtle_visible = DEFAULT_TURTLE_VISIBILITY
        self.pen_color = DEFAULT_PEN_COLOR
        self.fill_color = DEFAULT_FILL_COLOR
        self.turtle_degree = DEFAULT_TURTLE_DEGREE if (screen._mode in ["standard","world"]) else (270 - DEFAULT_TURTLE_DEGREE)
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
        if screen._mode != "world":
            self.turtle_pos = (screen.window_size[0] / 2, screen.window_size[1] / 2)
        else:
            self.turtle_pos = (screen._convertx(0),screen._converty(0))                           
        self.timeout = screen._speedToSec(DEFAULT_SPEED)
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
        self.shapeDict = {"turtle":TURTLE_TURTLE_SVG_TEMPLATE, 
              "ring":TURTLE_RING_SVG_TEMPLATE, 
              "classic":TURTLE_CLASSIC_SVG_TEMPLATE,
              "arrow":TURTLE_ARROW_SVG_TEMPLATE,
              "square":TURTLE_SQUARE_SVG_TEMPLATE,
              "triangle":TURTLE_TRIANGLE_SVG_TEMPLATE,
              "circle":TURTLE_CIRCLE_SVG_TEMPLATE,
              "turtle2":TURTLE_TURTLE2_SVG_TEMPLATE,
              "blank":""}
        if screen._mode == "svg": self.shapeDict.update({"circle":TURTLE_RING_SVG_TEMPLATE})                                          
        screen._add(self)
        
        
        
#=================================================================================
# Turtle Motion
#=================================================================================

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
        new_pos = (self.turtle_pos[0] + units * self.screen.xscale * math.cos(alpha), self.turtle_pos[1] + units * abs(self.screen.yscale) * math.sin(alpha))
        self.screen._moveToNewPosition(new_pos,units, turtle=self)
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
            self.screen._updateDrawing(turtle=self)
        elif self.turtle_shape != 'ring' and self.stretchfactor[0]==self.stretchfactor[1]:
            stretchfactor_orig = self.stretchfactor
            template = self.shapeDict[self.turtle_shape]        
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
            self.shapeDict.update({self.turtle_shape:newtemplate})
            self.stretchfactor = 1,1
            self.timeout = self.timeout*abs(deg)/90+0.001
            self.screen._updateDrawing(self)
            self.turtle_degree = (self.turtle_degree + deg) % 360
            self.turtle_orient = self._turtleOrientation()
            self.shapeDict.update({self.turtle_shape:template})
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
                self.screen._updateDrawing(turtle=self)
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
                self.screen._arc(radius,min(15,extent),True, turtle=self)
                extent -= 15 
            # return to original position and redo circle for svg strings without animation
            self.svg_lines_string = svg_lines_string_temp
            self.svg_fill_string = svg_fill_string_temp
            self.turtle_degree = turtle_degree_orig
            self.turtle_pos = turtle_pos_orig
            while degrees > 0:
                self.screen._arc(radius,min(180,degrees),False, turtle=self)
                degrees -= 180 
            self.timeout = timeout_temp
        else:  # no animation
            extent = extent*self.angle_conv
            while extent > 0:
                self.screen._arc(radius,min(180,extent),True, turtle=self)
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
                color = self._processColor(size)
                size = self.pen_width + max(self.pen_width,4)
            else:
                color = self.pen_color
                if not size:
                    size = self.pen_width + max(self.pen_width,4)
        else:
            if size is None:
                size = self.pen_width + max(self.pen_width,4)
            color = self._processColor(color[0])
        self.svg_dots_string += """<circle cx="{cx}" cy="{cy}" r="{radius}" fill="{kolor}" fill-opacity="1" />""".format(
            radius=size/2,
            cx=self.turtle_pos[0],
            cy=self.turtle_pos[1],
            kolor=color)
        self.screen._updateDrawing(turtle = self)

    # Move along a regular polygon of size sides, with length being the length of each side. The steps indicates how many sides are drawn.
    # The initial and concluding angle is half of the exteral angle.
    # A positive length draws the polygon to the left of the turtle's current direction and a negative length draws it to the right
    # of the turtle's current direction.
    # Sets fillcolor to "none" if necessary and turns on filling so that the polygon is coded as one path for SVG purposes rather than
    # as a sequence of line segments.
    def regularPolygon(self, sides, length, steps=None):
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
        if not self.is_filling:
            polyfilling = True
            fillcolor_temp = self.fill_color
            self.begin_fill()
        alpha = (360/self.angle_conv)/sides
        if length < 0: 
            alpha = -alpha
            length = -length
        self.left(alpha/2)
        for _ in range(steps-1):
            self.forward(length)
            self.left(alpha)
        self.forward(length)
        self.left(alpha/2)
        if polyfilling: 
            self.fill_color = "none"
            self.end_fill()       
            self.fill_color = fillcolor_temp
            self.screen._updateDrawing(turtle=self)
 
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
        if self.screen._mode == "standard": 
            self.turtle_degree = (360 - alpha) % 360
            self.tilt_angle = -((turtle_angle_orig-self.tilt_angle+alpha) % 360)
        elif self.screen._mode == "logo":
            self.turtle_degree = (270 + alpha) % 360
            self.tilt_angle = turtle_angle_orig+self.tilt_angle-alpha-270
        elif self.screen._mode == "world":
            self.turtle_degree = (360 - alpha) % 360
        else: # mode = "svg"
            self.turtle_degree = alpha % 360
            self.tilt_angle = turtle_angle_orig+self.tilt_angle-alpha
        self.screen._moveToNewPosition((self.screen._convertx(x), self.screen._converty(y)), units, turtle=self)
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
            y = x[1]
            x = x[0]
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
        if self.screen._mode in ["standard","world"]: 
            new_degree = (360 - deg) 
        elif self.screen.mode == "logo":
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
            self.screen._updateDrawing(turtle=self)
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
        if self.screen._mode != 'svg':
            self.goto(0,0)
        else:
            self.goto( (self.screen.window_size[0] / 2, self.screen.window_size[1] / 2) )
        #_turtle_degree is always in degrees, but angle mode might be radians
        #divide by _angle_conv so angle sent to left or right is in the correct mode
        if self.screen._mode in ['standard','world']:
            if self.turtle_degree <= 180:
                self.left(self.turtle_degree/self.angle_conv)
            else:
                self.right((360-self.turtle_degree)/self.angle_conv)
            self.turtle_orient = self._turtleOrientation()
            self.screen._updateDrawing(turtle=self, delay=False)
        else:
            if self.turtle_degree < 90:
                self.left((self.turtle_degree+90)/self.angle_conv)
            elif self.turtle_degree< 270:
                self.right((270-self.turtle_degree)/self.angle_conv)
            else:
                self.left((self.turtle_degree-270)/self.angle_conv)        

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
        self.timeout = self.screen._speedToSec(self.turtle_speed)                

    # Call this function at end of turtle commands when speed=0 (no animation) so that final image is drawn
    def done(self):
        """Shows the final image when speed=0
    
        No argument
    
        speed = 0 displays final image with no animation. Need to
        call done() at the end so the final image is displayed.
        """
        self.screen.drawing_window.update(HTML(self.screen._generateSvgDrawing()))  
    update = done #alias        

    #=======================
    # Turtle Motion - Stamps
    #=======================

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
            self.stampdictT[self.stampnum] = self.screen._generateTurtlesSvgDrawing()
            self.svg_stampsT_string += self.stampdictT[self.stampnum]
        else:
            self.stampdictB[self.stampnum] = self.screen._generateOneSvgTurtle(turtle=self)
            self.svg_stampsB_string += self.stampdictB[self.stampnum]
        self.screen._updateDrawing(turtle=self, delay=False)
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
        self.screen._updateDrawing(turtle=self, delay=False)

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

        return(self.turtle_pos[0]/self.screen.xscale+self.screen.xmin)
    getx = xcor # alias

    # Retrieve the turtle's currrent 'y' y-coordinate in current coordinate system
    def ycor(self):
        """Return the turtle's y coordinate."""
   
        return(self.screen.ymax-self.turtle_pos[1]/self.screen.yscale)
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
        if self.screen._mode == "svg":
            dy = -dy
        result = round(math.atan2(dy,dx)*180.0/math.pi, 10) % 360.0
        if self.screen._mode in ["standard","world"]:
            angle = result
        elif self.screen._mode == "logo":
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

        if self.screen._mode in ["standard","world"]:
            angle = (360 - self.turtle_degree) % 360
        elif self.screen._mode == "logo":
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

    # If world coordinates are such that the aspect ratio of the axes does not match the
    # aspect ratio of the graphic window (xscale != yscale), then this helper function is used to 
    # set the orientation of the turtle to line up with the direction of motion in the 
    # world coordinates.
    def _turtleOrientation(self):
        if self.screen.xscale == abs(self.screen.yscale):
            return self.turtle_degree
        else:
            alpha = math.radians(self.heading()*self.angle_conv)
            Dxy = (self.screen._convertx(self.getx()+math.cos(alpha))-self.screen._convertx(self.getx()),
                   self.screen._converty(self.gety()+math.sin(alpha))-self.screen._converty(self.gety()))
            deg = math.degrees(math.atan2(-Dxy[1],Dxy[0])) % 360
            return 360-deg

    #========================================
    # Turtle Motion - Setting and Measurement
    #========================================

    # Set the angle measurement units to radians.
    def radians(self):
        """ Sets the angle measurement units to radians."""
        self.angle_mode = 'radians'
        self.angle_conv = 180/math.pi

    # Set the angle measurement units to degrees.
    def degrees(self):
        """ Sets the angle measurement units to radians."""
        self.angle_mode = 'degrees'
        self.angle_conv = 1  
             
#===============================================================================
# Pen Control 
#===============================================================================
                              
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

    # Change the width of the lines drawn by the turtle, in pixels
    # If the function is called without arguments, it returns the current width
    def pensize(self, width = None):
        """Sets or returns the line thickness.

        Aliases:  pensize | width

        Args:
            width: positive number

        Set the line thickness to width or return it. If no argument is given,
        current pensize is returned.
        """
        if width is None:
            return self.pen_width
        else:
            if not isinstance(width, (int,float)):
                raise ValueError('New width value must be an integer.')
            if not width > 0:
                raise ValueError('New width value must be positive.')
            self.pen_width = width
        self.screen._updateDrawing(turtle=self, delay=False)
    width = pensize  #alias

    # Return or set the pen's attributes
    def pen(self, dictname=None, **pendict):
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
        _pd = {"shown"          : self.is_turtle_visible,
               "pendown"        : self.is_pen_down,
               "pencolor"       : self.pen_color,
               "fillcolor"      : self.fill_color,
               "pensize"        : self.pen_width,
               "speed"          : self.turtle_speed,
               "stretchfactor"  : self.stretchfactor,
               "shearfactor"    : self.shear_factor,
               "tilt"           : self.tilt_angle,
               "outline"        : self.outline_width
              }
        if not (dictname or pendict):
            sf_tmp = self.shear_factor
            _pd["shearfactor"] = round(math.tan((360-self.shear_factor)*math.pi/180),8)
            return _pd
            _pd["shearfactor"] = sf_tmp
        if isinstance(dictname,dict):
            p = dictname
        else:
            p = {}

        p.update(pendict)
        if "shown" in p:
            self.is_turtle_visible = p["shown"]
        if "pendown" in p:
            self.is_pen_down = p["pendown"]
        if "pencolor" in p:
            self.pen_color = self._processColor(p["pencolor"])
        if "fillcolor" in p:
            self.fill_color = self._processColor(p["fillcolor"])
        if "pensize" in p:
            self.pen_width = p["pensize"]
        if "speed" in p:
            self.turtle_speed = p["speed"]
            self.timeout = self.screen._speedToSec(self.turtle_speed)
        if "stretchfactor" in p:
            sf = p["stretchfactor"]
            if isinstance(sf, (int,float)):
                sf = (sf,sf)
            self.stretchfactor = sf
        if "shearfactor" in p:
            alpha = math.atan(p["shearfactor"])*180/math.pi
            self.shear_factor = (360 - alpha) % 360
            p["shearfactor"] = self.shear_factor
        if "tilt" in p:
            self.tilt_angle = p["tilt"]*self.angle_conv
        if "outline" in p:
           self.outline_width = p["outline"]
        self.screen._updateDrawing(turtle=self, delay=False)


    def isdown(self):
        """Return True if pen is down, False if it's up."""

        return self.is_pen_down

    #============================
    # Pen Control - Color Control
    #============================   

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
                self.pen_color = self.fill_color = self._processColor(args[0])
            elif narg == 2:
                self.pen_color = self._processColor(args[0])
                self.fill_color = self._processColor(args[1])
            elif narg == 3:
                kolor = (args[0],args[1],args[2])
                self.pen_color = self.fill_color = self._processColor(kolor)
            else:
                raise ValueError('Syntax: color(colorstring), color((r,g,b)), color(r,g,b), color(string1,string2), color((r1,g1,b1),(r2,g2,b2))')
        else:
            return self.pen_color, self.fill_color
        self.screen._updateDrawing(turtle=self, delay=False)              
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

        self.pen_color = self._processColor(color)
        self.screen._updateDrawing(turtle=self, delay=False)    

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

        self.fill_color = self._processColor(color)
        self.screen._updateDrawing(turtle=self, delay=False)
        
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
            self.screen._updateDrawing(turtle=self, delay=False)         

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
# More drawing contols
#===========================

    # Delete the turtle’s drawings from the screen, re-center the turtle and set (most) variables to the default values.
    def reset(self):
        """Resets the turtle to its initial state and clears drawing."""

        self.is_turtle_visible = True
        self.pen_color = DEFAULT_PEN_COLOR
        self.fill_color = DEFAULT_FILL_COLOR
        self.is_pen_down = True
        self.pen_width = DEFAULT_PEN_WIDTH
        self.stretchfactor = DEFAULT_STRETCHFACTOR
        self.shear_factor = DEFAULT_SHEARFACTOR
        self.tilt_angle = DEFAULT_TILT_ANGLE
        self.outline_width = DEFAULT_OUTLINE_WIDTH
        self.svg_lines_string = ""
        self.svg_fill_string = ""
        self.svg_dots_string = ""
        self.svg_stampsB_string = ""
        self.svg_stampsT_string = ""
        self.stampdictB = {}
        self.stampdictT = {}
        self.stampnum = 0
        self.stamplist = []
        self.turtle_degree = DEFAULT_TURTLE_DEGREE if (self.screen._mode in ["standard","world"]) else (270 - DEFAULT_TURTLE_DEGREE)
        self.turtle_orient = self.turtle_degree
        if self.screen._mode != "world":
            self.turtle_pos = (self.screen.window_size[0] / 2, self.screen.window_size[1] / 2)
        else:
            self.turtle_pos = (self.screen._convertx(0),self.screen._converty(0))
        self.screen._updateDrawing(turtle=self, delay=False)

    # Clear text and turtle
    def clear(self):
        """Delete the turtle's drawings from the screen. Do not move turtle.

        No arguments.

        Delete the turtle's drawings from the screen. Do not move turtle.
        State and position of the turtle as well as drawings of other
        turtles are not affected.
        """
        self.svg_lines_string = ""
        self.svg_fill_string = ""
        self.svg_dots_string = ""
        self.svg_stampsB_string = ""
        self.svg_stampsT_string = ""
        self.stampdictB = {}
        self.stampdictT = {}
        self.stampnum = 0
        self.stamplist=[]
        self.is_filling = False
        self.screen._updateDrawing(turtle=self, delay=False) 

    def write(self, obj, **kwargs):
        """Write text at the current turtle position.

        Args:
            obj: string which is to be written to the TurtleScreen
            **kwargs should be 
                align: (optional) one of the strings "left", "center" or right"
                font: (optional) a triple (fontname, fontsize, fonttype)
                      fonttype can be 'bold', 'italic', 'underline', or 'normal'

        Write the string text at the current turtle position according 
        to align ("left", "center" or right") and with the given font.
    
        Defaults are left, ('Arial',12, 'normal')
        """

        # The move argument in turtle.py is ignored here. The ImageFont in the Pillow package does not
        # seem to work in Colab because it cannot access the necessary font metric information.
        # Perhaps there is way to use SVG attributes to determine the length of the string.
        text = str(obj)
        font_size = 12
        font_family = 'Arial'
        font_type = 'normal'
        align = 'start'
        anchor = {'left':'start','center':'middle','right':'end'}
        if 'align' in kwargs:
            if kwargs['align'] in ('left', 'center', 'right'):
                align = anchor[kwargs['align']]
            else:
                raise ValueError('Align parameter must be one of left, center, or right.')
        if 'font' in kwargs:
            font = kwargs["font"]
            if len(font) != 3 or font[2] not in {'bold','italic','underline','normal'}:
                raise ValueError('Font parameter must be a triplet consisting of font family (str), font size (int), and font type (str). Font type can be one of {bold, italic, underline, normal}')
            elif isinstance(font[0], str) == True and isinstance(font[1], int) == True:
                font_family = font[0]           
                font_size = font[1]
                font_type = font[2]
            elif isinstance(font[0], int) == True and isinstance(font[1], str) == True:
                font_family = font[1]           
                font_size = font[0]
                font_type = font[2]
            else:
                raise ValueError('Font parameter must be a triplet consisting of font family (str), font size (int), and font type (str).')                
        style_string = ""
        style_string += "font-size:" + str(font_size) + "px;"
        style_string += "font-family:'" + font_family + "';"

        if font_type == 'bold':
            style_string += "font-weight:bold;"
        elif font_type == 'italic':
            style_string += "font-style:italic;"
        elif font_type == 'underline':
            style_string += "text-decoration: underline;"
            
        self.svg_lines_string += """<text x="{x}" y="{y}" fill="{strcolor}" text-anchor="{align}" style="{style}">{text}</text>""".format(
            x=self.turtle_pos[0], 
            y=self.turtle_pos[1], 
            text=text, 
            strcolor=self.pen_color, 
            align=align, 
            style=style_string)
        
        self.screen._updateDrawing(turtle=self)        

#========================================================================
# Turtle State
#========================================================================        
        
    #==========================
    # Turtle State - Visibility
    #==========================

    # Switch turtle visibility to ON
    def showturtle(self):
        """Makes the turtle visible.

        Aliases: showturtle | st
        """
        self.is_turtle_visible = True
        self.screen._updateDrawing(turtle=self, delay=False)
    st = showturtle # alias

    # Switch turtle visibility to OFF
    def hideturtle(self):
        """Makes the turtle invisible.

        Aliases: hideturtle | ht
        """
        self.is_turtle_visible = False
        self.screen._updateDrawing(turtle=self, delay=False)
    ht = hideturtle # alias

    def isvisible(self):
        """Return True if the Turtle is shown, False if it's hidden."""

        return self.is_turtle_visible

    #==========================
    # Turtle State - Appearance
    #==========================

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
        self.screen._updateDrawing(turtle=self)
 
    # Scale the size of the turtle
    # stretch_wid scales perpendicular to orientation
    # stretch_len scales in direction of turtle's orientation
    def shapesize(self, stretch_wid=None, stretch_len=None, outline=None):
        """Sets/returns turtle's stretchfactors/outline.

        Args:
            stretch_wid: positive number
            stretch_len: positive number
            outline: positive number

        Returns or sets the pen's attributes x/y-stretchfactors and/or outline.
        The turtle will be displayed stretched according to its stretchfactors.
        stretch_wid is _stretchfactor perpendicular to orientation
        stretch_len is _stretchfactor in direction of turtles orientation.
        outline determines the width of the shapes's outline.
        """
        if stretch_wid is stretch_len is outline is None:
            return self.stretchfactor[0], self.stretchfactor[1], self.outline_width
        if stretch_wid == 0 or stretch_len == 0:
            raise ValueError("stretch_wid/stretch_len must not be zero")
        if stretch_wid is not None:
            if not isinstance(stretch_wid, (int,float)):
                raise ValueError('The stretch_wid position must be a number.')        
            if stretch_len is None:
                self.stretchfactor = stretch_wid, stretch_wid
            else:
                if not isinstance(stretch_len, (int,float)):
                    raise ValueError('The stretch_len position must be a number.')                
                self.stretchfactor = stretch_wid, stretch_len
        elif stretch_len is not None:
            if not isinstance(stretch_len, (int,float)):
                raise ValueError('The stretch_len position must be a number.')         
            self.stretchfactor = stretch_len, stretch_len
        if outline is None:
            outline = self.outline_width
        elif not isinstance(outline, (int,float)):
            raise ValueError('The outline must be a positive number.')        
        self.outline_width = outline   
    turtlesize = shapesize #alias

    # Set or return the current shearfactor. Shear the turtleshape according to the given shearfactor shear, which is the tangent of the shear angle. 
    # Do not change the turtle’s heading (direction of movement). If shear is not given: return the current shearfactor, i. e. 
    # the tangent of the shear angle, by which lines parallel to the heading of the turtle are sheared.
    def shearfactor(self, shear=None):
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
        if shear is None:              
            return round(math.tan((360-_shear_factor)*math.pi/180),8)
        alpha = math.atan(shear)*180/math.pi
        self.shear_factor = (360 - alpha) % 360    
 
    # Rotate the turtleshape to point in the direction specified by angle, regardless of its current tilt-angle.
    # DO NOT change the turtle's heading (direction of movement). Deprecated since Python version 3.1.
    def settiltangle(self, angle):
        """Rotates the turtleshape to point in the specified direction

        Args:
            angle: number

        Rotates the turtleshape to point in the direction specified by angle,
        regardless of its current tilt-angle. DOES NOT change the turtle's
        heading (direction of movement).
    
        Deprecated since Python version 3.1.
        """
        self.tilt_angle = angle*self.angle_conv
        self.screen._updateDrawing(turtle=self,delay=False)  

    # Set or return the current tilt-angle. 
    # If angle is given, rotate the turtleshape to point in the direction specified by angle, regardless of its current tilt-angle. 
    # Do not change the turtle’s heading (direction of movement). If angle is not given: return the current tilt-angle, 
    # i. e. the angle between the orientation of the turtleshape and the heading of the turtle (its direction of movement).
    def tiltangle(self, angle=None):
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
        if angle == None:
            return self.tilt_angle
        if self.turtle_speed != 0 and self.animate: 
            turtle_degree_temp = self.turtle_degree
            if self.screen._mode in ["standard","world"]:
                self.left(-(self.tilt_angle-angle*self.angle_conv))
            else:
                self.right(self.tilt_angle-angle*self.angle_conv)
            self.turtle_degree = turtle_degree_temp
            self.tilt_angle = angle*self.angle_conv
        else:
            self.tilt_angle = angle*_angle_conv
            self.screen._updateDrawing(turtle=self, delay=False) 

    # Rotate the turtle shape by angle from its current tilt-angle, but do not change the turtle’s heading (direction of movement).
    def tilt(self, angle):
        """Rotates the turtleshape by angle.

        Args:
            angle: a number

        Rotates the turtle shape by angle from its current tilt-angle,
        but does NOT change the turtle's heading (direction of movement).
        """
        if self.turtle_speed != 0 and self.animate and self.screen._mode != "world":
            turtle_degree_temp = self.turtle_degree
            if self.screen._mode == "standard":
                self.left(angle*self.angle_conv)
            else:
                self.right(angle*self.angle_conv)
            self.turtle_degree = turtle_degree_temp
            self.tilt_angle += angle*self.angle_conv
        else:
            self.tilt_angle += angle*self.angle_conv
            self.screen._updateDrawing(turtle=self, delay=False)    

    def delete(self):
        """Deletes the turtle from the drawing window"""
        self.screen._turtles.remove(self)
        self.screen._updateDrawing(turtle=self, delay=False)

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

    def clone(self):
        screen = self.screen
        cloneTurtle = Turtle()
        cloneTurtle.ht()        
        x,y = self.position()
        cloneTurtle.turtle_pos = screen._convertx(x),screen._converty(y)        
        cloneTurtle.shape(self.shape())
        cloneTurtle.pen(self.pen())
        return cloneTurtle
        
    ########################################################################################
    #  Helper functions for color control 
    ########################################################################################        
        
    # Used to validate a color string
    def _validateColorString(self,color):
        return self.screen._validadeColorString(color)

    # Used to validate if a 3 tuple of integers is a valid RGB color
    def _validateColorTuple(self, color):
        return self.screen._validateColorTuple(color)

    # Helps validate color input to functions
    def _processColor(self, color):
        return self.screen._processColor(color)

class Turtle(RawTurtle):
    _pen = None
    _screen = None 
    
    def __init__(self):
        if Turtle._screen is None:
            Turtle._screen = Screen()
        RawTurtle.__init__(self, Turtle._screen)   


# Set the defaults used in the original version of ColabTurtle package
def oldDefaults():
    """Set the defaults used in the original version of ColabTurtle package."""

    global DEFAULT_BACKGROUND_COLOR
    global DEFAULT_PEN_COLOR
    global DEFAULT_PEN_WIDTH
    global DEFAULT_MODE
    global DEFAULT_TURTLE_SHAPE
    global DEFAULT_WINDOW_SIZE
    global DEFAULT_SPEED
    
    DEFAULT_BACKGROUND_COLOR = "black"
    DEFAULT_PEN_COLOR = "white"
    DEFAULT_PEN_WIDTH = 4
    DEFAULT_MODE = 'svg'
    DEFAULT_TURTLE_SHAPE = "turtle"
    DEFAULT_WINDOW_SIZE = (800, 500)
    DEFAULT_SPEED = 4
   
# Get the color corresponding to position n in the valid color list
def getcolor(n):
    """ Returns the color string in the valid color list at position n
    
    Args:
        n: an integer between 0 and 139
    
    Returns:
        str: color string in the valid color list at position n
    """

    if not isinstance(n,(int,float)):
        raise ValueError("color index must be an integer between 0 and 139")
    n = int(round(n))
    if (n < 0) or (n > 139):
        raise valueError("color index must be an integer between 0 and 139")
    return VALID_COLORS[n]


_tg_screen_functions = ['bgcolor', 'clearscreen', 'drawline', 'hideborder', 
         'initializescreen','initializeTurtle', 'showSVG', 'saveSVG',  'line',  'mode', 'resetscreen',  'setup', 
         'setworldcoordinates', 'showborder', 'turtles',  'window_width', 'window_height' ]

_tg_turtle_functions = ['animationOff', 'animationOn', 'bk', 'back', 'backward', 'begin_fill',
       'circle', 'clear', 'clearstamp', 'clearstamps', 'color', 'degrees', 'delay', 'distance', 'done',  
       'dot', 'down', 'end_fill', 'face', 'fd', 'fillcolor', 'filling', 'fillopacity', 'fillrule', 'forward',  
       'getheading', 'getx', 'gety', 'goto', 'heading', 'hideturtle', 'home', 'ht', 'isdown',
       'isvisible', 'jumpto', 'left', 'lt', 'pd', 'pen', 'pencolor', 'pensize', 'pendown', 'penup', 'pos', 
       'position',  'pu', 'radians', 'regularPolygon', 'reset', 'right', 'rt',  'setheading', 'seth',  
       'setpos', 'setposition', 'settiltangle', 'setx','sety', 'shape', 'shapesize', 'shearfactor',  
       'showturtle', 'speed', 'st', 'stamp', 'tilt', 'tiltangle', 'turtlesize', 'towards', 'up', 'update',  
       'width', 'write', 'xcor', 'ycor' ]

def _getmethparlist(ob):
    """Get strings describing the arguments for the given object

    Returns a pair of strings representing function parameter lists
    including parenthesis.  The first string is suitable for use in
    function definition and the second is suitable for use in function
    call.  The "self" parameter is not included.
    """
    defText = callText = ""
    # bit of a hack for methods - turn it into a function
    # but we drop the "self" param.
    # Try and build one for Python defined functions
    args, varargs, varkw = inspect.getargs(ob.__code__)
    items2 = args[1:]
    realArgs = args[1:]
    defaults = ob.__defaults__ or []
    defaults = ["=%r" % (value,) for value in defaults]
    defaults = [""] * (len(realArgs)-len(defaults)) + defaults
    items1 = [arg + dflt for arg, dflt in zip(realArgs, defaults)]
    if varargs is not None:
        items1.append("*" + varargs)
        items2.append("*" + varargs)
    if varkw is not None:
        items1.append("**" + varkw)
        items2.append("**" + varkw)
    defText = ", ".join(items1)
    defText = "(%s)" % defText
    callText = ", ".join(items2)
    callText = "(%s)" % callText
    return defText, callText

def _turtle_docrevise(docstr):
    """To reduce docstrings from RawTurtle class for functions
    """

    if docstr is None:
        return None
    turtlename = "turtle"
    newdocstr = docstr.replace("%s." % turtlename,"")
    parexp = re.compile(r' \(.+ %s\):' % turtlename)
    newdocstr = parexp.sub(":", newdocstr)
    return newdocstr

def _screen_docrevise(docstr):
    """To reduce docstrings from TurtleScreen class for functions
    """

    if docstr is None:
        return None
    screenname = "screen"
    newdocstr = docstr.replace("%s." % screenname,"")
    parexp = re.compile(r' \(.+ %s\):' % screenname)
    newdocstr = parexp.sub(":", newdocstr)
    return newdocstr


__func_body = """\
def {name}{paramslist}:
    if {obj} is None:
        {obj} = {init}
    return {obj}.{name}{argslist}
"""

def _make_global_funcs(functions, cls, obj, init, docrevise):
    for methodname in functions:
        try:
            method = getattr(cls, methodname)
        except AttributeError:
            print("method name missing:", methodname)
            continue
        pl1, pl2 = _getmethparlist(method)
        defstr = __func_body.format(obj=obj, init=init, name=methodname, paramslist=pl1, argslist=pl2)
        exec(defstr, globals())
        globals()[methodname].__doc__ = docrevise(method.__doc__)

_make_global_funcs(_tg_turtle_functions, Turtle, 'Turtle._pen', 'Turtle()',_turtle_docrevise)

_make_global_funcs(_tg_screen_functions, _Screen, 'Turtle._screen', 'Screen()',_screen_docrevise)



