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
from BrawlLib.Internal import Vector3

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

POINTS_TO_FREQUENCY = {
	100: 100,
	200: 95,
	300: 90,
	400: 85,
	500: 80,
	600: 65,
	700: 60,
	800: 55,
	900: 50,
	1000: 45,
	1300: 40,
	1500: 30,
	2000: 20,
	3000: 10,
}

class Enemy:
	enemy_id: int
	name: str
	points: int
	frequency: int
	instance_memory: int
	resource_memory: int
	starting_action: int
	persistent_memory: int
	def __init__(self, enemy_id, name, points, frequency, instance_memory, resource_memory, starting_action, persistent_memory = 0):
		self.enemy_id = enemy_id
		self.name = name
		self.points = points
		self.frequency = frequency
		self.instance_memory = instance_memory
		self.resource_memory = resource_memory
		self.starting_action = starting_action
		self.persistent_memory = persistent_memory

class EnemyGroupEntry:
	enemy_id: int
	name: str
	resource_memory: int
	def __init__(self, enemy_id, name, resource_memory):
		self.enemy_id = enemy_id
		self.name = name
		self.resource_memory = resource_memory

enemies = [
	Enemy(26, "Shaydas", 900,  POINTS_TO_FREQUENCY[900],  43712, 287424, 8),
	Enemy(12, "Armight", 1000, POINTS_TO_FREQUENCY[1000], 74400, 286912, 4),
	Enemy(22, "Puppit", 500,  POINTS_TO_FREQUENCY[500],  31392, 289376, 4),
	Enemy(21, "Floow", 800,  POINTS_TO_FREQUENCY[800],  36896, 199680, 4),
	Enemy(10, "Bucculus", 800, POINTS_TO_FREQUENCY[800], 51552, 203872, 7),
	Enemy(27, "Bombed", 500,  POINTS_TO_FREQUENCY[500],  45142, 304160, 7),
	Enemy(2, "Feyesh", 400,   POINTS_TO_FREQUENCY[400],  41952, 170880, 4),
	Enemy(1, "Poppant", 1000, POINTS_TO_FREQUENCY[1000], 38528, 338496, 0),
	Enemy(35, "Sword Primid", 400, POINTS_TO_FREQUENCY[400], 74176, 1254656, 8),
	Enemy(32, "Boomerang Primid", 500, POINTS_TO_FREQUENCY[500], 73728, 1256128, 0),
	Enemy(23, "Primid", 300,  POINTS_TO_FREQUENCY[300],  72160, 1254656, 0),
	Enemy(34, "Scope Primid", 500, POINTS_TO_FREQUENCY[500], 74528, 1256320, 0),
	Enemy(33, "Fire Primid", 400, POINTS_TO_FREQUENCY[400], 72256, 1255744, 92),
	Enemy(28, "Metal Primid", 500, POINTS_TO_FREQUENCY[500], 72256, 1254656, 0),
	Enemy(31, "Big Primid", 1000, POINTS_TO_FREQUENCY[1000], 72160, 1254656, 0),
	Enemy(11, "Greap", 1500, POINTS_TO_FREQUENCY[1500], 55680, 305024, 0),
	Enemy(6, "Roturret", 1500, POINTS_TO_FREQUENCY[1500], 29600, 255680, 4),
	Enemy(41, "Autolance", 1300, POINTS_TO_FREQUENCY[1300], 48896, 630784, 0),
	Enemy(18, "Towtow", 2000, POINTS_TO_FREQUENCY[2000], 42976, 390336, 9),
	Enemy(24, "Shellpod", 1500, POINTS_TO_FREQUENCY[1500], 44800, 393056, 0),
	Enemy(7, "Borboras", 600,  POINTS_TO_FREQUENCY[600],  38176, 399040, 7),
	Enemy(4, "Auroros", 400,  POINTS_TO_FREQUENCY[400],  38752, 312608, 4),
	Enemy(0, "Goomba", 200,   POINTS_TO_FREQUENCY[200],  51008, 217888, 7),
	Enemy(5, "Cymul", 700,    POINTS_TO_FREQUENCY[700],  28800, 137600, 4),
	Enemy(43, "Glire", 400,   POINTS_TO_FREQUENCY[400],  33824, 263904, 0),
	Enemy(45, "Glunder", 400, POINTS_TO_FREQUENCY[400],  33824, 263904, 0),
	Enemy(44, "Glice", 400,   POINTS_TO_FREQUENCY[400],  33824, 263904, 0),
	Enemy(15, "Spaak", 400,   POINTS_TO_FREQUENCY[400],  37120, 448544, 5),
	Enemy(16, "Mite", 100,    POINTS_TO_FREQUENCY[100],  29344, 75488, 0),
	Enemy(17, "Ticken", 1000, POINTS_TO_FREQUENCY[1000], 33056, 472832, 0),
	Enemy(9, "Buckot", 400,   POINTS_TO_FREQUENCY[400],  37408, 423136, 4),
	Enemy(20, "Bytan", 200,   POINTS_TO_FREQUENCY[200],  29408, 186816, 0),
	Enemy(14, "Roader", 800,  POINTS_TO_FREQUENCY[800],  36480, 288672, 0),
	Enemy(29, "Nagagog", 2000, POINTS_TO_FREQUENCY[2000], 45408, 490336, 5),
	Enemy(30, "Trowlon", 600, POINTS_TO_FREQUENCY[600],  35008, 363712, 5),
	Enemy(42, "Armank", 3000, POINTS_TO_FREQUENCY[3000], 55456, 749920, 29),
	Enemy(25, "Koopa", 200,   POINTS_TO_FREQUENCY[200],  55456, 314752, 5),
	Enemy(19, "Hammer Bro", 500, POINTS_TO_FREQUENCY[500], 36448, 225408, 0),
	Enemy(13, "Bullet Bill", 500, POINTS_TO_FREQUENCY[500], 31264, 282624, 6),
	Enemy(8, "Giant Goomba", 1000, POINTS_TO_FREQUENCY[1000], 50304, 258272, 0),
	Enemy(36, "Gamyga", 1500, POINTS_TO_FREQUENCY[1500], 30560, 287552, 5),
	Enemy(40, "R.O.B. Sentry", 300, POINTS_TO_FREQUENCY[300], 38368, 439168, 0),
	Enemy(37, "R.O.B. Blaster", 400, POINTS_TO_FREQUENCY[400], 37728, 435072, 0),
	Enemy(39, "R.O.B. Launcher", 600, POINTS_TO_FREQUENCY[600], 37696, 431424, 0),
	Enemy(38, "R.O.B. Distance", 400, POINTS_TO_FREQUENCY[400], 38560, 435648, 6),
]

