import os
import re
import subprocess
import sys
import yaml

def load_pipeline(file_path):
    """Load a pipeline configuration from a YAML file."""
    print("\033[93mLoading pipeline...\033[00m")
    with open(file_path, 'r') as f:
        pipeline = yaml.safe_load(f)
    return pipeline

def load_system_prompt(module_name):
    
    # Load the generic system prompt
    with open('general_system.txt', 'r') as file:
        system_prompt = file.read().replace('\n', '')

    with open(f'system_prompts/{module_name}.txt', 'r') as file:
        module_prompt = file.read().replace('\n', '')

    system_prompt = system_prompt + '\n' + module_name.upper() + '\n' +  module_prompt + '\n'
    return system_prompt

def parse_chat(chat):
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

def to_files(files):
    if not os.path.exists("generated_code"):
        os.mkdir("generated_code")
    
    # Create an empty requirements.txt file by default
    with open(os.path.join("generated_code", "requirements.txt"), "w") as req_file:
        req_file.write("")

    for file_name, file_content in files:
        with open(os.path.join("generated_code", file_name), "w") as file:
            file.write(file_content)

def run_main():
    """
    Execute the main.py script from the generated_code directory.

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

    # Start a new process to run the main.py script. 
    # stdout=None ensures the standard output (e.g., print statements, prompts for input) 
    # of the script is directly displayed in real-time on the terminal.
    # stderr=subprocess.PIPE captures the error stream of the script, which can be later accessed.
    process = subprocess.Popen(
        ["python", "generated_code/main.py"],
        text=True,
        bufsize=1,
        stdout=sys.stdout,  # Connect subprocess's stdout directly to the terminal
        stdin=sys.stdin,    # Connect subprocess's stdin directly to the terminal
        stderr=subprocess.PIPE
    )

    # Wait for the subprocess to finish and capture any error message from the stderr.
    _, stderr = process.communicate()

    return process.returncode, stderr

def extract_codebase(directory='generated_code', ignore_list=[]):
    """Extracts the exsiting codebase from the generated_code directory into a condensed string."""
    
    result_content = []

    for filename in os.listdir(directory):
        # Skip files in ignore list
        if filename in ignore_list:
            continue

        # Only process .py, .yml, or .md files
        if filename.endswith(('.yml', '.py', '.md')):
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, 'r') as infile:
                    # Read the contents of the file, remove line breaks and leading spaces
                    content = infile.read().replace('\n', '').replace('\r', '')
                    content = ' '.join(content.split())
                    result_content.append(f"--- File Name: {filename} ---\n{content}")
            except Exception:
                pass

    return "\n".join(result_content)
