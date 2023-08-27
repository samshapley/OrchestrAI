# agent.py
from orchestrate import execute_pipeline
import helpers as h
import time
import wandb
import datetime
from wandb.sdk.data_types.trace_tree import Trace
import globals
import yaml
import pandas as pd

# Load the configuration
with open('config.yml', 'r') as f:
    config = yaml.safe_load(f)

# Set the wandb_enabled flag
wandb_enabled = config['wandb_enabled']
pipeline_name = config['pipeline'] 
pipeline_path = "pipelines/" + pipeline_name + ".yml"

if wandb_enabled:
    wandb.init(project="OrchestrAI")
    wandb.config.wandb_enabled = wandb_enabled

def main():
    print("\033[95m ------- Welcome to OrchestrAI ------\033[00m")
    time.sleep(1)
    
    pipeline = h.load_pipeline(pipeline_path)
    
    # Get the name of the pipeline file
    pipeline_name = pipeline_path.split("/")[-1].split(".")[0]


    if wandb_enabled:
        globals.agent_start_time_ms = round(datetime.datetime.now().timestamp() * 1000) 

        # create a root span for the pipeline
        root_span = Trace(
            name="Agent",
            kind="agent",
            start_time_ms=globals.agent_start_time_ms,
            metadata={"pipeline_name": pipeline_name},
        )

        #The Agent calls into a LLMChain..
        globals.chain_span = Trace(
            name=pipeline_name,
            kind="chain",
            start_time_ms=globals.agent_start_time_ms,
        )

        root_span.add_child(globals.chain_span)

    # agent.py
    try:
        execute_pipeline(pipeline)
    except Exception as e:
        print(f"An error occurred during pipeline execution: {e}")
    finally:
        if wandb_enabled:
            # Log the root span to Weights & Biases
            agent_end_time_ms = round(datetime.datetime.now().timestamp() * 1000)
            root_span._span.end_time_ms = agent_end_time_ms
            root_span.log(name="pipeline_trace")
            # Open and load the JSON file
            # memory_df = pd.read_json('memory_log.json')
            # wandb.log({"memory_log": wandb.Table(dataframe=memory_df)}) # Log the DataFrame to Weights & Biases
            # wandb.finish()
            # print ("\033[98m Wandb logging completed.\033[00m")
            
        print("\033[95m ------- OrchestrAI finished  ------\033[00m")

if __name__ == "__main__":
    main()