enemyGroups = [
	[
		EnemyGroupEntry(35, "SharedPrimSword", 137856),
		EnemyGroupEntry(32, "SharedPrimBoom", 139488),
		EnemyGroupEntry(23, "SharedPrim", 137856),
		EnemyGroupEntry(34, "SharedPrimScope", 139520),
		EnemyGroupEntry(33, "SharedPrimFire", 138944),
		EnemyGroupEntry(28, "SharedPrimMetal", 137856),
		EnemyGroupEntry(31, "SharedPrimBig", 137856)
	],
	[
		EnemyGroupEntry(43, "SharedGlire", 21248),
		EnemyGroupEntry(45, "SharedGlunder", 21248),
		EnemyGroupEntry(44, "SharedGlice", 21248)
	]
]

bones = [
	"Targets",
	"Disks",
	"Platforms",
	"Sliders",
	"Springs",
	"Cannons",
	"Ladders",
	"Catapults",
	"Warps",
	"Toxins",
	"Conveyors",
	"Waters",
	"Winds",
	"Items",
	"Enemies",
	"EnemyGroups",
	"Spawners",
	"Respawns",
	"TourObjects",
	"TourStates",
	"End"
]

def generateSlipspaceNodes(node):
	boneGroup = node._boneGroup
	if (boneGroup and len(boneGroup.Children) > 0):
		topNode = boneGroup.Children[0]
		for bone in bones:
			# Check if bone exists already
			boneFound = False
			for child in topNode.Children:
				if child.Name == bone:
					boneFound = True
					break
			if boneFound:
				continue
			# If not, add it
			boneNode = MDL0BoneNode()
			boneNode.Name = bone
			topNode.AddChild(boneNode)
		enemyNode = topNode.FindChild("Enemies")
		if (enemyNode):
			for enemy in enemies:
				# Check if bone exists already
				boneFound = False
				for child in enemyNode.Children:
					if child.Name == enemy.name:
						boneFound = True
						break
				if boneFound:
					continue
				# If not, add it
				boneNode = MDL0BoneNode()
				boneNode.Scale = Vector3(enemy.enemy_id, 1, enemy.starting_action)
				boneNode.Translation = Vector3(enemy.points, enemy.instance_memory, enemy.resource_memory)
				boneNode.Name = enemy.name
				enemyNode.AddChild(boneNode)
		enemyGroupsNode = topNode.FindChild("EnemyGroups")
		if (enemyGroupsNode):
			groups = 0
			for enemyGroup in enemyGroups:
				# Check if bone exists already
				boneFound = False
				for child in enemyGroupsNode.Children:
					if child.Name == f"EnemyGroup{groups}":
						boneFound = True
						break
				if boneFound:
					continue
				# If not, add it
				enemyGroupStart = MDL0BoneNode()
				enemyGroupStart.Name = f"EnemyGroup{groups}"
				enemyGroupsNode.AddChild(enemyGroupStart)
				for enemyGroupEntry in enemyGroup:
					enemyGroupEntryBone = MDL0BoneNode()
					enemyGroupEntryBone.Name = enemyGroupEntry.name
					enemyGroupEntryBone.Scale = Vector3(enemyGroupEntry.enemy_id, 1, 1)
					enemyGroupEntryBone.Translation = Vector3(0,0,enemyGroupEntry.resource_memory)
					enemyGroupStart.AddChild(enemyGroupEntryBone)
				enemyGroupEnd = MDL0BoneNode()
				enemyGroupEnd.Name = f"EnemyGroupEnd{groups}"
				enemyGroupStart.AddChild(enemyGroupEnd)
				groups += 1

