# CameraHUD
CameraHUD is a plugin for drawing custom hud in the Maya viewport.

![CameraHUD](/screenshots/preview.png?raw=true "CameraHUD")

### Requirements
* PySide for Maya <= 2017
* PySide2 for Maya >= 2017
* Maya >= 2013


### How to use
##### Create node example
```
import maya import cmds

#load plugin
if not cmds.pluginInfo("CameraHUD", q=True, loaded=True):
    cmds.loadPlugin("path/to/plugin/directory/CameraHUD.py")

#create CameraHUD node
node = cmds.createNode("CameraHUD")

#connect to defaultResolution node for correct resolution
cmds.connectAttr("defaultResolution.width", node + ".uiResolution0")
cmds.connectAttr("defaultResolution.height", node + ".uiResolution1")

cmds.setAttr(node + ".ui[0].region", 50, 25)        # set region size
cmds.setAttr(node + ".ui[0].regionPosition", 0, 0)  # set region position
```


### TODO
* Interface over viewport
* Custom callbacks
* Fix crashes
