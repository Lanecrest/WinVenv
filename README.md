# WinVenv
WinVenv is a Python virtual environment (venv) manager for Windows built using tkinter with a minimal design optimized for easy execution of Python scrips via different venvs. 

# About
This application is intended to reside in the root of a folder in which you would like to keep multiple venvs. A simple GUI file tree allows you to launch any file, but when launching a Python script, it will default to being ran through a specific venv if the directory it is in contains a "Scripts" folder with a venv activation file (the default behavior for activating venvs on Windows).

You can also launch a shell for one of the venvs in the app's file menu dropdown which will allow you to execute any file through that specific venv. Additionally, launching a shell this way will list all packages installed for that venv when the shell opens. You can right click files out of the file tree to copy their path to make it easier to paste into the new shell window.

The last main feature is the ability to create a new venv directly through the GUI using the file menu. This will run the "python -m venv" from the root directory to make a subfolder for the venv and then will automatically add it to the environments drop down menu.

# Screenshots
[Screenshots](/screenshots)

![Alt text](/screenshots/v1-0-0_main.png?raw=true "Main Window")

# Change Log
[Change Log](CHANGELOG.md)

# Requirements
This app uses all default modules as it is intended to be able to run from a clean Python installation.

# Road Map
The scope of the project is to remain simple and not become too complex, however various optimizations or quality of life improvements will likely be added along the way.

# Credits
Lanecrest Tech © 2023

This program is free software released under the BSD 3-clause License.
