__author__ = "Squidgy"

import clr
from SquidLib import *
from System.Windows.Forms import *
clr.AddReference("System.Drawing")
from System.Drawing import *
from System.ComponentModel import *
from BrawlLib.SSBB.Types import *

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

class StateObjectView(object):
	def __init__(self, obj):
		self._obj = obj
	
	@property
	def Name(self):
		return self._obj.Name
	
	@Name.setter
	def Name(self, value):
		self._obj.Name = value

	@property
	def AnimationIndex(self):
		return self._obj.AnimationIndex
	
	@AnimationIndex.setter
	def AnimationIndex(self, value):
		self._obj.AnimationIndex = value

class DestinationView(object):
	def __init__(self, obj):
		self._obj = obj

	@property
	def Name(self):
		return self._obj.Name
	
	@Name.setter
	def Name(self, value):
		self._obj.Name = value

class ObjectPicker(Form):
	def __init__(self, objects, displayMember):
		self.Text = "Select Animation"
		self.Width = 420
		self.Height = 160
		self.MinimumSize = Size(350, 150)
		self.StartPosition = FormStartPosition.CenterParent
		self.FormBorderStyle = FormBorderStyle.FixedDialog
		self.MaximizeBox = False
		self.MinimizeBox = False
		self.Padding = Padding(12)

		# Main layout
		panel = TableLayoutPanel()
		panel.Dock = DockStyle.Fill
		panel.ColumnCount = 1
		panel.RowCount = 3
		panel.RowStyles.Add(RowStyle(SizeType.Absolute, 24))
		panel.RowStyles.Add(RowStyle(SizeType.Absolute, 32))
		panel.RowStyles.Add(RowStyle(SizeType.Percent, 100))

		# Label
		label = Label()
		label.Text = "Animation"
		label.Dock = DockStyle.Fill
		label.TextAlign = ContentAlignment.BottomLeft
		label.AutoSize = True

		# ComboBox
		self.comboBox = ComboBox()
		self.comboBox.Dock = DockStyle.Fill
		self.comboBox.DropDownStyle = ComboBoxStyle.DropDownList

		comboBoxBindingSource = BindingSource()
		comboBoxBindingSource.DataSource = objects

		self.comboBox.DataSource = comboBoxBindingSource
		self.comboBox.DisplayMember = displayMember
		self.comboBox.ValueMember = "self"

		# Button panel (right aligned)
		buttonPanel = FlowLayoutPanel()
		buttonPanel.Dock = DockStyle.Fill
		buttonPanel.FlowDirection = FlowDirection.RightToLeft
		buttonPanel.Padding = Padding(0, 10, 0, 0)

		button = Button()
		button.Text = "OK"
		button.Width = 90
		button.Height = 28

		def onSelect(sender, e):
			self.DialogResult = DialogResult.OK
			self.Close()

		button.Click += onSelect

		buttonPanel.Controls.Add(button)

		# Add controls
		panel.Controls.Add(label, 0, 0)
		panel.Controls.Add(self.comboBox, 0, 1)
		panel.Controls.Add(buttonPanel, 0, 2)

		self.Controls.Add(panel)

		# Enter key activates button
		self.AcceptButton = button

