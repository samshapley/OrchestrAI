from orchestrate import execute_pipeline
import helpers as h
import time
import wandb
from datetime import datetime
from wandb.sdk.data_types.trace_tree import Trace
import globals
import yaml
import atexit
import json
import os
import openai

# create logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Load the configuration
with open('config.yml', 'r') as f:
    config = yaml.safe_load(f)

# Check if the API key works
while True:
    try:
        openai.api_key = os.getenv('OPENAI_API_KEY')
        if not openai.api_key:
            openai.api_key = input("Please enter your OpenAI API key: ")
            os.environ['OPENAI_API_KEY'] = openai.api_key  # Set the API key as an environment variable
        openai.Model.list()
        break
    except openai.error.AuthenticationError:
        print("Invalid OpenAI API key. Please try again.")

# Obtain the config variables
wandb_enabled = config['wandb_enabled']
tools_enabled = config['tools_enabled']
pipeline_name = config['pipeline'] 
pipeline_path = "pipelines/" + pipeline_name + ".yml"

if wandb_enabled: # Initialize wandb if it's enabled
    wandb.init(project="OrchestrAI")
    wandb.config.wandb_enabled = wandb_enabled
if tools_enabled:
    print("\033[93mTools are enabled.\033[00m")

def main():
    print("\033[95m ------- Welcome to OrchestrAI ------\033[00m")
    time.sleep(1) # dramatic effect
    
    pipeline = h.load_pipeline(pipeline_path) # Load the pipeline

    with open('memory_log.json', 'w') as file:
        json.dump({
            'agent_start_time': time.time(),
            'pipeline_name': pipeline_name,
            'actions': []
        }, file)

    if wandb_enabled:
        globals.agent_start_time_ms = round(datetime.now().timestamp() * 1000) 

        # create a root span for the agent.
        root_span = Trace(
            name="Agent",
            kind="agent",
            start_time_ms=globals.agent_start_time_ms,
            end_time_ms=globals.agent_start_time_ms,
            metadata={"pipeline_name": pipeline_name},
        )

        # the agent calls into a pipeline, so we create a chain span.
        globals.chain_span = Trace(
            name=pipeline_name,
            kind="chain",
            start_time_ms=globals.agent_start_time_ms,
            end_time_ms=globals.agent_start_time_ms,
        )

        root_span.add_child(globals.chain_span) # add the chain span as a child of the root span

        ## Just in case it crashes, we want to log the root span to wandb anyway so we use atexit
        def closing_log():

            agent_end_time_ms = round(datetime.now().timestamp() * 1000)
          
            # Convert the timestamp to datetime
            agent_end_time = datetime.fromtimestamp(agent_end_time_ms / 1000)

            # Format the datetime object to a string
            current_time = agent_end_time.strftime("%Y-%m-%d_%H-%M-%S")

            
            os.replace('memory_log.json', f'logs/log_{current_time}.json')
            
            if wandb.run is None:
                return
            
            # Log the root span to Weights & Biases
            root_span._span.end_time_ms = agent_end_time_ms
            root_span.log(name="pipeline_trace")

        # Register the function to be called on exit
        atexit.register(closing_log)

    try:
        execute_pipeline(pipeline) # Execute the pipeline using the orchestrate.py script
    except Exception as e:
        print(f"An error occurred during pipeline execution: {e}")
    finally:
        if wandb_enabled:
            # Log the root span to Weights & Biases
            agent_end_time_ms = round(datetime.now().timestamp() * 1000)
            root_span._span.end_time_ms = agent_end_time_ms
            root_span.log(name="pipeline_trace")

            wandb.finish()
            print ("\033[93m Wandb logging completed.\033[00m")
            
        print("\033[95m ------- OrchestrAI finished  ------\033[00m")

if __name__ == "__main__":
    main()