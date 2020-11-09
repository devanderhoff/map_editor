# map_editor
A work in progress map editor for the video-game Ymir (https://store.steampowered.com/app/378360/Ymir/)

If you have any suggestions please let me know through issues or official ymir discord (https://discord.com/invite/cwJD5Ds)

How to use
1) Go to the releases page (https://github.com/devanderhoff/map_editor/releases/tag/v0.2) and download the map_editor.exe or clone this repo and run main.py
2) If using the exe, please run as administrator.

There are multiple options to start a new edit, but most advicable is editing a map ymir generated, or use the buildin "load pre-build tiny world" button.
  To edit a ymir generated world:
  1) Start Ymir, start a new game with the settings you desire and a mapsize of tiny. Or another size but currently the map editor is unoptimized and memory heavy.
  2) Then navigate to c:/user/yourname/appdata/ymir/saves/name_of_new_save/worldmap and copy the "world.ybin" from this folder to the folder of the editor.
  3) Load this world inside the editor. 
  4) Edit world and save. Then replace the editted .ybin file with the world.ybin in the ymir save folder.
  
Notes, please read!!

1) SAVE OFTEN! First release so it will probably crash at some point. I'll add auto-save soonish.
2) There are currently almost no "checks" in place to check the legitimacy of the map. So for example, ingame rivers are never next to each other, but you can do 
  this as much as you want with the current state of the editor. So make sure things make sense. 
3) Memory usage is about 1GB right now because of the sprite sizes, so keep that in mind.
