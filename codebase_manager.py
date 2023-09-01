import os
import shutil
import sys
import subprocess
import re
import wandb_logging as wb
import globals
from datetime import datetime
import time

# open the config file
import yaml
with open('config.yml', 'r') as f:
    config = yaml.safe_load(f)

wandb_enabled = config['wandb_enabled'] # Set the wandb_enabled flag

### Methods used by engineer, debugger and modify_codebase to build repositories
class CodebaseManager:
    
    def __init__(self, directory):
        self.parent_directory = 'generated_outputs'
        self.directory = os.path.join(self.parent_directory, directory)
        self.req_file_path = os.path.join(self.directory, 'requirements.txt')

    @staticmethod
    def extract_code(chat):
        """Extract any code files and script from response of chat"""
        print("\033[95mExtracting code...\033[00m")
        # Get all ``` blocks and preceding filenames
        regex = r"(\S+)\n\s*```[^\n]*\n(.+?)```"
        matches = re.finditer(regex, chat, re.DOTALL)
        files = []
        for match in matches:
            # Extract the filename and code, thanks gpt-engineer for this regex!
            path = re.sub(r"[<>'|?*]", "", match.group(1))
            path = re.sub(r"^\[(.*)\]$", r"\1", path)
            path = re.sub(r"^`(.*)`$", r"\1", path)
            path = re.sub(r"\]$", "", path)
            code = match.group(2)
            files.append((path, code))
        return files

    def update_codebase(self, files):
        """Create or replace any script in the updates list."""

        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        
        # Create an empty requirements.txt file only if it doesn't exist
        if not os.path.exists(self.req_file_path):
            with open(self.req_file_path, "w") as req_file:
                req_file.write("")

        for file_name, file_content in files:
            # Create directories in the file path if they don't exist
            os.makedirs(os.path.dirname(os.path.join(self.directory, file_name)), exist_ok=True)
            
            with open(os.path.join(self.directory, file_name), "w") as file:
                file.write(file_content)
        

    def compress_codebase(self):
        """Extracts the existing codebase from the directory.
           Compresses it into reduced token package."""
        
        ignore_list = ['filename_to_ignore.py', 'another_file_to_ignore.yml']
        ignore_endings = ['.pycache', '.pyc']

        result_content = []

        for root, dirs, files in os.walk(self.directory):
            for filename in files:
                # Skip files in ignore list
                if filename in ignore_list:
                    continue

                # Only process files not in ignore_endings list
                if not any(filename.endswith(ending) for ending in ignore_endings):
                    filepath = os.path.join(root, filename)
                    try:
                        with open(filepath, 'r') as infile:
                            # Read the contents of the file, remove line breaks and leading spaces
                            content = infile.read().replace('\n', '').replace('\r', '')
                            content = ' '.join(content.split())
                            # Get the relative path of the file
                            relative_filepath = os.path.relpath(filepath, self.directory)
                            result_content.append(f"----{relative_filepath}----\n{content}")
                            e= None
                    except Exception as e:
                        print(f"Error processing file {filepath}: {e}")

        return "\n".join(result_content)

    def list_dependencies(self):
        with open(self.req_file_path, 'r') as f:
            dependencies = f.read().splitlines()
        return dependencies
    
    def run_main(self):
        """
        Execute the main.py script from the working codebase (set in config).

        This function utilizes subprocess.Popen to run the main.py script in a separate process.
        The stdout (standard output) of the subprocess is set to be printed in real-time to the terminal.
        This ensures that any prompts in the main.py script requiring user input will be displayed and can be interacted with.
        Meanwhile, the stderr (standard error) of the subprocess is captured and returned, 
        which allows for error handling in the event of any issues during the script's execution.

        Returns:
            tuple: A tuple containing two items:
                - The return code (exit status) of the subprocess. A value of 0 typically indicates successful execution, while any other value suggests an error.
                - The error message (if any) captured from the stderr of the subprocess.
        """
        start_time_ms = round(datetime.now().timestamp() * 1000)

        # Start a new process to run the main.py script. 
        # stdout=None ensures the standard output (e.g., print statements, prompts for input) 
        # of the script is directly displayed in real-time on the terminal.
        # stderr=subprocess.PIPE captures the error stream of the script, which can be later accessed.
            # Check if 'python3' is available in PATH
        if shutil.which('python3') is not None:
            python_command = 'python3'
        else:
            python_command = 'python'

        process = subprocess.Popen(
            [python_command, os.path.join(self.directory, "main.py")],
            text=True,
            bufsize=1,
            stdout=sys.stdout,  # Connect subprocess's stdout directly to the terminal
            stdin=sys.stdin,    # Connect subprocess's stdin directly to the terminal
            stderr=subprocess.PIPE
        )

        # Wait for the subprocess to finish and capture any error message from the stderr.
        _, stderr = process.communicate()

        if wandb_enabled:
            time.sleep(0.5)
            wb.wandb_log_tool(
                tool_name="run_main",
                start_time_ms=start_time_ms,
                inputs={"python_command": python_command,
                        "run_script_path": os.path.join(self.directory, "main.py")},
                outputs={"stdout": process.stdout,
                        "stderr": stderr},
                status= "success" if process.returncode == 0 else "error",
                parent=globals.llm_span   
            )

        return process.returncode, stderr
    

        