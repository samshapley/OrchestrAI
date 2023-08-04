import json
import datetime

class Logger: 
    def __init__(self): 
        # Initialize an empty list for storing logs
        self.logs = [] 

    def log_action(self, module, prompt, response, model): 
        timestamp = datetime.datetime.now().isoformat() 
        action_log = { 
            "module": module, 
            "prompt": prompt, 
            "response": response, 
            "model": model, 
            "timestamp": timestamp, 
        } 
        # Append the action log to the logs list
        self.logs.append(action_log)
        # Update log file
        self.update_log_file()

    def update_log_file(self):
        # Save logs to a JSON file
        with open('memory_log.json', 'w') as f: 
            json.dump(self.logs, f)
