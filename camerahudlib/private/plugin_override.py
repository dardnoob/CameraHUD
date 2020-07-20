import maya.api.OpenMayaRender as OpenMayaRender
from camerahudlib import constants
from camerahudlib.private.logger import logger
from camerahudlib.private.plugin_draw_manager import PluginDrawManager


class PluginOverride(OpenMayaRender.MPxDrawOverride):

    @staticmethod
    def creator(obj):

        """
        get plugin node creator

        :return - creator object (PluginOverride)
        """

        return PluginOverride(obj)

    @staticmethod
    def draw(context, data):

        """
        empty draw method
        """

        return

    def __init__(self, obj):

        """
        initialize node

        :param obj - base object (MObject)
        """

        OpenMayaRender.MPxDrawOverride.__init__(self, obj, PluginOverride.draw)

    def supportedDrawAPIs(self):

        """
        get supported draw api

        :return - supported drawings api (OpenMayaRender.MRenderer.DrawAPI)
        """

        return OpenMayaRender.MRenderer.kOpenGL | OpenMayaRender.MRenderer.kDirectX11 | OpenMayaRender.MRenderer.kOpenGLCoreProfile

    def isTransparent(self):

        """
        node is transparent

        :return - node is transparent (bool)
        """

        return True

    def drawLast(self):

        """
        node is drawing last

        :return - is drawing last (bool)
        """

        return True

    def isBounded(self, path, camera_path):

        """
        node is bounded

        :param path - node path (MDagPath)
        :param camera_path - camera node path (MDagPath)

        :return - node is bounded (bool)
        """

        return False

    def hasUIDrawables(self):

        """
        node has drawable data

        :return - node has drawable data (bool)
        """

        return True

    def prepareForDraw(self, path, camera_path, frame_context, previous_data):

        """
        prepare for draw

        :param path - node path (MDagPath)
        :param camera_path - camera node path (MDagPath)
        :param frame_context - frame context (OpenMayaRender.MFrameContext)
        :param previous_data - user data (OpenMayaRender.MUserData)

        :return -
        """

        # manager prepare for draw
        data = PluginDrawManager.prepareForDraw(path, camera_path, frame_context, previous_data, constants.kViewport)
        return data

    def addUIDrawables(self, path, painter, frame_context, data):

        """
        add draw data

        :param path - node path (MDagPath)
        :param painter - painter object (GLPainter or OpenMayaRender.MUIDrawManager)
        :param frame_context - frame context (OpenMayaRender.MFrameContext)
        :param data - user data (OpenMayaRender.MUserData)
        """

        if data is not None:
            PluginDrawManager.draw(painter, frame_context, data)

        else:
            logger.warning("drawing data not provided")
