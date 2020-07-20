import maya.api.OpenMaya as OpenMaya
import maya.api.OpenMayaRender as OpenMayaRender
from camerahudlib import constants
from camerahudlib.private.canvas import Canvas


class PluginDrawRequest(object):

    __slots__ = (
        "uiDraw",
        "uiType",
        "uiSize",
        "uiColor",
        "uiResolutionGate",
        "uiDrawResolutionGate",
        "region",
        "uiRegion",
        "uiRegionPosition",
        "uiRegionColor",
        "uiTextBackgroundColor",
        "uiRegionIsFilled",
        "uiDrawRegion",
        "uiHorisontalAttach",
        "uiVerticalAttach",
        "uiHorisontalAlignment",
        "uiVerticalAlignment",
        "uiRadius",
        "uiFilled",
        "uiLineStyle",
        "uiLineWidth",
        "uiPositionList",
        "uiRegionPositionList",
        "uiText",
        "uiTextDynamic",
        "uiFitToResolutionGate",
        "uiFontStyle",
        "uiFontStyleSize",
        "uiFontStyleStretch",
        "uiFontStyleWeight",
        "uiFontStyleIncline",
        "uiFontStyleLine",
        "file",
        "year",
        "month",
        "day",
        "hour",
        "minute",
    )

    def __init__(self):

        """
        Initialize camera render ui manager draw request.
        """

        self.uiDraw = False
        self.uiType = constants.kText
        self.uiSize = 1.0
        self.uiColor = OpenMaya.MColor([0.0, 0.0, 0.0])

        self.uiResolutionGate = constants.kViewportGate
        self.uiDrawResolutionGate = True

        self.region = Canvas(0, 0, 0, 0)
        self.uiRegion = OpenMaya.MVector(0.0, 0.0, 0.0)
        self.uiRegionPosition = OpenMaya.MPoint(0.0, 0.0, 0.0)
        self.uiRegionColor = OpenMaya.MColor([0.0, 0.0, 0.0])
        self.uiTextBackgroundColor = None
        self.uiRegionIsFilled = False
        self.uiDrawRegion = False

        self.uiHorisontalAttach = constants.kAttachHorizontalLeft
        self.uiVerticalAttach = constants.kAttachVerticalTop

        self.uiHorisontalAlignment = constants.kHorizontalAlignmentLeft
        self.uiVerticalAlignment = constants.kVerticalAlignmentTop

        self.uiRadius = 1.0
        self.uiFilled = 1.0
        self.uiLineStyle = constants.kLineSolid
        self.uiLineWidth = 2.0

        self.uiPositionList = []
        self.uiRegionPositionList = []

        self.uiText = "Text"
        self.uiTextDynamic = False
        self.uiFitToResolutionGate = True
        self.uiFontStyle = None
        self.uiFontStyleSize = OpenMayaRender.MUIDrawManager.kDefaultFontSize
        self.uiFontStyleStretch = OpenMayaRender.MUIDrawManager.kStretchUnstretched
        self.uiFontStyleWeight = constants.kFontStyleWeightLight
        self.uiFontStyleIncline = constants.kFontStyleInclineNormal
        self.uiFontStyleLine = constants.kFontStyleLineNone

        self.file = ""
        self.year = ""
        self.month = ""
        self.day = ""
        self.hour = ""
        self.minute = ""

