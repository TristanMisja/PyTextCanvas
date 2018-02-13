# PyTextCanvas by Al Sweigart al@inventwithpython.com


"""
TODO

Design considerations:
- Canvas must track steps for undo/redo
- Canvas must track the written areas for clipping. This won't include use of fill.


"""

import doctest
import textwrap
import collections

def print(*args, default=' '):
    # draw multiple layers of Canvas objects, print to stdout
    pass

def format(*args, default=' '):
    # draw multiple layers of Canvas objects, return as string
    pass


# Constants for headings
NORTH = 90.0
SOUTH = 270.0
EAST = 0.0
WEST = 180.0

# Based off of the CSS3 standard names. Data from James Bennett's webcolors module: https://github.com/ubernostrum/webcolors
COLOR_NAMES_TO_HEX = {'aliceblue': '#f0f8ff','antiquewhite': '#faebd7','aqua': '#00ffff','aquamarine': '#7fffd4','azure': '#f0ffff','beige': '#f5f5dc','bisque': '#ffe4c4','black': '#000000','blanchedalmond': '#ffebcd','blue': '#0000ff','blueviolet': '#8a2be2','brown': '#a52a2a','burlywood': '#deb887','cadetblue': '#5f9ea0','chartreuse': '#7fff00','chocolate': '#d2691e','coral': '#ff7f50','cornflowerblue': '#6495ed','cornsilk': '#fff8dc','crimson': '#dc143c','cyan': '#00ffff','darkblue': '#00008b','darkcyan': '#008b8b','darkgoldenrod': '#b8860b','darkgray': '#a9a9a9','darkgrey': '#a9a9a9','darkgreen': '#006400','darkkhaki': '#bdb76b','darkmagenta': '#8b008b','darkolivegreen': '#556b2f','darkorange': '#ff8c00','darkorchid': '#9932cc','darkred': '#8b0000','darksalmon': '#e9967a','darkseagreen': '#8fbc8f','darkslateblue': '#483d8b','darkslategray': '#2f4f4f','darkslategrey': '#2f4f4f','darkturquoise': '#00ced1','darkviolet': '#9400d3','deeppink': '#ff1493','deepskyblue': '#00bfff','dimgray': '#696969','dimgrey': '#696969','dodgerblue': '#1e90ff','firebrick': '#b22222','floralwhite': '#fffaf0','forestgreen': '#228b22','fuchsia': '#ff00ff','gainsboro': '#dcdcdc','ghostwhite': '#f8f8ff','gold': '#ffd700','goldenrod': '#daa520','gray': '#808080','grey': '#808080','green': '#008000','greenyellow': '#adff2f','honeydew': '#f0fff0','hotpink': '#ff69b4','indianred': '#cd5c5c','indigo': '#4b0082','ivory': '#fffff0','khaki': '#f0e68c','lavender': '#e6e6fa','lavenderblush': '#fff0f5','lawngreen': '#7cfc00','lemonchiffon': '#fffacd','lightblue': '#add8e6','lightcoral': '#f08080','lightcyan': '#e0ffff','lightgoldenrodyellow': '#fafad2','lightgray': '#d3d3d3','lightgrey': '#d3d3d3','lightgreen': '#90ee90','lightpink': '#ffb6c1','lightsalmon': '#ffa07a','lightseagreen': '#20b2aa','lightskyblue': '#87cefa','lightslategray': '#778899','lightslategrey': '#778899','lightsteelblue': '#b0c4de','lightyellow': '#ffffe0','lime': '#00ff00','limegreen': '#32cd32','linen': '#faf0e6','magenta': '#ff00ff','maroon': '#800000','mediumaquamarine': '#66cdaa','mediumblue': '#0000cd','mediumorchid': '#ba55d3','mediumpurple': '#9370db','mediumseagreen': '#3cb371','mediumslateblue': '#7b68ee','mediumspringgreen': '#00fa9a','mediumturquoise': '#48d1cc','mediumvioletred': '#c71585','midnightblue': '#191970','mintcream': '#f5fffa','mistyrose': '#ffe4e1','moccasin': '#ffe4b5','navajowhite': '#ffdead','navy': '#000080','oldlace': '#fdf5e6','olive': '#808000','olivedrab': '#6b8e23','orange': '#ffa500','orangered': '#ff4500','orchid': '#da70d6','palegoldenrod': '#eee8aa','palegreen': '#98fb98','paleturquoise': '#afeeee','palevioletred': '#db7093','papayawhip': '#ffefd5','peachpuff': '#ffdab9','per': '#cd853f','pink': '#ffc0cb','plum': '#dda0dd','powderblue': '#b0e0e6','purple': '#800080','red': '#ff0000','rosybrown': '#bc8f8f','royalblue': '#4169e1','saddlebrown': '#8b4513','salmon': '#fa8072','sandybrown': '#f4a460','seagreen': '#2e8b57','seashell': '#fff5ee','sienna': '#a0522d','silver': '#c0c0c0','skyblue': '#87ceeb','slateblue': '#6a5acd','slategray': '#708090','slategrey': '#708090','snow': '#fffafa','springgreen': '#00ff7f','steelblue': '#4682b4','tan': '#d2b48c','teal': '#008080','thistle': '#d8bfd8','tomato': '#ff6347','turquoise': '#40e0d0','violet': '#ee82ee','wheat': '#f5deb3','white': '#ffffff','whitesmoke': '#f5f5f5','yellow': '#ffff00','yellowgreen': '#9acd32',}

