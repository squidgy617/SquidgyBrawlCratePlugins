__author__ = "Squidgy"

# Automatically add a rimlight to a selected material and all materials that share a shader with it
# Texture is pulled from Resources folder unless user selects the (Choose) option

from SquidLib import *

def generateSlipspace(sender, event_args):
	generateSlipspaceNodes(BrawlAPI.SelectedNode)

def disableEnemies(sender, event_args):
	disableEnemyNodes(BrawlAPI.SelectedNode)

def defaultMemoryEnemies(sender, event_args):
	defaultAllEnemyMemory(BrawlAPI.SelectedNode)

def defaultPointsEnemies(sender, event_args):
	defaultAllEnemyPoints(BrawlAPI.SelectedNode)

def defaultFrequencyEnemy(sender, event_args):
	defaultEnemyFrequency(BrawlAPI.SelectedNode)
	

BrawlAPI.AddContextMenuItem(MDL0Wrapper, "", "Generate Slipspace nodes", None, ToolStripMenuItem("Generate Slipspace Nodes", None, generateSlipspace))
BrawlAPI.AddContextMenuItem(MDL0Wrapper, "", "Disable all enemies", None, ToolStripMenuItem("Disable all enemies", None, disableEnemies))
BrawlAPI.AddContextMenuItem(MDL0Wrapper, "", "Set all enemy memory to default", None, ToolStripMenuItem("Set all enemy memory to default", None, defaultMemoryEnemies))
BrawlAPI.AddContextMenuItem(MDL0Wrapper, "", "Set all enemy points to default", None, ToolStripMenuItem("Set all enemy points to default", None, defaultPointsEnemies))
BrawlAPI.AddContextMenuItem(MDL0BoneWrapper, "", "Set enemy frequency to default", None, ToolStripMenuItem("Set enemy frequency to default", None, defaultFrequencyEnemy))