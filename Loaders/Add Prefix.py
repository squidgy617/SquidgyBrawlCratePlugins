__author__ = "Squidgy"

# Automatically add a prefix to selected nodes

from SquidLib import *

def addPrefix(sender, event_args):
	prefix = BrawlAPI.UserStringInput("Enter prefix")
	addPrefixNodes(BrawlAPI.SelectedNodes, prefix)

def removePrefix(sender, event_args):
	prefix = BrawlAPI.UserStringInput("Enter prefix")
	removePrefixNodes(BrawlAPI.SelectedNodes, prefix)
			
def addPrefixNodes(nodes, prefix):
	for node in nodes:
		node.Name = prefix + node.Name
		if len(node.Children) > 0:
			addPrefixNodes(node.Children, prefix)

def removePrefixNodes(nodes, prefix):
	for node in nodes:
		if node.Name.startswith(prefix):
			node.Name = node.Name.replace(prefix, "", 1)
			if len(node.Children) > 0:
				removePrefixNodes(node.Children, prefix)
	
def addChildrenPrefix(sender, event_args):
	prefix = BrawlAPI.UserStringInput("Enter prefix")
	for node in BrawlAPI.SelectedNodes:
		for child in node.Children:
			child.Name = prefix + child.Name

def removeChildrenPrefix(sender, event_args):
	prefix = BrawlAPI.UserStringInput("Enter prefix")
	for node in BrawlAPI.SelectedNodes:
		for child in node.Children:
			if child.Name.startswith(prefix):
				child.Name = child.Name.replace(prefix, "", 1)

BrawlAPI.AddMultiSelectContextMenuItem(CHR0EntryWrapper, "", "Add a prefix to selected CHR0 entries", None, ToolStripMenuItem("Add prefix", None, addPrefix))
BrawlAPI.AddContextMenuItem(CHR0EntryWrapper, "", "Add a prefix to selected CHR0 entries", None, ToolStripMenuItem("Add prefix", None, addPrefix))
BrawlAPI.AddMultiSelectContextMenuItem(CHR0Wrapper, "", "Add a prefix to CHR0 entries in selected CHR0 nodes", None, ToolStripMenuItem("Add prefix to entries", None, addChildrenPrefix))
BrawlAPI.AddContextMenuItem(CHR0Wrapper, "", "Add a prefix to CHR0 entries in selected CHR0 nodes", None, ToolStripMenuItem("Add prefix to entries", None, addChildrenPrefix))
BrawlAPI.AddMultiSelectContextMenuItem(MDL0BoneWrapper, "", "Add a prefix to selected bones and their children", None, ToolStripMenuItem("Add prefix", None, addPrefix))
BrawlAPI.AddContextMenuItem(MDL0BoneWrapper, "", "Add a prefix to selected bones and their children", None, ToolStripMenuItem("Add prefix", None, addPrefix))

BrawlAPI.AddMultiSelectContextMenuItem(CHR0EntryWrapper, "", "Remove a prefix from selected CHR0 entries", None, ToolStripMenuItem("Remove prefix", None, removePrefix))
BrawlAPI.AddContextMenuItem(CHR0EntryWrapper, "", "Remove a prefix from selected CHR0 entries", None, ToolStripMenuItem("Remove prefix", None, removePrefix))
BrawlAPI.AddMultiSelectContextMenuItem(CHR0Wrapper, "", "Remove a prefix from CHR0 entries in selected CHR0 nodes", None, ToolStripMenuItem("Remove prefix from entries", None, removeChildrenPrefix))
BrawlAPI.AddContextMenuItem(CHR0Wrapper, "", "Remove a prefix from CHR0 entries in selected CHR0 nodes", None, ToolStripMenuItem("Remove prefix from entries", None, removeChildrenPrefix))
BrawlAPI.AddMultiSelectContextMenuItem(MDL0BoneWrapper, "", "Remove a prefix from selected bones and their children", None, ToolStripMenuItem("Remove prefix", None, removePrefix))
BrawlAPI.AddContextMenuItem(MDL0BoneWrapper, "", "Remove a prefix from selected bones and their children", None, ToolStripMenuItem("Remove prefix", None, removePrefix))