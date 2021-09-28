
# =============================================================================
#    Author: Kenneth Perkins
#    Date:   Jul 25, 2013
#    Updated: Feb 12, 2021
#    Taken From: http://programmingnotes.org/
#    File:  setup.py
#    Description: This is the cx_Freeze setup file for creating an exe program
# =============================================================================
from cx_Freeze import setup, Executable
# NOTE: you can include any other necessary external imports here aswell
 
includefiles = ["images/ship.bmp",
                "images/alien.bmp", "game_stats.py", "bullet.py",
                "ship.py", "settings.py", "scoreboard.py",
                "alien.py", "button.py",
                ] # include any files here that you wish
excludes = []
packages = ["pygame"]
 
exe = Executable(
 # what to build
   script = "alien_invasion.py", # the name of your main python script goes here 
   init_script = None,
   base = None, # if creating a GUI instead of a console app, type "Win32GUI"
   target_name = "Alien Invasion.exe", # this is the name of the executable file
   icon = None # if you want to use an icon file, specify the file name here
)
 
setup(
 # the actual setup & the definition of other misc. info
    name = "Alien Invasion", # program name
    version = "0.1",
    description = 'A shootem up game!',
    author = "Vincent Reid",
    author_email = "",
    options = {"build_exe": {"excludes":excludes,"packages":packages,
      "include_files":includefiles}},
    executables = [exe]
)
# http://programmingnotes.org/