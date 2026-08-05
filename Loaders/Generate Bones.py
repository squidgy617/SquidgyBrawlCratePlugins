__author__ = "Squidgy"

from SquidLib import *

def generateBoneNodes(sender, event_args):
	prefix = BrawlAPI.UserStringInput("Enter a prefix for all bones")
	if prefix:
		startingIndex = BrawlAPI.UserIntegerInput("Enter starting index to use in bone names")
		if startingIndex != None and startingIndex > -1:
			numberToGenerate = BrawlAPI.UserIntegerInput("Enter number of bones to generate")
			if numberToGenerate != None and numberToGenerate > -1:
				node = BrawlAPI.SelectedNode
				node.Populate()
				for i in range(numberToGenerate):
					boneNode = MDL0BoneNode()
					boneNode.Name = f"{prefix}{startingIndex + i}"
					node.AddChild(boneNode)
	

BrawlAPI.AddContextMenuItem(MDL0BoneWrapper, "", "Batch generate child bones", None, ToolStripMenuItem("Batch generate bones", None, generateBoneNodes))