class TourManagerForm(Form):
	def __init__(self, tourObjects, tourStates):
		# Properties
		self.TourObjects = tourObjects
		self.TourStates = tourStates
		
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
		mainLayout = TableLayoutPanel()
		mainLayout.Dock = DockStyle.Fill
		mainLayout.RowCount = 2
		mainLayout.RowStyles.Add(RowStyle(SizeType.Percent, 90))
		mainLayout.RowStyles.Add(RowStyle(SizeType.Absolute, 32))

		tourStateLayout = TableLayoutPanel()
		tourStateLayout.Dock = DockStyle.Fill
		tourStateLayout.RowCount = 3
		for i in range(3):
			tourStateLayout.RowStyles.Add(
				RowStyle(SizeType.Percent, 33.33)
			)

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
		stateObjectComboBox.DropDownStyle = ComboBoxStyle.DropDownList

		stateObjectButton = Button()
		stateObjectButton.Text = "Auto-Name"

		stateObjectFindButton = Button()
		stateObjectFindButton.Text = "Select Anim"

		stateObjectPropertyGrid = PropertyGrid()
		stateObjectPropertyGrid.Dock = DockStyle.Fill
		stateObjectPropertyGrid.ToolbarVisible = False
		stateObjectPropertyGrid.HelpVisible = True
		stateObjectPropertyGrid.BrowsableAttributes = None

		destinationListBox = ListBox()
		destinationListBox.Dock = DockStyle.Fill

		destinationButton = Button()
		destinationButton.Text = "Auto-Name"

		destinationComboBox = ComboBox()
		destinationComboBox.DropDownStyle = ComboBoxStyle.DropDownList

		destinationPropertyGrid = PropertyGrid()
		destinationPropertyGrid.Dock = DockStyle.Fill
		destinationPropertyGrid.ToolbarVisible = False
		destinationPropertyGrid.HelpVisible = True
		destinationPropertyGrid.BrowsableAttributes = None

		applyButton = Button()
		applyButton.Text = "Apply"
		applyButton.Dock = DockStyle.Right

		# Labels
		tourObjectLabel = Label()
		tourObjectLabel.Text = "Tour Objects"
		tourObjectLabel.AutoSize = True

		tourStateLabel = Label()
		tourStateLabel.Text = "Tour States"
		tourStateLabel.AutoSize = True

		stateObjectLabel = Label()
		stateObjectLabel.Text = "State Objects"
		stateObjectLabel.AutoSize = True

		stateObjectComboLabel = Label()
		stateObjectComboLabel.Text = "Tour Object"
		stateObjectComboLabel.AutoSize = True

		destinationLabel = Label()
		destinationLabel.Text = "Destinations"
		destinationLabel.AutoSize = True

		destinationComboLabel = Label()
		destinationComboLabel.Text = "Destination State"
		destinationComboLabel.AutoSize = True


		# +/- buttons
		tourObjectAdd = Button()
		tourObjectAdd.Text = "+"
		tourObjectAdd.Width = 30

		tourObjectRemove = Button()
		tourObjectRemove.Text = "-"
		tourObjectRemove.Width = 30

		tourStateAdd = Button()
		tourStateAdd.Text = "+"
		tourStateAdd.Width = 30

		tourStateRemove = Button()
		tourStateRemove.Text = "-"
		tourStateRemove.Width = 30

		stateObjectAdd = Button()
		stateObjectAdd.Text = "+"
		stateObjectAdd.Width = 30

		stateObjectRemove = Button()
		stateObjectRemove.Text = "-"
		stateObjectRemove.Width = 30

		destinationAdd = Button()
		destinationAdd.Text = "+"
		destinationAdd.Width = 30

		destinationRemove = Button()
		destinationRemove.Text = "-"
		destinationRemove.Width = 30


		# Header helper
		def createHeader(label, addButton, removeButton):
			panel = TableLayoutPanel()
			panel.Dock = DockStyle.Top
			panel.Height = 30
			panel.ColumnCount = 3

			panel.ColumnStyles.Add(
				ColumnStyle(SizeType.Percent,100)
			)

			panel.ColumnStyles.Add(
				ColumnStyle(SizeType.Absolute,35)
			)

			panel.ColumnStyles.Add(
				ColumnStyle(SizeType.Absolute,35)
			)

			panel.Controls.Add(label,0,0)
			panel.Controls.Add(addButton,1,0)
			panel.Controls.Add(removeButton,2,0)

			return panel


		# List container helper
		def createListContainer(header,listbox):

			panel = Panel()
			panel.Dock = DockStyle.Fill

			listbox.Dock = DockStyle.Fill

			panel.Controls.Add(listbox)
			panel.Controls.Add(header)

			return panel


		# Combo container helper
		def createComboContainer(label,combo,buttons):

			panel=TableLayoutPanel()

			panel.Dock=DockStyle.Fill
			panel.RowCount=2 + len(buttons)

			panel.RowStyles.Add(
				RowStyle(SizeType.Absolute,20)
			)

			panel.RowStyles.Add(
				RowStyle(SizeType.Percent,100)
			)

			for i in range(len(buttons)):
				panel.RowStyles.Add(
					RowStyle(SizeType.Percent,100)
				)

			combo.Dock=DockStyle.Fill

			panel.Controls.Add(label,0,0)
			panel.Controls.Add(combo,0,1)
			
			for i in range(len(buttons)):
				panel.Controls.Add(buttons[i],i,2)

			return panel

		tourObjectHeader = createHeader(
			tourObjectLabel,
			tourObjectAdd,
			tourObjectRemove
		)

		tourStateHeader = createHeader(
			tourStateLabel,
			tourStateAdd,
			tourStateRemove
		)

		stateObjectHeader = createHeader(
			stateObjectLabel,
			stateObjectAdd,
			stateObjectRemove
		)

		destinationHeader = createHeader(
			destinationLabel,
			destinationAdd,
			destinationRemove
		)

		tourObjectPanel = createListContainer(
			tourObjectHeader,
			tourObjectListBox
		)

		tourStatePanel = createListContainer(
			tourStateHeader,
			tourStateListBox
		)

		stateObjectPanel = createListContainer(
			stateObjectHeader,
			stateObjectListBox
		)

		destinationPanel = createListContainer(
			destinationHeader,
			destinationListBox
		)

		stateObjectComboPanel = createComboContainer(
			stateObjectComboLabel,
			stateObjectComboBox,
			[stateObjectButton, stateObjectFindButton]
		)

		destinationComboPanel = createComboContainer(
			destinationComboLabel,
			destinationComboBox,
			[destinationButton]
		)

		# Tour object bindings
		tourObjectBindingSource = BindingSource()
		tourObjectBindingSource.DataSource = self.TourObjects

		tourObjectListBox.DataSource = tourObjectBindingSource
		tourObjectListBox.DisplayMember = "Name"

		tourObjectPropertyGrid.SelectedObject = TourObjectView(tourObjectBindingSource.Current)

		def onCurrentTourObjectChanged(sender, e):
			tourObjectPropertyGrid.SelectedObject = TourObjectView(tourObjectBindingSource.Current)

		tourObjectBindingSource.CurrentChanged += onCurrentTourObjectChanged

		# Tour state bindings
		tourStateBindingSource = BindingSource()
		tourStateBindingSource.DataSource = self.TourStates

		tourStateListBox.DataSource = tourStateBindingSource
		tourStateListBox.DisplayMember = "Name"

		tourStatePropertyGrid.SelectedObject = TourStateView(tourStateBindingSource.Current)

		def onCurrentTourStateChanged(sender, e):
			try:
				tourStatePropertyGrid.SelectedObject = TourStateView(tourStateBindingSource.Current)
				stateObjectBindingSource.DataSource = tourStateBindingSource.Current.StateObjects
				stateObjectBindingSource.ResetBindings(False)
				destinationBindingSource.DataSource = tourStateBindingSource.Current.Destinations
				destinationBindingSource.ResetBindings(False)
			except Exception as e:
				BrawlAPI.ShowMessage(str(e), "An Error Has Occurred")

		tourStateBindingSource.CurrentChanged += onCurrentTourStateChanged

		# State object bindings
		stateObjectBindingSource = BindingSource()
		stateObjectBindingSource.DataSource = tourStateBindingSource.Current.StateObjects

		stateObjectListBox.DataSource = stateObjectBindingSource
		stateObjectListBox.DisplayMember = "Name"

		stateObjectPropertyGrid.SelectedObject = StateObjectView(stateObjectBindingSource.Current)

		def onCurrentStateObjectChanged(sender, e):
			stateObjectPropertyGrid.SelectedObject = StateObjectView(stateObjectBindingSource.Current)

		stateObjectBindingSource.CurrentChanged += onCurrentStateObjectChanged

		stateObjectTourObjectBindingSource = BindingSource()
		stateObjectTourObjectBindingSource.DataSource = self.TourObjects
		stateObjectComboBox.DataSource = stateObjectTourObjectBindingSource
		stateObjectComboBox.DisplayMember = "Name"
		stateObjectComboBox.ValueMember = "self"
		stateObjectComboBox.DataBindings.Add("SelectedItem", stateObjectBindingSource, "TourObject", True, DataSourceUpdateMode.OnPropertyChanged)

		# Destination bindings
		destinationBindingSource = BindingSource()
		destinationBindingSource.DataSource = tourStateBindingSource.Current.Destinations

		destinationListBox.DataSource = destinationBindingSource
		destinationListBox.DisplayMember = "Name"

		destinationPropertyGrid.SelectedObject = DestinationView(destinationBindingSource.Current)

		def onCurrentDestinationChanged(sender, e):
			destinationPropertyGrid.SelectedObject = DestinationView(destinationBindingSource.Current)

		destinationBindingSource.CurrentChanged += onCurrentDestinationChanged

		destinationStateBindingSource = BindingSource()
		destinationStateBindingSource.DataSource = self.TourStates
		destinationComboBox.DataSource = destinationStateBindingSource
		destinationComboBox.DisplayMember = "Name"
		destinationComboBox.ValueMember = "self"
		destinationComboBox.DataBindings.Add("SelectedItem", destinationBindingSource, "TourState", True, DataSourceUpdateMode.OnPropertyChanged)

		# Click events
		def onTourObjectAdd(sender, e):
			tourObject = TourObject("NewObject", 0, 0)
			self.TourObjects.append(tourObject)
			tourObjectBindingSource.ResetBindings(False)
			stateObjectTourObjectBindingSource.ResetBindings(False)

		def onTourObjectRemove(sender, e):
			self.TourObjects.remove(tourObjectBindingSource.Current)
			tourObjectBindingSource.ResetBindings(False)
			stateObjectTourObjectBindingSource.ResetBindings(False)

		tourObjectAdd.Click += onTourObjectAdd
		tourObjectRemove.Click += onTourObjectRemove

		def onTourStateAdd(sender, e):
			stateObject = StateObject("NewStateObject", self.TourObjects[0], 0)
			stateObjects = []
			stateObjects.append(stateObject)
			destination = Destination("NewDestination", self.TourStates[0], 0)
			destinations = []
			destinations.append(destination)
			tourState = TourState("NewState", 100, stateObjects, destinations)
			tourStates.append(tourState)
			tourStateBindingSource.ResetBindings(False) 
			destinationStateBindingSource.ResetBindings(False)

		def onTourStateRemove(sender, e):
			tourStates.remove(tourStateBindingSource.Current)
			tourStateBindingSource.ResetBindings(False)
			destinationStateBindingSource.ResetBindings(False)

		tourStateAdd.Click += onTourStateAdd
		tourStateRemove.Click += onTourStateRemove

		def onStateObjectAdd(sender, e):
			stateObject = StateObject("NewStateObject", self.TourObjects[0], 0)
			tourStateBindingSource.Current.StateObjects.append(stateObject)
			stateObjectBindingSource.ResetBindings(False)

		def onStateObjectRemove(sender, e):
			tourStateBindingSource.Current.StateObjects.remove(stateObjectBindingSource.Current)
			stateObjectBindingSource.ResetBindings(False)

		stateObjectAdd.Click += onStateObjectAdd
		stateObjectRemove.Click += onStateObjectRemove

		def onStateObjectFind(sender, e):
			modelData = stateObjectBindingSource.Current.TourObject.ModelData
			if modelData:
				anmChr = modelData.FindChild("AnmChr(NW4R)")
				if anmChr:
					objectSelector = ObjectPicker(anmChr.Children, "Name")
					result = objectSelector.ShowDialog(MainForm.Instance)
					if result == DialogResult.OK and objectSelector.comboBox.SelectedItem:
						stateObjectBindingSource.Current.AnimationIndex = objectSelector.comboBox.SelectedItem.Index
						stateObjectBindingSource.ResetBindings(False)

		stateObjectFindButton.Click += onStateObjectFind

		def onDestinationAdd(sender, e):
			newDestination = Destination("NewDestination", self.TourStates[0], 0)
			tourStateBindingSource.Current.Destinations.append(newDestination)
			destinationBindingSource.ResetBindings(False)

		def onDestinationRemove(sender, e):
			tourStateBindingSource.Current.Destinations.remove(destinationBindingSource.Current)
			destinationBindingSource.ResetBindings(False)

		destinationAdd.Click += onDestinationAdd
		destinationRemove.Click += onDestinationRemove

		def onApply(sender, e):
			self.DialogResult = DialogResult.OK
			self.Close()

		applyButton.Click += onApply

		def onStateObjectAutoName(sender, e):
			stateObjectBindingSource.Current.Name = f"{tourStateBindingSource.Current.Name}StateObject{stateObjectBindingSource.Current.TourObject.Name}"
			stateObjectBindingSource.ResetBindings(False)

		stateObjectButton.Click += onStateObjectAutoName

		def onDestinationAutoName(sender, e):
			destinationBindingSource.Current.Name = f"{tourStateBindingSource.Current.Name}Dest{destinationBindingSource.Current.TourState.Name}"
			destinationBindingSource.ResetBindings(False)

		destinationButton.Click += onDestinationAutoName

		# Add controls to split panels
		tourObjectSplit.Panel1.Controls.Add(tourObjectPanel)
		tourObjectSplit.Panel2.Controls.Add(tourObjectPropertyGrid)

		stateObjectLayout.Controls.Add(stateObjectComboPanel, 0, 0)
		stateObjectLayout.Controls.Add(stateObjectPropertyGrid, 0, 1)

		stateObjectSplit.Panel1.Controls.Add(stateObjectPanel)
		stateObjectSplit.Panel2.Controls.Add(stateObjectLayout)

		destinationLayout.Controls.Add(destinationComboPanel, 0, 0)
		destinationLayout.Controls.Add(destinationPropertyGrid, 0, 1)

		destinationSplit.Panel1.Controls.Add(destinationPanel)
		destinationSplit.Panel2.Controls.Add(destinationLayout)

		tourStateSplit.Panel2.Controls.Add(tourStatePropertyGrid)

		tourStateLayout.Controls.Add(tourStatePropertyGrid, 0, 0)
		tourStateLayout.Controls.Add(stateObjectSplit, 0, 1)
		tourStateLayout.Controls.Add(destinationSplit, 0, 2)

		tourStateSplit.Panel1.Controls.Add(tourStatePanel)
		tourStateSplit.Panel2.Controls.Add(tourStateLayout)

		split.Panel1.Controls.Add(tourObjectSplit)
		split.Panel2.Controls.Add(tourStateSplit)

		# Add to form
		mainLayout.Controls.Add(split, 0, 0)
		mainLayout.Controls.Add(applyButton, 0, 1)

		self.Controls.Add(mainLayout)


