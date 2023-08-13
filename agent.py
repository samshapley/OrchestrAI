# agent.py
from orchestrate import execute_pipeline
import helpers as h
import time

def main():
    print("\033[95m ------- Welcome to OrchestrAI ------\033[00m")
    time.sleep(1)
    
    # Load the desired pipeline
    pipeline_path = "pipeline.yml"
    pipeline = h.load_pipeline(pipeline_path)
    
    # Execute the pipeline
    execute_pipeline(pipeline)

if __name__ == "__main__":
    main()