def normalizeHtmlColor(color):
    """Converts the `color` parameter to a standard '#ffffff' color string of
    a # followed by six hexadecimal digits. The `color` parameter can
    formatted as a CSS3 name, #ffffff, ffffff, #fff, or fff. If `color` is a
    valid HTML name (and appears as a key in the COLOR_NAMES_TO_HEX mapping),
    the lowercase form of the name is returned instead.

    TODO: Expand to include rgb triplet integers, and three percentages?

    >>> normalizeHtmlColor('white')
    'white'
    >>> normalizeHtmlColor('WHITE')
    'white'
    >>> normalizeHtmlColor('#ffffff')
    '#ffffff'
    >>> normalizeHtmlColor('#fff')
    '#ffffff'
    >>> normalizeHtmlColor('ffffff')
    '#ffffff'
    >>> normalizeHtmlColor('fff')
    '#ffffff'
    >>> normalizeHtmlColor('#abc')
    '#aabbcc'
    >>> normalizeHtmlColor('FFFFFF')
    '#ffffff'
    """
    if type(color) != str:
        raise TypeError('Parameter `color` must be of type str, not %s.' % (type(color)))

    color = color.lower() # normalize to lowercase

    if color in COLOR_NAMES_TO_HEX:
        return color

    if color.startswith('#'):
        color = color[1:] # remove the leading #

    try:
        int(color, 16) # check that it's a hexadecimal number
        if len(color) == 3:
            return '#' + color[0] + color[0] + color[1] + color[1] + color[2] + color[2] # normalize to '#ffffff' format
        elif len(color) == 6:
            return '#' + color
        else:
            raise ValueError('Parameter `color` must be a hexadecimal number or valid color name.')
    except ValueError:
        raise ValueError('Parameter `color` must be a hexadecimal number, not %s.' % (type(color)))

class ColorNameException(Exception):
    pass

