import re
import json

from tools.images import generate_image

def compress_tool_prompt(text):
    """Compress the tool prompt by removing all line breaks and spaces.
    This saves context for the model to use.
    Only leave the important part uncompressed, which is the tool tags it should use."""

    # Find all instances of text enclosed in <@ @>
    tool_tags = re.findall(r'<@.*?@>', text, re.DOTALL)
    
    # Remove these instances from the text
    for tag in tool_tags:
        text = text.replace(tag, '')
    
    # Remove all line breaks from the remaining text
    text = text.replace('\n', '')

    # # Remove all spaces from the remaining text, commented out for now as haven't figured out tools completely
    # text = text.replace(' ', '')
    
    # Add the tool tags back into the text
    for tag in tool_tags:
        text += tag
    
    return text

def use_tools(response_text):
    """Use tools on the response text in order of appearance.
    Add new tools by updating the tools folder and adding a case to the switch statement below.
    """
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
