from typing import Callable
from utils.prompt_loader import load_system_prompts, load_system_prompts, load_report_prompts
from langchain.agents import AgentState
from langchain.agents.middleware import wrap_tool_call, before_model, dynamic_prompt, ModelRequest
from langchain_core.messages import ToolMessage
from langgraph.prebuilt.tool_node import ToolCallRequest
from langgraph.runtime import Runtime
from langgraph.types import Command
from utils.logger_handler import logger
from utils.observability import elapsed_ms, now_ms, result_size

@wrap_tool_call
def monitor_tool(
        request: ToolCallRequest,
        # function
        handler: Callable[[ToolCallRequest], ToolMessage | Command],
) -> ToolMessage | Command:
    start_ms = now_ms()
    tool_name = request.tool_call['name']
    logger.info(f"[monitor_tool] tool: {request.tool_call['name']}")
    logger.info(f"[monitor_tool] args: {request.tool_call['args']}")
    try:
        result =  handler(request)
        logger.info(
            "[monitor_tool] status=success tool=%s latency_ms=%.2f result_size=%s",
            tool_name,
            elapsed_ms(start_ms),
            result_size(result),
        )
        logger.debug(f"[monitor_tool] result: {result}")

        if tool_name == "fill_context_for_report":
            request.runtime.context["report"] = True
        return result
    except Exception as e:
        logger.exception(
            "[monitor_tool] status=error tool=%s latency_ms=%.2f error=%s",
            tool_name,
            elapsed_ms(start_ms),
            e,
        )
        raise e


@before_model
def log_before_model(
        state: AgentState,             # Agent state
        runtime: Runtime,           # record context
):
    logger.info(f"[log_before_model] state length: {len(state['messages'])}")
    logger.info(f"[log_before_model] report_context: {runtime.context.get('report', False)}")
    logger.debug(f"[log_before_model] {type(state['messages'][-1]).__name__} | {state['messages'][-1].content.strip()}")
    return None

@dynamic_prompt         # whenever generate prompt, use this
def report_prompt_switch(request: ModelRequest):
    is_report = request.runtime.context.get("report", False)
    if is_report:
        return load_report_prompts()
    return load_system_prompts()
