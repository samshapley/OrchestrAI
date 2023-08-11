# modules.py
import helpers as h
from ai import AI
import os
from memory import Logger
logger = Logger()
    
def start_module(prompt):     
    print("\033[92mPlease specify the task you want to perform:\033[00m")
    start = input()
    logger.log_action("start", start, None, None)

    return prompt + start, []

def human_intervention(prompt):
    module_name = "human_intervention"
    print("Please provide additional information to guide the agent:")
    additional_info = input()

    logger.log_action(module_name, prompt, None, None)
    return prompt + additional_info, []

def task_planner(prompt):
    module_name = "task_planner"
    system_prompt = h.load_system_prompt(module_name)
    ai = AI(system=system_prompt, model='gpt-4')
    response, messages = ai.generate_response(prompt)

    logger.log_action(module_name, prompt, response, 'gpt-4')
    return response, messages

def scrutinizer(prompt):
    module_name = "scrutinizer"
    system_prompt = h.load_system_prompt(module_name)
    ai = AI(system=system_prompt, model='gpt-4')
    response, messages = ai.generate_response(prompt)

    logger.log_action(module_name, prompt, response, 'gpt-4')
    return response, messages

def enhancer(prompt):
    module_name = "enhancer"
    system_prompt = h.load_system_prompt(module_name)
    ai = AI(system=system_prompt, model='gpt-4')
    response, messages = ai.generate_response(prompt)

    logger.log_action(module_name, prompt, response, 'gpt-4')
    return response, messages

def code_planner(prompt):
    module_name = "code_planner"
    system_prompt = h.load_system_prompt(module_name)
    ai = AI(system=system_prompt, model='gpt-4')
    print("\033[93mPlanning code...\033[00m")
    response, messages = ai.generate_response(prompt)

    logger.log_action(module_name, prompt, response, 'gpt-4')
    return response, messages

def engineer(prompt):
    module_name = "engineer"
    system_prompt = h.load_system_prompt(module_name)
    ai = AI(system=system_prompt, model='gpt-4')
    print("\033[93mGenerating code...\033[00m")

    response, messages = ai.generate_response(prompt)

    logger.log_action(module_name, prompt, response, 'gpt-4')

    # Parse the chat and extract files
    files = h.parse_chat(response)
    
    # Save files to disk
    h.to_files(files)
    # Generate repo promtpt.
    return response, messages

def debugger(prompt):
    module_name = "debugger"
    system_prompt = h.load_system_prompt(module_name)
    ai = AI(system=system_prompt, model='gpt-3.5-turbo-16k')

    # Run the requirements.txt file in generated_code folder with pip3
    print("\033[94mInstalling dependencies...\033[00m")
    os.system("pip3 install -r generated_code/requirements.txt")
    print("\033[92mDependencies Done!\033[00m")

    while True:
        exit_code, error_msg = h.run_main()

        # If exit code is 0, the process ran successfully
        if exit_code == 0:
            print("main.py ran successfully!")
            break

        # If there was an error
        else:
            print(f"Error encountered: {error_msg}")
            print("\033[95mDebugging code...\033[00m")


            prompt = prompt + "\n The error encountered is: \n" + error_msg


            debug_response, messages = ai.generate_response(prompt)
            logger.log_action(module_name, prompt, debug_response, 'gpt-4')

            debugged_code = h.parse_chat(debug_response)
            h.to_files(debugged_code)

            # Check if requirements.txt is modified and reinstall the packages
            if any("requirements.txt" in file_name for file_name, _ in debugged_code):
                print("\033[94mReinstalling updated dependencies...\033[00m")
                os.system("pip3 install -r generated_code/requirements.txt")
                print("\033[92mUpdated dependencies installed!\033[00m")

            print("\033[92mDebugger module has made an attempt to fix. Rerunning main.py...\033[00m")
            # The loop will then repeat and try running main.py again

    