# from http://www.roguebasin.com/index.php?title=Bresenham%27s_Line_Algorithm#Python
def getLinePoints(x1, y1, x2, y2):
    """Returns a list of (x, y) tuples of every point on a line between
    (x1, y1) and (x2, y2). The x and y values inside the tuple are integers.

    Line generated with the Bresenham algorithm.

    Args:
      x1 (int, float): The x coordinate of the line's start point.
      y1 (int, float): The y coordinate of the line's start point.
      x2 (int, float): The x coordinate of the line's end point.
      y2 (int, float): The y coordiante of the line's end point.

    Returns:
      [(x1, y1), (x2, y2), (x3, y3), ...]

    Example:
    >>> getLinePoints(0, 0, 6, 6)
    [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)]
    >>> getLinePoints(0, 0, 3, 6)
    [(0, 0), (0, 1), (1, 2), (1, 3), (2, 4), (2, 5), (3, 6)]
    >>> getLinePoints(3, 3, -3, -3)
    [(3, 3), (2, 2), (1, 1), (0, 0), (-1, -1), (-2, -2), (-3, -3)]
    """

    # TODO - convert this to a generator/iterable

    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
    points = []
    issteep = abs(y2-y1) > abs(x2-x1)
    if issteep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    rev = x1 > x2
    if rev:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
    deltax = x2 - x1
    deltay = abs(y2-y1)
    error = int(deltax / 2)
    y = y1
    ystep = None
    if y1 < y2:
        ystep = 1
    else:
        ystep = -1
    for x in range(x1, x2 + 1):
        if issteep:
            points.append((y, x))
        else:
            points.append((x, y))
        error -= deltay
        if error < 0:
            y += ystep
            error += deltax
    # Reverse the list if the coordinates were reversed
    if rev:
        points.reverse()
    return points


def is_inside(point_x, point_y, area_left, area_top, area_width, area_height):
    '''
    Returns True if the point of point_x, point_y is inside the area described.

    >>> is_inside(0, 0, 0, 0, 1, 1)
    True
    >>> is_inside(1, 0, 0, 0, 1, 1)
    False
    >>> is_inside(0, 1, 0, 0, 1, 1)
    False
    >>> is_inside(1, 1, 0, 0, 1, 1)
    False
    >>> is_inside(5, 5, 4, 4, 4, 4)
    True
    >>> is_inside(8, 8, 4, 4, 4, 4)
    False
    >>> is_inside(10, 10, 4, 4, 4, 4)
    False
    '''
    return (area_left <= point_x < area_left + area_width) and (area_top <= point_y < area_top + area_height)


