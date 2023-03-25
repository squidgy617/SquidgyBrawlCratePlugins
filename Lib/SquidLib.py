# SquidLib
# Library for the plugins

from BrawlCrate.API import *
from BrawlCrate.NodeWrappers import * 
from BrawlLib.SSBB.ResourceNodes import *
from System.Windows.Forms import ToolStripMenuItem
from BrawlLib.Wii.Graphics import *
from BrawlLib.Wii.Textures import *
from BrawlCrate.API.BrawlAPI import AppPath
from BrawlLib.Internal.Windows.Forms import *
from BrawlCrate.UI import *
import clr
clr.AddReference("System")
from System.IO import *

RESOURCE_PATH = AppPath + '/BrawlAPI/Resources/SquidgyBrawlCratePlugins'

# Helper function that imports a texture automatically without prompting the user
def importTexture(node, imageSource, format, sizeW=0, sizeH=0):
		dlg = TextureConverterDialog()
		dlg.ImageSource = imageSource
		dlg.InitialFormat = format
		dlg.Automatic = 1
		replace = node.GetType() == TEX0Node
		# Resize image if sizes are passed in
		if sizeW != 0:
			if sizeH != 0:
				# If both width and height are passed in, resize using both
				dlg.InitialSize = Size(sizeW, sizeH)
			# If only width is passed in, use it for both
			else:
				dlg.InitialSize = Size(sizeW, sizeW)
		dlg.ShowDialog(MainForm.Instance, node)
		dlg.Dispose()
		if not replace:
			texFolder = getChildByName(node, "Textures(NW4R)")
			newNode = texFolder.Children[len(texFolder.Children) - 1]
			return newNode
		else:
			return node

# Get child node by name
def getChildByName(node, name):
		if node.Children:
			for child in node.Children:
				if child.Name == str(name):
					return child
		return 0

# Function to update texture matrixes on object nodes
def updateTextureMatrix(objectNode, index, enable=False):
	if index == 0:
		objectNode.TextureMatrix0Enabled = enable
	elif index == 1:
		objectNode.TextureMatrix1Enabled = enable
	elif index == 2:
		objectNode.TextureMatrix2Enabled = enable
	elif index == 3:
		objectNode.TextureMatrix3Enabled = enable
	elif index == 4:
		objectNode.TextureMatrix4Enabled = enable
	elif index == 5:
		objectNode.TextureMatrix5Enabled = enable
	elif index == 6:
		objectNode.TextureMatrix6Enabled = enable
	elif index == 7:
		objectNode.TextureMatrix7Enabled = enable
	

# Function to update texture refs on shader nodes
def updateTextureRef(shaderNode, index, enable=True):
	if index == 0:
		shaderNode.TextureRef0 = enable
	elif index == 1:
		shaderNode.TextureRef1 = enable
	elif index == 2:
		shaderNode.TextureRef2 = enable
	elif index == 3:
		shaderNode.TextureRef3 = enable
	elif index == 4:
		shaderNode.TextureRef4 = enable
	elif index == 5:
		shaderNode.TextureRef5 = enable
	elif index == 6:
		shaderNode.TextureRef6 = enable
	elif index == 7:
		shaderNode.TextureRef7 = enable

# Set map and coord ID for shader stages
def updateMapCoordId(shaderStage, index):
	if index == 0:
		shaderStage.TextureMapID = TexMapID.TexMap0
		shaderStage.TextureCoordID = TexCoordID.TexCoord0
	elif index == 1:
		shaderStage.TextureMapID = TexMapID.TexMap1
		shaderStage.TextureCoordID = TexCoordID.TexCoord1
	elif index == 2:
		shaderStage.TextureMapID = TexMapID.TexMap2
		shaderStage.TextureCoordID = TexCoordID.TexCoord2
	elif index == 3:
		shaderStage.TextureMapID = TexMapID.TexMap3
		shaderStage.TextureCoordID = TexCoordID.TexCoord3
	elif index == 4:
		shaderStage.TextureMapID = TexMapID.TexMap4
		shaderStage.TextureCoordID = TexCoordID.TexCoord4
	elif index == 5:
		shaderStage.TextureMapID = TexMapID.TexMap5
		shaderStage.TextureCoordID = TexCoordID.TexCoord5
	elif index == 6:
		shaderStage.TextureMapID = TexMapID.TexMap6
		shaderStage.TextureCoordID = TexCoordID.TexCoord6
	elif index == 7:
		shaderStage.TextureMapID = TexMapID.TexMap7
		shaderStage.TextureCoordID = TexCoordID.TexCoord7

def rimlightFile(file):
	fileOpened = BrawlAPI.OpenFile(file)
	if fileOpened:
		folder = BrawlAPI.RootNode.FindChild('Model Data [0]/3DModels(NW4R)', False)
		if folder:
			for child in folder.Children:
				# Get materials
				matFolder = child.FindChild('Materials', False)
				if matFolder:
					for material in matFolder.Children:
						# Don't apply to eyes or metal
						if 'eye' not in material.Name.lower() and 'ExtMtl' not in material.Name:
							applyRimlight(material, skipMessages=True)
					BrawlAPI.SaveFile()
		BrawlAPI.ForceCloseFile()

def removeRimlightFile(file, textureName):
	fileOpened = BrawlAPI.OpenFile(file)
	if fileOpened:
		folder = BrawlAPI.RootNode.FindChild('Texture Data [0]/Textures(NW4R)', False)
		if folder:
			textureNode = getChildByName(folder, textureName)
			if textureNode:
				changesMade = deleteRimlight(textureNode, skipMessages=True)
				if changesMade:
					BrawlAPI.SaveFile()
		BrawlAPI.ForceCloseFile()

