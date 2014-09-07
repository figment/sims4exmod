Sims 4 Scripting Example
==========

The purpose of this example to to show some basic but useful techniques for modding
  scripts in The Sims 4 which may speed up modding activities.

  
## WARNINGS
  The techniques used here may cause instability in your current game so I only 
  recommend using them while developing a new mod.
  
  Please do not ship a mod that uses the sys.stdout or sys.stderr redirect
  unless this is some super mod that is handling many other core functions
  and even then make it optional somehow.
  
  It would be better to just open a file and write to it but its illustrative 
  as an example so I've shown it.

  
## Included
  README.txt - This file
  ex - Example Mod Folder (this goes in )
  winmm.dll - Special helper file to work around scripts not loading
  scripts.ini - Config file for the winmm.dll hack

  
## Walkthrough
  * First, we need to put winmm.dll in the proper place this is where ever the game is 
    installed specifically the file 'TS4.exe'.  Unfortuately I dont know where yours 
    is so you will have to find it.
    
    It is probably 'C:\Program Files (x86)\Origin\Games\The Sims 4\Game\Bin' 
    
    This file is a special helper file to workaround scripts not loading.  It will
    probably not be required after the first Sims patch.  
	
	Source code will not be provided for this because its a hack.
    
  * Next, copy scripts.ini to 'Documents\Electronic Arts\The Sims 4\Mods' 
    This is a helper file for winmm.dll holding information required to 
    
  * This file does some code modification to load any scripts in the mods folder.  
    Basically it searches for the pattern "ex\ex.zip" and calls 'import ex'
    
  * Unpack ex folder to 'Documents\Electronic Arts\The Sims 4\Mods' so that it 
    somewhat like the following:
    
    + Documents
      + Electronic Arts
        + The Sims 4
          + Mods
            + ex
              - ex.zip
              + source
                - \_\_init\_\_.py
                - debug.py
                - hooks.py
                + subfolder
                  - \_\_init\_\_.py
                  - commands.py
                
    ### ex.zip
	  This has 3 files, ex.py, reloader.py, monitor.py.
	
	  The majority of the ex file is the code to load and reload the contents
	  of the source directory.  It effectively locates ex/source/__init__.py
	  and loads it.
	  
	  ex has has one command added which is the reload command.
	  	  
	  
	### ex/source/\_\_init\_\_.py
	  This is the package loader file.  It bootstraps the process and 
	  imports the hooks and subfolder packages.  If you dont do this then 
	  nothing will happen since the code is unreferenced.
	  
	  Note that I use 'ex.source' as the root of the ex/source folder.  This is 
	  because 'ex' is reserved for the ex.zip file and its contents.  Anything
	  that is prefixed with ex.source will be searched for in the source folder
	  everything else prefixed with ex will searched for in the ex.zip file.
	  
	  
	### ex/source/hooks.py
	  This file has some monkey patching examples.  Monkey patching is a basic
	  techinique for extending the current environment dynamically and replacing
	  existing functions with altered versions which do something interesting.
	  
	  In this case, I've replaced sys.stdout and sys.stderr which are the basic
	  output pipes with a file in the ex folder.  Any print statements will be
	  written to these files so that they can be read.
	  
	  It also overrides some log functions in the sims4 library so that we can
	  see the logs. At the moment we have no other way of seeing logs.


    ### ex/source/debug.py
      This shows how to connect a debugger.  In this case, I'm connecting to
      PyCharm Professional / IntelliJ IDEA Professional on my machine. 
      
      To get this to work copy the pycharm-debug-py3k.egg from PyCharm
      Professional install to the Mods folder and rename .egg to .zip.  Then
      start up a Remote Debugger configuration with 54321 as the port.
      
      Other IDE's namely Eclipse has similar mechanisms but will leave that as 
      an exercise for reader.  Visual Studio 2013 with Python Tools should work 
      but does not for me (I was able to get it loading with some effort but 
      I get an error about the version not being supported.)
	  
	### ex/source/subfolder/\_\_init\_\_.py
	  The reason for subfolder is just to show how to create subfolders in python.
	  If you want to reference other files like "commands" you have to have
	  and \_\_init\_\_.py file (and it can have just pass) as the contents.
	  
	### ex/source/subfolder/commands.py
	  Commands has a "hello" function.  This is show how to add a command
	  which prints out "world" to the cheat console when ex.hello is typed
	  
	  Note that it also uses print() which uses stdout which we redirected above
	  so that when ex.hello is run this file is updated.  This can be useful
	  for debugging as you can check the contents of stdout.log.
	  
	  There are better ways of doing logging that do not interfere with others
	  but this is a quick and dirty example.
	  

	### Notes
  	  When you type ex.reload in the cheat console (CTRL+SHIFT+C) when in game,
	  it will reload all of the source files in the source folder.
	  
	  This is useful for when you are making changes to and dont want to leave 
	  the current game.  This is by no means a perfect tool and I would expect
	  odd failures.  If you do then its probably best to restart the game.


## Source
  https://github.com/figment/sims4exmod