class Canvas:
    def __init__(self, width=80, height=25, name=''):
        try:
            self._width = int(width)
        except (TypeError, ValueError):
            raise TypeError('`width` arg must be a string, a bytes-like object or a number, not %r' % (width.__class__.__name__))

        if self._width < 1:
            raise ValueError('`width` arg must be 1 or greater, not %r' % (width))

        try:
            self._height = int(height)
        except (TypeError, ValueError):
            raise TypeError('`height` arg must be a string, a bytes-like object or a number, not %r' % (height.__class__.__name__))

        if self._height < 1:
            raise ValueError('`height` arg must be 1 or greater, not %r' % (height))

        self.name = name
        self.chars = {}

        self.cursor = (0, 0) # NOTE: Internally, the cursor is set to two floats. These can be viewed with `position`, but `cursor` always returns ints.
        self.position = (0.0, 0.0) # NOTE: Unlike cursor, negative indexing can't be used for position.
        self.heading = EAST

        """ Heading:
               90
                |
          180 --*-- 0
                |
               270
        """
        self.penIsDown = False
        self.cursorChar = None

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        raise TypeError('%r width is immutable' % (self.__class__.__name__))


    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        raise TypeError('%r height is immutable' % (self.__class__.__name__))


    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if value is None:
            self._name = None
        else:
            self._name = str(value)


    @property
    def cursor(self):
        return self._cursor

    @cursor.setter
    def cursor(self, value):
        self._cursor = value


    @property
    def cursorx(self):
        return self._cursor[0]

    @cursorx.setter
    def cursorx(self, value):
        self._cursor = (value, self.cursory)


    @property
    def cursory(self):
        return self._cursor[1]

    @cursory.setter
    def cursory(self, value):
        self._cursor = (self.cursorx, value)





    def __repr__(self):
        """Return a limited representation of this Canvas object. The width,
        height, and name information is included, but not the foreground or
        background color. A 7-digit hexadecimal fingerprint of the content
        is given, based on the string representation of this Canvas object."""
        return '<%r object, width=%r, height=%r, name=%r>' % \
            (self.__class__.__name__, self._width, self._height, self._name)


    def __str__(self):
        """Return a multiline string representation of this Canvas object.
        The bottom row does not end with a newline character."""

        # TODO - make this thread safe
        result = []

        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(self.chars.get((x, y), ' '))
            result.append(''.join(row))
        return '\n'.join(result)


    def __len__(self):
        """Returns the length of this Canvas object, which is the length of
        its string as returned by str(), not the width * height.

        The string representation includes newline characters at the end of
        each row, except for the last row."""
        return (self.width * self.height) + (self.height - 1)

    def __iadd__(self):
        pass # TODO

    def __getitem__(self, key):
        """Return the character in this Canvas object, specified by `key`.
        The `key` can be a tuple of integers (x, y) or a single integer
        (treating the Canvas as a single-lined string). This integer can
        also be negative to return a character from the end of the string.

        The `key` can also be a slice object of two tuples which represents
        the top left and bottom right corners of the area to return as a new
        Canvas object. The slice cannot be made up of two integers.

        Leaving the first item in the slice defaults to the top left corner
        of the canvas, while leaving the second item in the slice efaults
        to the bottom right corner of the object. Using [:] is the syntax
        to get a copy of the canvas.

        This method only raises KeyError, never IndexError."""
        if isinstance(key, (int, tuple)):
            x, y = self._checkKey(key)
            return self.chars.get((x, y), None)
        elif isinstance(key, slice):
            pass
        else:
            raise KeyError('key must be an int or tuple of two ints')

    def __setitem__(self, key, value):
        if isinstance(key, (int, tuple)):
            if value is not None:
                value = str(value)
                if len(value) != 1:
                    raise ValueError('value must have a length of 1')

            x, y = self._checkKey(key)

            self.chars[(x, y)] = value
        elif isinstance(key, slice):
            pass
        else:
            raise KeyError('key must be an int or tuple of two ints')


    def _checkKey(self, key):
        """Returns an (x, y) tuple key for all integer/tuple key formats.

        >>> canvas = Canvas()
        >>> canvas._checkKey(0)
        (0, 0)
        >>> canvas._checkKey(1)
        (1, 0)
        >>> canvas._checkKey(80)
        (0, 1)
        >>> canvas._checkKey(-1)
        (79, 24)
        >>> canvas._checkKey(-2)
        (78, 24)
        >>> canvas._checkKey((0, 0))
        (0, 0)
        >>> canvas._checkKey((-1, 0))
        (79, 0)
        >>> canvas._checkKey((0, -1))
        (0, 24)
        >>> canvas._checkKey((-2, -2))
        (78, 23)
        """
        if isinstance(key, int):
            key = self._convertNegativeIndexToPositiveIndex(key)
            key = self._convertPositiveIntegerIndexToKeyTuple(key)

        x, y = self._convertNegativeTupleKeyToPositiveTupleKey(key)
        return x, y


    def _convertNegativeIndexToPositiveIndex(self, negKey):
        """Returns a positive integer index given a negative integer index.

        >>> canvas = Canvas()
        >>> canvas._convertNegativeIndexToPositiveIndex(0)
        0
        >>> canvas._convertNegativeIndexToPositiveIndex(-1)
        1999
        >>> canvas._convertNegativeIndexToPositiveIndex(-2)
        1998
        """
        if negKey < 0:
            if -negKey > (self.width * self.height):
                raise KeyError('key %r is out of range' % (negKey))

            return (self.width * self.height) + negKey
        else:
            return negKey # return the original key


    def _convertPositiveIntegerIndexToKeyTuple(self, intKey):
        """Returns an (x, y) tuple from an integer index.

        >>> canvas = Canvas()
        >>> canvas._convertPositiveIntegerIndexToKeyTuple(0)
        (0, 0)
        >>> canvas._convertPositiveIntegerIndexToKeyTuple(80)
        (0, 1)
        >>> canvas._convertPositiveIntegerIndexToKeyTuple(85)
        (5, 1)
        """
        if intKey < 0 or intKey >= (self.width * self.height):
            raise KeyError('key %r is out of range' % (intKey))

        return intKey % self.width, intKey // self.width


    def _convertNegativeTupleKeyToPositiveTupleKey(self, tupleKey):
        """Returns a tuple key with positive integers instead of negative
        integers.

        >>> canvas = Canvas()
        >>> canvas._convertNegativeTupleKeyToPositiveTupleKey((-1, -1))
        (79, 24)
        >>> canvas._convertNegativeTupleKeyToPositiveTupleKey((-1, 0))
        (79, 0)
        >>> canvas._convertNegativeTupleKeyToPositiveTupleKey((0, -1))
        (0, 24)
        >>> canvas._convertNegativeTupleKeyToPositiveTupleKey((0, 0))
        (0, 0)
        """
        # check that tuple key is well formed: two ints as (x, y)

        if len(tupleKey) != 2 or not isinstance(tupleKey[0], int) or not isinstance(tupleKey[1], int):
            raise KeyError('key must be an int or tuple of two ints')

        x, y = tupleKey # syntactic sugar

        # check x and y are in range
        if not (-self.width <= x < self.width):
            raise KeyError('key\'s x (`%r`) is out of range' % (x))
        if not (-self.height <= y < self.height):
            raise KeyError('key\'s y (`%r`) is out of range' % (y))

        # convert negative x & y to corresponding x & y
        if x < 0:
            x = self.width + x
        if y < 0:
            y = self.height + y

        return x, y

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        if other.width != self.width or other.height != self.height:
            return False

        for x in range(self.width):
            for y in range(self.height):
                if self[x, y] != other[x, y]:
                    return False
        return True

    def shift(self):
        pass

    def copy(self):
        pass

    def rotate(self):
        pass

    def scale(self):
        pass

    def flip(self, vertical=False, horizontal=False):
        pass

    def vflip(self):
        self.flip(vertical=True, horizontal=False)

    def hflip(self):
        self.flip(vertical=False, horizontal=True)

    def box(self):
        pass

    def fill(self):
        pass

    def floodfill(self):
        pass

    def blit(self, dstCanvas):
        pass

    def square(self):
        pass

    def rect(self, *args):
        pass

    def diamond(self, *args):
        pass

    def hexagon(self):
        pass

    def arrow(self):
        pass

    def corner(self):
        pass # must be "horizontal" or "vertical"

    def line(self):
        pass

    def lines(self):
        pass

    def polygon(self):
        pass

    def ellipse(self):
        pass

    def circle(self):
        pass

    def arc(self):
        pass

