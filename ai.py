import openai
import yaml


# Load the configuration
with open('config.yml', 'r') as f:
    config = yaml.safe_load(f)

openai.api_key = config['openai_api_key']

default_model = config['default_model']
default_temperature = config['default_temperature']
default_top_p = config['default_top_p']
default_max_tokens = config['default_max_tokens']
default_frequency_penalty = config['default_frequency_penalty']
default_presence_penalty = config['default_presence_penalty']


# Check if the API key works
try:
    openai.Model.list()
except openai.error.AuthenticationError:
    raise ValueError("Invalid OpenAI API key")

from wandb.sdk.data_types.trace_tree import Trace
import datetime
import helpers as h
import globals
import yaml

class AI:
    def __init__(self, module_name, model_config=None, openai=openai):
        self.openai = openai
        self.model = model_config.get('model', default_model) if model_config else default_model
        self.temperature = model_config.get('temperature', default_temperature) if model_config else default_temperature
        self.top_p = model_config.get('top_p', default_top_p) if model_config else default_top_p
        self.max_tokens = model_config.get('max_tokens', default_max_tokens) if model_config else default_max_tokens
        self.frequency_penalty = model_config.get('frequency_penalty', default_frequency_penalty) if model_config else default_frequency_penalty
        self.presence_penalty = model_config.get('presence_penalty', default_presence_penalty) if model_config else default_presence_penalty
        self.module_name = module_name
        self.system = h.load_system_prompt(module_name)
        self.messages = [{"role": "system", "content": self.system}]


    def generate_response(self, prompt):
        self.messages.append({"role": "user", "content": prompt})
        # Start time
        llm_start_time_ms = round(datetime.datetime.now().timestamp() * 1000)  
        token_count = 0  

        try:
            response = self.openai.ChatCompletion.create(
                model=self.model,
                stream=True,
                messages=self.messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                top_p=self.top_p,
                frequency_penalty=self.frequency_penalty,
                presence_penalty=self.presence_penalty,
            )

            chat = []
            token_count = 0
            for chunk in response:
                delta = chunk["choices"][0]["delta"]
                msg = delta.get("content", "")
                print(msg, end="")
                chat.append(msg)
                token_count += len(msg.split())  # estimate token usage

            print()

            response_text = "".join(chat)
 
            llm_end_time_ms = round(datetime.datetime.now().timestamp() * 1000)  # logged in milliseconds
            status_code="success"
            status_message=None,
            token_usage = {"total_tokens": token_count}

        except Exception as e:
            llm_end_time_ms = round(datetime.datetime.now().timestamp() * 1000)  # logged in milliseconds
            status_code="error"
            status_message=str(e)
            response_text = ""
            token_usage = {}

                
        self.messages.append({"role": "assistant", "content": response_text})

        return {
        "module_name": self.module_name,
        "response_text": response_text,
        "messages": self.messages,
        "llm_end_time_ms": llm_end_time_ms,
        "llm_start_time_ms": llm_start_time_ms,
        "token_count": token_count,
        "status_code": status_code,
        "status_message": status_message,
        "system_prompt": self.system,
        "prompt": prompt
        }
