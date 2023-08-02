# OrchestrAI

OrchestrAI is a system built in Python that enables complex task execution by orchestrating interactions between multiple instances of OpenAI's GPT-4 model. It uses the `networkx` library to handle dependencies between various AI modules, and YAML to define and manage the task pipelines.

## Getting Started

### Prerequisites

To run OrchestrAI, you'll need:

- Python 3.7 or later
- OpenAI Python library
- networkx
- PyYAML

You can install these with pip:

```bash
pip install openai networkx pyyaml
```

### Configuration

To set up OrchestrAI, you need to organize the following files:

- `ai.py` - This file contains the AI class, which manages interactions with the OpenAI GPT-4 model. Your OpenAI API key must be set in this file.
- `modules.py` - This script lists the available AI modules.
- `orchestrate.py` - This main script loads modules and pipelines, constructs a Directed Acyclic Graph (DAG) of operations, and executes them in the correct order.
- `helpers.py` - This script provides helper functions, including loading system prompts, parsing chat data, and writing code files.
- `pipeline.yml` - This YAML file describes the sequence of operations to be executed in your pipeline.

### Setting Up a Pipeline

1. Define your pipeline in the `pipeline.yml` file. Each operation in the pipeline consists of a `module` and an `output_name`. The `module` represents a specific task performed by an AI, and the `output_name` is the output of that task, which can be used as input for subsequent operations. Here's an example of a simple pipeline:

```yaml
pipeline:
- module: start_module
  inputs: []
  output_name: request
- module: code_planner
  inputs: [request]
  output_name: code_plan
- module: engineer
  inputs: [code_plan]
  output_name: code
```

2. Save and close the `pipeline.yml` file.

3. Run the `orchestrate.py` script.

### Running the Script

To run OrchestrAI, execute `orchestrate.py`:

```bash
python orchestrate.py
```

The script will execute the operations in the pipeline in the order specified, querying the GPT-4 model as necessary and storing the results.

## Understanding the Modules

The `modules.py` file contains different AI modules, each responsible for a specific type of operation, such as `start_module`, `human_intervention`, `task_planner`, `scrutinizer`, `enhancer`, `code_planner`, `debugger`, and `engineer`.

Each module interacts with the GPT-4 model to execute its specific task, and the output is stored for use in subsequent operations as defined in the pipeline.

## Contributing

Contributions to OrchestrAI are welcome! Please submit a pull request with your changes, and be sure to include tests and documentation.

## License

OrchestrAI is open-source software, released under the MIT License.
