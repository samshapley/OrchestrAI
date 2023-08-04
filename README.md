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
- `helpers.py` - Provides helper functions, including loading system prompts, parsing chat data, and writing code files.
- `pipeline.yml` - Describes the sequence of operations to be executed in your pipeline.

### Setting Up a Pipeline

1. Define your pipeline in the `pipeline.yml` file. Each operation in the pipeline consists of a `module`, `inputs`, and an `output_name`. The `module` represents a specific task performed by an AI, `inputs` are the dependencies for the module and the `output_name` is the output of that task, which can be used as input for subsequent operations. 

Here's an example of a pipeline:

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

To run OrchestrAI, execute `orchestrate.py`:

```bash
python orchestrate.py
```

The script will execute the operations in the pipeline in the order specified, querying the GPT-4 model as necessary and storing the results.

## Understanding the Modules

The `modules.py` file contains different AI modules, each responsible for a specific type of operation, such as `start_module`, `task_planner`, `scrutinizer`, `enhancer`, `code_planner`, `debugger`, and `engineer`.

Each module interacts with the GPT-4 model to execute its specific task, and the output is stored for use in subsequent operations as defined in the pipeline.

## Memory Logging

The `memory.py` file contains a Logger class that logs the actions of each module. Each action log contains the module name, prompt, response, model used, and a timestamp. The logs are stored in a JSON file named 'memory_log.json'.
