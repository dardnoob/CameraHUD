import os
import json
import maya.api.OpenMaya as OpenMaya
import maya.cmds as cmds
from camerahudlib.private.logger import logger


class PluginCommand(OpenMaya.MPxCommand):

    kExport = "-ex"
    kExportLong = "-export"

    kImport = "-im"
    kImportLong = "-import"

    @staticmethod
    def cmdCreator():

        """
        get command creator
        """

        return PluginCommand()

    @staticmethod
    def syntaxCreator():

        """
        get syntax creator
        """

        syntax = OpenMaya.MSyntax()
        syntax.addFlag(PluginCommand.kExport, PluginCommand.kExportLong, OpenMaya.MSyntax.kString)
        syntax.addFlag(PluginCommand.kImport, PluginCommand.kImportLong, OpenMaya.MSyntax.kString)
        syntax.setObjectType(OpenMaya.MSyntax.kStringObjects)

        return syntax

    def __init__(self):

        """
        initialize command
        """

        OpenMaya.MPxCommand.__init__(self)

    def doIt(self, arg_list):

        """
        do command
        """

        result = []
        args_data, kwargs_data = self.parseArgument(arg_list)

        if args_data:
            # export node
            if "export" in kwargs_data:
                filename = kwargs_data["export"]
                data = {}
                for node in args_data:
                    if node:
                        if cmds.objExists(node):
                            result.append(node)
                            data["name"] = node
                            ui = {}
                            data["ui"] = ui

                            indexList = cmds.getAttr(node + ".ui", multiIndices=True)
                            size = cmds.getAttr(node + ".ui", size=True)
                            i = 0
                            while i < size:
                                index = indexList[i]
                                attribute = node + ".ui[" + str(index) + "]"
                                alias_name = cmds.aliasAttr(attribute, q=True)
                                if not alias_name:
                                    alias_name = None

                                ui_item = dict()
                                ui[attribute] = ui_item
                                ui_item["name"] = alias_name

                                ui_item["draw"] = cmds.getAttr(attribute + ".draw")
                                ui_item["gateDraw"] = cmds.getAttr(attribute + ".gateDraw")
                                ui_item["uiType"] = cmds.getAttr(attribute + ".uiType")
                                ui_item["resolutionGate"] = cmds.getAttr(attribute + ".resolutionGate")
                                ui_item["horizontalAttach"] = cmds.getAttr(attribute + ".horizontalAttach")
                                ui_item["verticalAttach"] = cmds.getAttr(attribute + ".verticalAttach")
                                ui_item["textBackgroundColor"] = cmds.getAttr(attribute + ".textBackgroundColor")[0]
                                ui_item["textBackgroundTransparency"] = cmds.getAttr(attribute + ".textBackgroundTransparency")
                                ui_item["fontStyle"] = cmds.getAttr(attribute + ".fontStyle", asString=True)
                                ui_item["text"] = cmds.getAttr(attribute + ".text")
                                ui_item["fontWeight"] = cmds.getAttr(attribute + ".fontWeight")
                                ui_item["textIncline"] = cmds.getAttr(attribute + ".textIncline")
                                ui_item["fontLine"] = cmds.getAttr(attribute + ".fontLine")
                                ui_item["verticalAlignment"] = cmds.getAttr(attribute + ".verticalAlignment")
                                ui_item["horizontalAlignment"] = cmds.getAttr(attribute + ".horizontalAlignment")
                                ui_item["fontSize"] = cmds.getAttr(attribute + ".fontSize")
                                ui_item["fontStretch"] = cmds.getAttr(attribute + ".fontStretch")
                                ui_item["size"] = cmds.getAttr(attribute + ".size")
                                ui_item["lineWidth"] = cmds.getAttr(attribute + ".lineWidth")
                                ui_item["fitToResolutionGate"] = cmds.getAttr(attribute + ".fitToResolutionGate")
                                ui_item["radius"] = cmds.getAttr(attribute + ".radius")
                                ui_item["filled"] = cmds.getAttr(attribute + ".filled")
                                ui_item["regionColor"] = cmds.getAttr(attribute + ".regionColor")[0]
                                ui_item["regionTransparency"] = cmds.getAttr(attribute + ".regionTransparency")
                                ui_item["color"] = cmds.getAttr(attribute + ".color")[0]
                                ui_item["transparency"] = cmds.getAttr(attribute + ".transparency")
                                ui_item["region"] = cmds.getAttr(attribute + ".region")[0]
                                ui_item["regionPosition"] = cmds.getAttr(attribute + ".regionPosition")[0]
                                ui_item["regionDraw"] = cmds.getAttr(attribute + ".regionDraw")
                                ui_item["regionIsFilled"] = cmds.getAttr(attribute + ".regionIsFilled")

                                positions = []
                                ui_item["position"] = positions
                                position_size = cmds.getAttr(attribute + ".position", size=True)
                                if position_size == 0:
                                    position_size = 1

                                positions_indexes = cmds.getAttr(attribute + ".position", multiIndices=True)
                                if not positions_indexes:
                                    positions_indexes = [0]

                                n = 0
                                while n < position_size:
                                    index = positions_indexes[i]
                                    position = cmds.getAttr(attribute + ".position[" + str(index) + "]")
                                    if position:
                                        position = position[0]
                                        positions.append(position)

                                    n += 1

                                i += 1

                # write to file
                try:
                    data = json.dumps(data)

                except Exception as exception_data:
                    logger.error(exception_data)
                    logger.error("can`t load json data")
                    data = ""

                if data:
                    if os.path.isfile(filename):
                        os.remove(filename)

                    obj = open(filename, "w")
                    obj.write(data)
                    obj.close()

            # import node
            if "import" in kwargs_data:
                filename = kwargs_data["import"]
                if filename:
                    if os.path.isfile(filename):
                        # load from file
                        obj = open(filename, "r")
                        data = obj.read()
                        obj.close()
                        if data:
                            try:
                                data = json.loads(data)

                            except Exception as exception_data:
                                logger.error(exception_data)
                                logger.error("can`t load json data")
                                data = {}

                            if data:
                                for node_name in args_data:
                                    # create node
                                    name = data["name"]
                                    node = cmds.createNode("CameraHUD", name=name + "#")
                                    if name:
                                        node = cmds.rename(node, node_name)
                                        result.append(node)

                                    cmds.connectAttr("defaultResolution.width", node + ".uiResolution0")
                                    cmds.connectAttr("defaultResolution.height", node + ".uiResolution1")

                                    # load attribute data
                                    index = 0
                                    for attribute_key in data["ui"]:
                                        attribute = node + ".ui[" + str(index) + "]"
                                        ui_item = data["ui"][attribute_key]
                                        attribute_name = None
                                        if "name" in ui_item:
                                            attribute_name = ui_item["name"]
                                            del ui_item["name"]

                                        for ui_attribute in ui_item:
                                            if ui_attribute == "draw":
                                                cmds.setAttr(attribute + "." + ui_attribute, ui_item[ui_attribute])

                                            elif ui_attribute == "gateDraw":
                                                cmds.setAttr(attribute + "." + ui_attribute, ui_item[ui_attribute])

                                            elif ui_attribute == "uiType":
                                                cmds.setAttr(attribute + "." + ui_attribute, ui_item[ui_attribute])

                                            elif ui_attribute == "resolutionGate":
                                                cmds.setAttr(attribute + "." + ui_attribute, ui_item[ui_attribute])

                                            elif ui_attribute == "horizontalAttach":
                                                cmds.setAttr(attribute + "." + ui_attribute, ui_item[ui_attribute])

                                            elif ui_attribute == "verticalAttach":
                                                cmds.setAttr(attribute + "." + ui_attribute, ui_item[ui_attribute])

                                            elif ui_attribute == "textBackgroundColor":
                                                value = ui_item[ui_attribute]
                                                cmds.setAttr(attribute + "." + ui_attribute, value[0], value[1], value[2], type="double3")

                                            elif ui_attribute == "textBackgroundTransparency":
                                                cmds.setAttr(attribute + "." + ui_attribute, ui_item[ui_attribute])

                                            elif ui_attribute == "fontStyle":
                                                active_item = ui_item[ui_attribute]
                                                item_list = cmds.attributeQuery("fontStyle", node=node, listEnum=True)
                                                active_item_index = 0
                                                if item_list:
                                                    item_list = item_list[0]
                                                    item_list = item_list.split(":")
                                                    item_index = 0
                                                    for item in item_list:
                                                        if item == active_item:
                                                            active_item_index = item_index
                                                            break

                                                        item_index += 1

                                                cmds.setAttr(attribute + "." + ui_attribute, active_item_index)

                                            elif ui_attribute == "text":
                                                cmds.setAttr(attribute + "." + ui_attribute, ui_item[ui_attribute], type="string")

                                            elif ui_attribute == "fontWeight":
                                                cmds.setAttr(attribute + "." + ui_attribute, ui_item[ui_attribute])

                                            elif ui_attribute == "textIncline":
                                                cmds.setAttr(attribute + "." + ui_attribute, ui_item[ui_attribute])

                                            elif ui_attribute == "fontLine":
                                                cmds.setAttr(attribute + "." + ui_attribute, ui_item[ui_attribute])

                                            elif ui_attribute == "verticalAlignment":
                                                cmds.setAttr(attribute + "." + ui_attribute, ui_item[ui_attribute])

                                            elif ui_attribute == "horizontalAlignment":
                                                cmds.setAttr(attribute + "." + ui_attribute, ui_item[ui_attribute])

                                            elif ui_attribute == "fontSize":
                                                cmds.setAttr(attribute + "." + ui_attribute, ui_item[ui_attribute])

                                            elif ui_attribute == "fontStretch":
                                                cmds.setAttr(attribute + "." + ui_attribute, ui_item[ui_attribute])

                                            elif ui_attribute == "size":
                                                cmds.setAttr(attribute + "." + ui_attribute, ui_item[ui_attribute])

                                            elif ui_attribute == "lineWidth":
                                                cmds.setAttr(attribute + "." + ui_attribute, ui_item[ui_attribute])

                                            elif ui_attribute == "fitToResolutionGate":
                                                cmds.setAttr(attribute + "." + ui_attribute, ui_item[ui_attribute])

                                            elif ui_attribute == "radius":
                                                cmds.setAttr(attribute + "." + ui_attribute, ui_item[ui_attribute])

                                            elif ui_attribute == "filled":
                                                cmds.setAttr(attribute + "." + ui_attribute, ui_item[ui_attribute])

                                            elif ui_attribute == "regionColor":
                                                value = ui_item[ui_attribute]
                                                cmds.setAttr(attribute + "." + ui_attribute, value[0], value[1], value[2], type="double3")

                                            elif ui_attribute == "regionTransparency":
                                                cmds.setAttr(attribute + "." + ui_attribute, ui_item[ui_attribute])

                                            elif ui_attribute == "color":
                                                value = ui_item[ui_attribute]
                                                cmds.setAttr(attribute + "." + ui_attribute, value[0], value[1], value[2], type="double3")

                                            elif ui_attribute == "transparency":
                                                cmds.setAttr(attribute + "." + ui_attribute, ui_item[ui_attribute])

                                            elif ui_attribute == "regionDraw":
                                                cmds.setAttr(attribute + "." + ui_attribute, ui_item[ui_attribute])

                                            elif ui_attribute == "regionIsFilled":
                                                cmds.setAttr(attribute + "." + ui_attribute, ui_item[ui_attribute])

                                            elif ui_attribute == "region":
                                                value = ui_item[ui_attribute]
                                                cmds.setAttr(attribute + "." + ui_attribute, value[0], value[1], type="double2")

                                            elif ui_attribute == "regionPosition":
                                                value = ui_item[ui_attribute]
                                                cmds.setAttr(attribute + "." + ui_attribute, value[0], value[1], type="double2")

                                            elif ui_attribute == "position":
                                                position_index = 0
                                                for position_value in ui_item[ui_attribute]:
                                                    cmds.setAttr(attribute + "." + ui_attribute + "[" + str(position_index) + "]", position_value[0], position_value[1], type="double2")
                                                    position_index += 1

                                        if attribute_name:
                                            cmds.aliasAttr(attribute_name, attribute)

                                        index += 1

        self.setResult(result)

    def parseArgument(self, arg_list):

        """
        get parsed dictionary
        """

        result_args, result_kwargs = [], {}
        arg_data = OpenMaya.MArgParser(self.syntax(), arg_list)
        if arg_data.isFlagSet(PluginCommand.kExport):
            filename = arg_data.flagArgumentString(PluginCommand.kExport, 0)
            result_kwargs["export"] = filename

        if arg_data.isFlagSet(PluginCommand.kImport):
            filename = arg_data.flagArgumentString(PluginCommand.kImport, 0)
            result_kwargs["import"] = filename

        result_args = arg_data.getObjectStrings()
        result_args = list(result_args)

        return result_args, result_kwargs
