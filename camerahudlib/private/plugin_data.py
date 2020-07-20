import maya.api.OpenMaya as OpenMaya
from camerahudlib import constants
from camerahudlib.private.canvas import Canvas


class PluginData(OpenMaya.MUserData):

    def __init__(self):

        """
        initialize maya display draw data
        """

        OpenMaya.MUserData.__init__(self, False)

        self.manager = None
        self.pixelResolutionScale = 1.0
        self.pixelScale = 1.0
        self.camera = ""
        self.cameraFocalLenght = 0
        self.cameraFocusDistance = 0
        self.resolutionWidth = 0.0
        self.resolutionHeight = 0.0
        self.height = 0.0
        self.fit = OpenMaya.MFnCamera.kHorizontalFilmFit
        self.width = 0.0
        self.scale = 1.0
        self.port = Canvas(0, 0, 0, 0)
        self.viewport = Canvas(0, 0, 0, 0)
        self.film = Canvas(0, 0, 0, 0)
        self.image = Canvas(0, 0, 0, 0)
        self.render = Canvas(0, 0, 0, 0)
        self.safeAction = Canvas(0, 0, 0, 0)
        self.safeTitle = Canvas(0, 0, 0, 0)
        self.renderSafeTitle = Canvas(0, 0, 0, 0)
        self.renderSafeAction = Canvas(0, 0, 0, 0)

    def gate(self, key):

        """
        get resolution gate at given key
        """

        if key == constants.kPortGate:
            return self.port

        elif key == constants.kViewportGate:
            return self.viewport

        elif key == constants.kFilmGate:
            return self.film

        elif key == constants.kImageGate:
            return self.image

        elif key == constants.kSafeTitleGate:
            return self.safeTitle

        elif key == constants.kSafeTitleAction:
            return self.safeAction

        elif key == constants.kRenderGate:
            return self.render

        elif key == constants.kSafeTitleRenderGate:
            return self.renderSafeTitle

        elif key == constants.kSafeTitleRenderAction:
            return self.renderSafeAction

        return self.port


