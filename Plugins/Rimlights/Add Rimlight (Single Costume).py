__author__ = "Squidgy"

from SquidLib import *

def main():
	file = BrawlAPI.OpenFileDialog("Select costume PAC file", "PAC Files|*.pac")
	if file:
		rimlightFile(file)
		BrawlAPI.ShowMessage("Process completed.", "Complete")

main()