class TourObject(object):
	def __init__(self, name, modelIndex, collisionIndex, modelData):
		self._name = name
		self._modelIndex = modelIndex
		self._collisionIndex = collisionIndex
		self._modelData = modelData

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

	@property
	def ModelData(self):
		return self._modelData
	
	@ModelData.setter
	def ModelData(self, value):
		self._modelData = value

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
					model.Populate()
					# Find tour stuff
					for bone in model.AllBones:
						if bone.Name == "TourObjects":
							# Add all tour objects to list
							for tourObjectBone in bone.Children:
								newModelData = None
								archive = BrawlAPI.RootNode.FindChild("2")
								for child in archive.Children:
									if child.NodeType == "BrawlLib.SSBB.ResourceNodes.BRRESNode" and child.FileType == ARCFileType.ModelData and child.FileIndex == int(tourObjectBone.Rotation._x):
										newModelData = child
								tourObjectList.append(TourObject(tourObjectBone.Name, tourObjectBone.Rotation._x, tourObjectBone.Rotation._y, newModelData))
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
				destination.TourState = tourStateList[destination.TourStateIndex]
		# Test code
		# test = ""
		# for tourState in tourStateList:
		# 	test += tourState.StateObjects[0].Name + "\n"
		# BrawlAPI.ShowMessage(test, "Title")
		# Populate form
		form = TourManagerForm(tourObjectList, tourStateList)
		result = form.ShowDialog(MainForm.Instance)
		# Apply changes
		if result == DialogResult.OK:
			# Replace tour objects
			modelFolder = modelData.GetFolder[MDL0Node]()
			if modelFolder:
				model = modelFolder.Children[0]
				if model:
					model.Populate()
					# Find tour stuff
					for bone in model.AllBones:
						if bone.Name == "TourObjects":
							# Generate tour object bones
							tourObjectRoot = MDL0BoneNode()
							tourObjectRoot.Name = "TourObjects"
							# Replace tour object bone
							bone.Children.Clear()
							bone.Replace(tourObjectRoot)
							for tourObject in form.TourObjects:
								tourObjectBone = MDL0BoneNode()
								tourObjectBone.Name = tourObject.Name
								tourObjectBone.Rotation = Vector3(tourObject.ModelIndex, tourObject.CollisionIndex, 0)
								bone.AddChild(tourObjectBone)
						if bone.Name == "TourStates":
							# Generate tour state bones
							tourStateRoot = MDL0BoneNode()
							tourStateRoot.Name = "TourStates"
							# Replace tour state bone
							bone.Children.Clear()
							bone.Replace(tourStateRoot)
							for tourState in form.TourStates:
								tourStateBone = MDL0BoneNode()
								tourStateBone.Name = tourState.Name
								tourStateBone.Rotation = Vector3(tourState.FrameCount, 0, 0)
								bone.AddChild(tourStateBone)
								# Add state objects
								stateObjectBoneRoot = MDL0BoneNode()
								stateObjectBoneRoot.Name = f"StateObjects{tourState.Name}"
								tourStateBone.AddChild(stateObjectBoneRoot)
								for stateObject in tourState.StateObjects:
									stateObjectBone = MDL0BoneNode()
									stateObjectBone.Name = stateObject.Name
									tourObjectIndex = form.TourObjects.index(stateObject.TourObject)
									stateObjectBone.Rotation = Vector3(tourObjectIndex, stateObject.AnimationIndex, 0)
									stateObjectBoneRoot.AddChild(stateObjectBone)
								stateObjectEndBone = MDL0BoneNode()
								stateObjectEndBone.Name = f"StateObjectsEnd{tourState.Name}"
								stateObjectBoneRoot.AddChild(stateObjectEndBone)
								# Add destinations
								destinationBoneRoot = MDL0BoneNode()
								destinationBoneRoot.Name = f"Destinations{tourState.Name}"
								tourStateBone.AddChild(destinationBoneRoot)
								for destination in tourState.Destinations:
									destinationBone = MDL0BoneNode()
									destinationBone.Name = destination.Name
									tourStateIndex = form.TourStates.index(destination.TourState)
									destinationBone.Rotation = Vector3(tourStateIndex, 0, 0)
									destinationBoneRoot.AddChild(destinationBone)
								destinationEndBone = MDL0BoneNode()
								destinationEndBone.Name = f"DestinationsEnd{tourState.Name}"
								destinationBoneRoot.AddChild(destinationEndBone)
						# Regenerate bone array
						rootBone = model.AllBones[0]
						BaseWrapper.Wrap(rootBone).Regen()
		form.Dispose()

main()