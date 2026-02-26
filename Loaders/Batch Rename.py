__author__ = "Squidgy"

# Automatically add a rimlight to a selected material and all materials that share a shader with it
# Texture is pulled from Resources folder unless user selects the (Choose) option

from SquidLib import *

def batchRenameBoneNode(sender, event_args):
	batchRenameBone(BrawlAPI.SelectedNode)
	

BrawlAPI.AddContextMenuItem(MDL0BoneWrapper, "", "Rename bone and update CHR0s to match", None, ToolStripMenuItem("Batch rename bone", None, batchRenameBoneNode))