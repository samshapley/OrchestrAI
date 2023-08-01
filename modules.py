# modules.py
from ai import AI
import os

def load_system_prompt(module_name):
    with open(f'system_prompts/{module_name}.txt', 'r') as file:
        return file.read().replace('\n', '')
    
def start_module(prompt):
    print("\033[92mPlease specify the task you want to perform:\033[00m")
    return input(prompt), []

def human_intervention(prompt):
    print("Please provide additional information to guide the agent:")
    return input(prompt), []

def task_planner(prompt):
    system_prompt = load_system_prompt("task_planner")
    ai = AI(system=system_prompt, model='gpt-4')
    return ai.generate_response(prompt)

def scrutinizer(prompt):
    system_prompt = load_system_prompt("scrutinizer")
    ai = AI(system=system_prompt, model='gpt-4')
    return ai.generate_response(prompt)

def enhancer(prompt):
    system_prompt = load_system_prompt("enhancer")
    ai = AI(system=system_prompt, model='gpt-4')
    return ai.generate_response(prompt)

def code_planner(prompt):
    system_prompt = load_system_prompt("code_planner")
    ai = AI(system=system_prompt, model='gpt-4')
    return ai.generate_response(prompt)

def engineer(prompt):
    system_prompt = load_system_prompt("engineer")
    ai = AI(system=system_prompt, model='gpt-4')
    return ai.generate_response(prompt)

# Define other module functions here

