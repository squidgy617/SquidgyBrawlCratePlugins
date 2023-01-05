__author__ = "Squidgy"
__version__ = "1.0.0"

# Automatically add a rimlight to a selected material and all materials that share a shader with it
# Texture is pulled from Resources folder unless user selects the (Choose) option

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

# Function to update texture refs on shader nodes
def updateTextureRef(shaderNode, index):
	if index == 0:
		shaderNode.TextureRef0 = True
	elif index == 1:
		shaderNode.TextureRef1 = True
	elif index == 2:
		shaderNode.TextureRef2 = True
	elif index == 3:
		shaderNode.TextureRef3 = True
	elif index == 4:
		shaderNode.TextureRef4 = True
	elif index == 5:
		shaderNode.TextureRef5 = True
	elif index == 6:
		shaderNode.TextureRef6 = True
	elif index == 7:
		shaderNode.TextureRef7 = True

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

def addRimlight(sender, event_args):
	main(BrawlAPI.SelectedNode)

def addRimlightChoose(sender, event_args):
	main(BrawlAPI.SelectedNode, True)

def main(node, choose=False):
	index = 0
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
		doContinue = BrawlAPI.ShowYesNoPrompt("This change will affect all materials that share this material's shader. Continue?", "Continue?")
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
			doContinue = BrawlAPI.ShowYesNoPrompt("No rimlight texture could be found! Proceed anyway?", "No Texture Found")
			if not doContinue:
				return
		if image:
			rimLightName = FileInfo(image).Name.replace(".png", "")
			texFolder = getChildByName(texBres, "Textures(NW4R)")
			if texFolder:
				texNodeExists = getChildByName(texFolder, rimLightName)
			if not texNodeExists:
				texNode = importTexture(texBres, image, WiiPixelFormat.I8)
	# For each material that shares the same shader, add the rimlight
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
	updateTextureRef(shaderNode, index)
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
	

BrawlAPI.AddContextMenuItem(MDL0MaterialWrapper, "", "Add a rimlight to a material", None, ToolStripMenuItem("Add Rimlight", None, addRimlight))
BrawlAPI.AddContextMenuItem(MDL0MaterialWrapper, "", "Add a rimlight to a material", None, ToolStripMenuItem("Add Rimlight (Choose)", None, addRimlightChoose))