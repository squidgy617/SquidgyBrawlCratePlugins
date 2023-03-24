# BrawlCrate Plugins by Squidgy
Miscellaneous plugins for BrawlCrate for general quality of life use.

# Installation
1. If you do not already have BrawlCrate, download and install the [latest release](https://github.com/soopercool101/BrawlCrate/releases/latest).
2. Download the latest version of [Python](https://www.python.org/).
3. In BrawlCrate, navigate to `Tools > Settings > BrawlAPI` and ensure the `Installation Path` field under `Python` is set to the correct path.
4. In BrawlCrate, navigate to `Tools > Settings > Updater`, click `Manage Subscriptions`, and paste this link: `https://github.com/squidgy617/SquidgyBrawlCratePlugins`. If you set this up in BrawlCrate, the plugins will update automatically when you launch BrawlCrate.
5. Restart BrawlCrate.

# Plugins

## Add Rimlight
**Usage**: Right-Click any material > Plugins > Add Rimlight **OR** Add Rimlight (Choose)

Adds a rimlight to the selected material and to all materials that share the selected material's shader. If using the standard version of this plugin, the rimlight texture is the first image found in `Resources/SquidgyBrawlCratePlugins/Rimlight Texture` in your BrawlCrate directory. This image can be replaced if you prefer to use something else. If using the "Choose" variant, you will be prompted to select a rimlight texture from your computer. The plugin will not add a rimlight if that exact rimlight already exists for the chosen material and shader.

## Remove Rimlight
**Usage**: Right-Click any TEX0 (texture) node > Remove Rimlight

Removes any rimlights using the selected texture from all materials.

## Add Rimlight (Single Costume)
**Usage**: Plugins > Rimlights > Add Rimlight (Single Costume)

Prompts user to select a single costume `.pac` file. The plugin then attempts to add a rimlight the same way as the `Add Rimlight` plugin, but to all materials on that costume except for metal and eye materials (which it attempts to identify by name). Changes will be saved and a success message will appear on completion.

## Remove Rimlight (Single Costume)
**Usage**: Plugins > Rimlights > Remove Rimlight (Single Costume)

Prompts the user to select a single costume `.pac` file and to enter a name for the rimlight. The plugin then attempts to remove any rimlights associated with a texture using the name entered by the user from all materials.

## Add Rimlight (All Costumes)
**Usage**: Plugins > Rimlights > Add Rimlight (All Costumes)

Attempts to add rimlights in the same manner as `Add Rimlight (Single Costume)`, but to every costume in the build set in BrawlCrate's default build path. **NOTE**: This plugin can take a long time to run and could have unexpected results, so use at your own risk, and always back up your build first!

## Remove Rimlight (All Costumes)
**Usage**: Plugins > Rimlights > Remove Rimlight (All Costumes)

Attempts to remove rimlights in the same manner as `Remove Rimlight (Single Costume)`, but from every costume in the build set in BrawlCrate's default build path. **NOTE**: This plugin can take a long time to run and could have unexpected results, so use at your own risk, and always back up your build first!

# Credits
- Soopercool101, Kryal, BlackJax96, and libertyernie for BrawlLib, BrawlBox, and BrawlCrate.
- markymawk, for their basic guide to writing plug-ins and for their plug-ins which served as a great learning resource.
- Xenthos, for providing guidance on the procedure for creating rimlights.
