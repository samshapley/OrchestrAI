import openai
import yaml

# Load the configuration
with open('config.yml', 'r') as f:
    config = yaml.safe_load(f)

# Set the wandb_enabled flag
wandb_enabled = config['wandb_enabled']
openai.api_key = config['openai_api_key']

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
    def __init__(self, module_name, model = 'gpt-4', temperature=0.7, openai=openai):
        self.model = model
        self.openai = openai
        self.temperature = temperature
        self.module_name = module_name
        self.system = h.load_system_prompt(module_name)
        self.messages = [{"role": "system", "content": self.system}]


    def generate_response(self, prompt):
        self.messages.append({"role": "user", "content": prompt})

        try:
            response = self.openai.ChatCompletion.create(
                model=self.model,
                stream=True,
                messages=self.messages,
                temperature=self.temperature,
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

        if wandb_enabled:
            # calculate the runtime of the LLM
            runtime = llm_end_time_ms - globals.agent_start_time_ms
        # create a child span in wandb
            llm_span = Trace(
                name=self.module_name,
                kind="llm",  # kind can be "llm", "chain", "agent" or "tool"
                status_code=status_code,
                status_message=status_message,
                metadata={"temperature": self.temperature,
                        "token_usage": token_usage,
                        "runtime_ms": runtime,
                        "module_name": self.module_name,
                        "model_name": self.model},
                start_time_ms=globals.chain_span._span.end_time_ms,
                end_time_ms=llm_end_time_ms,
                inputs={"system_prompt": self.system, "query": prompt},
                outputs={"response": response_text}
            )

            # add the child span to the root span
            globals.chain_span.add_child(llm_span)

            # update the end time of the Chain span
            globals.chain_span.add_inputs_and_outputs(
                inputs={"query": prompt},
                outputs={"response": response_text})

            # update the Chain span's end time
            globals.chain_span._span.end_time_ms = llm_end_time_ms

            # log the child span to wandb
            llm_span.log(name="pipeline_trace")
        
        self.messages.append({"role": "assistant", "content": response_text})
        return response_text, self.messages