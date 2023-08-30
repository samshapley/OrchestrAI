# OrchestrAI

OrchestrAI is a Python-based system that orchestrates interactions between multiple instances of OpenAI's GPT-4 model to execute complex tasks. It uses the `networkx` library to manage dependencies between various AI modules, and YAML to define and manage task pipelines.  

A couple of things to bear in mind
 1. Autonomous Agents are still toys, and you're likely to come across several issues, breaks and associated problems the more complex  your pipeline / task is.
 2. This project aims to demonstrate a scalable framework for experimenting with autonomous agents. Instead of a fixed execution order, OrchestrAI offers flexibility to define and compare variations of strategies and settings, to find the best approach for your use case.
 3. Be nice to your agents, or you might regret it later.

## Getting Started

Watch this demo video to see how you can build a low-code autonomous agent in 2 minutes.

[![Demo Video](https://img.youtube.com/vi/pTyiPPZu20U/0.jpg)](https://youtu.be/pTyiPPZu20U)

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

- `agent.py` - Run the script and the specified pipeline.
- `config.yml` - Configure the OpenAI API key, default model parameters, and pipeline to be executed. Also choose whether to enable wandb logging.
- `ai.py` - Manages interactions with the OpenAI API.
- `modules.py` - Contains available modules and their logic.
- `orchestrate.py` - Loads modules and pipelines, constructs a Directed Acyclic Graph (DAG) of operations, and executes them in the    correct order.
- `helpers.py` - Provides helper functions, including loading system prompts, parsing chat data, and writing code files.

We store pipeline.yml files in the pipelines folder. This allows you to create multiple pipelines for different tasks. You can specify which pipeline the agent runs in the config.yml file.

Agents run pipelines -> pipelines orchestrate modules -> modules make LLM calls and use tools.

## Modules

The `modules.py` file contains different AI modules, each responsible for a specific type of operation.

Each module interacts with the a language model to execute its specific task, and the output is stored for use in subsequent operations as defined in the pipeline. Currently, the modules are only communicating with OpenAI, but this can be extended to other language models as well.

The most basic module is the `chameleon` module, which is a generic module used to make an OpenAI call with custom settings and system prompt. This allows you to easily create new modules by simply adding a system prompt to the `system_prompts` folder. This module will be invoked if the system prompt exists, and the module name is specified in the pipeline, but no matching function exists in `modules.py`.

### Setting Up a Pipeline

1. Define your pipeline in a yml file in the pipelines folder. Each operation in the pipeline must consist of a `module`, `inputs`, and an `output_name`. The `module` represents a specific task performed by an AI, `inputs` are the dependencies for the module and the `output_name` is the output of that task, which can be used as input for subsequent operations. Here's an example of a pipeline used to do multi-step reasoning to come up with a plan.

```yaml
pipeline: 
  - module: start_module
    inputs: []
    output_name: request
  - module: task_planner
    inputs: [request]
    output_name: task_plan
  - module: scrutinizer
    model_config:
      model: 'gpt-3.5-turbo'
      temperature: 0.7
    inputs: [request, task_plan]
    output_name: scrutinized_task_plan
  - module: enhancer
    inputs: [request, scrutinized_task_plan, task_plan]
    output_name: enhanced_task_plan
  - module: markdown_converter
    model_config:
      model: 'gpt-3.5-turbo'
      temperature: 0.3
    inputs: [enhanced_task_plan]
    output_name: markdown_plan
```
For each module present, you can read the system prompts in the system_prompts folder. 

Additionally, you can specify the model_config for each module. This allows you to control the openai settings on a per module basis,  For example, easier tasks might want gpt-3.5-turbo, or more creative tasks might need higher temperature. The default model_config is specified in the config.yml file.

You can also specify a `supplement`, an additional context string that the module will use in it's response. For some modules, this is necessary to control desired behaviour. For example, in a basic translation pipeline.

```yaml
pipeline: 
  - module: start_module
    inputs: []
    output_name: request
  - module: translator
    model_config:
      model: 'gpt-3.5-turbo'
      temperature: 0.2
    inputs: [request]
    supplement: "Spanish"
    output_name: translation
```
Once you have defined your pipeline, you can ensure it will be run by specifying the pipeline name in the config.yml file.

### Running the Script

Ensure that you've added your OpenAI API key to `config.yml`.

To run OrchestrAI, execute `agent.py`:

```bash
python3 agent.py
```
The script will execute the operations in the pipeline in the order specified, querying the model as necessary and storing the results in the `memory_log.json`.

## The Engineering Pipeline 

This is an example pipeline built to demonstrate the capabilities of OrchestrAI. It is a pipeline that uses AI to generate a working codebase from a high-level description of the task. For full understanding, please read the system prompts of each module in the system_prompts folder, and the code in the modules.py file. (this base version can essentially only create python based repositories)

```yaml
pipeline: 
  - module: start_module
    inputs: []
    output_name: request
  - module: code_planner
    inputs: [request]
    output_name: code_plan
  - module: engineer
    inputs: [request, code_plan]
    output_name: code
  - module: debugger
    model_config:
      model: 'gpt-3.5-turbo-16k'
      temperature: 0.7
    inputs: [request, code]
    output_name: working_codebase
  - module: modify_codebase
    inputs: [working_codebase]
    output_name: modified_codebase
  - module: create_readme
    inputs: [modified_codebase]
    output_name: readme
```
### Code Planning and Engineering

The `code_planner` and `engineer` modules should be used in tandem to create a repository in the `generated_code` folder. The code planner will provide a detailed overview of the implementation, and the engineer will generate the code to implement the plan. The engineer module is custom, and does not use the chameleon. We carry out regex based parsing to extract the code into the repository. This repository is then condensed into a token-reduced version, and used as the output `code` for the engineer module. This condensed codebase string can be used as input for the debugger module and/or the modify_codebase module.

### Self-Debugging

The `debugger` module implements a self-debugging loop to automatically fix errors in the generated code. 

It first tries to run `main.py` and if it encounters any runtime errors, it sends the error message back to the model to generate fixed code. During testing, I've found that the gpt-3.5-turbo-16k model is able to fix most errors in the generated code, so this is recommended as a default model used for debugging. Potentially something could be implemented that swaps to a different model if the error is not fixed after a certain number of iterations.

It also checks if `requirements.txt` was modified and re-installs any new dependencies. This loop repeats until `main.py` runs successfully without errors.

This enables OrchestrAI to iteratively improve and fix the generated code until it works as intended.

### Modifying the Codebase

The `modify_codebase` module allows OrchestrAI to modify the generated codebase to add new features. You can ask for modifications to the codebase, and the module will reutrn all modified and new scripts, handling the update to the repository. This module is also custom, and does not use the chameleon. It has a nested debugger module, which is further used to fix any errors in the modified codebase.

### What can it actually do?

It's great at pygames, fun demos and little epxeiremnts, but we're still a (short) way off from autonomously building entire codebases for any task, with included debugging and modification. But have fun anayway!

## Creating New Modules

Sometimes, you might want to create a more complex module, that goes beyond the capabilities of the basic `chameleon` module.
To add new capabilities to OrchestrAI, you can create custom modules.

Steps to create a new module:

1. Add a new function in `modules.py` with the name of your module. For example:

```python
def new_module(prompt):
  # Module logic
  ...
  return output
```

2. If this module requires a call to OpenAI, design the appropriate system prompt for your module from `system_prompts/`.

3. Interact with the model via the `AI` class to generate a response.

4. Log the action using the local and wandb logging (if desired.)

5. Add your new module to the pipeline, specifying its inputs and outputs.

6. Run `orchestrate.py` to execute your new pipeline.

The modularity of OrchestrAI makes it easy to add new AI capabilities as needed for your use case. Simply define the interface in `modules.py` and `pipeline.yml`, and OrchestrAI will automatically coordinate and execute the new module.

## Logging with Weights and Biases

By default, interactions are logged using `log_action' during the process to a file created at the start of the agent. This file is then renamed and moved to the logs folder at the termination of the agent. This allows you to see the full history of the agent's interactions.

However, we can leverage the power of Wandb Prompts (https://docs.wandb.ai/guides/prompts?_gl=1)

Provided you've set up wandb, you can enable wandb logging in the config.yml file.

This allows you to log the agent as a run, with modules as child runs of the chain. This allows you to see the full history of the agent's interactions, and the full history of each module's interactions. This is useful for debugging, and for understanding the agent's behaviour as you explore different pipelines and modules.

------------------

Let me know if you need any clarification or have additional questions!
