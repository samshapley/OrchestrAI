# wandb_logging.py
from wandb.sdk.data_types.trace_tree import Trace
import time

def wandb_log_llm(data, model, temperature, parent):
    
    runtime = data["llm_end_time_ms"] - data["llm_start_time_ms"]


    llm_span = Trace(
        name=data["module_name"],
        kind="llm",
        status_code=data["status_code"],
        status_message=data["status_message"],
        metadata={
            "temperature": temperature,
            "token_usage": {"total_tokens": data["token_count"]},
            "runtime_ms": runtime,
            "module_name": data["module_name"],
            "model_name": model,
            "max_tokens": data["max_tokens"],
            "top_p": data["top_p"],
            "frequency_penalty": data["frequency_penalty"],
            "presence_penalty": data["presence_penalty"]
        },
        start_time_ms=parent._span.end_time_ms,
        end_time_ms=data["llm_end_time_ms"],
        inputs={"system_prompt": data["system_prompt"], "query": data["prompt"]},
        outputs={"response": data["response_text"]}
    )
    
    parent.add_child(llm_span)

    parent.add_inputs_and_outputs(
        inputs={"query": data["prompt"]},
        outputs={"response": data["response_text"]}
    )
    parent._span.end_time_ms = data["llm_end_time_ms"]

    llm_span.log(name="pipeline_trace")


def wandb_log_tool(tool_name, inputs, outputs, parent, status="success"):

    time.sleep(1)  # simulate tool execution time
    end_time_ms = round(time.time() * 1000)

    tool_span = Trace(
        name=tool_name,
        kind="tool",
        status_code=status,
        start_time_ms=parent._span.end_time_ms,
        end_time_ms=end_time_ms,
        inputs=inputs,
        outputs=outputs
    )

    # add the tool span as a child of the parent span
    parent.add_child(tool_span)

    # add the tool span's inputs and outputs to the parent span
    parent.add_inputs_and_outputs(
        inputs=inputs,
        outputs=outputs
    )

    # update the parent span's end time
    parent._span.end_time_ms = end_time_ms

    # log the span to wandb
    tool_span.log(name="pipeline_trace")

    return tool_span