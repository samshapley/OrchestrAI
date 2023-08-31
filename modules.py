# modules.py
import os
import yaml
import helpers as h
from ai import AI
from codebase_manager import CodebaseManager
import wandb_logging as wb
import local_logging as ll
import globals


# Load the configuration
with open('config.yml', 'r') as f:
    config = yaml.safe_load(f)

wandb_enabled = config['wandb_enabled'] # Set the wandb_enabled flag
working_codebase_dirname = config['working_codebase_dirname'] # Where code is accessed during a pipeline run

codebase_portal = CodebaseManager(working_codebase_dirname)

def start_module(module_input, dummy=None):   
    """This function is used to invoke the start module, to accept user input into the pipeline""" 
    module_name = "start_module"
    print("\033[92mPlease specify the task you want to perform:\033[00m")
    start = input()

    output = module_input + start

    ll.log_action({"module": module_name, "input": module_input, "output": output})
    if wandb_enabled:
        wb.wandb_log_tool(tool_name = module_name,
                    inputs    = {},
                    outputs   = {"original_input": output},
                    parent    = globals.chain_span,
                    status    = "success")

    return output

def human_intervention(module_input, dummy=None):
    module_name = "human_intervention"
    print("Please provide additional information to guide the agent:")
    additional_info = input()

    output = module_input + additional_info

    ll.log_action({"module": module_name, "input": module_input, "output": output})
    if wandb_enabled:
        wb.wandb_log_tool(tool_name = module_name,
                    inputs    = {},
                    outputs   = {"human_intervention": output},
                    parent    = globals.chain_span,
                    status    = "success")

    return output

def chameleon(prompt, module_name, model_config=None):
    """This function is used to invoke the chameleon module.
    The orchestration is set up to invoke this model when:
        1. A function specified in the pipeline does not exist.
        2. A system prompt with a matching module name exists.

    This is so all the user has to do is provide a system prompt for a module if it's a simple AI call module, 
    and the orchestration will take care of the rest.
    """
    ai = AI(module_name, model_config=model_config)
    response = ai.generate_response(prompt)

    ll.log_action({"module": module_name, "input": prompt, "output": response})
    if wandb_enabled:
        wb.wandb_log_llm(response, ai.model, ai.temperature, parent = globals.chain_span)

    return response["response_text"]

def engineer(prompt, model_config=None):
    """This function is used to invoke the engineer module.
    The generated code is extracted from the response and
    saved to the working codebase."""

    module_name = "engineer"
    ai = AI(module_name, model_config=model_config)
    print("\033[93mGenerating code...\033[00m")

    response = ai.generate_response(prompt)

    ll.log_action({"module": module_name, "input": prompt, "output": response})
    if wandb_enabled:
        wb.wandb_log_llm(response, ai.model, ai.temperature, parent = globals.chain_span)

    response_text = response["response_text"]

    # Parse the chat and extract files
    files = codebase_portal.extract_code(response_text)
    
    # Save files
    codebase_portal.update_codebase(files)
    # Generate repo promtpt.

    # Output of the module is a concatenated text of the codebase
    codebase = codebase_portal.compress_codebase()
    return codebase

def debugger(codebase, model_config=None):
    module_name = "debugger"
    
    # Add a debug_attempt counter
    debug_attempt = 0
    max_attempts = 3
    attempts_left = max_attempts

        # Install dependencies before starting the debugging process
    print("\033[94mInstalling dependencies...\033[00m")
    print(codebase_portal.list_dependencies())
    os.system(f"pip3 install -r {working_codebase_dirname}/requirements.txt")
    print("\033[92mDependencies installed!\033[00m")
    
    human_intervention_provided = False

    while True:
        if not human_intervention_provided:
            exit_code, error_msg = codebase_portal.run_main()
        else:
            human_intervention_provided = False
        
        # If exit code is 0, the process ran successfully
        if exit_code == 0:
            print("main.py ran successfully!")
            break
        
        # If there was an error
        else:
            if not human_intervention_provided:
                print(f"Error encountered: {error_msg}")
            
            # Check if we have made more than 3 debugging attempts
            if debug_attempt >= max_attempts:
                print("\033[91mDebugging has taken more than 3 attempts.\033[00m")
                print("1: Invoke human intervention")
                print("2: End debugging and move to next module")
                choice = input("Please select an option (1 or 2): ")
                
                if choice == "1":
                    human_intervention_provided = True
                    debug_attempt = 0
                    attempts_left = max_attempts
                    print("\033[93mPlease provide input for human intervention:\033[00m")
                    human_input = human_intervention(codebase)
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
                ai = AI(module_name, model_config=model_config)
                debug_response = ai.generate_response(prompt)

                ll.log_action({"module": module_name, "input": prompt, "output": debug_response})
                if wandb_enabled:
                    wb.wandb_log_llm(debug_response, ai.model, ai.temperature, parent = globals.chain_span)

                debugged_code = codebase_portal.extract_code(debug_response["response_text"])
                codebase_portal.update_codebase(debugged_code)
                
                if any("requirements.txt" in file_name for file_name, _ in debugged_code):
                    print("\033[94mReinstalling updated dependencies...\033[00m")
                    os.system(f"pip3 install -r {working_codebase_dirname}/requirements.txt")
                    print("\033[92mUpdated dependencies installed!\033[00m")
                
                print("\033[93mDebugger module has made an attempt to fix. Rerunning main.py...\033[00m")
                
                # Increment the debug_attempt counter
                debug_attempt += 1
                attempts_left -= 1
    
    # Output of the module is a concatenated text of the codebase
    codebase = codebase_portal.compress_codebase()
    return codebase

def modify_codebase(codebase, model_config=None):
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

        ai = AI(module_name, model_config=model_config)
        print("\033[93mModifying codebase...\033[00m")
        response = ai.generate_response(codebase)

        ll.log_action({"module": module_name, "input": codebase, "output": response})
        if wandb_enabled:
            wb.wandb_log_llm(response, ai.model, ai.temperature, parent = globals.chain_span)

        # Parse the chat and extract files
        files = codebase_portal.extract_code(response["response_text"])

        # Save the codebase.
        codebase_portal.update_codebase(files)

        # Extract the updated codebase
        updated_codebase = codebase_portal.compress_codebase()

        # After modification, invoke the debugger module on the updated codebase
        codebase = debugger(updated_codebase)

    return codebase

def create_readme(codebase, model_config=None):
    module_name = "create_readme"
    ai = AI(module_name, model_config=model_config)

    print("\033[93mGenerating README.md...\033[00m")
    response = ai.generate_response(codebase)

    ll.log_action({"module": module_name, "input": codebase, "output": response})
    if wandb_enabled:
        wb.wandb_log_llm(response, ai.model, ai.temperature, parent = globals.chain_span)

    # Save the response to a README.md file to the working codebase
    codebase_portal.update_codebase([("README.md", response["response_text"])])

    return response