def disableEnemyNodes(node):
	boneGroup = node._boneGroup
	if (boneGroup and len(boneGroup.Children) > 0):
		topNode = boneGroup.Children[0]
		enemyNode = topNode.FindChild("Enemies")
		if (enemyNode):
			for enemyBone in enemyNode.Children:
				boneNode = MDL0BoneNode()
				boneNode.Scale = enemyBone.Scale
				boneNode.Translation = enemyBone.Translation
				boneNode.Rotation = Vector3(enemyBone.Rotation._x, enemyBone.Rotation._y, 0)
				boneNode.BoneIndex = enemyBone.BoneIndex
				enemyBone.Replace(boneNode)

def findEnemy(id):
	for enemy in enemies:
		if enemy.enemy_id == id:
			return enemy
	return None

def defaultAllEnemyMemory(node):
	boneGroup = node._boneGroup
	if (boneGroup and len(boneGroup.Children) > 0):
		topNode = boneGroup.Children[0]
		enemyNode = topNode.FindChild("Enemies")
		if (enemyNode):
			for enemyBone in enemyNode.Children:
				boneNode = MDL0BoneNode()
				enemy = findEnemy(enemyBone.Scale._x)
				if enemy:
					boneNode.Scale = enemyBone.Scale
					boneNode.Translation = Vector3(enemyBone.Translation._x, enemy.persistent_memory, enemyBone.Translation._z)
					boneNode.Rotation = Vector3(enemyBone.Rotation._x, enemy.instance_memory, enemy.resource_memory)
					boneNode.BoneIndex = enemyBone.BoneIndex
					enemyBone.Replace(boneNode)

def defaultAllEnemyPoints(node):
	boneGroup = node._boneGroup
	if (boneGroup and len(boneGroup.Children) > 0):
		topNode = boneGroup.Children[0]
		enemyNode = topNode.FindChild("Enemies")
		if (enemyNode):
			for enemyBone in enemyNode.Children:
				boneNode = MDL0BoneNode()
				enemy = findEnemy(enemyBone.Scale._x)
				if enemy:
					boneNode.Scale = enemyBone.Scale
					boneNode.Translation = enemyBone.Translation
					boneNode.Rotation = Vector3(enemy.points, enemyBone.Rotation._y, enemyBone.Rotation._z)
					boneNode.BoneIndex = enemyBone.BoneIndex
					enemyBone.Replace(boneNode)

def defaultEnemyFrequency(node):
	enemy = findEnemy(node.Scale._x)
	if enemy:
		boneNode = MDL0BoneNode()
		boneNode.Scale = node.Scale
		boneNode.Translation = node.Translation
		boneNode.Rotation = Vector3(node.Rotation._x, node.Rotation._y, enemy.frequency)
		boneNode.BoneIndex = node.BoneIndex
		node.Replace(boneNode)