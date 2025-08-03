# Add these utility functions to your views.py
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage, ToolMessage
import json
def serialize_message(msg:BaseMessage) -> dict: 
    """Convert LangChain messages to JSON-serializable dicts"""
    base = {
        "type": msg.type,
        "content": msg.content,
        "additional_kwargs": getattr(msg, "additional_kwargs", {}),
        "id": str(getattr(msg, "id", ""))
    }
    
    if isinstance(msg, AIMessage):
        tool_calls = getattr(msg, "tool_calls", [])
        if tool_calls:
            base["tool_calls"] = [
                {
                    "name": call.get("name"),
                    "args": call.get("args"),
                    "id": call.get("id", "")
                }
                for call in tool_calls
            ]
    
    if isinstance(msg, ToolMessage):
        base.update({
            'name': msg.name,
            'tool_call_id': msg.tool_call_id,
            'status': getattr(msg, 'status', 'completed')
        })
    
    return base

def convert_tool_calls_openai_to_langchain(tool_calls: list[dict]) -> list[dict]:
    """Convert OpenAI-style tool_calls into LangChain-style format."""
    return [
        {
            "name": tc["function"]["name"],
            "args": json.loads(tc["function"]["arguments"]),
            "id": tc.get("id", "")
        }
        for tc in tool_calls
        if "function" in tc
    ]

def deserialize_message(msg_dict:dict)-> BaseMessage: 
    """Convert dicts back to LangChain messages"""
    msg_type = msg_dict.get('type')
    content = msg_dict.get("content", "")
    kwargs = msg_dict.get("additional_kwargs", {})

    
    if msg_type == "ai" and "tool_calls" in msg_dict:
        raw_tool_calls = msg_dict["tool_calls"]
        if raw_tool_calls and "function" in raw_tool_calls[0]:
            # OpenAI-style tool calls – convert to LangChain format
            kwargs["tool_calls"] = convert_tool_calls_openai_to_langchain(raw_tool_calls)
        else:
            kwargs["tool_calls"] = raw_tool_calls

    if msg_type == "human":
        return HumanMessage(content=content, **kwargs)

    elif msg_type == "ai":
        return AIMessage(content=content, **kwargs)

    elif msg_type == "tool":
        return ToolMessage(
            content=content,
            name=msg_dict["name"],
            tool_call_id=msg_dict["tool_call_id"],
            status=msg_dict.get("status", "completed")
        )

    elif msg_type == "system":
        return SystemMessage(content=content)

    else:
        raise ValueError(f"Unknown message type: {msg_type}")