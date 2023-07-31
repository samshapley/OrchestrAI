# OrchestrAI

OrchestrAI is a modular system for orchestrating interactions between several instances of OpenAI's GPT-4 model, potentially trained with different settings or data, in order to accomplish complex tasks. The system is built in Python and leverages the `networkx` library to handle the dependencies between different AI modules.

## Getting Started

### Prerequisites

To run OrchestrAI, you'll need:

- Python 3.7 or later
- The OpenAI Python library
- networkx
- PyYAML

You can install these with pip:

```bash
pip install openai networkx pyyaml
```

### Configuration

To configure OrchestrAI, you'll need to set up a few files:

- `ai.py` contains the AI class, which manages interactions with an OpenAI GPT-4 model. You'll need to set your OpenAI API key in this file.
- `modules.yml` lists the AI modules available for use. Each module is either a large language model (LLM) or a non-LLM module. LLM modules are driven by OpenAI's GPT-4, while non-LLM modules are placeholders for manual human intervention.
- `orchestrate.py` is the main script, which loads the modules and pipelines, constructs a directed acyclic graph (DAG) of operations, and executes them in the correct order.
- The `systems/` directory contains a text file for each LLM module, which provides an introductory prompt for the module.
- The `pipelines/` directory contains one or more YAML files describing pipelines of operations to execute.

### Running the Script

To run OrchestrAI, execute `orchestrate.py`:

```bash
python orchestrate.py
```

The script will execute the operations in the pipeline(s) as specified, querying the GPT-4 model as necessary and storing the results.

## Understanding the Modules

Each module in the `modules.yml` file is either an LLM module or a non-LLM module.

LLM modules, like `planner`, `scrutinizer`, `enhancer`, `grounder`, and `dreamer`, each have a specific role:

- `planner` generates a plan from a task.
- `scrutinizer` scrutinizes a plan or piece of information and provides feedback.
- `enhancer` enhances a plan with additional information.
- `grounder` provides real-world grounding for a plan, pointing out unrealistic actions.
- `dreamer` adds creative flair and inspiration to a plan.

Non-LLM modules, like `human_intervention`, record terminal input from the user.

## Contributing

We welcome contributions to OrchestrAI! Please submit a pull request with your changes, and be sure to include tests and documentation.

## License

OrchestrAI is open-source software, released under the [MIT License](https://opensource.org/licenses/MIT).