__author__ = "Squidgy"

import clr
from SquidLib import *
from System.Windows.Forms import *
clr.AddReference("System.Drawing")
from System.Drawing import *
from System.ComponentModel import *

class TourObjectView(object):
	def __init__(self, obj):
		self._obj = obj

	@property
	def Name(self):
		return self._obj.Name

	@Name.setter
	def Name(self, value):
		self._obj.Name = value

	@property
	def ModelIndex(self):
		return self._obj.ModelIndex

	@ModelIndex.setter
	def ModelIndex(self, value):
		self._obj.ModelIndex = value

	@property
	def CollisionIndex(self):
		return self._obj.CollisionIndex

	@CollisionIndex.setter
	def CollisionIndex(self, value):
		self._obj.CollisionIndex = value

class TourStateView(object):
	def __init__(self, obj):
		self._obj = obj

	@property
	def Name(self):
		return self._obj.Name
	
	@Name.setter
	def Name(self, value):
		self._obj.Name = value

	@property
	def FrameCount(self):
		return self._obj.FrameCount
	
	@FrameCount.setter
	def FrameCount(self, value):
		self._obj.FrameCount = value

class TourManagerForm(Form):
	def __init__(self, tourObjects, tourStates):

		tourObjectView = []
		tourStateView = []
		# View setup
		for tourObject in tourObjects:
			tourObjectView.append(TourObjectView(tourObject))

		for tourState in tourStates:
			tourStateView.append(TourStateView(tourState))

		# Form settings
		self.Text = "Tour Manager"
		self.StartPosition = FormStartPosition.CenterParent
		self.ShowIcon = False

		self.Width = 800
		self.Height = 600
		self.MinimumSize = Size(500, 400)

		# Make window resizable
		self.FormBorderStyle = FormBorderStyle.Sizable

		# Main split container
		split = SplitContainer()
		split.Dock = DockStyle.Fill
		split.Orientation = Orientation.Vertical
		split.SplitterDistance = 250
		split.Panel1MinSize = 100
		split.Panel2MinSize = 100

		# Tour object split container
		tourObjectSplit = SplitContainer()
		tourObjectSplit.Dock = DockStyle.Fill
		tourObjectSplit.Orientation = Orientation.Vertical
		tourObjectSplit.SplitterDistance = 250
		tourObjectSplit.Panel1MinSize = 100
		tourObjectSplit.Panel2MinSize = 100

		# Tour state split container
		tourStateSplit = SplitContainer()
		tourStateSplit.Dock = DockStyle.Fill
		tourStateSplit.Orientation = Orientation.Vertical
		tourStateSplit.SplitterDistance = 250
		tourStateSplit.Panel1MinSize = 100
		tourStateSplit.Panel2MinSize = 100

		# State object split container
		stateObjectSplit = SplitContainer()
		stateObjectSplit.Dock = DockStyle.Fill
		stateObjectSplit.Orientation = Orientation.Vertical
		stateObjectSplit.SplitterDistance = 250
		stateObjectSplit.Panel1MinSize = 100
		stateObjectSplit.Panel2MinSize = 100

		# Destination split container
		destinationSplit = SplitContainer()
		destinationSplit.Dock = DockStyle.Fill
		destinationSplit.Orientation = Orientation.Vertical
		destinationSplit.SplitterDistance = 250
		destinationSplit.Panel1MinSize = 100
		destinationSplit.Panel2MinSize = 100

		# Layouts
		tourStateLayout = TableLayoutPanel()
		tourStateLayout.Dock = DockStyle.Fill
		tourStateLayout.RowCount = 3

		stateObjectLayout = TableLayoutPanel()
		stateObjectLayout.Dock = DockStyle.Fill
		stateObjectLayout.RowCount = 2

		destinationLayout = TableLayoutPanel()
		destinationLayout.Dock = DockStyle.Fill
		destinationLayout.RowCount = 2

		# Controls
		tourObjectListBox = ListBox()
		tourObjectListBox.Dock = DockStyle.Fill

		tourObjectPropertyGrid = PropertyGrid()
		tourObjectPropertyGrid.Dock = DockStyle.Fill
		tourObjectPropertyGrid.ToolbarVisible = False
		tourObjectPropertyGrid.HelpVisible = True
		tourObjectPropertyGrid.BrowsableAttributes = None

		tourStateListBox = ListBox()
		tourStateListBox.Dock = DockStyle.Fill
		
		tourStatePropertyGrid = PropertyGrid()
		tourStatePropertyGrid.Dock = DockStyle.Fill
		tourStatePropertyGrid.ToolbarVisible = False
		tourStatePropertyGrid.HelpVisible = True
		tourStatePropertyGrid.BrowsableAttributes = None
		
		stateObjectListBox = ListBox()
		stateObjectListBox.Dock = DockStyle.Fill

		stateObjectComboBox = ComboBox()

		stateObjectPropertyGrid = PropertyGrid()
		stateObjectPropertyGrid.Dock = DockStyle.Fill
		stateObjectPropertyGrid.ToolbarVisible = False
		stateObjectPropertyGrid.HelpVisible = True
		stateObjectPropertyGrid.BrowsableAttributes = None

		destinationListBox = ListBox()
		destinationListBox.Dock = DockStyle.Fill

		destinationComboBox = ComboBox()

		destinationPropertyGrid = PropertyGrid()
		destinationPropertyGrid.Dock = DockStyle.Fill
		destinationPropertyGrid.ToolbarVisible = False
		destinationPropertyGrid.HelpVisible = True
		destinationPropertyGrid.BrowsableAttributes = None

		# Tour object bindings
		tourObjectBindingSource = BindingSource()
		tourObjectBindingSource.DataSource = tourObjectView

		tourObjectListBox.DataSource = tourObjectBindingSource
		tourObjectListBox.DisplayMember = "Name"

		tourObjectPropertyGrid.SelectedObject = tourObjectBindingSource.Current

		def onCurrentTourObjectChanged(sender, e):
			tourObjectPropertyGrid.SelectedObject = tourObjectBindingSource.Current

		tourObjectBindingSource.CurrentChanged += onCurrentTourObjectChanged

		# Tour state bindings
		tourStateBindingSource = BindingSource()
		tourStateBindingSource.DataSource = tourStateView

		tourStateListBox.DataSource = tourStateBindingSource
		tourStateListBox.DisplayMember = "Name"

		tourStatePropertyGrid.SelectedObject = tourStateBindingSource.Current

		def onCurrentTourStateChanged(sender, e):
			tourStatePropertyGrid.SelectedObject = tourStateBindingSource.Current
			stateObjectBindingSource.DataSource = tourStateBindingSource.Current._obj.StateObjects
			destinationBindingSource.DataSource = tourStateBindingSource.Current._obj.Destinations

		tourStateBindingSource.CurrentChanged += onCurrentTourStateChanged

		# State object bindings
		stateObjectBindingSource = BindingSource()
		stateObjectBindingSource.DataSource = tourStateBindingSource.Current._obj.StateObjects

		stateObjectListBox.DataSource = stateObjectBindingSource
		stateObjectListBox.DisplayMember = "Name"

		stateObjectPropertyGrid.SelectedObject = stateObjectBindingSource.Current

		def onCurrentStateObjectChanged(sender, e):
			stateObjectPropertyGrid.SelectedObject = stateObjectBindingSource.Current

		stateObjectBindingSource.CurrentChanged += onCurrentStateObjectChanged

		stateObjectComboBox.DataSource = tourObjectBindingSource
		stateObjectComboBox.DisplayMember = "Name"

		stateObjectComboBox.SelectedItem = stateObjectBindingSource.Current.TourObject

		# Destination bindings
		destinationBindingSource = BindingSource()
		destinationBindingSource.DataSource = tourStateBindingSource.Current._obj.Destinations

		destinationListBox.DataSource = destinationBindingSource
		destinationListBox.DisplayMember = "Name"

		destinationPropertyGrid.SelectedObject = destinationBindingSource.Current

		def onCurrentDestinationChanged(sender, e):
			destinationPropertyGrid.SelectedObject = destinationBindingSource.Current

		destinationBindingSource.CurrentChanged += onCurrentDestinationChanged

		destinationComboBox.DataSource = tourStateBindingSource
		destinationComboBox.DisplayMember = "Name"

		destinationComboBox.SelectedItem = destinationBindingSource.Current.TourState

		# Add controls to split panels
		tourObjectSplit.Panel1.Controls.Add(tourObjectListBox)
		tourObjectSplit.Panel2.Controls.Add(tourObjectPropertyGrid)

		stateObjectLayout.Controls.Add(stateObjectComboBox, 0, 0)
		stateObjectLayout.Controls.Add(stateObjectPropertyGrid, 0, 1)

		stateObjectSplit.Panel1.Controls.Add(stateObjectListBox)
		stateObjectSplit.Panel2.Controls.Add(stateObjectLayout)

		destinationLayout.Controls.Add(destinationComboBox, 0, 0)
		destinationLayout.Controls.Add(destinationPropertyGrid, 0, 1)

		destinationSplit.Panel1.Controls.Add(destinationListBox)
		destinationSplit.Panel2.Controls.Add(destinationLayout)

		tourStateSplit.Panel2.Controls.Add(tourStatePropertyGrid)

		tourStateLayout.Controls.Add(tourStatePropertyGrid, 0, 0)
		tourStateLayout.Controls.Add(stateObjectSplit, 0, 1)
		tourStateLayout.Controls.Add(destinationSplit, 0, 2)

		tourStateSplit.Panel1.Controls.Add(tourStateListBox)
		tourStateSplit.Panel2.Controls.Add(tourStateLayout)

		split.Panel1.Controls.Add(tourObjectSplit)
		split.Panel2.Controls.Add(tourStateSplit)

		# Add to form
		self.Controls.Add(split)