# TODO - should I use camelcase? I want to match the original Turtle module, but it uses, well, just lowercase.



    def print(self):
        pass


    # Methods dervied from turtle module:

    def forward(self, distance):
        pass

    fd = forward

    def backward(self, distance):
        pass

    bk = back = backward

    def right(self, angle):
        pass

    rt = right

    def left(self, angle):
        pass

    lt = left

    def goto(self, x, y=None):
        """Sets the curor to a specific xy point on the Canvas. `x` and `y`
        are the x and y coordinates (which can be ints or floats), or `x`
        is a tuple of two int/float values."""
        if isinstance(x, (int, float)):
            if not isinstance(y, (int, float)):
                raise TypeError('`x` and `y` arguments must be int or float')
        else:
            try:
                x, y = tuple(x)
            except TypeError:
                raise TypeError('argument must be iterable of two int or float values')
            if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
                raise TypeError('`x` and `y` arguments must be int or float')

        self.position = (x, y)

    setpost = setposition = goto

    def setx(self, x):
        pass

    def sety(self, y):
        pass

    def setheading(self, toAngle):
        pass

    seth = setheading

    def home(self):
        pass

    # NOTE: No undo in PyTextCanvas.

    def towards(self, x, y=None):
        pass

    def distance(self, x, y=None):
        pass

    def degrees(self):
        pass

    def radians(self):
        pass

    def penDown(self):
        pass

    pd = down = penDown

    def penUp(self):
        pass

    pu = up = penUp

    def penColor(self):
        pass

    def fillColor(self):
        pass

    """
    def filling(self):
        pass

    def begin_fill(self):
        pass

    def end_fill(self):
        pass
    """

    def reset(self):
        pass

    def clear(self):
        pass

    #def write(self):
    #    pass

    def showCursor(self):
        pass

    sc = showCursor

    def hideCursor(self):
        pass

    hc = hideCursor


    def _convertNegativeWidthIndexToPositiveIndex(self, negIndex):
        # check the type of negIndex
        if not isinstance(negIndex, int):
            raise TypeError('x index must be of type int, not %r' % (negIndex.__class__.__name__))

        # check that negIndex is in range
        if not (-self.width <= negIndex < self.width):
            raise ValueError('x index must be in between range of %s and %s' % (-self.width, self.width - 1))

        if negIndex < 0:
            return self.width + negIndex
        else:
            return negIndex # if negIndex is positive, just return it as is


    def _convertNegativeHeightIndexToPositiveIndex(self, negIndex):
        # check the type of negIndex
        if not isinstance(negIndex, int):
            raise TypeError('y index must be of type int, not %r' % (negIndex.__class__.__name__))

        # check that negIndex is in range
        if not (-self.height <= negIndex < self.height):
            raise ValueError('y index must be in between range of %s and %s' % (-self.height, self.height - 1))

        if negIndex < 0:
            return self.height + negIndex
        else:
            return negIndex # if negIndex is positive, just return it as is


