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

# Load pipeline.yml from pipelines folder
with open('pipelines/pipeline.yml') as f: 
    pipeline = yaml.safe_load(f)

# Create the DAG
G = nx.DiGraph()

# Data dictionary to store the outputs of each module
data_dict = {}

for operation in pipeline['pipeline']:
    module_name = operation['module']
    output_name = operation['output_name']
    inputs = operation['inputs']
    
    # Add node for this module if it doesn't already exist 
    G.add_node(module_name) 
    
    # Add edges for inputs 
    for i in inputs: 
        G.add_edge(i, module_name)
        
    G.add_edge(module_name, output_name)

# Now you can use topological sort to get the execution order:
execution_order = list(nx.topological_sort(G))

# And execute the tasks in this order, passing the necessary data between them:
for operation in pipeline['pipeline']:
    module_name = operation['module']
    
    if module_name in ai_dict and ai_dict[module_name] is not None:
        ai_instance = ai_dict[module_name]
        
        # Construct the prompt based on previous outputs
        prompt = '\n'.join([data_dict[input] for input in operation['inputs']])
        
        print(f"\n\n{'='*50}\n{module_name}\n{'='*50}\n")
        
        # Generate the response
        result, messages = ai_instance.generate_response(prompt)
        
        print(f"Result: {result}\n")
        
        # Save the output in data_dict for use in later modules 
        data_dict[operation['output_name']] = result
        
    elif not module_dict[module_name]['is_llm']:
        input_value = input("Please provide input: ") 
        data_dict[operation['output_name']] = input_value
        
    else:
        print(f"Warning: No AI instance for module '{module_name}'. Ignoring.")

# At this point, data_dict contains the final outputs from all modules
# Save the final output to a file

with open('final_output.txt', 'w') as file:
    file.write(data_dict['output'])
