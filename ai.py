import openai
import yaml
import datetime
import helpers as h

# Load the configuration
with open('config.yml', 'r') as f:
    config = yaml.safe_load(f)

default_model = config['default_model']
default_temperature = config['default_temperature']
default_top_p = config['default_top_p']
default_max_tokens = config['default_max_tokens']
default_frequency_penalty = config['default_frequency_penalty']
default_presence_penalty = config['default_presence_penalty']

class AI:
    def __init__(self, module_name, model_config=None, openai_client=None):
        self.openai = openai_client or openai
        self.model_config = model_config
        self.model = model_config.get('model', default_model) if model_config else default_model
        self.temperature = model_config.get('temperature', default_temperature) if model_config else default_temperature
        self.top_p = model_config.get('top_p', default_top_p) if model_config else default_top_p
        self.max_tokens = model_config.get('max_tokens', default_max_tokens) if model_config else default_max_tokens
        self.frequency_penalty = model_config.get('frequency_penalty', default_frequency_penalty) if model_config else default_frequency_penalty
        self.presence_penalty = model_config.get('presence_penalty', default_presence_penalty) if model_config else default_presence_penalty
        self.module_name = module_name
        self.system, self.component_prompts = h.load_system_prompt(module_name)
        self.messages = [{"role": "system", "content": self.system}]


    def generate_response(self, prompt):
        self.messages.append({"role": "user", "content": prompt})
        # Start time
        llm_start_time_ms = round(datetime.datetime.now().timestamp() * 1000)  
        token_count = 0  

        try:
            response = self.openai.chat.completions.create(
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
                msg = chunk.choices[0].delta.content
                if msg is not None:
                    print(msg, end="")
                    chat.append(msg)
                    token_count += len(msg.split())  # estimate token usage

            print(len(chat))
            response_text = "".join(chat)
 
            llm_end_time_ms = round(datetime.datetime.now().timestamp() * 1000)  # logged in milliseconds
            status_code="success"
            status_message=None,
            token_usage = {"total_tokens": token_count}

        except Exception as e:
            print("Error: ", e)
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
        "component_prompts": self.component_prompts,
        "prompt": prompt,
        "max_tokens": self.max_tokens,
        "top_p": self.top_p,
        "temperature": self.temperature,
        "frequency_penalty": self.frequency_penalty,
        "presence_penalty": self.presence_penalty,
        }
