import os
import json

# Ignore list, a list of files to ignore if name matches
ignore = [
    'prompt.py',
    'README.md',
] 

def get_current_dir():
    return os.getcwd()

def write_content(outfile, filepath, content):
    # Writing file path to the output file
    outfile.write(f"\n--- File Path: {filepath} ---\n")
    
    # Writing the cleaned contents of the file to the output file
    outfile.write(content)
    outfile.write("\n")

def process_file(filename, outfile):
    # Check if the file is in the ignore list
    if filename in ignore:
        return
    
    filepath = os.path.join(get_current_dir(), filename)
    
    # Check if the file is a .py or .yml file
    if filename.endswith('.yml') or filename.endswith('.py') or filename.endswith('.md'):
        try:
            with open(filepath, 'r') as infile:
                # Read the contents of the file, remove line breaks and leading spaces
                content = infile.read().replace('\n', '').replace('\r', '')
                content = ' '.join(content.split())
                write_content(outfile, filepath, content)
        except Exception:
            pass

def main():
    # Get the current directory
    current_dir = get_current_dir()

    # Open the target file
    with open('prompt.txt', 'w') as outfile:
        # Loop over all files in the current directory
        for filename in os.listdir(current_dir):
            process_file(filename, outfile)
        
        # Add the chosen text string at the end
        chosen_text = "\nIf you understand, generate only YES."
        outfile.write(chosen_text)


if __name__ == "__main__":
    main()