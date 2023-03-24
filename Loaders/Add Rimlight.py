__author__ = "Squidgy"

# Automatically add a rimlight to a selected material and all materials that share a shader with it
# Texture is pulled from Resources folder unless user selects the (Choose) option

from SquidLib import *

def addRimlight(sender, event_args):
	applyRimlight(BrawlAPI.SelectedNode)

def addRimlightChoose(sender, event_args):
	applyRimlight(BrawlAPI.SelectedNode, True)

def removeRimlight(sender, event_args):
	deleteRimlight(BrawlAPI.SelectedNode)
	

BrawlAPI.AddContextMenuItem(MDL0MaterialWrapper, "", "Add a rimlight to a material", None, ToolStripMenuItem("Add Rimlight", None, addRimlight))
BrawlAPI.AddContextMenuItem(MDL0MaterialWrapper, "", "Add a rimlight to a material", None, ToolStripMenuItem("Add Rimlight (Choose)", None, addRimlightChoose))
BrawlAPI.AddContextMenuItem(TEX0Wrapper, "", "Remove a rimlight based on texture name", None, ToolStripMenuItem("Remove Rimlight", None, removeRimlight))