class TourObject(object):
	def __init__(self, name, modelIndex, collisionIndex):
		self._name = name
		self._modelIndex = modelIndex
		self._collisionIndex = collisionIndex

	@property
	def Name(self):
		return self._name

	@Name.setter
	def Name(self, value):
		self._name = value

	@property
	def ModelIndex(self):
		return self._modelIndex

	@ModelIndex.setter
	def ModelIndex(self, value):
		self._modelIndex = value

	@property
	def CollisionIndex(self):
		return self._collisionIndex

	@CollisionIndex.setter
	def CollisionIndex(self, value):
		self._collisionIndex = value

class StateObject(object):
	def __init__(self, name, tourObject, animationIndex):
		self._name = name
		self._tourObject = tourObject
		self._animationindex = animationIndex
	
	@property
	def Name(self):
		return self._name
	
	@Name.setter
	def Name(self, value):
		self._name = value

	@property
	def TourObject(self):
		return self._tourObject
	
	@TourObject.setter
	def TourObject(self, value):
		self._tourObject = value

	@property
	def AnimationIndex(self):
		return self._animationindex
	
	@AnimationIndex.setter
	def AnimationIndex(self, value):
		self._animationindex = value

class Destination(object):
	def __init__(self, name, tourState, tourStateIndex):
		self._name = name
		self._tourState = tourState
		self._tourStateIndex = tourStateIndex

	@property
	def Name(self):
		return self._name
	
	@Name.setter
	def Name(self, value):
		self._name = value

	@property
	def TourState(self):
		return self._tourState
	
	@TourState.setter
	def TourState(self, value):
		self._tourState = value

	@property 
	def TourStateIndex(self):
		return self._tourStateIndex
	
	@TourStateIndex.setter
	def TourStateIndex(self, value):
		self._tourStateIndex = value

