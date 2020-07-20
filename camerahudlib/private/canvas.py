import maya.api.OpenMaya as OpenMaya


class Canvas(object):

    # canvas corner
    kLeftTop = 0
    kRightTop = 1
    kLeftBottom = 2
    kRightBottom = 3

    def __init__(self, x, y, width, height):

        """
        initialize canvas canvas

        :param x - x coordinate (int)
        :param y - y coordinate (int)
        :param width - canvas width (int)
        :param height - canvas height (int)
        """

        self._width = width
        self._height = height
        self._position = OpenMaya.MPoint(x, y, 0.0, 1.0)
        self._up = OpenMaya.MVector(0.0, 1.0, 0.0)
        self._aspect_ratio = 1.0
        self._left_top = OpenMaya.MPoint(0.0, 0.0, 0.0, 1.0)
        self._right_top = OpenMaya.MPoint(0.0, 0.0, 0.0, 1.0)
        self._left_bottom = OpenMaya.MPoint(0.0, 0.0, 0.0, 1.0)
        self._right_bottom = OpenMaya.MPoint(0.0, 0.0, 0.0, 1.0)

        self.refresh()

    def apply(self, x, y, width, height):

        """
        apply canvas

        :param x - x coordinate (int)
        :param y - y coordinate (int)
        :param width - canvas width (int)
        :param height - canvas height (int)
        """

        self._position.x = x
        self._position.y = y
        self._width = width
        self._height = height
        self.refresh()

    def refresh(self):

        """
        refresh canvas
        """

        # update aspect ratio
        if self._height != 0.0:
            self._aspect_ratio = float(self._width) / float(self._height)

        else:
            self._aspect_ratio = 1.0

        # update corner data
        self._left_top.x = self._position.x - (self._width * 0.5)
        self._left_top.y = self._position.y + (self._height * 0.5)

        self._right_top.x = self._position.x + (self._width * 0.5)
        self._right_top.y = self._position.y + (self._height * 0.5)

        self._left_bottom.x = self._position.x - (self._width * 0.5)
        self._left_bottom.y = self._position.y - (self._height * 0.5)

        self._right_bottom.x = self._position.x + (self._width * 0.5)
        self._right_bottom.y = self._position.y - (self._height * 0.5)

    def corner(self, corner):

        """
        get canvas corner point

        :param corner - canvas corner (canvas corner)
        :return - canvas cornet point (OpenMaya.MPoint)
        """

        if corner == Canvas.kLeftTop:
            return OpenMaya.MPoint(self._left_top)

        elif corner == Canvas.kRightTop:
            return OpenMaya.MPoint(self._right_top)

        elif corner == Canvas.kLeftBottom:
            return OpenMaya.MPoint(self._left_bottom)

        elif corner == Canvas.kRightBottom:
            return OpenMaya.MPoint(self._right_bottom)

        return OpenMaya.MPoint(0.0, 0.0, 0.0, 0.0)

    def position(self):

        """
        get canvas position point.

        :return - canvas cornet point (OpenMaya.MPoint)
        """

        return OpenMaya.MPoint(self._position)

    def setX(self, x):

        """
        set canvas x coordinate

        :param x - x coordinate (int)
        """

        self._position.x = x
        self.refresh()

    def setY(self, y):

        """
        set canvas y coordinate

        :param y - y coordinate (int)
        """

        self._position.y = y
        self.refresh()

    def move(self, x, y):

        """
        move canvas

        :param x - x coordinate (int)
        :param y - y coordinate (int)
        """

        self._position.x = x
        self._position.y = y
        self.refresh()

    def x(self):

        """
        get canvas x coordinate

        :return - x coordinate (int)
        """

        return self._position.x

    def y(self):

        """
        get canvas y coordinate

        :return - y coordinate (int)
        """

        return self._position.y

    def width(self):

        """
        get canvas width

        :return - canvas width (int)
        """

        return self._width

    def height(self):

        """
        get canvas height

        :return - canvas height (int)
        """

        return self._height

    def setHeight(self, height):

        """
        set canvas height

        :param height - canvas height (int)
        """

        self._height = height
        self.refresh()

    def setWidth(self, width):

        """
        set canvas width

        :param width - canvas width (int)
        """

        self._width = width
        self.refresh()

    def resize(self, width, height):

        """
        resize canvas.

        :param width - canvas width (int)
        :param height - canvas height (int)
        """

        self._width = width
        self._height = height
        self.refresh()

    def up(self):

        """
        get up direction

        :return - up direction vector (OpenMaya.MVector)
        """

        return OpenMaya.MVector(self._up)

    def __repr__(self):

        """
        get string representation of canvas

        :return - string representation (str)
        """

        return "Canvas(" + str(self._position.x) + ", " + str(self._position.y) + ", " + str(self._width) + ", " + str(self._height) + ")"

    def inherit(self, canvas):

        """
        inherit canvas

        :param canvas - canvas (Canvas)
        """

        self.apply(
            canvas.x(),
            canvas.y(),
            canvas.width(),
            canvas.height()
        )

    def aspectRatio(self):

        """
        get aspect ratio

        :return - aspect ratio (float)
        """

        return self._aspect_ratio

    def scale(self, scale_x, scale_y):

        """
        scale canvas rectangle

        :param scale_x - scale x (int)
        :param scale_y - scale y (int)
        """

        self._width *= scale_x
        self._height *= scale_y
        self.refresh()
