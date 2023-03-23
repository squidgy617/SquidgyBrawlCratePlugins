__author__ = "Squidgy"
__version__ = "1.0.0"

# Automatically add a rimlight to a selected material and all materials that share a shader with it
# Texture is pulled from Resources folder unless user selects the (Choose) option

from SquidLib import *

def addRimlight(sender, event_args):
	applyRimlight(BrawlAPI.SelectedNode)

def addRimlightChoose(sender, event_args):
	applyRimlight(BrawlAPI.SelectedNode, True)
	

BrawlAPI.AddContextMenuItem(MDL0MaterialWrapper, "", "Add a rimlight to a material", None, ToolStripMenuItem("Add Rimlight", None, addRimlight))
BrawlAPI.AddContextMenuItem(MDL0MaterialWrapper, "", "Add a rimlight to a material", None, ToolStripMenuItem("Add Rimlight (Choose)", None, addRimlightChoose))