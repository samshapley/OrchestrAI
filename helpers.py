import os
import re

def load_system_prompt(module_name):
    
    # Load the generic system prompt
    with open('general_system.txt', 'r') as file:
        system_prompt = file.read().replace('\n', '')

    with open(f'system_prompts/{module_name}.txt', 'r') as file:
        module_prompt = file.read().replace('\n', '')

    system_prompt = system_prompt + '\n' + module_name.upper() + '\n' +  module_prompt + '\n'
    return system_prompt

def parse_chat(chat):
    # Get all ``` blocks and preceding filenames
    regex = r"(\S+)\n\s*```[^\n]*\n(.+?)```"
    matches = re.finditer(regex, chat, re.DOTALL)
    files = []
    for match in matches:
        # Follow similar steps as your original function...
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
    for file_name, file_content in files:
        with open(os.path.join("generated_code", file_name), "w") as file:
            file.write(file_content)
