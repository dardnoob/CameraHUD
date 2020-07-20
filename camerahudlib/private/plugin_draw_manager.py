import datetime
import maya.api.OpenMaya as OpenMaya
import maya.api.OpenMayaUI as OpenMayaUI
import maya.cmds as cmds
from camerahudlib import constants
from camerahudlib.private.canvas import Canvas
from camerahudlib.private.plugin_data import PluginData
from camerahudlib.private.plugin_draw_request import PluginDrawRequest


class PluginDrawManager(object):

    __cache__ = {}

    @staticmethod
    def get_next_index():

        """
        get next available index

        :return: cached draw manager index (int)
        """

        # get existing id list.
        used_index_list = []
        for node in cmds.ls(type=constants.kName):
            existing_index = cmds.getAttr(node + ".hudi")
            if existing_index != -1 and existing_index not in used_index_list:
                used_index_list.append(existing_index)

        # remove unknown index data
        for cache_index in PluginDrawManager.__cache__.keys():
            if cache_index not in used_index_list:
                del PluginDrawManager.__cache__[cache_index]

        # get free index
        index = 0
        while index in PluginDrawManager.__cache__ and index in used_index_list:
            index += 1

        return index

    def __new__(cls, index=None):

        """
        get instance

        :param index - cached draw manager index (int)

        :return - instance of PluginDrawManager (PluginDrawManager)
        """

        if index is None:
            next_index = cls.get_next_index()

        else:
            next_index = index

        if next_index in PluginDrawManager.__cache__:
            instance = PluginDrawManager.__cache__[next_index]

        else:
            instance = super(PluginDrawManager, cls).__new__(cls, next_index)
            instance._requested_index = next_index

        return instance

    def __init__(self, index=None):

        """
        initialize draw manager

        :param index - cached draw manager index
        """

        if index is None:
            index = self.get_next_index()

        if index not in PluginDrawManager.__cache__:
            PluginDrawManager.__cache__[index] = self
            self._requested_index = index
            self._request_data = {}
            self._resolution = [256, 256]

    def setResolution(self, width, height):

        """
        set resolution gate

        :param width - resolution gate width (int)
        :param height - resolution gate height (int)
        """

        self._resolution[0] = width
        self._resolution[1] = height

    def setWidth(self, width):

        """
        set resolution gate width

        :param width - resolution gate width (int)
        """

        self._resolution[0] = width

    def setHeight(self, height):

        """
        set resolution gate height

        :param height - resolution gate height (int)
        """

        self._resolution[1] = height

    def width(self):

        """
        get resolution gate width

        :return - resolution gate width (int)
        """

        return self._resolution[0]

    def height(self):

        """
        get resolution gate height

        :return - resolution gate height (int)
        """

        return self._resolution[1]

    def __nonzero__(self):

        """
        is non-zero

        :return - is non-zero object (bool)
        """

        return True

    def __len__(self):

        """
        get draw request count

        :return - draw draw request count (int)
        """

        return len(self._request_data)

    def __getitem__(self, index):

        """
        get draw request

        :param index - draw request index (int)

        :return - draw request (PluginDrawRequest)
        """

        if index not in self._request_data:
            result = PluginDrawRequest()
            self._request_data[index] = result

        else:
            result = self._request_data[index]

        return result

    def __delitem__(self, index):

        """
        remove draw request

        :param index - draw request index (int)
        """

        if index in self._request_data:
            del self._request_data[index]

    def __iter__(self):

        """
        iterate draw request

        :return - request index (int)
        """

        for index in self._request_data.keys():
            yield index

    def index(self):

        """
        get used index

        :return - current node index (int)
        """

        return self._requested_index

    def attached(self):

        """
        get attached node index list

        :return - attached node index list (list)
        """

        result = []
        index = self.index()
        for node in cmds.ls(type=constants.kName):
            if cmds.getAttr(node + ".hudi") == index:
                result.append(index)

        return result

    @staticmethod
    def compute(instance, plug, datablock):

        """
        request node compute attribute data

        :param instance - plugin node instance (Plugin)
        :param plug - attribute plug (OpenMaya.MPLug)
        :param datablock - attribute data handle (OpenMaya.MDataBlock)
        """

        from camerahudlib.private.plugin import Plugin

        # get this node
        node = instance.thisMObject()

        # get manager date instance
        time_index_handle = datablock.inputValue(Plugin.aCreationUnixTime)
        creation_time = time_index_handle.asDouble()
        time_index_handle.setClean()

        # get manager instance
        hud_index_handle = datablock.inputValue(Plugin.aHudIndex)
        hud_index = hud_index_handle.asShort()
        hud_index_handle.setClean()
        manager = PluginDrawManager(hud_index)

        # get drawing request id
        active_request_index = None

        used_plug = plug
        if plug.isElement:
            # can parent array attribute
            used_plug = plug.array()

        # attribute is child of compound attribute
        if used_plug.isNull is False:
            ui_compound_plug = None
            compound_child_plug = None

            if used_plug.isChild:
                # get parent compound attribute
                compound_child_plug = used_plug.parent()
                if compound_child_plug.isNull is False:
                    if compound_child_plug.isElement:
                        ui_compound_plug = compound_child_plug.array()

            elif used_plug.isCompound:
                if plug.isElement:
                    compound_child_plug = plug
                    ui_compound_plug = used_plug

            if compound_child_plug is not None and ui_compound_plug is not None:
                if ui_compound_plug.isNull is False and ui_compound_plug.partialName(False, False, False, False, False, False) == "ui":
                    # get active request index
                    active_request_index = compound_child_plug.logicalIndex()

        # update resolution gate
        resolution_gate_handle = datablock.inputValue(Plugin.aResolution)
        width, height = resolution_gate_handle.asDouble2()
        resolution_gate_handle.setClean()
        manager.setResolution(width, height)

        # compute drawing request data
        if active_request_index is not None:
            request = manager[active_request_index]

            # update scene info
            request.file = cmds.file(q=True, sn=True)
            if not request.file:
                request.file = ""

            # update creation date
            date = datetime.datetime.fromtimestamp(creation_time)
            request.year = "%04d" % date.year
            request.month = "%02d" % date.month
            request.day = "%02d" % date.day
            request.hour = "%02d" % date.hour
            request.minute = "%02d" % date.minute

            # get parent compound attribute
            ui_compound_array_handle = datablock.inputArrayValue(Plugin.aUI)
            ui_compound_array_handle.jumpToLogicalElement(active_request_index)
            ui_compound_handle = ui_compound_array_handle.inputValue()

            # prepare manager drawing data
            # get hud type
            data_handle = ui_compound_handle.child(Plugin.aUIType)
            request.uiType = data_handle.asShort()
            data_handle.setClean()

            # get size
            data_handle = ui_compound_handle.child(Plugin.aSize)
            request.uiSize = data_handle.asDouble()
            data_handle.setClean()

            # get fill
            data_handle = ui_compound_handle.child(Plugin.aFilled)
            request.uiFilled = data_handle.asBool()
            data_handle.setClean()

            # get size
            data_handle = ui_compound_handle.child(Plugin.aRadius)
            request.uiRadius = data_handle.asDouble()
            data_handle.setClean()

            # get color
            data_handle = ui_compound_handle.child(Plugin.aColor)
            color = data_handle.asFloat3()
            request.uiColor = OpenMaya.MColor([color[0], color[1], color[2]])
            data_handle.setClean()

            # get transparency
            data_handle = ui_compound_handle.child(Plugin.aTransparency)
            request.uiColor.a = 1.0 - data_handle.asFloat()
            data_handle.setClean()

            # Get resolution gate.
            data_handle = ui_compound_handle.child(Plugin.aResolutionGate)
            request.uiResolutionGate = data_handle.asShort()
            data_handle.setClean()

            # get region position offset
            data_handle = ui_compound_handle.child(Plugin.aUIRegionPosition)
            position = data_handle.asDouble2()
            request.uiRegionPosition = OpenMaya.MPoint(position[0], position[1], 0.0, 1.0)
            data_handle.setClean()

            # get region size
            data_handle = ui_compound_handle.child(Plugin.aUIRegion)
            size = data_handle.asDouble2()
            request.uiRegion = OpenMaya.MVector(size[0], size[1], 0.0)
            data_handle.setClean()

            # get region draw enable
            data_handle = ui_compound_handle.child(Plugin.aUIRegionDrawEnable)
            draw_region = data_handle.asBool()
            request.uiDrawRegion = draw_region
            data_handle.setClean()

            # get resolution gate draw enable
            data_handle = ui_compound_handle.child(Plugin.aDrawResolutionGateEnable)
            draw_gate = data_handle.asBool()
            request.uiDrawResolutionGate = draw_gate
            data_handle.setClean()

            # get region attachment side
            data_handle = ui_compound_handle.child(Plugin.aHorizontalUiAttach)
            request.uiHorisontalAttach = data_handle.asShort()
            data_handle.setClean()

            data_handle = ui_compound_handle.child(Plugin.aVerticalUiAttach)
            request.uiVerticalAttach = data_handle.asShort()
            data_handle.setClean()

            # get region content alignment side
            data_handle = ui_compound_handle.child(Plugin.aHorizontalUiAlignment)
            request.uiHorisontalAlignment = data_handle.asShort()
            data_handle.setClean()

            data_handle = ui_compound_handle.child(Plugin.aVerticalUiAlignment)
            request.uiVerticalAlignment = data_handle.asShort()
            data_handle.setClean()

            # get region filling state
            data_handle = ui_compound_handle.child(Plugin.aUIRegionIsFilled)
            request.uiRegionIsFilled = data_handle.asBool()
            data_handle.setClean()

            # Set request drawing state
            data_handle = ui_compound_handle.child(Plugin.aUIDrawEnable)
            request.uiDraw = data_handle.asBool()
            data_handle.setClean()

            # get region color
            data_handle = ui_compound_handle.child(Plugin.aUIRegionColor)
            color = data_handle.asFloat3()
            request.uiRegionColor = OpenMaya.MColor([color[0], color[1], color[2]])
            data_handle.setClean()

            # get region transparency
            data_handle = ui_compound_handle.child(Plugin.aUIRegionTransparency)
            request.uiRegionColor.a = 1.0 - data_handle.asFloat()
            data_handle.setClean()

            # get position data
            ui_position_handle = ui_compound_handle.child(Plugin.aPosition)
            ui_position_list_handle = OpenMaya.MArrayDataHandle(ui_position_handle)
            request.uiPositionList = []
            if len(ui_position_list_handle) > 0:
                if request.uiType != constants.kText:
                    i = 0
                    while i < len(ui_position_list_handle):
                        ui_position_list_handle.jumpToPhysicalElement(i)
                        data_handle = ui_position_list_handle.inputValue()
                        position = data_handle.asDouble2()
                        request.uiPositionList.append(OpenMaya.MPoint(
                            position[0],
                            position[1],
                            0.0,
                            1.0
                        ))
                        i += 1

                else:
                    data_handle = ui_position_list_handle.inputValue()
                    position = data_handle.asDouble2()
                    request.uiPositionList.append(OpenMaya.MPoint(
                        position[0],
                        position[1],
                        0.0,
                        1.0
                    ))

            else:
                request.uiPositionList.append(OpenMaya.MPoint(0.0, 0.0, 0.0, 1.0))

            ui_position_list_handle.setClean()

            # get text data
            request.uiFontStyleLine = constants.kFontStyleLineNone
            if request.uiType == constants.kText:
                # get text string
                data_handle = ui_compound_handle.child(Plugin.aText)
                request.uiText = data_handle.asString()

                # get text is dynamic
                data_handle = ui_compound_handle.child(Plugin.aTextDynamic)
                request.uiTextDynamic = data_handle.asBool()

                # get text is auto resize
                data_handle = ui_compound_handle.child(Plugin.aFitToResolutionGate)
                request.uiFitToResolutionGate = data_handle.asBool()

                # get text line
                data_handle = ui_compound_handle.child(Plugin.aFontLine)
                request.uiFontStyleLine = data_handle.asShort()
                data_handle.setClean()

                # get font incline mode
                data_handle = ui_compound_handle.child(Plugin.aFontIncline)
                request.uiFontStyleIncline = data_handle.asShort()
                data_handle.setClean()

                # get font weight
                data_handle = ui_compound_handle.child(Plugin.aFontWeight)
                request.uiFontStyleWeight = data_handle.asShort()
                data_handle.setClean()

                # get font size
                data_handle = ui_compound_handle.child(Plugin.aFontStyleSize)
                request.uiFontStyleSize = data_handle.asShort()
                data_handle.setClean()

                # get font size
                data_handle = ui_compound_handle.child(Plugin.aFontStyleStretch)
                request.uiFontStyleStretch = data_handle.asShort()
                data_handle.setClean()

                # get font style
                data_handle = ui_compound_handle.child(Plugin.aFontStyleName)
                font_style_index =  data_handle.asShort()
                if 0 <= font_style_index < len(Plugin.uiFontStyleList):
                    request.uiFontStyle = Plugin.uiFontStyleList[font_style_index]

                data_handle.setClean()

                # get text background transparency
                data_handle = ui_compound_handle.child(Plugin.aUITextBackgroundTransparency)
                alpha = 1.0 - data_handle.asFloat()
                data_handle.setClean()
                if alpha > 0.0:
                    # get text background color
                    data_handle = ui_compound_handle.child(Plugin.aUITextBackgroundColor)
                    color = data_handle.asFloat3()
                    request.uiTextBackgroundColor = OpenMaya.MColor([color[0], color[1], color[2]])
                    request.uiTextBackgroundColor.a = alpha
                    data_handle.setClean()

                else:
                    request.uiTextBackgroundColor = None

            # get line style
            data_handle = ui_compound_handle.child(Plugin.aLineStyle)
            request.uiLineStyle = data_handle.asShort()
            data_handle.setClean()

            # get line width
            data_handle = ui_compound_handle.child(Plugin.aLineWidth)
            request.uiLineWidth = data_handle.asFloat()
            data_handle.setClean()

            ui_compound_handle.setClean()
            ui_compound_array_handle.setClean()

    @staticmethod
    def prepareForDraw(path, camera_path, frame_context, previous_data, viewport_version):

        """
        prepare for draw

        :param path - node path (MDagPath)
        :param camera_path - camera node path (MDagPath)
        :param frame_context - frame context (OpenMayaRender.MFrameContext)
        :param previous_data - user data (OpenMayaRender.MUserData)
        :param viewport_version - viewport version (int)
        """

        from camerahudlib.private.plugin import Plugin

        # re-initialize data
        data = previous_data
        if not isinstance(data, PluginData):
            data = PluginData()

        # get used node
        node = path.node()
        if node.isNull():
            return None

        # get render manager
        plug = OpenMaya.MPlug(node, Plugin.aHudIndex)
        hud_index = plug.asInt()
        if hud_index < 0:
            return None

        manager = PluginDrawManager(hud_index)
        data.manager = manager
        resolution_width = manager.width()
        resolution_height = manager.height()
        resolution_aspect = float(resolution_width) / float(resolution_height)
        vertical_resolution_aperture = 1.0
        horizontal_resolution_aperture = 1.0
        data.resolutionWidth = resolution_width
        data.resolutionHeight = resolution_height

        # update viewport canvas rectangle
        if frame_context is None:
            view = OpenMayaUI.M3dView.active3dView()
            viewport_width = view.portWidth()
            viewport_height = view.portHeight()

            viewport_x = viewport_width * 0.5
            viewport_y = viewport_height * 0.5

        else:
            origin_x, origin_y, viewport_width, viewport_height = frame_context.getViewportDimensions()
            viewport_x = origin_x + viewport_width * 0.5
            viewport_y = origin_y + viewport_height * 0.5

        data.width = viewport_width
        data.height = viewport_height

        data.viewport.apply(
            viewport_x,
            viewport_y,
            viewport_width,
            viewport_height
        )
        data.port.inherit(data.viewport)

        # update camera option
        camera = OpenMaya.MFnCamera(camera_path)
        if camera.panZoomEnabled:
            zoom = camera.zoom
            pan_x = camera.horizontalPan
            pan_y = camera.verticalPan

        else:
            zoom = 1.0
            pan_x = 0.0
            pan_y = 0.0

        lens_squeeze_ratio = camera.lensSqueezeRatio
        horizontal_film_aperture = camera.horizontalFilmAperture
        vertical_film_aperture = camera.verticalFilmAperture
        data.camera = camera_path.fullPathName().rsplit("|", 2)[1]
        data.cameraFocalLenght = camera.focalLength
        data.cameraFocusDistance = camera.focusDistance

        # calculate aspect ratio
        aspect_ratio = horizontal_film_aperture / vertical_film_aperture
        viewport_aspect_ratio = data.viewport.aspectRatio()

        # calculate film fit
        film_fit = camera.filmFit
        resolution_film_fit = film_fit
        if film_fit == OpenMaya.MFnCamera.kFillFilmFit:
            if viewport_aspect_ratio < aspect_ratio:
                film_fit = OpenMaya.MFnCamera.kVerticalFilmFit

            else:
                film_fit = OpenMaya.MFnCamera.kHorizontalFilmFit

            if resolution_aspect < aspect_ratio:
                resolution_film_fit = OpenMaya.MFnCamera.kVerticalFilmFit

            else:
                resolution_film_fit = OpenMaya.MFnCamera.kHorizontalFilmFit

        elif film_fit == OpenMaya.MFnCamera.kOverscanFilmFit:
            if viewport_aspect_ratio < aspect_ratio:
                film_fit = OpenMaya.MFnCamera.kHorizontalFilmFit

            else:
                film_fit = OpenMaya.MFnCamera.kVerticalFilmFit

            if resolution_aspect < aspect_ratio:
                resolution_film_fit = OpenMaya.MFnCamera.kHorizontalFilmFit

            else:
                resolution_film_fit = OpenMaya.MFnCamera.kVerticalFilmFit

        # calculate resolution aperture
        if resolution_film_fit == OpenMaya.MFnCamera.kHorizontalFilmFit:
            horizontal_resolution_aperture = horizontal_film_aperture
            vertical_resolution_aperture = horizontal_film_aperture / resolution_aspect

        elif resolution_film_fit == OpenMaya.MFnCamera.kVerticalFilmFit:
            vertical_resolution_aperture = vertical_film_aperture
            horizontal_resolution_aperture = vertical_film_aperture * resolution_aspect

        data.fit = film_fit

        # calculate pixel scale
        if film_fit == OpenMaya.MFnCamera.kHorizontalFilmFit:
            pixel_scale = data.viewport.width() / camera.overscan / horizontal_film_aperture / zoom
            pixel_resolution_scale = data.viewport.width() / camera.overscan / horizontal_resolution_aperture / zoom

        else:
            pixel_scale = data.viewport.height() / camera.overscan / vertical_film_aperture / zoom
            pixel_resolution_scale = data.viewport.height() / camera.overscan / vertical_resolution_aperture / zoom

        pixel_scale_x = pixel_scale * lens_squeeze_ratio
        pixel_resolution_scale_x = pixel_resolution_scale * lens_squeeze_ratio
        data.pixelScale = pixel_scale
        data.pixelResolutionScale = pixel_resolution_scale

        # update port gate position
        data.port.move(
            data.port.x() - (pan_x * pixel_scale),
            data.port.y() - (pan_y * pixel_scale)
        )

        # update film canvas rectangle
        width = (horizontal_film_aperture * pixel_scale_x)
        height = (vertical_film_aperture * pixel_scale)
        data.film.apply(
            data.port.x(),
            data.port.y(),
            width,
            height
        )

        # calculate interface fit to resolution scale
        data.scale = ((viewport_width / width) / (viewport_height / height))

        # update image canvas rectangle
        width = (horizontal_film_aperture * pixel_scale_x)
        height = (vertical_film_aperture * pixel_scale)
        data.image.apply(
            data.port.x(),
            data.port.y(),
            width,
            height
        )

        # update render canvas rectangle
        width = (horizontal_resolution_aperture * pixel_resolution_scale_x)
        height = (vertical_resolution_aperture * pixel_resolution_scale)
        data.render.apply(
            data.port.x(),
            data.port.y(),
            width,
            height
        )

        # update safe action canvas rectangle
        width = (horizontal_film_aperture * pixel_scale_x) * 0.9
        height = (vertical_film_aperture * pixel_scale) * 0.9
        data.safeAction.apply(
            data.port.x(),
            data.port.y(),
            width,
            height
        )

        # update safe title canvas rectangle
        width = (horizontal_film_aperture * pixel_scale_x) * 0.8
        height = (vertical_film_aperture * pixel_scale) * 0.8
        data.safeTitle.apply(
            data.port.x(),
            data.port.y(),
            width,
            height
        )

        # update safe render title canvas rectangle
        width = data.render.width() * 0.8
        height = data.render.height() * 0.8
        data.renderSafeTitle.apply(
            data.port.x(),
            data.port.y(),
            width,
            height
        )

        # update safe render action canvas rectangle
        width = data.render.width() * 0.9
        height = data.render.height() * 0.9
        data.renderSafeAction.apply(
            data.port.x(),
            data.port.y(),
            width,
            height
        )

        # update region rectangle for each drawing request
        for request_key in data.manager:
            request = data.manager[request_key]
            if request.uiDraw:
                gate = data.gate(request.uiResolutionGate)
                real_x, real_y, real_width, real_height = request.uiRegionPosition.x, request.uiRegionPosition.y, request.uiRegion.x, request.uiRegion.y

                # calculate real region value
                width_percentage = (gate.width() / 100.0)
                height_percentage = (gate.height() / 100.0)
                real_x *= width_percentage
                real_y *= height_percentage
                real_width *= width_percentage
                real_height *= height_percentage

                # calculate region position
                if request.uiHorisontalAttach == constants.kAttachHorizontalLeft:
                    x = (gate.x() - (gate.width() * 0.5) + real_width * 0.5) + real_x

                elif request.uiHorisontalAttach == constants.kAttachHorizontalRight:
                    x = (gate.x() + (gate.width() * 0.5) - real_width * 0.5) + real_x

                elif request.uiHorisontalAttach == constants.kAttachHorizontalMiddle:
                    x = gate.x() + real_x

                else:
                    x = real_x

                if request.uiVerticalAttach == constants.kAttachVerticalTop:
                    y = (gate.y() + (gate.height() * 0.5) - real_height * 0.5) + real_y

                elif request.uiVerticalAttach == constants.kAttachVerticalBottom:
                    y = (gate.y() - (gate.height() * 0.5) + real_height * 0.5) + real_y

                elif request.uiVerticalAttach == constants.kAttachVerticalMiddle:
                    y = gate.y() + real_y

                else:
                    y = real_y

                width = int(real_width)
                height = int(real_height)

                # apply region rectangle
                request.region.apply(
                    x,
                    y,
                    width,
                    height
                )

                # update region position list
                size = len(request.uiRegionPositionList)
                point_index = 0
                for point in request.uiPositionList:
                    if point_index >= size:
                        region_point = OpenMaya.MPoint()
                        request.uiRegionPositionList.append(region_point)
                        size += 1

                    else:
                        region_point = request.uiRegionPositionList[point_index]

                    # calculate real position value
                    region_point.x = point.x * (real_width / 100.0)
                    region_point.y = point.y * (real_height / 100.0)

                    point_index += 1

                request.uiRegionPositionList = request.uiRegionPositionList[:point_index + 1]

        return data

    @staticmethod
    def draw(painter, frame_context, data):

        """
        request viewport 2.0 draw

        :param painter - painter object (GLPainter or OpenMayaRender.MUIDrawManager)
        :param frame_context - frame context (OpenMayaRender.MFrameContext)
        :param data - user data (OpenMayaRender.MUserData)
        """

        if not isinstance(data, PluginData):
            return None

        if data.manager is None:
            return None

        for request_key in data.manager:
            request = data.manager[request_key]
            if request.uiDraw:
                gate = data.gate(request.uiResolutionGate)
                region_corner = request.region.corner(Canvas.kLeftBottom)
                x, y = region_corner.x, region_corner.y
                width, height = request.region.width(), request.region.height()

                scale = request.uiSize

                width_scaled = width * scale
                x_offset = (width_scaled - width) * 0.5
                x -= x_offset
                width = int(width_scaled)
                height_scale = height * scale
                y_offset = (height_scale - height) * 0.5
                y -= y_offset
                height = int(height_scale)

                if request.uiFitToResolutionGate:
                    if data.fit == OpenMaya.MFnCamera.kHorizontalFilmFit:
                        gate_scale = gate.width() / data.resolutionWidth

                    else:
                        gate_scale = gate.height() / data.resolutionHeight

                    scale *= gate_scale

                line_width = request.uiLineWidth
                line_width *= scale

                alignment_offset_x = 0.0
                if request.uiHorisontalAlignment == constants.kHorizontalAlignmentRight:
                    alignment_offset_x = width

                elif request.uiHorisontalAlignment == constants.kHorizontalAlignmentCenter:
                    alignment_offset_x = width * 0.5

                # draw resolution gate
                if request.uiDrawResolutionGate:
                    painter.beginDrawable()
                    painter.setColor(request.uiColor)
                    painter.setLineWidth(line_width)
                    painter.setLineStyle(request.uiLineStyle)
                    position = gate.position()
                    painter.rect2d(position, OpenMaya.MVector.kYaxisVector, gate.width() * 0.5, gate.height() * 0.5, False)
                    painter.endDrawable()

                # draw paint region
                if request.uiDrawRegion:
                    painter.beginDrawable()
                    painter.setColor(request.uiRegionColor)
                    painter.setLineWidth(line_width)
                    painter.setLineStyle(request.uiLineStyle)
                    position = request.region.position()
                    painter.rect2d(position, OpenMaya.MVector.kYaxisVector, width * 0.5, height * 0.5, request.uiRegionIsFilled)
                    painter.setPointSize(10)
                    painter.endDrawable()

                # draw text
                if request.uiType == constants.kText:
                    text = request.uiText
                    if text:
                        painter.beginDrawable()
                        painter.setColor(request.uiColor)
                        if request.uiFontStyle is not None:
                            painter.setFontName(request.uiFontStyle)

                        painter.setFontSize(int(request.uiFontStyleSize * scale))
                        painter.setFontStretch(request.uiFontStyleStretch)
                        painter.setFontLine(request.uiFontStyleLine)
                        painter.setFontWeight(request.uiFontStyleWeight)
                        painter.setFontIncline(request.uiFontStyleIncline)
                        point = request.uiRegionPositionList[0]

                        point = OpenMaya.MPoint(x + point.x * scale + alignment_offset_x, y + point.y * scale, 0.0, 1.0)

                        # information about animation range
                        if "$FRAME_AST" in text:
                            text = text.replace("$FRAME_AST", "%03d" % cmds.playbackOptions(q=True, ast=True))

                        if "$FRAME_AET" in text:
                            text = text.replace("$FRAME_AET", "%03d" % cmds.playbackOptions(q=True, aet=True))

                        if "$FRAME_COUNT" in text:
                            text = text.replace("$FRAME_COUNT", "%03d" % ((cmds.playbackOptions(q=True, aet=True) - cmds.playbackOptions(q=True, ast=True)) + 1))

                        if "$FRAME_REAL" in text:
                            text = text.replace("$FRAME_REAL", "%03d" % cmds.currentTime(q=True))

                        if "$FRAME" in text:
                            text = text.replace("$FRAME", "%03d" % ((cmds.currentTime(q=True) - cmds.playbackOptions(q=True, ast=True)) + 1))

                        # Information about scene
                        if "$FILE_SHORT" in text:
                            text = text.replace("$FILE_SHORT", request.file.rsplit("/", 1)[-1].split(".", 1)[0])

                        if "$FILE" in text:
                            text = text.replace("$FILE", request.file)

                        # information about creation date
                        if "$YEAR" in text:
                            text = text.replace("$YEAR", request.year)

                        if "$MONTH" in text:
                            text = text.replace("$MONTH", request.month)

                        if "$DAY" in text:
                            text = text.replace("$DAY", request.day)

                        if "$HOUR" in text:
                            text = text.replace("$HOUR", request.hour)

                        if "$MINUTE" in text:
                            text = text.replace("$MINUTE", request.minute)

                        # information about camera
                        if "$CAMERA" in text:
                            text = text.replace("$CAMERA", data.camera)

                        if "$FOCAL_LENGHT" in text:
                            digit = str(data.cameraFocalLenght)
                            buffer = digit.split(".", 1)
                            if buffer:
                                digit = buffer[0] + "." + buffer[1][:2]

                            text = text.replace("$FOCAL_LENGHT", digit)

                        if "$FOCUS_DISTANCE" in text:
                            digit = str(data.cameraFocusDistance)
                            buffer = digit.split(".", 1)
                            if buffer:
                                digit = buffer[0] + "." + buffer[1][:2]

                            text = text.replace("$FOCUS_DISTANCE", digit)

                        # special symbol
                        text = text.replace("\\n", "\n")
                        text = text.replace("\\r", "\r")
                        text = text.replace("\\t", "\t")

                        # paint
                        painter.text2d(
                            point,
                            text,
                            request.uiHorisontalAlignment,
                            [width, height],
                            request.uiTextBackgroundColor,
                            request.uiTextDynamic
                        )
                        painter.endDrawable()

                # draw point
                elif request.uiType == constants.kPoint:
                    painter.beginDrawable()
                    painter.setColor(request.uiColor)
                    radius = request.uiRadius
                    radius *= scale
                    painter.setPointSize(radius)
                    for point in request.uiRegionPositionList:
                        point = OpenMaya.MPoint(x + point.x * scale + alignment_offset_x, y + point.y * scale, 0.0, 1.0)
                        painter.point2d(point)

                    painter.endDrawable()

                # draw point
                elif request.uiType == constants.kCircle:
                    painter.beginDrawable()
                    painter.setColor(request.uiColor)
                    painter.setLineWidth(line_width)
                    painter.setLineStyle(request.uiLineStyle)
                    radius = request.uiRadius
                    radius *= scale
                    for point in request.uiRegionPositionList:
                        point = OpenMaya.MPoint(x + point.x * scale + alignment_offset_x, y + point.y * scale, 0.0, 1.0)
                        painter.circle2d(point, radius, filled=request.uiFilled)

                    painter.endDrawable()

                # draw line
                elif request.uiType == constants.kLine:
                    painter.beginDrawable()
                    painter.setColor(request.uiColor)
                    painter.setLineWidth(line_width)
                    painter.setLineStyle(request.uiLineStyle)
                    previous_point = None
                    for point in request.uiRegionPositionList:
                        point = OpenMaya.MPoint(x + point.x * scale + alignment_offset_x, y + point.y * scale, 0.0, 1.0)
                        if previous_point is None:
                            previous_point = point
                            continue

                        else:
                            painter.line2d(previous_point, point)
                            previous_point = point

                    painter.endDrawable()
