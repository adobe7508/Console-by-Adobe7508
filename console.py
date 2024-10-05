import os
import subprocess
import shutil
import pygame  # Import pygame for playing music
from lang import MyLangInterpreter  # Import the custom language interpreter

class WindowsLikeConsole:
    def __init__(self):
        self.running = True
        self.commands = {
            "help": self.help,
            "exit": self.exit_console,
            "cd": self.change_directory,
            "dir": self.list_directory,
            "mkdir": self.make_directory,
            "rmdir": self.remove_directory,
            "echo": self.echo,
            "set": self.set_env_var,
            "get": self.get_env_var,
            #"open": self.open_cla_file,  # Add the open command for .cla files
            "play": self.play_music,  # Add the play command for music
            "pause": self.pause_music,  # Add the pause command for music
            "stop": self.stop_music,  # Add the stop command for music
            "run": self.run_file,  # Add command to run files
            "edit": self.edit_file,  # Add command to edit files with Vim
            "clear": self.clear_screen  # Add the clear command
        }
        self.mylang = MyLangInterpreter()  # Initialize custom language interpreter
        pygame.mixer.init()  # Initialize the Pygame mixer

        # Check if Vim is installed
        self.vim_installed = self.check_vim_installed()

    def check_vim_installed(self):
        try:
            subprocess.run(['vim', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except FileNotFoundError:
            print("Error: Vim is not installed on this system.")
            return False

    def run(self):
        print("Console by Adobe7508. Type 'help' for a list of commands.")
        while self.running:
            current_dir = os.getcwd()
            user_input = input(f"{current_dir}> ")
            self.process_command(user_input.strip())

    def process_command(self, user_input):
        # Check if it's a custom language command
        if self.is_custom_language_command(user_input):
            self.mylang.interpret(user_input)
        else:
            parts = user_input.split()
            command = parts[0].lower() if parts else ''
            args = parts[1:]

            if command in self.commands:
                self.commands[command](args)
            else:
                self.run_external_command(user_input)

    def is_custom_language_command(self, user_input):
        # Detect if the input starts with a custom language command keyword
        return user_input.startswith(("p ", "i ", "new "))

    def open_cla_file(self, args):
        if not args:
            print("Usage: open <filename>")
            return
        filename = args[0]

        if not filename.endswith('.cla'):
            print("Error: Can only open .cla files.")
            return

        if not os.path.isfile(filename):
            print(f"Error: File '{filename}' not found.")
            return

        print(f"Opening and executing '{filename}'...")
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    print(f"Executing: {line}")
                    self.mylang.interpret(line)

    def play_music(self, args):
        if not args:
            print("Usage: play <music_file>")
            return
        music_file = args[0]

        if not os.path.isfile(music_file):
            print(f"Error: File '{music_file}' not found.")
            return

        try:
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play()
            print(f"Playing '{music_file}'...")
        except pygame.error as e:
            print(f"Error: {str(e)}")

    def pause_music(self, args):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            print("Music paused.")
        else:
            print("No music is currently playing.")

    def stop_music(self, args):
        pygame.mixer.music.stop()
        print("Music stopped.")

    def help(self, args):
        print("-------------------")
        print("Available commands:")
        for command in self.commands:
            print(f" - {command}")
        print("-------------------")

    def exit_console(self, args):
        print("Exiting...")
        self.running = False

    def echo(self, args):
        print(" ".join(args))

    def change_directory(self, args):
        if not args:
            print("Usage: cd <directory>")
            return
        try:
            os.chdir(args[0])
            print(f"Directory changed to: {os.getcwd()}")
        except FileNotFoundError:
            print("The system cannot find the path specified.")
        except NotADirectoryError:
            print("The system cannot find the path specified.")

    def list_directory(self, args):
        current_dir = os.getcwd()
        try:
            files = os.listdir(current_dir)
            print(f"Directory of {current_dir}")
            print("--------------------------")
            for file in files:
                print(file)
            print("--------------------------")
        except FileNotFoundError:
            print("Directory not found.")

    def make_directory(self, args):
        if not args:
            print("Usage: mkdir <directory>")
            return
        try:
            os.makedirs(args[0], exist_ok=True)
            print(f"Directory '{args[0]}' created.")
        except Exception as e:
            print(f"Error: {str(e)}")

    def remove_directory(self, args):
        if not args:
            print("Usage: rmdir <directory>")
            return
        try:
            shutil.rmtree(args[0])
            print(f"Directory '{args[0]}' removed.")
        except FileNotFoundError:
            print("The directory does not exist.")
        except Exception as e:
            print(f"Error: {str(e)}")

    def set_env_var(self, args):
        if len(args) == 2:
            os.environ[args[0]] = args[1]
            print(f"Environment variable '{args[0]}' set to '{args[1]}'.")
        else:
            print("Usage: set VAR_NAME VALUE")

    def get_env_var(self, args):
        if len(args) == 1:
            value = os.environ.get(args[0], None)
            if value is not None:
                print(f"{args[0]}={value}")
            else:
                print(f"Error: Environment variable '{args[0]}' not found.")
        else:
            print("Usage: get VAR_NAME")

    def run_file(self, args):
        if not args:
            print("Usage: run <file>")
            return
        file_path = args[0]

        if os.path.isfile(file_path):
            try:
                if file_path.lower().endswith(('.exe', '.lnk')):  # For executables and shortcuts
                    subprocess.run(file_path, shell=True)
                elif file_path.lower().endswith(('.png', '.jpg', '.jpeg')):  # For images
                    subprocess.run(['start', file_path], shell=True)
                elif file_path.lower().endswith(('.mp4', '.avi', '.mkv')):  # For videos
                    subprocess.run(['start', file_path], shell=True)
                elif file_path.lower().endswith('.py'):  # For Python files
                    subprocess.run(['python', file_path], check=True)
                elif file_path.lower().endswith('.cla'):  # For .cla files
                    print(f"Running .cla file: {file_path}")
                    self.open_cla_file(args)  # Reuse the open command for .cla files
                else:
                    print("Unsupported file type.")
            except Exception as e:
                print(f"Error: {str(e)}")
        else:
            print(f"Error: File '{file_path}' not found.")

    def edit_file(self, args):
        if not args:
            print("Usage: edit <filename>")
            return
        filename = args[0]

        if not os.path.isfile(filename):
            print(f"Error: File '{filename}' not found.")
            return

        if self.vim_installed:
            try:
                subprocess.run(['vim', filename])
            except Exception as e:
                print(f"Error: {str(e)}")
        else:
            print("Error: Vim is not installed on this system.")

    def clear_screen(self, args):
        # Clear the console screen
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Screen cleared.")

    def run_external_command(self, command):
        # For other commands, try to run them normally
        try:
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            print(result.stdout.strip())
        except subprocess.CalledProcessError as e:
            print(f"Error: {e.stderr.strip()}")

if __name__ == "__main__":
    console = WindowsLikeConsole()
    console.run()
