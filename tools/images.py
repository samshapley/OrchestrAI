import openai
import yaml
import wandb_logging as wb
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import requests
from io import BytesIO
from datetime import datetime
import globals

import os
import time

# Load the configuration
with open('config.yml', 'r') as f:
    config = yaml.safe_load(f)

openai.api_key = config['openai_api_key']
wandb_enabled = config['wandb_enabled']


def generate_image(prompt):
    """This function is used to invoke the generate_image tool"""
    start_time_ms = round(datetime.now().timestamp() * 1000) 

    print("\033[92mGenerating an image...\033[00m")
    
    response = openai.Image.create(
      prompt=prompt,
      n=1,
      size="1024x1024"
    )

    image_url = response['data'][0]['url']

    # Open the URL and pass the result to Pillow
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    img_array = np.array(img)

    # Display the image
    print("Displaying the image...")
    plt.figure()  # This line creates a new figure
    plt.imshow(img_array)
    plt.axis('off')  # This line removes the axis
    plt.title(prompt)  # This line adds the prompt as a caption
    plt.show(block=False)  # This line displays the image without blocking
    
    # Save the image
    if not os.path.exists('generated_images'):
        os.makedirs('generated_images')
    img.save(f'generated_images/image_{start_time_ms}.png')
    
    if wandb_enabled:
        wb.wandb_log_tool(
            tool_name="generate_image",
            start_time_ms=start_time_ms,
            inputs={"prompt": prompt},
            outputs={"caption": prompt},
            parent=globals.llm_span,
            status="success"
        )
      
    return prompt