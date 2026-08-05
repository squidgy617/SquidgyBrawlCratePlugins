__author__ = "Squidgy"

from SquidLib import *

MAX_INT = 99999

def copyBones(sender, event_args):
	modelIndex = BrawlAPI.UserIntegerInput("Enter index of MDL0 to copy to", "MDL0 Index", 0, 0, MAX_INT)
	if modelIndex != None and modelIndex > -1:
		model = BrawlAPI.SelectedNode
		model.Populate()
		modelFolder = model.BRESNode.GetFolder[MDL0Node]()
		if modelFolder:
			newModel = modelFolder.Children[modelIndex]
			if newModel:
				newModel.Populate()
				newModelBone = newModel.AllBones[0]
				modelBone = model.AllBones[0]
				if newModelBone and modelBone:
					addBones(newModelBone, modelBone)

def addBones(newParentBone, parentBone):
	for bone in parentBone.Children:
		boneNode = MDL0BoneNode()
		boneNode.Scale = bone.Scale
		boneNode.Rotation = bone.Rotation
		boneNode.Translation = bone.Translation
		boneNode.BoneIndex = bone.BoneIndex
		boneNode.Name = bone.Name
		newParentBone.AddChild(boneNode)
		addBones(boneNode, bone)
	

BrawlAPI.AddContextMenuItem(MDL0Wrapper, "", "Copy bones to another model", None, ToolStripMenuItem("Copy bones to another model", None, copyBones))