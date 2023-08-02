# modules.py
import helpers as h
from ai import AI
import os
    
def start_module(prompt):
    print("\033[92mPlease specify the task you want to perform:\033[00m")
    start = input()
    return prompt + start, []

def human_intervention(prompt):
    print("Please provide additional information to guide the agent:")
    additional_info = input()
    return prompt + additional_info, []

def task_planner(prompt):
    system_prompt = h.load_system_prompt("task_planner")
    ai = AI(system=system_prompt, model='gpt-4')
    response, messages = ai.generate_response(prompt)
    print(response)
    return response, messages

def scrutinizer(prompt):
    system_prompt = h.load_system_prompt("scrutinizer")
    ai = AI(system=system_prompt, model='gpt-4')
    response, messages = ai.generate_response(prompt)
    print(response)
    return response, messages

def enhancer(prompt):
    system_prompt = h.load_system_prompt("enhancer")
    ai = AI(system=system_prompt, model='gpt-4')
    response, messages = ai.generate_response(prompt)
    print(response)
    return response, messages

def code_planner(prompt):
    system_prompt = h.load_system_prompt("code_planner")
    ai = AI(system=system_prompt, model='gpt-4')
    print("\033[93mPlanning code...\033[00m")
    response, messages = ai.generate_response(prompt)
    print(response)
    return response, messages

def debugger(prompt):
    system_prompt = h.load_system_prompt("debugger")
    ai = AI(system=system_prompt, model='gpt-4')
    print("\033[93mDebugging code...\033[00m")
    response, messages = ai.generate_response(prompt)
    print(response)
    return response, messages

def engineer(prompt):
    system_prompt = h.load_system_prompt("engineer")
    ai = AI(system=system_prompt, model='gpt-4')
    print("\033[93mGenerating code...\033[00m")
    response, messages = ai.generate_response(prompt)
    print(response)
    
    # Parse the chat and extract files
    print("\033[95mExtracting code...\033[00m")
    files = h.parse_chat(response)
    
    # Save files to disk
    h.to_files(files)

    # Run the requirements.txt file in generated_code folder with pip3
    print("\033[94mInstalling dependencies...\033[00m")
    os.system("pip3 install -r generated_code/requirements.txt")
    print("\033[92mDependencies Done!\033[00m")

    # In a while loop, run main.py, and if it crashes, pass the full codebase to the debugger.
    print("\033[91mRunning code...\033[00m")
    os.system("python3 generated_code/main.py")
    
    return response, messages