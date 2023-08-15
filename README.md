# OrchestrAI

OrchestrAI is a Python-based system that orchestrates interactions between multiple instances of OpenAI's GPT-4 model to execute complex tasks. It uses the `networkx` library to manage dependencies between various AI modules, and YAML to define and manage task pipelines.  

## Getting Started

### Prerequisites

To run OrchestrAI, you'll need:

- Python 3.7 or later
- OpenAI Python library  
- networkx
- PyYAML

Install these with pip:

```bash
pip install -r requirements.txt
```

### Configuration  

OrchestrAI requires the following files:

- `ai.py` - Manages interactions with the OpenAI GPT-4 model. Set your OpenAI API key here.
- `modules.py` - Contains available AI modules. 
- `orchestrate.py` - Loads modules and pipelines, constructs a Directed Acyclic Graph (DAG) of operations, and executes them in the correct order.
- `agent.py` - Run the script and the specified pipeline.
- `helpers.py` - Provides helper functions, including loading system prompts, parsing chat data, and writing code files.
- `pipeline.yml` - Describes the sequence of operations to be executed in your pipeline.

## Understanding the Modules

The `modules.py` file contains different AI modules, each responsible for a specific type of operation, such as `start_module`, `task_planner`, `scrutinizer`, `enhancer`, `code_planner`, `debugger`, and `engineer`.

Each module interacts with the a language model to execute its specific task, and the output is stored for use in subsequent operations as defined in the pipeline. Currently, the modules are only communicating with OpenAI, but this can be extended to other language models as well.

### Setting Up a Pipeline

1. Define your pipeline in the `pipeline.yml` file. Each operation in the pipeline consists of a `module`, `inputs`, and an `output_name`. The `module` represents a specific task performed by an AI, `inputs` are the dependencies for the module and the `output_name` is the output of that task, which can be used as input for subsequent operations. Here's an example of a pipeline:

```yaml
pipeline:
  - module: start_module 
    inputs: [] 
    output_name: request
  - module: task_planner
    inputs: [request]
    output_name: task_plan
  - module: scrutinizer 
    inputs: [request, task_plan]
    output_name: scrutinized_task_plan
  - module: enhancer
    inputs: [request, scrutinized_task_plan, task_plan] 
    output_name: enhanced_task_plan
  - module: code_planner
    inputs: [request, enhanced_task_plan]
    supplement: "Use only python."  
    output_name: code_plan
  - module: engineer 
    inputs: [code_plan]
    output_name: code
  - module: debugger
    inputs: [code] 
    output_name: debugged_code
```

2. Save and close the `pipeline.yml` file.


### Running the Script

To run OrchestrAI, execute `agent.py`:

```bash
python agent.py
```

The script will execute the operations in the pipeline in the order specified, querying the GPT-4 model as necessary and storing the results. The 'orchestrate.py' script handles the pipeline and the execution order of the tasks and modules.

## Self-Debugging

The `debugger` module implements a self-debugging loop to automatically fix errors in the generated code. 

It first tries to run `main.py` and if it encounters any runtime errors, it sends the error message back to the model to generate fixed code. During testing, I've found that the gpt-3.5-turbo-16k model is able to fix most errors in the generated code, so this is currently the default model used for debugging. Potentially something could be implemented that swaps to a different model if the error is not fixed after a certain number of iterations.

It also checks if `requirements.txt` was modified and re-installs any new dependencies. This loop repeats until `main.py` runs successfully without errors.

This enables OrchestrAI to iteratively improve and fix the generated code until it works as intended.

## Memory Logging

The `memory.py` file contains a Logger class that logs the actions of each module. Each action log contains the module name, prompt, response, model used, and a timestamp. The logs are stored in a JSON file named 'memory_log.json'.

This enables OrchestrAI to maintain memory and context across pipeline executions.

Here is a section on how to create a new module in OrchestrAI:

## Creating New Modules

To add new capabilities to OrchestrAI, you can create custom modules.

Steps to create a new module:

1. Add a new function in `modules.py` with the name of your module. For example:

```python
def new_module(prompt):
  # Module logic
  ...
  return output, messages
```

2. If this module requires a call to OpenAI, design and load the appropriate system prompt for your module from `system_prompts/`.

3. Interact with the model via the `AI` class to generate a response.

4. Log the action using the `Logger` in `memory.py`.

5. Return the output and chat history.

6. Add your new module to the pipeline in `pipeline.yml`, specifying its inputs and outputs.

7. Run `orchestrate.py` to execute your new pipeline.

The modularity of OrchestrAI makes it easy to add new AI capabilities as needed for your use case. Simply define the interface in `modules.py` and `pipeline.yml`, and OrchestrAI will automatically coordinate and execute the new module.

Let me know if you need any clarification or have additional questions!