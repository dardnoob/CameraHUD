import maya.api.OpenMayaRender as OpenMayaRender
import maya.api.OpenMaya as OpenMaya


kId = OpenMaya.MTypeId(0x80007)
kName = "CameraHUD"
kDrawDbClassification = "drawdb/geometry/" + kName
kDrawRegistrantId = kName + "Plugin"

# viewport version
kViewport = 0
kLegacyViewport = 1

# draw type
kText = 0
kPoint = 1
kCircle = 2
kLine = 3
kNone = 100

# draw alignment
kAttachHorizontalLeft = 0
kAttachHorizontalRight = 1
kAttachHorizontalMiddle = 2

kAttachVerticalTop = 0
kAttachVerticalBottom = 1
kAttachVerticalMiddle = 2

# draw gate
kPortGate = 0
kViewportGate = 1
kFilmGate = 2
kImageGate = 3
kSafeTitleGate = 4
kSafeTitleAction = 5
kRenderGate = 6
kSafeTitleRenderGate = 7
kSafeTitleRenderAction = 8

# text draw alignment
kHorizontalAlignmentLeft = OpenMayaRender.MUIDrawManager.kLeft
kHorizontalAlignmentRight = OpenMayaRender.MUIDrawManager.kRight
kHorizontalAlignmentCenter = OpenMayaRender.MUIDrawManager.kCenter

kVerticalAlignmentTop = OpenMayaRender.MUIDrawManager.kLeft
kVerticalAlignmentBottom = OpenMayaRender.MUIDrawManager.kRight
kVerticalAlignmentCenter = OpenMayaRender.MUIDrawManager.kCenter

# direction
kLeft = OpenMayaRender.MUIDrawManager.kLeft
kCenter = OpenMayaRender.MUIDrawManager.kCenter
kRight = OpenMayaRender.MUIDrawManager.kRight

# text draw incline
kFontStyleInclineNormal = OpenMayaRender.MUIDrawManager.kInclineNormal
KFontStyleInclineItalic = OpenMayaRender.MUIDrawManager.kInclineItalic

# text draw weight
kFontStyleWeightLight = OpenMayaRender.MUIDrawManager.kWeightLight
KFontStyleWeightBold = OpenMayaRender.MUIDrawManager.kWeightBold

# text draw line
kFontStyleLineNone = 0
kFontStyleLineOverline = OpenMayaRender.MUIDrawManager.kLineOverline
KFontStyleLineUnderline = OpenMayaRender.MUIDrawManager.kLineUnderline
KFontStyleLineStrikeout = OpenMayaRender.MUIDrawManager.kLineStrikeoutLine

# line style
kLineSolid = OpenMayaRender.MUIDrawManager.kSolid
kLineShortDotted = OpenMayaRender.MUIDrawManager.kShortDotted
kLineShortDashed = OpenMayaRender.MUIDrawManager.kShortDashed
kLineDashed = OpenMayaRender.MUIDrawManager.kDashed
kLineDotted = OpenMayaRender.MUIDrawManager.kDotted
