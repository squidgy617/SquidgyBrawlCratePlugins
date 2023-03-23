__author__ = "Squidgy"

from SquidLib import *

def main():
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
			progressBar = ProgressWindow(MainForm.Instance, "Adding Rimlights...", "Adding Rimlights", False)
			progressBar.Begin(0, i, progressCounter)
			# Add rimlights
			for directory in Directory.GetDirectories(MainForm.BuildPath + '/pf/fighter'):
				progressBar.Caption = "Adding rimlights to: " + DirectoryInfo(directory).Name
				for file in Directory.GetFiles(directory, "*.pac"):
					# Check that it's a costume
					if FileInfo(file).Name.lower().replace(DirectoryInfo(directory).Name.lower(), "").replace('.pac', '').replace("fit", "").isnumeric():
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
											if 'eye' not in material.Name.lower() and 'ExtMtl' not in material.Name.lower():
												applyRimlight(material, skipMessages=True)
										BrawlAPI.SaveFile()
							BrawlAPI.ForceCloseFile()
							progressCounter += 1
							progressBar.Update(progressCounter)
			progressCounter += 1
			progressBar.Update(progressCounter)
			progressBar.Finish()
			BrawlAPI.ShowMessage("Process completed.", "Complete")

main()