import openai
import yaml
import wandb_logging as wb
from PIL import Image
import requests
from io import BytesIO
from datetime import datetime
import globals
import os

# Load the configuration
with open('config.yml', 'r') as f:
    config = yaml.safe_load(f)

openai.api_key = config['openai_api_key']
wandb_enabled = config['wandb_enabled']
working_image_dirname = config['working_image_dirname']
parent_directory = 'generated_outputs'


def generate_image(contents_json):
    """This function is used to invoke the generate_image tool"""
    start_time_ms = round(datetime.now().timestamp() * 1000) 

    try:
        # Parse the contents as a JSON object
        filename = contents_json.get('filename')
        prompt = contents_json.get('prompt')
        print("\033[92mGenerating image | Prompt: " + prompt + "\033[00m")
        
        response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
        )

        image_url = response['data'][0]['url']

        # Open the URL and pass the result to Pillow
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))

        # Save the image
        output_directory = os.path.join(parent_directory, working_image_dirname)
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        img.save(os.path.join(output_directory, f'{filename}.png'))

        status = "success"
        e = None

    except Exception as e:
        print("Error using image generation tool.", e)
        status = "error"
    
    if wandb_enabled:
        wb.wandb_log_tool(
            tool_name="generate_image",
            start_time_ms=start_time_ms,
            inputs={"prompt": prompt},
            outputs={"caption": prompt},
            parent=globals.llm_span,
            status=status,
            metadata={"error_message": str(e)}
        )
            
    return prompt