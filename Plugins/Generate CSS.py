__author__ = "Squidgy"

from SquidLib import *
from BrawlLib.Internal import Vector3
from BrawlLib.Wii.Models.ModelLinker import RegenerateBoneCache
from BrawlLib.SSBB.Types import BoneFlags

ICON_COUNT = 42
ICONS_PER_ROW = 7
ROWCOUNT = 6
STARTPOINT = -18.6
HORIZONTAL_DIST = 6.2
VERTICAL_DIST = 5.4
TOTAL_DIST = 43.4
ICON_SCALE = 1

def main():
		mdl0Bones = BrawlAPI.RootNode.FindChild('3DModels(NW4R)/MenAdvChrC0001_TopN/Bones/MenAdvChrC0001_TopN')
		chr = BrawlAPI.RootNode.FindChild('AnmChr(NW4R)/MenAdvChrC0001_TopN__0')
		# Modify this
		setIconsPerRow = 13
		# Calculate new values
		iconsPerRow = setIconsPerRow - 1
		horizontalDist = TOTAL_DIST / iconsPerRow
		modifier = HORIZONTAL_DIST / horizontalDist # the amount by which each item is modified for new CSS
		verticalDist = VERTICAL_DIST / modifier
		rowCount = ROWCOUNT * modifier
		totalDist = horizontalDist * iconsPerRow
		startpoint = STARTPOINT - horizontalDist # * modifier
		iconScale = ICON_SCALE / modifier
		iconCount = iconsPerRow * rowCount

		# Generate missing icons and update flags
		i = 0
		flags = [ BoneFlags.FixedRotation, BoneFlags.FixedScale, BoneFlags.ScaleEqual, BoneFlags.Visible]
		for node in mdl0Bones.Children:
			if node.Name.startswith('pos'):
				node.Flags = BoneFlags.None
				finalFlag = 0
				for flag in flags:
					finalFlag += int(flag)
				node.Flags = BoneFlags(finalFlag)
				i += 1
		while i < iconCount:
			newNode = MDL0BoneNode()
			newNode.Name = 'pos' + addLeadingZeros(str(i), 2)
			newNode.Flags = BoneFlags.None
			finalFlag = 0
			for flag in flags:
				finalFlag += int(flag)
			newNode.Flags = BoneFlags(finalFlag)
			mdl0Bones.AddChild(newNode)
			i += 1

		# Move the upN1 bone to the bottom
		upNBone = mdl0Bones.FindChild('upN1')
		while upNBone.NextSibling():
			upNBone.MoveDown()

		# Regenerate bone array
		mdl0Bones.Model._linker.RegenerateBoneCache(True)

		# Generate missing bones in animation
		i = 0
		for node in chr.Children:
			if node.Name.startswith('pos'):
				i += 1
		while i < iconCount:
			chr.CreateEntry('pos' + addLeadingZeros(str(i), 2))
			i += 1

		# Animate the slots
		rowIcons = 0
		xPos = startpoint
		yPos = 0
		for node in chr.Children:
			if node.Name.startswith('pos'):
				# For each frame of the animation
				for k in range(node.FrameCount):
					# Set scale
					node.SetKeyframeOnlyScale(k, Vector3(iconScale, iconScale, iconScale))
					# Set translation
					node.SetKeyframeOnlyTrans(k, Vector3(xPos, yPos, 0))
				# Move to the right one
				xPos += horizontalDist
				# If we are at the end of a row, go back to start and go down 1 row
				if rowIcons == iconsPerRow:
					rowIcons = 0
					xPos = startpoint
					yPos -= verticalDist
				else:
					rowIcons += 1

main()