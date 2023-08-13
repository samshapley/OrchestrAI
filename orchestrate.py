# orchestrate.py
import yaml
import networkx as nx
import modules
import sys

def execute_pipeline(pipeline):
    
    # Create the DAG
    G = nx.DiGraph()

    # Create an empty string to store our ASCII pipeline representation
    ascii_pipeline = ""

    # Data dictionary to store the outputs of each module
    data_dict = {}

    for operation in pipeline['pipeline']:
      module_name = operation['module']
      output_name = operation['output_name']
      inputs = operation['inputs']
      supplement = operation.get('supplement', '')

      # Add node for this operation's output if it doesn't already exist
      G.add_node(output_name)

      # Add edges for inputs
      for i in inputs:
        G.add_edge(i, output_name)

      # Add this operation to our ASCII pipeline representation
      ascii_pipeline += "{} --> {} --> {}\n".format(inputs, module_name, output_name)

    print(ascii_pipeline)

    # Now we use topological sort to get the execution order:
    try:
        execution_order = list(nx.topological_sort(G))
    except nx.NetworkXUnfeasible:
        print("\033[91mError: The pipeline has a cycle and is therefore invalid.\033[00m")
        sys.exit(1)

    # Check if the DAG is connected:
    if not nx.is_weakly_connected(G):
        print("\033[91mError: The pipeline is invalid. Not all operations are connected.\033[00m")
        sys.exit(1)

    # And execute the tasks in this order, passing the necessary data between them:
    for output_name in execution_order:
      if output_name in data_dict: 
        # skip over inputs that are already defined
        continue

      operation = [item for item in pipeline['pipeline'] if item['output_name'] == output_name][0]
      module_name = operation['module']
      supplement = operation.get('supplement', '')
      
      # Print the module name in red
      print(f"\033[91m{module_name.upper()}\033[00m")

      if hasattr(modules, module_name):
        module_func = getattr(modules, module_name)
        module_input = '\n'.join([data_dict.get(input, '') for input in operation['inputs']])
        module_input += '\n Additional User Input' + supplement
        module_output = module_func(module_input)
        data_dict[output_name] = module_output
      else:
        print(f"Warning: No module function '{module_name}'. Ignoring.")
