import maya.api.OpenMaya as OpenMaya
import maya.api.OpenMayaRender as OpenMayaRender
from camerahudlib import constants
from camerahudlib.private.logger import logger
from camerahudlib.private.plugin import Plugin
from camerahudlib.private.plugin_override import PluginOverride
from camerahudlib.private.plugin_command import PluginCommand


def maya_useNewAPI():

    """
    The presence of this function tells Maya that the plugin produces, and
    expects to be passed, objects created using the Maya Python API 2.0.
    """

    pass


def initializePlugin(obj):

    """
    Initialize plugin.
    """

    plugin = OpenMaya.MFnPlugin(obj, "Autodesk", "3.0", "Any")

    try:
        plugin.registerNode(
            constants.kName,
            constants.kId,
            Plugin.creator,
            Plugin.initialize,
            OpenMaya.MPxNode.kLocatorNode,
            constants.kDrawDbClassification
        )

    except Exception as exception_data:
        logger.error(repr(exception_data))
        logger.error("can`t register node")
        raise

    try:
        OpenMayaRender.MDrawRegistry.registerDrawOverrideCreator(
            constants.kDrawDbClassification,
            constants.kDrawRegistrantId,
            PluginOverride.creator
        )

    except Exception as exception_data:
        logger.error(repr(exception_data))
        logger.error("can`t register override")
        raise

    try:
        plugin.registerCommand(constants.kName, PluginCommand.cmdCreator, PluginCommand.syntaxCreator)

    except Exception as exception_data:
        logger.error(repr(exception_data))
        logger.error("can`t register command")
        raise


def uninitializePlugin(obj):

    """
    Uninitialize plugin.
    """

    plugin = OpenMaya.MFnPlugin(obj)

    try:
        plugin.deregisterNode(constants.kId)

    except Exception as exception_data:
        logger.error(repr(exception_data))
        logger.error("can`t unregister node")
        raise

    try:
        OpenMayaRender.MDrawRegistry.deregisterDrawOverrideCreator(
            constants.kDrawDbClassification,
            constants.kDrawRegistrantId
        )

    except Exception as exception_data:
        logger.error(repr(exception_data))
        logger.error("can`t unregister override")
        raise

    try:
        plugin.deregisterCommand(constants.kName)

    except Exception as exception_data:
        logger.error(repr(exception_data))
        logger.error("can`t unregister command")
        raise
