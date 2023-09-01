import re
import json

from tools.images import generate_image

def compress_tool_prompt(text):
    # Find all instances of text enclosed in <@ @>
    tool_tags = re.findall(r'<@.*?@>', text, re.DOTALL)
    
    # Remove these instances from the text
    for tag in tool_tags:
        text = text.replace(tag, '')
    
    # Remove all spaces and line breaks from the remaining text
    text = text.replace('\n', '')
    
    # Add the tool tags back into the text
    for tag in tool_tags:
        text += tag
    
    return text

def use_tools(response_text):
    # Extract all contents between <@ @> tags
    contents_list = re.findall('<@(.*)@>', response_text)
    if len(contents_list) == 0:
        return
    else:
        print("\033[92mUsing tools...\033[00m")
        for contents in contents_list:
            try:
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
                    generate_image(contents_json)
                else:
                    pass
            except:
                print("Invalid tool use.")
