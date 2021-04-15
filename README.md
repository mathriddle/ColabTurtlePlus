
`begin_fill()` -> To be called just before drawing a shape to be filled.\
`end_fill()` -> Fill the shape drawn after the last call to begin_fill().

`showturtle() | st()` -> Makes the turtle visible.

`hideturtle() | ht()` -> Makes the turtle invisible.

`isvisible()` -> Returns whether turtle is currently visible as boolean.

```
bgcolor()
bgcolor(r,g,b)
bgcolor((r,g,b))
bgcolor(colorstring)
```
If no parameter given, returns the current background color as string. Else, changes the background color of the drawing area. The color can be given as three separate color arguments as in the RGB color encoding: red,green,blue. These three numbers can be given in a single tuple as well. The color can be given as a single color string, too! The following formats are accepted for this color string:
- HTML standard color names: 140 color names defined as standard ( https://www.w3schools.com/colors/colors_names.asp ) . Examples: `"red"`, `"black"`, `"magenta"`, `"cyan"` etc.
- Hex string with 3 or 6 digits, like `"#fff"`, `"FFF"`, `"#dfdfdf"`, `"#DFDFDF"`
- RGB string, like `"rgb(10 20 30)"`, `"rgb(10, 20, 30)"`

```
pencolor()
pencolor(r,g,b)
pencolor((r,g,b))
pencolor(colorstring)
```
Works the same as `bgcolor` for the pencolor.

```
fillcolor()
fillcolor(r,g,b)
fillcolor((r,g,b))
fillcolor(colorstring)
```
Works the same as `bgcolor` for the fillcolor.

`color()` -> Return the current pencolor and the current fillcolor\
`color(colorstring), color((r,g,b)` -> set both fillcolor and pencolor to the given value\
`color(string1,string2), color((r1,g1,b1),(r2,g2,b2))` -> Equivalent to pencolor(string1) and fillcolor(string2)

`showBorder(color)` -> Show a border around the graphics window. Default (no parameters) is gray. A color can be specified in a similar way as with `bgcolor`.

`width(w) | pensize(w)` -> Changes the width of the pen. If the parameter is omitted, returns the current pen width.

`distance(x,y) | distance((x,y))` -> Returns the turtle's distance to a given point x,y. The coordinates can be given separately or as a single tuple.

`clear()` -> Clear any drawing on the screen.

`write(obj, align=, font=)` -> Writes the string equivalent of any value to the screen. `align` and `font` **named** parameters can be given as arguments optionally. `align` must be one of `"left","center","right"`. It specifies where to put the text with respect to the turtle. `font` must be a tuple of three values like `(20, "Arial", "bold")`. The first value is the size, second value is the font family (only the ones that your browser natively supports must be used), the third value is font style that must be one of `"normal","bold","italic","underline"`.

`shape(sh)` -> Takes a shape name `sh` and transforms the main character's look. This library only has `'circle'`, `'turtle'`, and `'arrow'` shapes available. If no argument is supplied, this function returns the name of the current shape.

`setworldcoordinates(llx,lly,urx,ury)` -> Set up user-defined coordinate system and switch to mode “world”. This should be done immediately after initializing the turtle window.\
* `llx` : x-coordinate of lower left corner of canvas
* `lly` : y-coordinate of lower left corner of canvas
* `urx` : x-coordinate of upper right corner of canvas
* `ury` : y-coordinate of upper right corner of canvas

`window_width()` -> Return the width of the turtle window.

`window_height()` -> Return the height of the turtle window.
