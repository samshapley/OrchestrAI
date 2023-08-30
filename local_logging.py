import json
import os
import time

def log_action(action):
    """Super simple, log any json object you want during pipeline execution."""
    with open('memory_log.json', 'r+') as file:
        data = json.load(file)
        data['actions'].append(action)
        file.seek(0)
        json.dump(data, file)