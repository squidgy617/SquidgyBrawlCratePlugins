__author__ = "Squidgy"

from SquidLib import *

MAX_INT = 99999

def transferBones(sender, event_args):
	keyframe = BrawlAPI.UserIntegerInput("Enter keyframe of animation", "Keyframe", 0, 0, MAX_INT)
	if keyframe != None and keyframe > -1:
		startingIndex = BrawlAPI.UserIntegerInput("Enter first CHR0 entry index to transfer", "CHR0 Start Index", 0, 0, MAX_INT)
		if startingIndex != None and startingIndex > -1:
			endIndex = BrawlAPI.UserIntegerInput("Enter last CHR0 entry index to transfer", "CHR0 End Index", 0, 0, MAX_INT)
			if endIndex != None and endIndex > -1:
				modelIndex = BrawlAPI.UserIntegerInput("Enter index of MDL0 containing bones", "MDL0 Index", 0, 0, MAX_INT)
				if modelIndex != None and modelIndex > -1:
					node = BrawlAPI.SelectedNode
					modelFolder = node.BRESNode.GetFolder[MDL0Node]()
					if modelFolder:
						model = modelFolder.Children[modelIndex]
						if model:
							model.Populate()
							i = startingIndex
							while i < endIndex + 1:
								chr0Entry = node.Children[i]
								mdl0Bone = None
								# Find matching bone
								for bone in model.AllBones:
									if bone.Name == chr0Entry.Name:
										mdl0Bone = bone
								if mdl0Bone:
									scaleX = chr0Entry.GetFrameValue(0, keyframe)
									scaleY = chr0Entry.GetFrameValue(1, keyframe)
									scaleZ = chr0Entry.GetFrameValue(2, keyframe)
									rotX = chr0Entry.GetFrameValue(3, keyframe)
									rotY = chr0Entry.GetFrameValue(4, keyframe)
									rotZ = chr0Entry.GetFrameValue(5, keyframe)
									trnX = chr0Entry.GetFrameValue(6, keyframe)
									trnY = chr0Entry.GetFrameValue(7, keyframe)
									trnZ = chr0Entry.GetFrameValue(8, keyframe)
									boneNode = MDL0BoneNode()
									boneNode.Scale = Vector3(scaleX, scaleY, scaleZ)
									boneNode.Rotation = Vector3(rotX, rotY, rotZ)
									boneNode.Translation = Vector3(trnX, trnY, trnZ)
									boneNode.BoneIndex = mdl0Bone.BoneIndex
									mdl0Bone.Replace(boneNode)
									i += 1
								else:
									BrawlAPI.ShowMessage("Matching bone could not be found!", "Error")
	

BrawlAPI.AddContextMenuItem(CHR0Wrapper, "", "Transfer bone transformations to model", None, ToolStripMenuItem("Transfer bone transformations to model", None, transferBones))