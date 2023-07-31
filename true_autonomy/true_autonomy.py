import yaml
import networkx as nx
from ai import AI

# Load modules
with open('modules.yml') as f:
    modules = yaml.safe_load(f)

# Create a dictionary for quick lookup of modules
module_dict = {module['name']: module for module in modules['modules']}

# Create a dictionary of AI instances
ai_dict = {}

# Load general_system.txt for use in all modules
with open('general_system.txt', 'r') as file: 
    general_system = file.read().replace('\n', '')

for module in modules['modules']:
    module_name = module['name']
    is_llm = module['is_llm']
    if is_llm:
        with open(f'systems/{module_name}.txt', 'r') as file: 
            system = file.read().replace('\n', '') 
        ai_dict[module_name] = AI(system=general_system + module_name.upper() + system)
    else: 
        ai_dict[module_name] = None

# Create a pipeline
pipeline = {"pipeline": []}

steps = 0
n = 10 # Set the number of steps before choose module stage

while True:
    if steps % n == 0:
        module_name = "choose_module"
    else:
        module_name = ai_dict[module_name].generate_response() # choose the next module

    if module_name in ai_dict and ai_dict[module_name] is not None:
        ai_instance = ai_dict[module_name]
        prompt = '\n'.join([output for output in pipeline["pipeline"]]) # use previous outputs as the prompt
        result, messages = ai_instance.generate_response(prompt)
        pipeline["pipeline"].append({"module": module_name, "output": result})

        # Save the updated pipeline to pipeline.yml every time choose_module is called
        if module_name == "choose_module":
            with open('pipeline.yml', 'w') as outfile: 
                yaml.dump(pipeline, outfile, default_flow_style=False)
    elif not module_dict[module_name]['is_llm']:
        input_value = input("Please provide input: ")
        pipeline["pipeline"].append({"module": module_name, "output": input_value})
    else:
        print(f"Warning: No AI instance for module '{module_name}'. Ignoring.")

    steps += 1