def deleteRimlight(node, skipMessages=False):
	shaderStages = {}
	changesMade = False
	doContinue = True
	if not skipMessages:
		doContinue = BrawlAPI.ShowYesNoPrompt("This will remove rimlights using this texture from all materials. Continue?", "Continue?")
		if not doContinue:
			return
	# Get the models
	bresName = node.Parent.Parent.Name
	mdlBresName = bresName.replace("Texture", "Model")
	mdlBres = getChildByName(BrawlAPI.RootNode, mdlBresName)
	if mdlBres:
		modelFolder = getChildByName(mdlBres, "3DModels(NW4R)")
		if modelFolder:
			# Go through each model to remove rimlights
			for model in modelFolder.Children:
				matFolder = getChildByName(model, "Materials")
				if matFolder:
					for material in matFolder.Children:
						# Check if the rimlight is here
						matRefNode = None
						for matRef in material.Children:
							if matRef.Texture == node.Name:
								matRefNode = matRef
						# If it's here, store the shader and index
						if matRefNode:
							if material.ShaderNode.Name not in shaderStages:
								shaderStages[material.ShaderNode.Name] = matRefNode.Index
							# Find objects that use material
							objectFolder = getChildByName(model, "Objects")
							if objectFolder:
								for object in objectFolder.Children:
									for drawCall in object.DrawCalls:
										if drawCall.MaterialNode == material:
											updateTextureMatrix(object, matRefNode.Index, False)
							# Remove material reference
							matRefNode.Remove()
							changesMade = True
					# Remove shader stages
					if shaderStages != {}:
						shaderFolder = getChildByName(model, "Shaders")
						if shaderFolder:
							for key, value in shaderStages.items():
								shaderNode = getChildByName(shaderFolder, key)
								if shaderNode:
									shaderNode.Children[value].Remove()
									changesMade = True
	# Remove texture node
	node.Remove()
	return changesMade

def applyRimlight(node, choose=False, skipMessages=False):
	index = -1
	rimLightName = "Edge"
	image = None
	texNodeExists = False
	shaderNode = node.ShaderNode
	# Check materials to change and warning message
	nodesToChange = 0
	for child in node.Parent.Children:
		if child.ShaderNode == shaderNode:
			nodesToChange += 1
	if nodesToChange > 1:
		if not skipMessages:
			doContinue = BrawlAPI.ShowYesNoPrompt("This change will affect all materials that share this material's shader. Continue?", "Continue?")
		else: doContinue = True
		if not doContinue:
			return
	# Import texture if it does not exist
	bresName = node.Parent.Parent.Parent.Parent.Name
	texBresName = bresName.replace("Model", "Texture")
	texBres = getChildByName(BrawlAPI.RootNode, texBresName)
	if texBres:
		if choose:
			image = BrawlAPI.OpenFileDialog("Select rimlight texture", "PNG files|*.png")
		elif Directory.Exists(RESOURCE_PATH + '/Rimlight Texture'):
			images = Directory.GetFiles(RESOURCE_PATH + '/Rimlight Texture', '*.png')
			if len(images) > 0:
				image = images[0]
		else:
			if not skipMessages:
				doContinue = BrawlAPI.ShowYesNoPrompt("No rimlight texture could be found! Proceed anyway?", "No Texture Found")
			else:
				doContinue = True
			if not doContinue:
				return
		if image:
			rimLightName = FileInfo(image).Name.replace(".png", "")
			texFolder = getChildByName(texBres, "Textures(NW4R)")
			if texFolder:
				texNodeExists = getChildByName(texFolder, rimLightName)
			if not texNodeExists:
				texNode = importTexture(texBres, image, WiiPixelFormat.CMPR)
	# For each material that shares the same shader, add the rimlight if it does not exist
	for child in node.Parent.Children:
		if child.ShaderNode == shaderNode:
			if not getChildByName(child, rimLightName):
				newNode = MDL0MaterialRefNode()
				child.AddChild(newNode)
				newNode.Texture = rimLightName
				newNode.HasTextureMatrix = True
				newNode.MapMode = MappingMethod.EnvCamera
				newNode.UWrapMode = MatWrapMode.Clamp
				newNode.VWrapMode = MatWrapMode.Clamp
				newNode.Projection = TexProjection.STQ
				newNode.InputForm = TexInputForm.ABC1
				newNode.Coordinates = TexSourceRow.Normals
				newNode.EmbossSource = 5
				newNode.Normalize = True
				index = newNode.Index
	# Update the shader and add the shader stage to it
	if index > -1:
		updateTextureRef(shaderNode, index)
		match = False
		for stage in shaderNode.Children:
			if str(stage.TextureMapID) == "TexMap" + str(index):
				if str(stage.TextureCoordID) == "TexCoord" + str(index):
					match = True
		# Only add a shader stage if one with the same TexMap and TexCoord don't already exist
		if not match:
			shaderStage = MDL0TEVStageNode()
			shaderNode.AddChild(shaderStage)
			shaderStage.TextureEnabled = True
			updateMapCoordId(shaderStage, index)
			shaderStage.ConstantColorSelection = TevKColorSel.Constant1_2
			shaderStage.ColorSelectionB = ColorArg.TextureColor
			shaderStage.ColorSelectionC = ColorArg.ConstantColorSelection
			shaderStage.ColorSelectionD = ColorArg.OutputColor
			shaderStage.AlphaSelectionD = AlphaArg.OutputAlpha
			shaderStage.MoveUp()
			shaderStage.MoveUp()