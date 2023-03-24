__author__ = "Squidgy"

from SquidLib import *

def main():
	file = BrawlAPI.OpenFileDialog("Select costume PAC file", "PAC Files|*.pac")
	if file:
		textureName = BrawlAPI.UserStringInput("Enter texture name for rimlights")
		if textureName:
			removeRimlightFile(file, textureName)
			BrawlAPI.ShowMessage("Process completed.", "Complete")

main()