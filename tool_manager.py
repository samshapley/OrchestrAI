import os
import importlib.util
import re
import json

def load_all_functions(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".py"):
            script_name = filename[:-3]  # Remove the .py extension
            script_path = os.path.join(directory, filename)
            spec = importlib.util.spec_from_file_location(script_name, script_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            globals().update(
                {n: getattr(module, n) for n in dir(module) if not n.startswith("_")}
            )

# Use the function to load all scripts from the 'tools' directory
load_all_functions('tools')

def use_tools(response_text):
    print("\033[93mUsing tools...\033[00m")
    # Extract all contents between <@ @> tags
    contents_list = re.findall('<@(.*)@>', response_text)
    print(contents_list)
    for contents in contents_list:
        contents = contents.strip()  # Trim the extracted contents

        # Parse the contents as a JSON object
        try:
            contents_json = json.loads(contents)
        except:
            print("Invalid tool use.")
            continue

        # Perform different actions depending on the tool_name key
        tool_name = contents_json.get('tool_name')
        if tool_name == 'GENERATE_IMAGE':
            generate_image(contents_json.get('prompt'))
        else:
            pass