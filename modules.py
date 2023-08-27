# modules.py
import helpers as h
from ai import AI
import os
from memory import Logger
logger = Logger()
    
def start_module(module_input):     
    print("\033[92mPlease specify the task you want to perform:\033[00m")
    start = input()
    logger.log_action("start", start, None, None)

    return module_input + start

def human_intervention(module_input):
    module_name = "human_intervention"
    print("Please provide additional information to guide the agent:")
    additional_info = input()

    logger.log_action(module_name, module_input, None, None)
    return module_input + additional_info

def task_planner(prompt):
    module_name = "task_planner"
    ai = AI(module_name, model='gpt-4')
    response, messages = ai.generate_response(prompt)

    logger.log_action(module_name, prompt, response, 'gpt-4')
    return response

def scrutinizer(prompt):
    module_name = "scrutinizer"
    ai = AI(module_name, model='gpt-4')
    response, messages = ai.generate_response(prompt)

    logger.log_action(module_name, prompt, response, 'gpt-4')
    return response

def enhancer(prompt):
    module_name = "enhancer"
    ai = AI(module_name, model='gpt-4')
    response, messages = ai.generate_response(prompt)

    logger.log_action(module_name, prompt, response, 'gpt-4')
    return response

def code_planner(prompt):
    module_name = "code_planner"
    ai = AI(module_name, model='gpt-4')
    print("\033[93mPlanning code...\033[00m")
    response, messages = ai.generate_response(prompt)

    logger.log_action(module_name, prompt, response, 'gpt-4')
    return response

def engineer(prompt):
    module_name = "engineer"
    ai = AI(module_name, model='gpt-4')
    print("\033[93mGenerating code...\033[00m")

    response, messages = ai.generate_response(prompt)

    logger.log_action(module_name, prompt, response, 'gpt-4')

    # Parse the chat and extract files
    files = h.parse_chat(response)
    
    # Save files to disk
    h.to_files(files)
    # Generate repo promtpt.

    # Output of the module is a concatenated text of the codebase
    codebase = h.extract_codebase('generated_code')
    return codebase

def debugger(codebase):
    module_name = "debugger"
    
    # Add a debug_attempt counter
    debug_attempt = 0
    max_attempts = 3
    attempts_left = max_attempts
    
    while True:
        exit_code, error_msg = h.run_main()
        
        # If exit code is 0, the process ran successfully
        if exit_code == 0:
            print("main.py ran successfully!")
            break
        
        # If there was an error
        else:
            print(f"Error encountered: {error_msg}")
            
            # Check if we have made more than 3 debugging attempts
            if debug_attempt >= max_attempts:
                print("\033[91mDebugging has taken more than 3 attempts.\033[00m")
                print("1: Invoke human intervention")
                print("2: End debugging and move to next module")
                choice = input("Please select an option (1 or 2): ")
                
                if choice == "1":
                    debug_attempt = 0
                    attempts_left = max_attempts
                    print("Please provide input for human intervention:")
                    human_input = input()
                    prompt = codebase + "\n The error encountered is: \n" + error_msg + "\n Human Intervention: \n" + human_input
                elif choice == "2":
                    break # End debugging and move to next module
                else:
                    print("Invalid choice. Please try again.")
                    continue
            
            else:
                print("\033[95mDebugging codebase...\033[00m")
                print(f"\033[96m{attempts_left} attempts left\033[00m")
                prompt = codebase + "\n The error encountered is: \n" + error_msg
                ai = AI(module_name, model='gpt-3.5-turbo-16k')
                debug_response, messages = ai.generate_response(prompt)
                logger.log_action(module_name, prompt, debug_response, 'gpt-4')
                debugged_code = h.parse_chat(debug_response)
                h.to_files(debugged_code)
                
                if any("requirements.txt" in file_name for file_name, _ in debugged_code):
                    print("\033[94mReinstalling updated dependencies...\033[00m")
                    os.system("pip3 install -r generated_code/requirements.txt")
                    print("\033[92mUpdated dependencies installed!\033[00m")
                
                print("\033[93mDebugger module has made an attempt to fix. Rerunning main.py...\033[00m")
                
                # Increment the debug_attempt counter
                debug_attempt += 1
                attempts_left -= 1
    
    # Output of the module is a concatenated text of the codebase
    codebase = h.extract_codebase('generated_code')
    return codebase

def modify_codebase(codebase):
    module_name = "modify_codebase"
    while True:
        # Ask the user if they want to modify the codebase or provide feedback
        print("\033[92mDo you want to modify the codebase or provide feedback? y/n:\033[00m")
        choice = input().strip().lower()

        # If the user chooses 'n', exit the loop and return the current state of the codebase
        if choice == 'n':
            break

        # If the user chooses 'y', proceed with the current modification logic
        print("\033[94mPlease specify how you want to modify the codebase:\033[00m")
        instructions = input()


        # Add instructions to codebase
        codebase = codebase + "\n -- User Instructions --" + instructions

        ai = AI(module_name, model='gpt-4')
        print("\033[93mModifying codebase...\033[00m")
        response, messages = ai.generate_response(codebase)
        logger.log_action(module_name, codebase, response, 'gpt-4')

        # Parse the chat and extract files
        files = h.parse_chat(response)
        # Save the codebase.
        h.to_files(files)

        # Extract the updated codebase
        updated_codebase = h.extract_codebase('generated_code')

        # After modification, invoke the debugger module on the updated codebase
        codebase = debugger(updated_codebase)

    return codebase

def create_readme(codebase):
    module_name = "create_readme"
    ai = AI(module_name, model='gpt-4')

    print("\033[93mGenerating README.md...\033[00m")
    response, messages = ai.generate_response(codebase)

    logger.log_action(module_name, codebase, response, 'gpt-4')

    # Save the response to a README.md file in the generated_code folder
    h.to_files([("README.md", response)])

    return response