class CanvasDict(dict):
    def __init__(self, width, height):
        pass # TODO

    def __getitem__(self):
        pass

    def __setitem__(self, value):
        pass

class Scene:
    def __init__(self, canvasesAndPositions):
        self.canvasesAndPositions = []
        # NOTE: The Canvas at index 0 is significant because it sets the size
        # of the entire Scene. All other Canvases will be truncated to fit.

        try:
            for i, canvasAndPosition in enumerate(self.canvasesAndPositions):
                canvas, top, left = canvasAndPosition
                if not isinstance(canvas, Canvas):
                    raise TypeError('item at index %s does not have Canvas object' % (i))
                if not isinstance(top, int):
                    raise TypeError('item at index %s does not have an int top value' % (i))
                if not isinstance(left, int):
                    raise TypeError('item at index %s does not have an int left value' % (i))
                self.canvasesAndPositions.appendCanvas(*(canvas, top, left))
        except TypeError:
            raise TypeError('%r object is not iterable' % (canvasesAndPositions.__class__.__name__))

    def __len__(self):
        if self.canvasesAndPositions == []:
            return 0
        else:
            return len(self.canvasesAndPositions[0][0])

    def __str__(self):
        pass # TODO

    def __eq__(self, other):
        pass # TODO - can be compared against Canvas objects and other Scene objects.

    # TODO - implement __getitem__ and __setitem__ and __del__ as well? How do we move the canvases around?

    def __iadd__(self, other):
        pass # TODO - calls appendCanvas.

    def appendCanvas(self, canvas, top, left):
        pass

    def moveCanvas(self, indexName, movex, movey):
        pass # used to move the canvas around



    def append(self, canvas, position):
        pass



if __name__ == '__main__':
    doctest.testmod()