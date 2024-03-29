[![forthebadge](https://forthebadge.com/images/badges/60-percent-of-the-time-works-every-time.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/contains-tasty-spaghetti-code.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/as-seen-on-tv.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/certified-snoop-lion.svg)](https://forthebadge.com)

# map_editor
A work in progress map editor for the videogame Ymir (https://store.steampowered.com/app/378360/Ymir/)

If you have any suggestions please let me know by making an issue or via the official Ymir discord (https://discord.com/invite/cwJD5Ds)

How to use:

1) Go to the releases page (https://github.com/devanderhoff/map_editor/releases/) and download the map_editor.exe, clone this repo and run ```python main.py``` or download the .rar file (a pip installable release is on the TODO list).

2) If using the exe, please run as administrator.

There are multiple ways to start editing a new/existing map, but the recommended approaches are to either edit a map already generated by Ymir, or use the built-in "load pre-build tiny world" button.

  To edit an Ymir generated world:
  1) Start Ymir, start a new game with the settings you desire and a mapsize of 'tiny'. Or another size but currently the map editor is unoptimized and memory heavy.
  2) Then navigate to ```%USERPROFILE%/appdata/ymir/saves/name_of_new_save/worldmap``` and copy ```world.ybin``` from this directory to the editor's root directory.
  3) Load this world inside the editor. 
  4) Edit the world, and save. Then replace the edited ```.ybin``` file with the ```world.ybin``` in the ymir save folder.
  
> :warning: Notes, please read!!: 

1)  **SAVE OFTEN!** The project is in an experimental stage, so it's not unlikely to crash at some point. I'll add auto-save soonish.Be very careful here!
2) There are currently almost no mechanisms in place to validate maps. So for example, ingame rivers are never next to each other, but you can do this as much as you want with the current state of the editor. So; make sure things make sense.
3) Memory usage is about 1GB right now because of the sprite sizes, so keep that in mind.
