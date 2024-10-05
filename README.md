Console-by-Adobe7508



This project implements a command-line interface (CLI) resembling the functionality of Windows Command Prompt. It supports various commands for file management, music playback, and custom language interpretation.

Features
Command Management: Supports a range of built-in commands.
Music Playback: Play, pause, and stop music files using pygame.
Directory Management: Change, create, and remove directories.
File Execution: Run scripts, executables, and open files of various types.
Custom Language Support: Execute commands from a custom language interpreter.
To run this project, you need Python 3.6 or higher and the following libraries:

pygame==2.6.0


vim


You can install the required libraries using:

python console.py


Usage


Once the console is running, you can use various commands. Here are some common commands:

help: Display available commands.


exit: Exit the console.


cd <directory>: Change the current directory.


dir: List files in the current directory.


mkdir <directory>: Create a new directory.


rmdir <directory>: Remove a directory.


echo <message>: Print a message to the console.


play <music_file>: Play a music file.


pause: Pause the currently playing music.


stop: Stop the currently playing music.


run <file>: Run an executable, script, or open a file.


edit <filename>: Edit a file using Vim.


Custom Language Support




The console supports a custom language interpreter through the MyLangInterpreter class. You can create and run commands in this custom language by using keywords like p, i, and new.
