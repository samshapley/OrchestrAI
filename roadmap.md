# OrchestrAI - To do list

## General 

Each module should understand the original task that was asked when it is initialised in the system prompt (or similar)

Figure out what to do with the outputs of code as the debugger module/engineer.

Define additional modules such as image generators. 

The model should have read and write access.

A memory module will keep track of what is actual going on. This will have a log of the modules accessed, when, and the existing pipeline. This will then form the core of the self build module later on.

## Code Generation

Engineer Module: This should only be responsible for the generation of the code. I need to adjust the system prompt so it does not generate anything else outside of the file structure. 

- Package versions don't need to be identified
- I want it to be able to handle dependency issues by itself. For example, debug should take place also when it is first run. 

- Self debugging. What does the debug module need to do?

- First try to run the generated code.
- If we don't get an error, then the code should run as successfuly, I need to figure out a way for this to run outside of the main run of the program, so when this code stops running, the pipeline can continue. 

- If we get an error, we will pass the error message to the debugger module, with the repo as a prompt.py file. 
- The debugger must return instructions to modify any files that are needed, returning the full unredacted code as previously in the engineer step.
- We are then going to extract these from the debugger response, update the repo, and try to run the code again. 
-- This loop should persist until the code is able to run. 
---- If it is persisting for too long, i'd like an option either for human guiadance (i.e after n failures or at any point you wish to interject you can)

Once the code is running successfully, we then need to take human input as a rule. Is this what you wanted? yes/no

If yes, presented with option to add aditional features, and the cycle starts again. 
We should use prompt.py to create a base which we then pass to a code_modifier module. In theory, we would pass the engineer module again, but this time instead of text input, we would specify repository input. 

## Autonomous Pipeline

1. We need a system prompt that clearly explains how OrchestrAI works, and how to use the pipelines. 

We should then have an option called self_autonomy, which if true, the initial pipeline set up is 
module_start + autonomy

The autonomous module does the following 
- Using the context of the task, and the available modules and examples, constructs the pipeline.yml file and then reloads it. It's important that at the end of it, there is always another self_autonomy_pipeline, and each time this is about to start, it get's confirmation from the user.

