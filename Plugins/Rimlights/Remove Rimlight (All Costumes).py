__author__ = "Squidgy"

from SquidLib import *

def main():
		doContinue = BrawlAPI.ShowYesNoPrompt("This process can take a long time. Do you wish to continue?", "Continue?")
		if doContinue:
			textureName = BrawlAPI.UserStringInput("Enter texture name for rimlights")
			if textureName:
				if Directory.Exists(MainForm.BuildPath + '/pf/fighter'):
					# First get all files
					i = 0
					for directory in Directory.GetDirectories(MainForm.BuildPath + '/pf/fighter'):
						for file in Directory.GetFiles(directory, "*.pac"):
							# Check that it's a costume
							if FileInfo(file).Name.lower().replace(DirectoryInfo(directory).Name.lower(), "").replace('.pac', '').replace("fit", "").isnumeric():
								i += 1
					# Set up progressbar
					progressCounter = 0
					progressBar = ProgressWindow(MainForm.Instance, "Removing Rimlights...", "Removing Rimlights", False)
					progressBar.Begin(0, i, progressCounter)
					# Remove rimlights
					for directory in Directory.GetDirectories(MainForm.BuildPath + '/pf/fighter'):
						progressBar.Caption = "Removing rimlights from: " + DirectoryInfo(directory).Name
						for file in Directory.GetFiles(directory, "*.pac"):
							# Check that it's a costume
							if FileInfo(file).Name.lower().replace(DirectoryInfo(directory).Name.lower(), "").replace('.pac', '').replace("fit", "").isnumeric():
								removeRimlightFile(file, textureName)
								progressCounter += 1
								progressBar.Update(progressCounter)
					progressCounter += 1
					progressBar.Update(progressCounter)
					progressBar.Finish()
					BrawlAPI.ShowMessage("Process completed.", "Complete")

main()