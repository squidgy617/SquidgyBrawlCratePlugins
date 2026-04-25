__author__ = "Squidgy"

# Automatically remove a GFX from the model it references

from SquidLib import *

def removeGFX(sender, event_args):
	removeGFXByNode(BrawlAPI.SelectedNode)

def removeGFXBRRES(sender, event_args):
	removeGFXByBRRES(BrawlAPI.SelectedNode)
	

BrawlAPI.AddContextMenuItem(MDL0Wrapper, "", "Remove GFX based on model", None, ToolStripMenuItem("Remove GFX", None, removeGFX))

BrawlAPI.AddContextMenuItem(BRESWrapper, "", "Remove GFX based on BRRES", None, ToolStripMenuItem("Remove GFX", None, removeGFXBRRES))