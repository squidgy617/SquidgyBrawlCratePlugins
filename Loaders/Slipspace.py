__author__ = "Squidgy"

# Automatically add a rimlight to a selected material and all materials that share a shader with it
# Texture is pulled from Resources folder unless user selects the (Choose) option

from SquidLib import *

def generateSlipspace(sender, event_args):
	generateSlipspaceNodes(BrawlAPI.SelectedNode)

def disableEnemies(sender, event_args):
	disableEnemyNodes(BrawlAPI.SelectedNode)
	

BrawlAPI.AddContextMenuItem(MDL0Wrapper, "", "Generate Slipspace nodes", None, ToolStripMenuItem("Generate Slipspace Nodes", None, generateSlipspace))
BrawlAPI.AddContextMenuItem(MDL0Wrapper, "", "Disable all enemies", None, ToolStripMenuItem("Disable all enemies", None, disableEnemies))