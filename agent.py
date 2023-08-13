# agent.py
from orchestrate import execute_pipeline
import helpers as h

def main():
    # Load the desired pipeline
    pipeline_path = "pipeline.yml"
    pipeline = h.load_pipeline(pipeline_path)
    
    # Execute the pipeline
    execute_pipeline(pipeline)

if __name__ == "__main__":
    main()