class TourState(object):
	def __init__(self, name, frameCount, stateObjects, destinations):
		self._name = name
		self._frameCount = frameCount
		self._stateObjects = stateObjects
		self._destinations = destinations

	@property
	def Name(self):
		return self._name
	
	@Name.setter
	def Name(self, value):
		self._name = value

	@property
	def FrameCount(self):
		return self._frameCount
	
	@FrameCount.setter
	def FrameCount(self, value):
		self._frameCount = value

	@property
	def StateObjects(self):
		return self._stateObjects
	
	@StateObjects.setter
	def StateObjects(self, value):
		self._stateObjects = value

	@property
	def Destinations(self):
		return self._destinations
	
	@Destinations.setter
	def Destinations(self, value):
		self._destinations = value

def main():
	tourObjectList = []
	tourStateList = []
	if BrawlAPI.RootNode:
		modelData = BrawlAPI.RootNode.FindChild("2/Model Data [0]")
		if modelData:
			modelFolder = modelData.GetFolder[MDL0Node]()
			if modelFolder:
				model = modelFolder.Children[0]
				if model:
					# Find tour stuff
					for bone in model.AllBones:
						if bone.Name == "TourObjects":
							# Add all tour objects to list
							for tourObjectBone in bone.Children:
								tourObjectList.append(TourObject(tourObjectBone.Name, tourObjectBone.Rotation._x, tourObjectBone.Rotation._y))
						if bone.Name == "TourStates":
							# Iterate through the tour states
							for tourStateBone in bone.Children:
								stateObjects = []
								# Each state has state objects, get those
								stateObjectsBone = getChildByPrefix(tourStateBone, "StateObjects")
								if stateObjectsBone:
									for stateObjectBone in stateObjectsBone.Children:
										if not stateObjectBone.Name.StartsWith("StateObjectsEnd"):
											tourObjectIndex = int(stateObjectBone.Rotation._x)
											stateObject = StateObject(stateObjectBone.Name, tourObjectList[tourObjectIndex], stateObjectBone.Rotation._y)
											stateObjects.append(stateObject)
								destinations = []
								# Each state has destinations, get those
								destinationsBone = getChildByPrefix(tourStateBone, "Destinations")
								if destinationsBone:
									for destinationBone in destinationsBone.Children:
										if not destinationBone.Name.StartsWith("DestinationsEnd"):
											destination = Destination(destinationBone.Name, None, int(destinationBone.Rotation._x))
											destinations.append(destination)
								# Finally, create the tour state
								tourState = TourState(tourStateBone.Name, tourStateBone.Rotation._x, stateObjects, destinations)
								tourStateList.append(tourState)
		# Iterate through tour states and populate their destinations
		for tourState in tourStateList:
			for destination in tourState.Destinations:
				destination.tourState = tourStateList[destination.TourStateIndex]
		# Test code
		# test = ""
		# for tourState in tourStateList:
		# 	test += tourState.StateObjects[0].Name + "\n"
		# BrawlAPI.ShowMessage(test, "Title")
		# Populate form
		form = TourManagerForm(tourObjectList, tourStateList)
		result = form.ShowDialog(MainForm.Instance)
		form.Dispose()

main()