import math
import maya.api.OpenMaya as OpenMaya
import maya.OpenMayaRender as OpenMayaRender_old
from camerahudlib import constants
from camerahudlib.private.qt import Qt
from camerahudlib.private.qt.Qt import QtCore, QtGui


class GlPainter(object):

    def __init__(self, view):

        """
        initialize painter

        :param view - target view (OpenMayaUI.M3dView)
        """

        self._view = view
        self._is_begin = False

        self._gl_function_table = None
        self._gl_renderer = None

        self._font_size = 10.0
        self._font_stretch = 2.0
        self._font_weight = constants.kFontStyleWeightLight
        self._font_incline = constants.kFontStyleInclineNormal
        self._font_line = constants.kFontStyleLineNone
        self._font = QtGui.QFont()
        self._font_name = "Arial"
        self._font_metric = QtGui.QFontMetrics(self._font)

        q_color = QtGui.QColor(0.0, 0.0, 0.0)
        self._pen = QtGui.QPen(q_color)
        self._brush = QtGui.QBrush(q_color)

        self._painter = QtGui.QPainter()

    def beginDrawable(self, view=None):

        """
        begin paint

        :param view - target view (OpenMayaUI.M3dView)
        """

        if self._is_begin is False:
            if view is not None:
                self._view = view

            self._view.beginGL()

            self._is_begin = True
            self._gl_renderer = OpenMayaRender_old.MHardwareRenderer.theRenderer()
            self._gl_function_table = self._gl_renderer.glFunctionTable()

            self._gl_function_table.glPushAttrib(OpenMayaRender_old.MGL_ALL_ATTRIB_BITS)

            self._gl_function_table.glMatrixMode(OpenMayaRender_old.MGL_MODELVIEW)
            self._gl_function_table.glPushMatrix()

            self._gl_function_table.glMatrixMode(OpenMayaRender_old.MGL_PROJECTION)
            self._gl_function_table.glPushMatrix()
            self._gl_function_table.glLoadIdentity()

            self._gl_function_table.glOrtho(
                0.0, self._view.portWidth(),
                0.0, self._view.portHeight(),
                0.0, 100.0
            )

            self._gl_function_table.glMatrixMode(OpenMayaRender_old.MGL_MODELVIEW)
            self._gl_function_table.glLoadIdentity()

            self._gl_function_table.glBlendFunc(OpenMayaRender_old.MGL_SRC_ALPHA, OpenMayaRender_old.MGL_ONE_MINUS_SRC_ALPHA)
            self._gl_function_table.glEnable(OpenMayaRender_old.MGL_BLEND)
            self._gl_function_table.glDisable(OpenMayaRender_old.MGL_CULL_VERTEX_EXT)

    def endDrawable(self):

        """
        end paint
        """

        if self._is_begin:
            self._gl_function_table.glEnable(OpenMayaRender_old.MGL_CULL_VERTEX_EXT)
            self._gl_function_table.glDisable(OpenMayaRender_old.MGL_BLEND)

            self._gl_function_table.glMatrixMode(OpenMayaRender_old.MGL_PROJECTION)
            self._gl_function_table.glPopMatrix()
            self._gl_function_table.glMatrixMode(OpenMayaRender_old.MGL_MODELVIEW)
            self._gl_function_table.glPopMatrix()

            self._gl_function_table.glPopAttrib()

            self._view.endGL()
            self._is_begin = False

    def isBegin(self):

        """
        is begin

        :return - is begin paint (bool)
        """

        if self._is_begin and self._gl_function_table is not None:
            return True

        return False

    def isValid(self):

        """
        is valid

        :return - is valid (bool)
        """

        if self._is_begin and self._gl_function_table is not None:
            return True

        elif self._is_begin:
            return False

        return True

    def setColor(self, color):

        """
        set color

        :param color - color (OpenMaya.MColor)
        """

        if self.isBegin():
            self._gl_function_table.glColor4f(color.r, color.g, color.b, color.a)
            q_color = QtGui.QColor(color.r * 255, color.g * 255, color.b * 255, color.a * 255)
            self._pen = QtGui.QPen(q_color)
            self._brush = QtGui.QBrush(q_color)

    def setFontSize(self, size):

        """
        set font size

        :param size - font size (int)
        """

        if self.isBegin():
            self._font_size = size
            self._font.setPixelSize(size)
            self._font_metric = QtGui.QFontMetrics(self._font)

    def setFontIncline(self, incline):

        """
        set font incline

        :param incline - font incline (OpenMayaRender.MUIDrawManager.TextIncline)
        """

        if self.isBegin():
            self._font_incline = incline
            if incline == constants.kFontStyleInclineNormal:
                self._font.setItalic(False)

            elif incline == constants.KFontStyleInclineItalic:
                self._font.setItalic(True)

    def setFontWeight(self, weight):

        """
        set font weight

        :param weight - font weight (int)
        """

        if self.isBegin():
            self._font_weight = weight

            if self._font_weight == constants.kFontStyleWeightLight:
                weight = QtGui.QFont.Light

            else:
                weight = QtGui.QFont.Bold

            self._font.setWeight(weight)
            self._font_metric = QtGui.QFontMetrics(self._font)

    def setFontStretch(self, stretch):

        """
        set font stretch

        :param stretch - font stretch (int)
        """

        if self.isBegin():
            self._font_stretch = stretch
            self._font.setStretch(stretch)
            self._font_metric = QtGui.QFontMetrics(self._font)

    def setFontLine(self, line):

        """
        set font line

        :param line - font line (OpenMayaRender.MUIDrawManager.TextLine)
        """

        if self.isBegin():
            self._font_line = line
            if line == constants.kFontStyleLineNone:
                self._font.setOverline(False)
                self._font.setUnderline(False)
                self._font.setStrikeOut(False)

            elif line == constants.kFontStyleLineOverline:
                self._font.setUnderline(False)
                self._font.setStrikeOut(False)
                self._font.setOverline(True)

            elif line == constants.KFontStyleLineUnderline:
                self._font.setOverline(False)
                self._font.setStrikeOut(False)
                self._font.setUnderline(True)

            elif line == constants.KFontStyleLineStrikeout:
                self._font.setOverline(False)
                self._font.setUnderline(False)
                self._font.setStrikeOut(True)

    def setFontName(self, name):

        """
        set font name

        :param name - font name (str)
        """

        if self.isBegin():
            self._font_name = name
            self._font = QtGui.QFont(name)
            self._font_metric = QtGui.QFontMetrics(self._font)

            self.setFontWeight(self._font_weight)
            self.setFontSize(self._font_size)
            self.setFontIncline(self._font_incline)
            self.setFontLine(self._font_line)

    def setPointSize(self, size):

        """
        set point size

        :param size - point size (int)
        """

        if self.isBegin():
            self._gl_function_table.glPointSize(size)

    def setLineWidth(self, width):

        """
        set line width

        :param width - line width (int)
        """

        if self.isBegin():
            self._gl_function_table.glLineWidth(width)

    def setLineStyle(self, style):

        """
        set line style

        :param style - line style (OpenMayaRender.MUIDrawManager.LineStyle)
        """

        if self.isBegin():
            if style != constants.kLineSolid:
                self._gl_function_table.glEnable(OpenMayaRender_old.MGL_LINE_STIPPLE)
                # 0x00FF - dashed line.
                # 0x0101 - dotted line.
                if style == constants.kLineShortDotted:
                    self._gl_function_table.glLineStipple(2, 0x0101)

                elif style == constants.kLineDotted:
                    self._gl_function_table.glLineStipple(1, 0x0101)

                elif style == constants.kLineShortDashed:
                    self._gl_function_table.glLineStipple(2, 0x00FF)

                elif style == constants.kLineDashed:
                    self._gl_function_table.glLineStipple(1, 0x00FF)

                else:
                    # default line style
                    self._gl_function_table.glLineStipple(1, 0x00FF)

            else:
                self._gl_function_table.glDisable(OpenMayaRender_old.MGL_LINE_STIPPLE)

    def line2d(self, from_point, to_point):

        """
        draw line 2d

        :param from_point - source point (OpenMaya.MPoint)
        :param to_point - target point (OpenMaya.MPoint)
        """

        if self.isBegin():
            self._gl_function_table.glBegin(OpenMayaRender_old.MGL_LINES)
            self._gl_function_table.glVertex2d(from_point.x, from_point.y)
            self._gl_function_table.glVertex2d(to_point.x, to_point.y)
            self._gl_function_table.glEnd()

    def point2d(self, point):

        """
        draw point 2d

        :param point - point (OpenMaya.MPoint)
        """

        if self.isBegin():
            self._gl_function_table.glBegin(OpenMayaRender_old.MGL_POINTS)
            self._gl_function_table.glVertex2d(point.x, point.y)
            self._gl_function_table.glEnd()

    def rect2d(self, position, up, scale_x, scale_y, filled=False):

        """
        draw rectangle 2d

        :param position - rectangle position (OpenMaya.MPoint)
        :param up - position direction (OpenMaya.MVector)
        :param scale_x - scale by x (float)
        :param scale_y - scale by y (float)
        :param filled - fill rectangle (bool)
        """

        if self.isBegin():
            angle = math.atan2(up.x, up.y) * 180 / math.pi

            self._gl_function_table.glPushMatrix()
            self._gl_function_table.glTranslatef(position.x - scale_x, position.y - scale_y, 0)
            self._gl_function_table.glRotatef(angle, 0.0, 0.0, 1.0)

            if filled:
                self._gl_function_table.glBegin(OpenMayaRender_old.MGL_POLYGON)

            else:
                self._gl_function_table.glBegin(OpenMayaRender_old.MGL_LINE_LOOP)

            self._gl_function_table.glVertex2d(0.0, 0.0)
            self._gl_function_table.glVertex2d(scale_x * 2.0, 0.0)
            self._gl_function_table.glVertex2d(scale_x * 2.0, scale_y * 2.0)
            self._gl_function_table.glVertex2d(0.0, scale_y * 2.0)
            self._gl_function_table.glEnd()
            self._gl_function_table.glPopMatrix()

    def circle2d(self, position, radius, filled=False):

        """
        draw circle 2d

        :param position - circle position (OpenMaya.MPoint)
        :param radius - circle radius (float)
        :param filled - fill circle (bool)
        """

        if self.isBegin():
            if filled:
                self._gl_function_table.glBegin(OpenMayaRender_old.MGL_POLYGON)

            else:
                self._gl_function_table.glBegin(OpenMayaRender_old.MGL_LINE_LOOP)

            segment_count = int(radius)
            if segment_count > 360:
                segment_count = 360

            elif segment_count < 8:
                segment_count = 8

            i = 0
            while i < segment_count:
                angle = 2.0 * math.pi * i / float(segment_count)
                x = math.cos(angle) * radius
                y = math.sin(angle) * radius
                self._gl_function_table.glVertex2d(position.x + x, position.y + y)
                i += 1

            self._gl_function_table.glEnd()

    def text2d(self, position, text, alignment=constants.kLeft, backgroundSize=None, backgroundColor=None, dynamic=False):

        """
        draw text 2d

        :param position - text position (OpenMaya.MPoint)
        :param text - text (str)
        :param alignment - text (OpenMayaRender.MUIDrawManager.TextAlignment)
        :param backgroundSize - text background size (int)
        :param backgroundColor - text background color (OpenMaya.MColor)
        :param dynamic - text is dynamic (bool)
        """

        if self.isBegin():
            # generate texture with QtGui.QPainter
            if not backgroundSize:
                backgroundSize = [self._font_metric.width(text), self._font_metric.height()]

            # calculate position.
            alignment_offset = 0.0
            if alignment == constants.kLeft:
                alignment = QtCore.Qt.AlignLeft

            else:
                if alignment == constants.kRight:
                    alignment = QtCore.Qt.AlignRight
                    alignment_offset = backgroundSize[0]

                elif alignment == constants.kCenter:
                    alignment = QtCore.Qt.AlignHCenter
                    alignment_offset = backgroundSize[0] * 0.5

                else:
                    alignment = QtCore.Qt.AlignLeft

                text_width = self._font_metric.width(text)
                if text_width >= backgroundSize[0]:
                    alignment = QtCore.Qt.AlignLeft

            alignment |= QtCore.Qt.AlignVCenter

            # calculate position and size
            width, height = backgroundSize[0], backgroundSize[1]
            x = int(position.x - alignment_offset)
            y = int(position.y)
            x_offset = 0
            y_offset = 0
            if x < 0:
                x_offset = x
                width += x_offset
                x = 0

            if y < 0:
                y_offset = y
                height += y_offset
                y = 0

            if width > 0 and height > 0:
                # create image.
                q_image = QtGui.QImage(width, height, QtGui.QImage.Format_RGBA8888)
                q_image.fill(QtCore.Qt.transparent)
                self._painter.begin(q_image)
                self._painter.setRenderHint(QtGui.QPainter.Antialiasing)

                self._painter.setPen(self._pen)
                self._painter.setBrush(self._brush)
                self._painter.setFont(self._font)

                # fill background color.
                if backgroundColor is not None:
                    self._painter.fillRect(0, 0, width, height, QtGui.QColor(backgroundColor.r * 255, backgroundColor.g * 255, backgroundColor.b * 255, backgroundColor.a * 255))

                # paint text
                self._painter.drawText(x_offset, y_offset, backgroundSize[0], backgroundSize[1], alignment, text)
                self._painter.end()

                # generate MImage texture object and write it to color buffer
                m_image = self.qimage_to_mimage(q_image)
                if m_image:
                    self._view.writeColorBuffer(m_image, x, y)

    @staticmethod
    def qimage_to_mimage(q_image):

        """
        create OpenMaya.MImage from QtGui.QImage

        :param q_image - input image (QtGui.QImage)
        :return - output image (OpenMaya.MImage)
        """

        m_image = None

        width = q_image.width()
        height = q_image.height()

        byte_size = q_image.byteCount()

        if byte_size and width and height:
            m_image = OpenMaya.MImage()
            byte_pt = q_image.bits()
            if Qt.IsPyQt4 or Qt.IsPyQt5:
                byte_string = byte_pt.asstring(byte_size)

            else:
                byte_string = byte_pt[:byte_size]

            m_image.setPixels(byte_string, width, height)
            m_image.verticalFlip()
            m_image.setRGBA(True)

        return m_image
