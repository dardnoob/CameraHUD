import time
import maya.api.OpenMaya as OpenMaya
import maya.api.OpenMayaUI as OpenMayaUI
import maya.api.OpenMayaRender as OpenMayaRender
from camerahudlib import constants
from camerahudlib.private.logger import logger
from camerahudlib.private.glpainter import GlPainter
from camerahudlib.private.plugin_draw_manager import PluginDrawManager


class Plugin(OpenMayaUI.MPxLocatorNode):

    # drawing manager index attribute
    aHudIndex = None
    aCreationUnixTime = None
    # compound attribute used for ui grouping

    aUI = None
    # canvas rectangle attribute
    aUIRegion = None
    aUIRegionDrawEnable = None
    aUIRegionPosition = None
    aUIRegionIsFilled = None
    aUIRegionColor = None
    aUIRegionTransparency = None
    aUITextBackgroundColor = None
    aUITextBackgroundTransparency = None

    # canvas alignment and attachment position attribute
    aHorizontalUiAttach = None
    aVerticalUiAttach = None
    aHorizontalUiAlignment = None
    aVerticalUiAlignment = None
    aResolutionGate = None
    aDrawResolutionGateEnable = None

    # hud drawing type attribute
    aUIType = None
    aUIDrawEnable = None

    # hud size attribute
    aSize = None

    # drawing color attribute
    aColor = None
    aTransparency = None

    # font option attribute
    aText = None
    aTextDynamic = None
    aFitToResolutionGate = None
    aFontLine = None
    aFontIncline = None
    aFontWeight = None
    aFontStyleName = None
    aFontStyleSize = None
    aFontStyleStretch = None

    # line option attribute
    aLineStyle = None
    aLineWidth = None
    aFilled = None
    aRadius = None

    # position attribute used for text, point, circle, line placement
    aPosition = None

    # render resolution attribute
    aResolution = None

    # initialize data
    uiFontStyleList = []

    @staticmethod
    def creator():

        """
        get plugin node creator
        """

        return Plugin()

    @staticmethod
    def initialize():

        """
        initialize plugin
        """

        compound_attribute = OpenMaya.MFnCompoundAttribute()
        enumerate_attribute = OpenMaya.MFnEnumAttribute()
        numeric_attribute = OpenMaya.MFnNumericAttribute()
        typed_attribute = OpenMaya.MFnTypedAttribute()

        # create unique ui manager index attribute
        Plugin.aHudIndex = numeric_attribute.create(
            "hudIndex",
            "hudi",
            OpenMaya.MFnNumericData.kInt
        )
        numeric_attribute.default = -1
        numeric_attribute.hidden = True
        OpenMaya.MPxNode.addAttribute(Plugin.aHudIndex)

        Plugin.aCreationUnixTime = numeric_attribute.create(
            "creationUnixTime",
            "cutime",
            OpenMaya.MFnNumericData.kDouble
        )
        numeric_attribute.default = -1
        numeric_attribute.hidden = True
        OpenMaya.MPxNode.addAttribute(Plugin.aCreationUnixTime)

        # add resolution attribute
        Plugin.aResolution = numeric_attribute.create(
            "uiResolution",
            "ures",
            OpenMaya.MFnNumericData.k2Double
        )
        numeric_attribute.default = (256.0, 256.0)
        OpenMaya.MPxNode.addAttribute(Plugin.aResolution)

        # create ui type attribute
        Plugin.aUIType = enumerate_attribute.create(
            "uiType",
            "ut",
            constants.kText
        )
        enumerate_attribute.addField("Text", constants.kText)
        enumerate_attribute.addField("Point", constants.kPoint)
        enumerate_attribute.addField("Circle", constants.kCircle)
        enumerate_attribute.addField("Line", constants.kLine)
        enumerate_attribute.addField("None", constants.kNone)

        # create size attribute
        Plugin.aSize = numeric_attribute.create(
            "size",
            "sz",
            OpenMaya.MFnNumericData.kDouble,
            1.0
        )

        # create radius attribute
        Plugin.aRadius = numeric_attribute.create(
            "radius",
            "rad",
            OpenMaya.MFnNumericData.kDouble,
            5.0
        )

        # create text attribute
        string_data = OpenMaya.MFnStringData()
        default_text_value = string_data.create("Text")
        Plugin.aText = typed_attribute.create(
            "text",
            "t",
            OpenMaya.MFnData.kString,
            default_text_value
        )

        # create text dynamic control attribute
        Plugin.aTextDynamic = numeric_attribute.create(
            "textDynamic",
            "txtdyn",
            OpenMaya.MFnNumericData.kBoolean,
            0
        )

        # create text auto resize control attribute
        Plugin.aFitToResolutionGate = numeric_attribute.create(
            "fitToResolutionGate",
            "fittoresg",
            OpenMaya.MFnNumericData.kBoolean,
            0
        )

        # create horizontal alignment attribute
        Plugin.aHorizontalUiAttach = enumerate_attribute.create(
            "horizontalAttach",
            "ha",
            constants.kAttachHorizontalLeft
        )
        enumerate_attribute.addField("Left", constants.kAttachHorizontalLeft)
        enumerate_attribute.addField("Right", constants.kAttachHorizontalRight)
        enumerate_attribute.addField("Middle", constants.kAttachHorizontalMiddle)

        # create attach vertical attribute
        Plugin.aVerticalUiAttach = enumerate_attribute.create(
            "verticalAttach",
            "va",
            constants.kAttachVerticalTop
        )
        enumerate_attribute.addField("Top", constants.kAttachVerticalTop)
        enumerate_attribute.addField("Bottom", constants.kAttachVerticalBottom)
        enumerate_attribute.addField("Middle", constants.kAttachVerticalMiddle)

        # create attach vertical attribute
        Plugin.aResolutionGate = enumerate_attribute.create(
            "resolutionGate",
            "rgt",
            constants.kFilmGate
        )
        enumerate_attribute.addField("Port", constants.kPortGate)
        enumerate_attribute.addField("Viewport", constants.kViewportGate)
        enumerate_attribute.addField("Film", constants.kFilmGate)
        enumerate_attribute.addField("Image", constants.kImageGate)
        enumerate_attribute.addField("Safe title", constants.kSafeTitleGate)
        enumerate_attribute.addField("Safe action", constants.kSafeTitleAction)
        enumerate_attribute.addField("Render", constants.kRenderGate)
        enumerate_attribute.addField("Render safe title", constants.kSafeTitleRenderGate)
        enumerate_attribute.addField("Render safe action", constants.kSafeTitleRenderAction)

        # create drawing enable attribute
        Plugin.aDrawResolutionGateEnable = numeric_attribute.create(
            "gateDraw",
            "gdraw",
            OpenMaya.MFnNumericData.kBoolean,
            0
        )

        # create horizontal alignment attribute
        Plugin.aHorizontalUiAlignment = enumerate_attribute.create(
            "horizontalAlignment",
            "hal",
            constants.kHorizontalAlignmentLeft
        )
        enumerate_attribute.addField("Left", constants.kHorizontalAlignmentLeft)
        enumerate_attribute.addField("Right", constants.kHorizontalAlignmentRight)
        enumerate_attribute.addField("Center", constants.kHorizontalAlignmentCenter)

        # create vertical alignment attribute
        Plugin.aVerticalUiAlignment = enumerate_attribute.create(
            "verticalAlignment",
            "val",
            constants.kVerticalAlignmentTop
        )
        enumerate_attribute.addField("Top", constants.kVerticalAlignmentTop)
        enumerate_attribute.addField("Bottom", constants.kVerticalAlignmentBottom)
        enumerate_attribute.addField("Center", constants.kVerticalAlignmentCenter)

        # create position alignment attribute
        Plugin.aPosition = numeric_attribute.create(
            "position",
            "pos",
            OpenMaya.MFnNumericData.k2Double
        )
        numeric_attribute.default = (0.0, 0.0)
        numeric_attribute.array = True

        # create drawing rectangle filled attribute
        Plugin.aUIRegionIsFilled = numeric_attribute.create(
            "regionIsFilled",
            "rif",
            OpenMaya.MFnNumericData.kBoolean,
            0
       )

        # create drawing enable attribute
        Plugin.aUIDrawEnable = numeric_attribute.create(
            "draw",
            "draw",
            OpenMaya.MFnNumericData.kBoolean,
            0
        )

        # create drawing enable attribute
        Plugin.aUIRegionDrawEnable = numeric_attribute.create(
            "regionDraw",
            "rdraw",
            OpenMaya.MFnNumericData.kBoolean,
            0
        )

        # create drawing rectangle attribute
        Plugin.aUIRegion = numeric_attribute.create(
            "region",
            "reg",
            OpenMaya.MFnNumericData.k2Double
        )
        numeric_attribute.default = (0.0, 1.0)

        # create drawing filled attribute
        Plugin.aFilled = numeric_attribute.create(
            "filled",
            "fil",
            OpenMaya.MFnNumericData.kBoolean,
            0
        )

        # create drawing rectangle offset position attribute
        Plugin.aUIRegionPosition = numeric_attribute.create(
            "regionPosition",
            "rpos",
            OpenMaya.MFnNumericData.k2Double
        )
        numeric_attribute.default = (0.0, 0.0)

        # create color attribute
        Plugin.aColor = numeric_attribute.create(
            "color",
            "col",
            OpenMaya.MFnNumericData.k3Float
        )
        numeric_attribute.default = (0.0, 1.0, 1.0)
        numeric_attribute.usedAsColor = True

        # create color transparency attribute
        Plugin.aTransparency = numeric_attribute.create(
            "transparency",
            "trans",
            OpenMaya.MFnNumericData.kFloat,
            0.0
        )
        numeric_attribute.setSoftMin(0.0)
        numeric_attribute.setSoftMax(1.0)

        # create drawing rectangle fill color attribute
        Plugin.aUIRegionColor = numeric_attribute.create(
            "regionColor",
            "rcol",
            OpenMaya.MFnNumericData.k3Float
        )
        numeric_attribute.default = (0.0, 1.0, 1.0)
        numeric_attribute.usedAsColor = True

        # create drawing rectangle fill color transparency attribute
        Plugin.aUIRegionTransparency = numeric_attribute.create(
            "regionTransparency",
            "rtrans",
            OpenMaya.MFnNumericData.kFloat,
            0.0
        )
        numeric_attribute.setSoftMin(0.0)
        numeric_attribute.setSoftMax(1.0)

        # create drawing text background fill color attribute
        Plugin.aUITextBackgroundColor = numeric_attribute.create(
            "textBackgroundColor",
            "tbcol",
            OpenMaya.MFnNumericData.k3Float
        )
        numeric_attribute.default = (0.0, 1.0, 1.0)
        numeric_attribute.usedAsColor = True

        # create drawing text background fill color transparency attribute
        Plugin.aUITextBackgroundTransparency = numeric_attribute.create(
            "textBackgroundTransparency",
            "tbtrans",
            OpenMaya.MFnNumericData.kFloat,
            1.0
        )
        numeric_attribute.setSoftMin(0.0)
        numeric_attribute.setSoftMax(1.0)

        # create text incline attribute
        Plugin.aFontIncline = enumerate_attribute.create(
            "textIncline",
            "tic",
            constants.kFontStyleInclineNormal
        )
        enumerate_attribute.addField("Normal", constants.kFontStyleInclineNormal)
        enumerate_attribute.addField("Italic", constants.KFontStyleInclineItalic)

        # create text incline attribute
        Plugin.aFontWeight = enumerate_attribute.create(
            "fontWeight",
            "fw",
            constants.kFontStyleWeightLight
        )
        enumerate_attribute.addField("Normal", constants.kFontStyleWeightLight)
        enumerate_attribute.addField("Bold", constants.KFontStyleWeightBold)

        # create text font size attribute
        Plugin.aFontStyleSize = numeric_attribute.create(
            "fontSize",
            "fs",
            OpenMaya.MFnNumericData.kInt,
            OpenMayaRender.MUIDrawManager.kDefaultFontSize
        )
        numeric_attribute.setMin(-1)
        numeric_attribute.setMax(1000)

        # create text font size attribute
        Plugin.aLineWidth = numeric_attribute.create(
            "lineWidth",
            "lwd",
            OpenMaya.MFnNumericData.kFloat,
            2.0
        )

        # create text font style attribute
        try:
            Plugin.uiFontStyleList = OpenMayaRender.MUIDrawManager.getFontList()

        except Exception as exception_data:
            Plugin.uiFontStyleList = []
            logger.error(repr(exception_data))
            logger.error("can`t read font list")

        if len(Plugin.uiFontStyleList) == 0:
            logger.error("no available font founded")

        # create text stretch attribute
        Plugin.aFontStyleStretch = numeric_attribute.create(
            "fontStretch",
            "fstr",
            OpenMaya.MFnNumericData.kInt,
            OpenMayaRender.MUIDrawManager.kStretchUnstretched
        )
        numeric_attribute.setMin(50)
        numeric_attribute.setMax(200)

        Plugin.aFontStyleName = enumerate_attribute.create(
            "fontStyle",
            "fstl",
            0
        )
        for i, font_style in enumerate(Plugin.uiFontStyleList):
            try:
                enumerate_attribute.addField(font_style, i)

            except Exception as exception_data:
                logger.error(repr(exception_data))
                logger.error("can`t add font field")

        # create text draw line attribute
        Plugin.aFontLine = enumerate_attribute.create(
            "fontLine",
            "fln",
            constants.kFontStyleLineNone
        )
        enumerate_attribute.addField("None", constants.kFontStyleLineNone)
        enumerate_attribute.addField("Overline", constants.kFontStyleLineOverline)
        enumerate_attribute.addField("Underline", constants.KFontStyleLineUnderline)
        enumerate_attribute.addField("Strikeout", constants.KFontStyleLineStrikeout)

        # create draw line style attribute
        Plugin.aLineStyle = enumerate_attribute.create(
            "lineStyle",
            "ls",
            constants.kLineSolid
        )
        enumerate_attribute.addField("Solid", constants.kLineSolid)
        enumerate_attribute.addField("Short dotted", constants.kLineShortDotted)
        enumerate_attribute.addField("Short dashed", constants.kLineShortDashed)
        enumerate_attribute.addField("Dotted", constants.kLineDotted)
        enumerate_attribute.addField("Dashed", constants.kLineDashed)

        # create ui list attribute
        Plugin.aUI = compound_attribute.create(
            "ui",
            "ui"
        )
        compound_attribute.array = True
        compound_attribute.readable = True
        compound_attribute.writable = True

        # add attribute to compound attribute list
        compound_attribute.addChild(Plugin.aUIType)
        compound_attribute.addChild(Plugin.aUIDrawEnable)
        compound_attribute.addChild(Plugin.aDrawResolutionGateEnable)
        compound_attribute.addChild(Plugin.aResolutionGate)
        compound_attribute.addChild(Plugin.aUIRegionIsFilled)
        compound_attribute.addChild(Plugin.aRadius)
        compound_attribute.addChild(Plugin.aUIRegionColor)
        compound_attribute.addChild(Plugin.aUIRegionDrawEnable)
        compound_attribute.addChild(Plugin.aUIRegionTransparency)
        compound_attribute.addChild(Plugin.aHorizontalUiAttach)
        compound_attribute.addChild(Plugin.aVerticalUiAttach)
        compound_attribute.addChild(Plugin.aHorizontalUiAlignment)
        compound_attribute.addChild(Plugin.aVerticalUiAlignment)
        compound_attribute.addChild(Plugin.aText)
        compound_attribute.addChild(Plugin.aTextDynamic)
        compound_attribute.addChild(Plugin.aFitToResolutionGate)
        compound_attribute.addChild(Plugin.aUITextBackgroundColor)
        compound_attribute.addChild(Plugin.aUITextBackgroundTransparency)
        compound_attribute.addChild(Plugin.aFontIncline)
        compound_attribute.addChild(Plugin.aFilled)
        compound_attribute.addChild(Plugin.aFontWeight)
        compound_attribute.addChild(Plugin.aFontStyleName)
        compound_attribute.addChild(Plugin.aFontStyleSize)
        compound_attribute.addChild(Plugin.aUIRegion)
        compound_attribute.addChild(Plugin.aUIRegionPosition)
        compound_attribute.addChild(Plugin.aFontLine)
        compound_attribute.addChild(Plugin.aLineStyle)
        compound_attribute.addChild(Plugin.aLineWidth)
        compound_attribute.addChild(Plugin.aSize)
        compound_attribute.addChild(Plugin.aPosition)
        compound_attribute.addChild(Plugin.aFontStyleStretch)
        compound_attribute.addChild(Plugin.aColor)
        compound_attribute.addChild(Plugin.aTransparency)

        compound_attribute.usesArrayDataBuilder = True
        OpenMaya.MPxNode.addAttribute(Plugin.aUI)

        OpenMaya.MPxNode.attributeAffects(Plugin.aUIType, Plugin.aUI)
        OpenMaya.MPxNode.attributeAffects(Plugin.aResolutionGate, Plugin.aUI)
        OpenMaya.MPxNode.attributeAffects(Plugin.aUIRegionIsFilled, Plugin.aUI)
        OpenMaya.MPxNode.attributeAffects(Plugin.aDrawResolutionGateEnable, Plugin.aUI)
        OpenMaya.MPxNode.attributeAffects(Plugin.aUIDrawEnable, Plugin.aUI)
        OpenMaya.MPxNode.attributeAffects(Plugin.aUIRegionColor, Plugin.aUI)
        OpenMaya.MPxNode.attributeAffects(Plugin.aUIRegionDrawEnable, Plugin.aUI)
        OpenMaya.MPxNode.attributeAffects(Plugin.aUIRegionTransparency, Plugin.aUI)
        OpenMaya.MPxNode.attributeAffects(Plugin.aHorizontalUiAttach, Plugin.aUI)
        OpenMaya.MPxNode.attributeAffects(Plugin.aVerticalUiAttach, Plugin.aUI)
        OpenMaya.MPxNode.attributeAffects(Plugin.aHorizontalUiAlignment, Plugin.aUI)
        OpenMaya.MPxNode.attributeAffects(Plugin.aUITextBackgroundColor, Plugin.aUI)
        OpenMaya.MPxNode.attributeAffects(Plugin.aUITextBackgroundTransparency, Plugin.aUI)
        OpenMaya.MPxNode.attributeAffects(Plugin.aRadius, Plugin.aUI)
        OpenMaya.MPxNode.attributeAffects(Plugin.aVerticalUiAlignment, Plugin.aUI)
        OpenMaya.MPxNode.attributeAffects(Plugin.aText, Plugin.aUI)
        OpenMaya.MPxNode.attributeAffects(Plugin.aTextDynamic, Plugin.aUI)
        OpenMaya.MPxNode.attributeAffects(Plugin.aFitToResolutionGate, Plugin.aUI)
        OpenMaya.MPxNode.attributeAffects(Plugin.aFilled, Plugin.aUI)
        OpenMaya.MPxNode.attributeAffects(Plugin.aFontIncline, Plugin.aUI)
        OpenMaya.MPxNode.attributeAffects(Plugin.aFontWeight, Plugin.aUI)
        OpenMaya.MPxNode.attributeAffects(Plugin.aFontStyleName, Plugin.aUI)
        OpenMaya.MPxNode.attributeAffects(Plugin.aFontStyleSize, Plugin.aUI)
        OpenMaya.MPxNode.attributeAffects(Plugin.aUIRegion, Plugin.aUI)
        OpenMaya.MPxNode.attributeAffects(Plugin.aUIRegionPosition, Plugin.aUI)
        OpenMaya.MPxNode.attributeAffects(Plugin.aFontLine, Plugin.aUI)
        OpenMaya.MPxNode.attributeAffects(Plugin.aLineStyle, Plugin.aUI)
        OpenMaya.MPxNode.attributeAffects(Plugin.aLineWidth, Plugin.aUI)
        OpenMaya.MPxNode.attributeAffects(Plugin.aSize, Plugin.aUI)
        OpenMaya.MPxNode.attributeAffects(Plugin.aPosition, Plugin.aUI)
        OpenMaya.MPxNode.attributeAffects(Plugin.aFontStyleStretch, Plugin.aUI)
        OpenMaya.MPxNode.attributeAffects(Plugin.aColor, Plugin.aUI)
        OpenMaya.MPxNode.attributeAffects(Plugin.aTransparency, Plugin.aUI)
        OpenMaya.MPxNode.attributeAffects(Plugin.aResolution, Plugin.aUI)

    def __init__(self):

        """
        initialize node
        """

        OpenMayaUI.MPxLocatorNode.__init__(self)

        # cache previously used data
        self.__previous_data = None

    def excludeAsLocator(self):

        """
        disable this node used as locator

        :return - exclude as locator (bool)
        """

        return False

    def postConstructor(self):

        """
        setup node after creation
        """

        # set next drawable ui manager index
        node = self.thisMObject()
        plug = OpenMaya.MPlug(node, Plugin.aHudIndex)
        manager = PluginDrawManager()
        plug.setInt(manager.index())

        # set creation time
        plug = OpenMaya.MPlug(node, Plugin.aCreationUnixTime)
        plug.setDouble(time.time())

        # disable node saving
        self.setDoNotWrite(True)

    def compute(self, plug, datablock):

        """
        request node compute attribute data

        :param plug - attribute plug (OpenMaya.MPLug)
        :param datablock - attribute data handle (OpenMaya.MDataBlock)
        """

        return PluginDrawManager.compute(self, plug, datablock)

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

    def isBounded(self):

        """
        node is bounded

        :return - node is bounded (bool)
        """

        return False

    def draw(self, view, path, style, status):

        """
        draw event

        :param view - target view (OpenMayaUI.M3dView)
        :param path - node path (MDagPath)
        :param style - display style (M3dView.DisplayStyle)
        :param status - display status (M3dView.DisplayStatus)
        """

        node = path.node()
        if node.isNull():
            return None

        # get information about used camera
        camera_path = view.getCamera()

        # prepare for draw
        data = PluginDrawManager.prepareForDraw(path, camera_path, None, self.__previous_data, constants.kLegacyViewport)
        self.__previous_data = data

        # request draw
        painter = GlPainter(view)
        PluginDrawManager.draw(painter, style, data)
