import yaml
import matplotlib.pyplot as plt
from tool_manager import compress_tool_prompt

# Load the configuration
with open('config.yml', 'r') as f:
    config = yaml.safe_load(f)

tools_enabled = config['tools_enabled']

def load_pipeline(file_path):
    """Load a pipeline configuration from a YAML file."""
    print("\033[93mLoading pipeline...\033[00m")
    with open(file_path, 'r') as f:
        pipeline = yaml.safe_load(f)
    return pipeline

def load_system_prompt(module_name):
    # Load the generic system prompt
    with open('general_system.txt', 'r') as file:
        general_system_prompt = file.read().replace('\n', '')

    system_prompt = general_system_prompt

    if tools_enabled:
        with open(f'tools/tool_prompt.txt', 'r') as file:
            tool_prompt = file.read().replace('\n', '')

        tool_prompt = compress_tool_prompt(tool_prompt) # Compress the tool prompt
        system_prompt += '\n\n' + tool_prompt + '\n'
    else:
        tool_prompt = None

    with open(f'system_prompts/{module_name}.txt', 'r') as file:
        module_prompt = file.read().replace('\n', '')

    system_prompt += '\n\n --- ' + module_name.upper() + ' ---\n\n' +  module_prompt + '\n'

    component_prompts = {
        'general_system_prompt': general_system_prompt,
        'tool_prompt': tool_prompt,
        'module_prompt': module_prompt,
    }
        
    return system_prompt, component_prompts

def visualize_pipeline(nx, G):
    # Increase distance between nodes by setting k parameter
    pos = nx.spring_layout(G, seed=42, k=2)  
    
    # Get module names as labels
    labels = nx.get_node_attributes(G, 'module')  
    
    # Draw the nodes
    nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=300)
    
    # Draw the edges with arrows
    nx.draw_networkx_edges(G, pos, arrowstyle="->", arrowsize=10, edge_color="gray")
    
    # Draw the labels for the nodes with reduced font size
    nx.draw_networkx_labels(G, pos, labels, font_size=8)
    
    # Draw the labels for the edges with reduced font size
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6)
    
    plt.savefig("pipeline.png", dpi=300, bbox_inches='tight')
